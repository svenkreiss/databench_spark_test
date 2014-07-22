"""Helloworld example for pyspark in databench."""


import databench

from pyspark import SparkContext


ANALYSIS = databench.Analysis('helloworld', __name__)
ANALYSIS.description = __doc__


@ANALYSIS.signals.on('connect')
def onconnect():
    """Run as soon as a browser connects to this."""
    ANALYSIS.signals.emit('status', {'message': 'Hello World'})

    sc = SparkContext("local", "App Name", pyFiles=['helloworld.py'])
    ANALYSIS.signals.emit('spark_context', sc)
