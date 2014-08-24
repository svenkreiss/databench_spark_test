"""mcrisk example for pyspark in databench."""

import databench_py
from pyspark import SparkContext

import numpy
import random

import mpld3
import matplotlib.pyplot as plt


class Analysis(databench_py.Analysis):

    def on_connect(self):
        self.emit('log', 'on_connect: mcrisk')
        self.sc = SparkContext("local", "App Name", pyFiles=[
            'analyses/mcrisk_pyspark/analysis.py'
        ])

        # Quick histogram vis
        self.fig = plt.figure(figsize=(8, 4))
        self.ax1 = self.fig.add_subplot(111)
        # ax2 = self.fig.add_subplot(122)

    def on_disconnect(self):
        self.sc.stop()

    def on_run(self):
        self.emit('log', 'Starting VaR calculation ...')

        # Parse arguments and input data
        numTrials = 10000
        parallelism = 8
        instruments = [
            [0.0, 30.0, 0.5, 3.0, -2.3],
            [0.0, 7.0, 0.6, -2.0, .4],
            [5.0, 100.0, 0.8, -0.8, 2.0],
            [0.0, 5.0, 1.0, -2.8, 1.2],
        ]
        factorMeans = [12.0, 13.5, 4.5]
        factorCovariances = [
            [2.0, -1.2, 0.0],
            [-1.2, 3.0, -0.8],
            [0.0, -0.8, 3.0],
        ]
        seed = random.randint(1e5, 1e10)

        # Send all instruments to every node
        broadcastInstruments = self.sc.broadcast(instruments)

        # Generate different seeds so that our simulations
        # don't all end up with the same results
        seeds = [seed+i for i in xrange(parallelism)]
        seedRdd = self.sc.parallelize(seeds, parallelism)

        """
        Enclose the functions that need to be called on the client side.
        Making them @staticmethod of the class does not work for cPickle.
        """

        def trial_values(seed, numTrials, instruments,
                         factorMeans, factorCovariances):
            numpy.random.seed(seed)
            trialValues = numpy.random.multivariate_normal(
                factorMeans, factorCovariances, numTrials
            )

            trialValues = [trial_value(i, instruments)
                           for i in trialValues]
            return trialValues

        def trial_value(trial, instruments):
            """Calculate the full value of the portfolio under particular
            trial conditions."""

            return sum((instrument_trial_value(i, trial)
                        for i in instruments))

        def instrument_trial_value(instrument, trial):
            """Calculate the value of a particular instrument under
            particular trial conditions."""

            value = 0.0
            for i in xrange(len(trial)):
                value += trial[i] * instrument[2+i]
            return min(max(value, instrument[0]), instrument[1])

        # Main computation: run simulations and compute
        # aggregate return for each
        trialsRdd = seedRdd.flatMap(
            lambda x: trial_values(
                x, numTrials / parallelism, broadcastInstruments.value,
                factorMeans, factorCovariances
            )
        )

        # Cache the results so that we don't recompute for both of
        # the summarizations below
        trialsRdd.cache()

        # Calculate VaR
        trials = sorted(trialsRdd.collect())
        # self.emit('log', "values: "+str(trials))
        varFivePercent = trials[numTrials / 20]
        self.emit('varFivePercent', varFivePercent)
        self.emit('log', "VaR: " + str(varFivePercent))

        # update histogram
        self.ax1.cla()
        self.ax1.set_xlabel('Portfolio Value (millions US$)')
        self.ax1.set_ylabel('Distribtuion')
        self.ax1.set_xlim(32, 48)
        self.ax1.grid(True)
        self.ax1.hist(
            trials, 50,
            range=(32, 48), normed=0, facecolor='green', alpha=0.75
        )
        self.emit('mpld3canvas', mpld3.fig_to_dict(self.fig))

        # Kernel density estimation
        # domain = Range.Double(20.0, 60.0, .2).toArray
        # densities = KernelDensity.estimate(trialsRdd, 0.25, domain)
        # pw = new PrintWriter("densities.csv")
        # for (point <- domain.zip(densities)) {
        #   pw.println(point._1 + "," + point._2)
        # }
        # pw.close()


if __name__ == "__main__":
    analysis = databench_py.Meta('mcrisk_pyspark', __doc__, Analysis)
    analysis.event_loop()
