"""Helloworld example for pyspark in databench."""

import databench_py

from pyspark import SparkContext


class HelloWorld(databench_py.Analysis):
    def __init__(self, name, description):
        databench_py.Analysis.__init__(self, name, description)

        self.sc = SparkContext("local", "App Name", pyFiles=[
            'analyses_pyspark/helloworld.py'
        ])

    def on_connect(self):
        self.emit('log', 'on_connect: Hello World')

    def on_frontendmessage(self, msg):
        self.emit('log', 'on_frontendmessage: Hello World')

        do_something = self.sc.parallelize(range(5), 2)
        self.emit('log', do_something.glom().collect())


if __name__ == "__main__":
    hw = HelloWorld('helloworld', __doc__)
    hw.event_loop()
