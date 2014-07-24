"""Helloworld example for pyspark in databench."""

import databench_py

import logging
from pyspark import SparkContext

# logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('helloworld_kernel')


class HelloWorld(databench_py.Analysis):
    def __init__(self, name, description):
        databench_py.Analysis.__init__(self, name, description)

        self.sc = SparkContext("local", "App Name", pyFiles=[
            'analyses_pyspark/helloworld.py'
        ])

    def on_connect(self):
        self.emit('log', 'on_connect: Hello World')

    def on_frontendmessage(self, msg):
        logger.debug('on_frontendmessage: '+str(msg))
        self.emit('log', 'on_frontendmessage: Hello World')

        do_something = self.sc.parallelize(range(5), 5).glom().collect()
        print do_something
        self.emit('log', str(do_something))


if __name__ == "__main__":
    hw = HelloWorld('helloworld', __doc__)
    hw.event_loop()
