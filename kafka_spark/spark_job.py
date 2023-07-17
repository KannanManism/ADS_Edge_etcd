from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql import functions as F


# from pyspark.sql import
def write(df, batch_id):
    df.select(F.to_json(F.struct("*")).alias("value")) \
        .agg(F.collect_list(F.col("value")).cast("string").alias("value")) \
        .write \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("topic", "output") \
        .save()
    #


if __name__ == '__main__':
    spark = SparkSession.builder.appName('CarAndTower') \
        .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.1') \
        .getOrCreate()

    spark.conf.set("spark.sql.streaming.forceDeleteTempCheckpointLocation", "true")

    schema = StructType([StructField("timestamp", TimestampType(), True), StructField("carid", IntegerType(), True),
                         StructField("position", IntegerType(), True), StructField("speed", IntegerType(), True),
                         StructField("tower", IntegerType(), True)])

    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "towers") \
        .option("startingOffsets", "latest") \
        .load()

    value_df = df \
        .select(F.from_json(F.col("value").cast("string"), schema).alias("value")) \
        .withColumn("timestamp", F.col("value.timestamp")) \
        .withColumn("carid", F.col("value.carid")) \
        .withColumn("position", F.col("value.position")) \
        .withColumn("speed", F.col("value.speed")) \
        .withColumn("tower", F.col("value.tower")).drop("value")

    towerByCar = value_df.groupBy("carid").agg(F.max("tower").alias("Listed Tower"))

    test = towerByCar.writeStream.outputMode("complete") \
        .foreachBatch(write).start()

    # test = towerByCar.select(F.to_json(F.struct("*")).cast("string").alias("value")) \
    #     .writeStream.outputMode("complete") \
    #     .format("kafka") \
    #     .option("kafka.bootstrap.servers", "localhost:9092") \
    #     .option("topic", "output") \
    #     .option("checkpointLocation", "C:\\Users\\Animesh\\ads ins\\Checkpoint1") \
    #     .start()

    test.awaitTermination()

    # df.show()
