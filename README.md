# Start Cluster

> Following: https://aws.amazon.com/articles/4926593393724923

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
