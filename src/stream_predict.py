#!/usr/bin/env python3
# Task 4.2: Real-time prediction using Spark Structured Streaming
from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer, HashingTF, IDF, StringIndexer
from pyspark.ml.classification import LinearSVC
from pyspark.ml import Pipeline
from pyspark.sql.functions import col
from pyspark.sql.types import StringType, StructType, StructField

spark = SparkSession.builder.appName("StreamPredict") \
    .config("spark.sql.streaming.checkpointLocation","/home/centos/stream_checkpoint") \
    .getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

schema = StructType([
    StructField("label", StringType(), True),
    StructField("text",  StringType(), True)
])

# Train model on train data
train = spark.read \
    .option("header","true").option("multiline","true") \
    .option("quote",'"').option("escape",'"') \
    .schema(schema).csv("/home/centos/hf_data/train.csv").dropna()

model = Pipeline(stages=[
    StringIndexer(inputCol="label", outputCol="labelIdx"),
    Tokenizer(inputCol="text", outputCol="words"),
    HashingTF(inputCol="words", outputCol="tf", numFeatures=10000),
    IDF(inputCol="tf", outputCol="features"),
    LinearSVC(labelCol="labelIdx", featuresCol="features")
]).fit(train)

print("Model trained! Waiting for stream...")

# Read stream
stream_df = spark.readStream \
    .option("header","true") \
    .schema(schema) \
    .csv("/home/centos/stream_input")

# Predict
preds = model.transform(stream_df) \
    .select("label","prediction")

# Output to console
query = preds.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", False) \
    .start()

query.awaitTermination(60)
spark.stop()
