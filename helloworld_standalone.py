"""Helloworld for pyspark. The purpose is to simple test the Spark
environment."""

from pyspark import SparkContext


if __name__ == "__main__":
    sc = SparkContext("local", "App Name",
                      pyFiles=['helloworld_standalone.py'])

    print 'hello world'
    print sc
