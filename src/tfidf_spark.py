#!/usr/bin/env python3
from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer, HashingTF, IDF
from pyspark.ml import Pipeline
from pyspark.sql.functions import col, size, udf
from pyspark.sql.types import StringType, StructType, StructField

spark = SparkSession.builder.appName("TF-IDF").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

schema = StructType([
    StructField("label", StringType(), True),
    StructField("text",  StringType(), True)
])

df = spark.read \
    .option("header", "true") \
    .option("multiline", "true") \
    .option("quote", '"') \
    .option("escape", '"') \
    .option("sep", ",") \
    .schema(schema) \
    .csv("/home/centos/mapreduce_results/ai_human_labeled.csv") \
    .dropna() \
    .filter(col("label").isin("ai", "human"))

print("Records:", df.count())
df.show(3, truncate=50)

pipeline = Pipeline(stages=[
    Tokenizer(inputCol="text", outputCol="words"),
    HashingTF(inputCol="words", outputCol="tf", numFeatures=10000),
    IDF(inputCol="tf", outputCol="tfidf")
])

result = pipeline.fit(df).transform(df)

vec_udf = udf(lambda v: str(dict(zip(
    v.indices[:5].tolist(),
    [round(x,4) for x in v.values[:5].tolist()]
))), StringType())

result.select(
    "label",
    size("words").alias("word_count"),
    vec_udf("tfidf").alias("tfidf_sample")
).coalesce(1).write.mode("overwrite") \
 .csv("/home/centos/mapreduce_results/feature6_tfidf_out", header=True)

print("Done!")
spark.stop()
