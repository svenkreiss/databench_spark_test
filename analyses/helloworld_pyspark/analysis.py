"""Helloworld example for pyspark in databench."""

import databench_py

from pyspark import SparkContext

# import logging
# logging.basicConfig(level='DEBUG')


class Analysis(databench_py.Analysis):

    def on_connect(self):
        self.emit('log', 'on_connect: Hello World')

        self.sc = SparkContext("local", "App Name", pyFiles=[
            'analyses/helloworld_pyspark/analysis.py'
        ])

    def on_disconnect(self):
        self.sc.stop()

    def on_frontendmessage(self):
        self.emit('log', {'on_frontendmessage': 'Hello World'})

        do_something = self.sc.parallelize(range(5), 2)
        self.emit('log', do_something.glom().collect())


if __name__ == "__main__":
    analysis = databench_py.Meta('helloworld_pyspark', __doc__, Analysis)
    analysis.event_loop()
