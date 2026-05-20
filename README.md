# Scalable Real-time Detection of AI-Generated Arabic Text

**Student:** Amani Abdullah Eid Alsehli
**Course:** MSBDA-801 Big Data Analytics
**Dataset:** [KFUPM-JRCAI Arabic Generated Abstracts](https://huggingface.co/datasets/KFUPM-JRCAI/arabic-generated-abstracts)

---

## Project Overview

A distributed big data pipeline for detecting AI-generated Arabic text using Hadoop MapReduce and Apache Spark, achieving 97.89% accuracy with Linear SVM.

---

## Pipeline Architecture

```
Phase 1: Data Ingestion    → HDFS (51.9 MB, 8,388 records)
Phase 2: MapReduce         → Word Count · Bigrams · AI/Human Labeling
Phase 3: Feature Eng. + ML → 5 Stylometric Features + TF-IDF + 3 Models
Phase 4: Streaming         → Spark Structured Streaming (real-time SVM)
Phase 5: Visualization     → Apache Zeppelin
```

---

## Project Structure

```
arabic-ai-text-detection/
├── data/
│   ├── raw/                  # Original dataset
│   └── processed/            # Labeled + feature files
├── src/
│   ├── mr_label_mapper.py    # MapReduce: AI/Human labeling
│   ├── mr_label_reducer.py
│   ├── f1_mapper.py          # Feature 1: Elongations
│   ├── f2_mapper.py          # Feature 2: Periods
│   ├── f3_mapper.py          # Feature 3: Verbs (Camel-tools)
│   ├── f4_mapper.py          # Feature 4: Dual Words
│   ├── f5_mapper.py          # Feature 5: Entity Diversity
│   ├── tfidf_spark.py        # TF-IDF (Spark MLlib)
│   ├── split_data.py         # Train/Val/Test split (70/15/15)
│   ├── logistic_regression.py # Baseline model
│   ├── advanced_models.py    # Random Forest + Linear SVM
│   ├── evaluation.py         # Metrics + Confusion Matrix
│   ├── scalability_test.py   # Benchmark (1-6 cores)
│   ├── stream_simulate.py    # Stream simulation
│   └── stream_predict.py     # Real-time prediction
├── models/                   # Saved Spark ML models
├── reports/
│   └── figures/              # Visualization outputs
├── notebooks/                # Zeppelin notebooks
├── requirements.txt
└── README.md

```

---

## Results

| Model | Accuracy | F1-Score | ROC-AUC |
|-------|----------|----------|---------|
| Logistic Regression | 97.37% | 97.41% | 99.52% |
| Random Forest | 79.53% | 70.51% | 96.58% |
| **Linear SVM** ⭐ | **97.89%** | **97.91%** | **99.63%** |

---

## Scalability

| Cores | Batch Time | Throughput |
|-------|-----------|------------|
| 1 | 40.03s | 157 rec/s |
| 2 | 23.19s | 271 rec/s |
| 4 | 23.40s | 269 rec/s |
| 6 | 17.02s | 370 rec/s |

---

## Setup

### Requirements
- CentOS / Linux
- Java 21+
- Hadoop 3.3.6
- Python 3.12+
- PySpark 4.1.1
- Camel-tools 1.5.7

### Install dependencies
```bash
pip3 install -r requirements.txt --user
camel_data -i morphology-db-msa-r13
```

### Run Pipeline
```bash
# Phase 2: MapReduce labeling
bash src/run_label_job.sh

# Phase 3: Features
bash src/run_f1.sh
bash src/run_f2.sh
bash src/run_f3.sh
bash src/run_f4.sh
bash src/run_f5.sh

# Phase 3: TF-IDF + Models
spark-submit src/tfidf_spark.py
spark-submit src/split_data.py
spark-submit src/logistic_regression.py
spark-submit src/advanced_models.py

# Phase 4: Streaming (two terminals)
spark-submit src/stream_predict.py   # Terminal 1
python3 src/stream_simulate.py       # Terminal 2
```
