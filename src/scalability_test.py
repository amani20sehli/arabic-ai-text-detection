#!/usr/bin/env python3
import time, os
from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer, HashingTF, IDF, StringIndexer
from pyspark.ml.classification import LinearSVC
from pyspark.ml import Pipeline
from pyspark.sql.types import StringType, StructType, StructField

schema = StructType([
    StructField("label", StringType(), True),
    StructField("text",  StringType(), True)
])

results = []

for cores in [1, 2, 4, 6]:
    spark = SparkSession.builder \
        .appName("ScalabilityTest") \
        .master(f"local[{cores}]") \
        .config("spark.sql.streaming.checkpointLocation","/home/centos/scale_checkpoint") \
        .getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")

    def load(path):
        return spark.read \
            .option("header","true").option("multiline","true") \
            .option("quote",'"').option("escape",'"') \
            .schema(schema).csv(path).dropna()

    train = load("/home/centos/hf_data/train.csv")
    test  = load("/home/centos/hf_data/test.csv")

    pipeline = Pipeline(stages=[
        StringIndexer(inputCol="label", outputCol="labelIdx"),
        Tokenizer(inputCol="text", outputCol="words"),
        HashingTF(inputCol="words", outputCol="tf", numFeatures=10000),
        IDF(inputCol="tf", outputCol="features"),
        LinearSVC(labelCol="labelIdx", featuresCol="features")
    ])

    # ── Phase 3: Batch Processing Time ──
    start = time.time()
    model = pipeline.fit(train)
    preds = model.transform(test)
    preds.count()
    batch_time = round(time.time() - start, 2)

    # ── Phase 4: Stream Latency ──
    os.makedirs("/home/centos/scale_stream", exist_ok=True)
    # write small test batch
    test.limit(100).coalesce(1).write.mode("overwrite") \
        .option("header","true").csv("/home/centos/scale_stream")

    stream_df = spark.readStream \
        .option("header","true").schema(schema) \
        .csv("/home/centos/scale_stream")

    start_stream = time.time()
    query = model.transform(stream_df) \
        .writeStream.outputMode("append") \
        .format("memory").queryName("stream_test") \
        .start()
    query.processAllAvailable()
    stream_latency = round(time.time() - start_stream, 2)
    query.stop()

    records = test.count()
    throughput = round(records / batch_time, 2)

    results.append((cores, batch_time, stream_latency, throughput))
    print(f"Cores={cores} | Batch={batch_time}s | Stream Latency={stream_latency}s | Throughput={throughput} rec/s")

    spark.stop()
    import shutil
    shutil.rmtree("/home/centos/scale_checkpoint", ignore_errors=True)
    shutil.rmtree("/home/centos/scale_stream", ignore_errors=True)

print("\n=== Scalability Test Results ===")
print("Cores | Batch Time(s) | Stream Latency(s) | Throughput(rec/s)")
for r in results:
    print(f"  {r[0]}   |     {r[1]}       |       {r[2]}        |     {r[3]}")
print("="*60)
