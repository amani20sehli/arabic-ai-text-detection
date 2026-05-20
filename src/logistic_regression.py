#!/usr/bin/env python3
from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer, HashingTF, IDF, StringIndexer
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import BinaryClassificationEvaluator, MulticlassClassificationEvaluator
from pyspark.sql.functions import col
from pyspark.sql.types import StringType, StructType, StructField

spark = SparkSession.builder.appName("LogisticRegression").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

schema = StructType([
    StructField("label", StringType(), True),
    StructField("text",  StringType(), True)
])

def load(path):
    return spark.read \
        .option("header","true").option("multiline","true") \
        .option("quote",'"').option("escape",'"') \
        .schema(schema).csv(path).dropna()

train = load("/home/centos/hf_data/train.csv")
val   = load("/home/centos/hf_data/val.csv")
test  = load("/home/centos/hf_data/test.csv")

pipeline = Pipeline(stages=[
    StringIndexer(inputCol="label", outputCol="labelIdx"),
    Tokenizer(inputCol="text", outputCol="words"),
    HashingTF(inputCol="words", outputCol="tf", numFeatures=10000),
    IDF(inputCol="tf", outputCol="features"),
    LogisticRegression(labelCol="labelIdx", featuresCol="features")
])

model = pipeline.fit(train)
preds = model.transform(test)

acc = MulticlassClassificationEvaluator(labelCol="labelIdx", metricName="accuracy").evaluate(preds)
f1  = MulticlassClassificationEvaluator(labelCol="labelIdx", metricName="f1").evaluate(preds)
auc = BinaryClassificationEvaluator(labelCol="labelIdx").evaluate(preds)

print("\n=== Logistic Regression Results ===")
print(f"Accuracy : {round(acc,4)}")
print(f"F1 Score : {round(f1,4)}")
print(f"ROC-AUC  : {round(auc,4)}")
print("===================================\n")

# Save label and prediction only (no probability)
preds.select("label", "prediction") \
     .coalesce(1).write.mode("overwrite") \
     .csv("/home/centos/mapreduce_results/lr_predictions_out", header=True)

import subprocess
subprocess.run("cat /home/centos/mapreduce_results/lr_predictions_out/part-*.csv > /home/centos/mapreduce_results/lr_predictions.csv", shell=True)
subprocess.run("rm -rf /home/centos/mapreduce_results/lr_predictions_out", shell=True)

print("Saved: lr_predictions.csv")
spark.stop()
