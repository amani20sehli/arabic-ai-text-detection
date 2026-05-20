#!/usr/bin/env python3
from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer, HashingTF, IDF, StringIndexer
from pyspark.ml.classification import RandomForestClassifier, LinearSVC
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import BinaryClassificationEvaluator, MulticlassClassificationEvaluator
from pyspark.sql.types import StringType, StructType, StructField
import subprocess

spark = SparkSession.builder.appName("AdvancedModels").getOrCreate()
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
test  = load("/home/centos/hf_data/test.csv")

def evaluate(preds, name):
    acc = MulticlassClassificationEvaluator(labelCol="labelIdx", metricName="accuracy").evaluate(preds)
    f1  = MulticlassClassificationEvaluator(labelCol="labelIdx", metricName="f1").evaluate(preds)
    auc = BinaryClassificationEvaluator(labelCol="labelIdx").evaluate(preds)
    print(f"\n=== {name} Results ===")
    print(f"Accuracy : {round(acc,4)}")
    print(f"F1 Score : {round(f1,4)}")
    print(f"ROC-AUC  : {round(auc,4)}")
    print("="*30)
    return preds.select("label","prediction")

base_stages = [
    StringIndexer(inputCol="label", outputCol="labelIdx"),
    Tokenizer(inputCol="text", outputCol="words"),
    HashingTF(inputCol="words", outputCol="tf", numFeatures=10000),
    IDF(inputCol="tf", outputCol="features")
]

# Random Forest
rf_preds = Pipeline(stages=base_stages + [
    RandomForestClassifier(labelCol="labelIdx", featuresCol="features", numTrees=50)
]).fit(train).transform(test)
evaluate(rf_preds, "Random Forest") \
    .coalesce(1).write.mode("overwrite") \
    .csv("/home/centos/mapreduce_results/rf_out", header=True)

# Linear SVM
svm_preds = Pipeline(stages=base_stages + [
    LinearSVC(labelCol="labelIdx", featuresCol="features")
]).fit(train).transform(test)
evaluate(svm_preds, "Linear SVM") \
    .coalesce(1).write.mode("overwrite") \
    .csv("/home/centos/mapreduce_results/svm_out", header=True)

# Merge outputs
for name in ["rf","svm"]:
    subprocess.run(f"cat /home/centos/mapreduce_results/{name}_out/part-*.csv > /home/centos/mapreduce_results/{name}_predictions.csv", shell=True)
    subprocess.run(f"rm -rf /home/centos/mapreduce_results/{name}_out", shell=True)

print("\nSaved: rf_predictions.csv, svm_predictions.csv")
spark.stop()
