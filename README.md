# Start Cluster

> Following: https://aws.amazon.com/articles/4926593393724923

This assumes you have the elastic-mapreduce-cli (in Ruby) installed in a parallel folder.

In IAM create a role for EC2 with Poweruser rights called `sparktest`.
Create an S3 bucket (here svenkreiss-spark-test) and under properties, allows "List" rights for "Authenticated Users".

Have a `credentials.json` file:

```
{
"access_id": "xxxxxx",
"private_key": "xxxxxx",
"key-pair": "xxxxxx",
"key-pair-file": "xxxxxx.pem",
"log_uri": "s3n://svenkreiss-spark-test/log/",
"region": "us-east-1"
}
```

Create cluster with:

```bash
../elastic-mapreduce-cli/elastic-mapreduce --create --alive --name "Spark/Shark Cluster"  --bootstrap-action s3://elasticmapreduce/samples/spark/0.8.1/install-spark-shark.sh --bootstrap-name "Spark/Shark"  --instance-type m1.medium --instance-count 2 --jobflow-role sparktest
```


# Run example

To ssh into the master node: `../elastic-mapreduce-cli/elastic-mapreduce -j j-xxxxx --ssh`
Optional: To create a socks tunnel: `../elastic-mapreduce-cli/elastic-mapreduce -j j-xxxxx --socks`

On the master:

```bash
SPARK_MEM="2g" /home/hadoop/spark/spark-shell
```

```scala
val file = sc.textFile("s3://bigdatademo/sample/wiki/")
val reducedList = file.map(l => l.split(" ")).map(l => (l(1), l(2).toInt)).reduceByKey(_+_, 3)
reducedList.cache
val sortedList = reducedList.map(x => (x._2, x._1)).sortByKey(false).take(50)
```


# Beyond trivial

> Inspired by http://www.sujee.net/tech/articles/hadoop/amazon-emr-beyond-basics/

The test project I am going to use is this one: [montecarlorisk](https://github.com/sryza/montecarlorisk). Clone it and run `mvn package` to produce a jar file.

Put this jar on S3 (configure s3 with `s3cmd --configure` first).

```bash
s3cmd put ../spark_montecarlorisk/target/montecarlo-risk-0.0.1-SNAPSHOT.jar s3://svenkreiss-spark-test/jars/
```

Also put the data files on S3:

```bash
s3cmd sync ../spark_montecarlorisk/data/ s3://svenkreiss-spark-test/data/
```

Launch cluster and run job (broken):

```bash
../elastic-mapreduce-cli/elastic-mapreduce \
--create --plain-output \
--name "testspark__$(date +%Y%m%d-%H%M%S)"  \
--num-instances "2"  \
--master-instance-type "m1.medium" \
--slave-instance-type "m1.medium" \
--jar s3://svenkreiss-spark-test/jars/montecarlo-risk-0.0.1-SNAPSHOT.jar \
--main-class com.cloudera.datascience.montecarlorisk.MonteCarloRisk \
--args "s3://svenkreiss-spark-test/data/instruments.csv 50 2 s3://svenkreiss-spark-test/data/means.csv s3://svenkreiss-spark-test/data/covariances.csv" \
--log-uri s3://svenkreiss-spark-test/logs/
```

Launch cluster (takes 18min). This can probably also simply be done in the web console.

```bash
export JOBFLOWID=$(../elastic-mapreduce-cli/elastic-mapreduce --create --plain-output --alive --name "Spark/Shark Cluster"  --bootstrap-action s3://elasticmapreduce/samples/spark/0.8.1/install-spark-shark.sh --bootstrap-name "Spark/Shark"  --instance-type m1.medium --instance-count 2 --jobflow-role sparktest)
```

Run job. It seems the "Add Step" web interface could do the same.

```bash
../elastic-mapreduce-cli/elastic-mapreduce \
-j $JOBFLOWID \
--jar s3://svenkreiss-spark-test/jars/montecarlo-risk-0.0.1-SNAPSHOT.jar \
--main-class com.cloudera.datascience.montecarlorisk.MonteCarloRisk \
--args "s3://svenkreiss-spark-test/data/instruments.csv 50 2 s3://svenkreiss-spark-test/data/means.csv s3://svenkreiss-spark-test/data/covariances.csv" \
--log-uri s3://svenkreiss-spark-test/log/
```

Investigate log:

```bash
s3cmd sync s3://svenkreiss-spark-test/log/ log/
```



# Experiments

```bash
java -cp /home/hadoop/spark/jars/*:/home/hadoop/spark/conf:/home/hadoop/spark/jars/spark-assembly-0.8.1-incubating-hadoop1.0.4.jar:/home/hadoop/commons-math3-3.3.jar:/home/hadoop/montecarlorisk/target/montecarlo-risk-0.0.1-SNAPSHOT.jar com.cloudera.datascience.montecarlorisk.MonteCarloRisk
```


# Local Apache Spark

On a Mac, it is as simple as `brew install apache-spark` now which installs `spark` and `pyspark`. You can run `helloworld.py` with pyspark, but not with plain python.

