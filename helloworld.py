from pyspark import SparkContext
sc = SparkContext("local", "App Name", pyFiles=['helloworld.py'])

print 'hello world'
print sc
