from pyspark import SparkContext
sc = SparkContext("local", "App Name", pyFiles=['helloworld_standalone.py'])

print 'hello world'
print sc
