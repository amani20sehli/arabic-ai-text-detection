#!/usr/bin/env python3
from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer, HashingTF, IDF, StringIndexer
from pyspark.ml.classification import LogisticRegression, RandomForestClassifier, LinearSVC
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import BinaryClassificationEvaluator, MulticlassClassificationEvaluator
from pyspark.mllib.evaluation import MulticlassMetrics
from pyspark.sql.types import StringType, StructType, StructField

spark = SparkSession.builder.appName("Evaluation").getOrCreate()
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

base_stages = [
    StringIndexer(inputCol="label", outputCol="labelIdx"),
    Tokenizer(inputCol="text", outputCol="words"),
    HashingTF(inputCol="words", outputCol="tf", numFeatures=10000),
    IDF(inputCol="tf", outputCol="features")
]

models = {
    "Logistic Regression": LogisticRegression(labelCol="labelIdx", featuresCol="features"),
    "Random Forest":       RandomForestClassifier(labelCol="labelIdx", featuresCol="features", numTrees=50),
    "Linear SVM":          LinearSVC(labelCol="labelIdx", featuresCol="features")
}

for name, clf in models.items():
    preds = Pipeline(stages=base_stages + [clf]).fit(train).transform(test)

    acc = MulticlassClassificationEvaluator(labelCol="labelIdx", metricName="accuracy").evaluate(preds)
    f1  = MulticlassClassificationEvaluator(labelCol="labelIdx", metricName="f1").evaluate(preds)
    auc = BinaryClassificationEvaluator(labelCol="labelIdx").evaluate(preds)

    # Confusion Matrix
    metrics = MulticlassMetrics(preds.select("prediction","labelIdx").rdd.map(tuple))
    cm = metrics.confusionMatrix().toArray()

    print(f"\n=== {name} ===")
    print(f"Accuracy : {round(acc,4)}")
    print(f"F1 Score : {round(f1,4)}")
    print(f"ROC-AUC  : {round(auc,4)}")
    print(f"Confusion Matrix:")
    print(f"  TP={int(cm[0][0])} FP={int(cm[0][1])}")
    print(f"  FN={int(cm[1][0])} TN={int(cm[1][1])}")
    print("="*30)

spark.stop()
