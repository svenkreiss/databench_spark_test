# Databench and Spark

This demo runs `pyspark` locally and interfaces with [Databench](http://www.svenkreiss.com/databench/). On a Mac, run `brew install apache-spark` which installs `spark` and `pyspark`. As a test, you can run `pyspark helloworld_standalone.py`.

For Databench, run `pip install -r requirements.txt` (which installs the experiemental `dev-0.3` branch of Databench) and then run `databench`.

The `mcrisk` example is based on [montecarlorisk](https://github.com/sryza/montecarlorisk) code in Scala/Spark which is explained in this Cloudera blog post by Sandy Ryza: [Estimizing Financial Risk with Apache Spark](http://blog.cloudera.com/blog/2014/07/estimating-financial-risk-with-apache-spark/).


### Notes

I am also working on interfacing Databench with Scala and then running the mcrisk example in Scala with Databench. Some dev notes (meaning nothing works) are here [notes_emr](notes_emr.md).
