#!/usr/bin/env python3
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import StringType, StructType, StructField

spark = SparkSession.builder.appName("SplitData").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

schema = StructType([
    StructField("label", StringType(), True),
    StructField("text",  StringType(), True)
])

df = spark.read \
    .option("header","true").option("multiline","true") \
    .option("quote",'"').option("escape",'"') \
    .schema(schema) \
    .csv("/home/centos/mapreduce_results/ai_human_labeled.csv") \
    .dropna().filter(col("label").isin("ai","human"))

train, val, test = df.randomSplit([0.70, 0.15, 0.15], seed=42)

OUT = "/home/centos/mapreduce_results"
train.coalesce(1).write.mode("overwrite").csv(f"{OUT}/train_out", header=True)
val.coalesce(1).write.mode("overwrite").csv(f"{OUT}/val_out",   header=True)
test.coalesce(1).write.mode("overwrite").csv(f"{OUT}/test_out",  header=True)

import subprocess
for split in ["train","val","test"]:
    subprocess.run(f"cat {OUT}/{split}_out/part-*.csv > {OUT}/{split}.csv", shell=True)
    subprocess.run(f"rm -rf {OUT}/{split}_out", shell=True)

print(f"Train: {train.count()} | Val: {val.count()} | Test: {test.count()}")
print("Done! Saved: train.csv, val.csv, test.csv")
spark.stop()
