#!/bin/bash
INPUT_PATH="/user/centos/output/ai_human_labeled/part-00000"
OUTPUT_PATH="/user/centos/output/feature3_verbs"
RESULTS_DIR=~/mapreduce_results

echo "======================================"
echo " Feature 3: Number of Verbs"
echo "======================================"

chmod +x f3_mapper.py f3_reducer.py
hdfs dfs -rm -r -f $OUTPUT_PATH

hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
    -files f3_mapper.py,f3_reducer.py \
    -mapper "python3 f3_mapper.py" \
    -reducer "python3 f3_reducer.py" \
    -input $INPUT_PATH \
    -output $OUTPUT_PATH

if [ $? -eq 0 ]; then
    mkdir -p $RESULTS_DIR
    hdfs dfs -getmerge $OUTPUT_PATH/part-* $RESULTS_DIR/feature3_verbs.csv
    echo "======================================"
    echo " Saved: ~/mapreduce_results/feature3_verbs.csv"
    echo "======================================"
else
    echo "ERROR: Job failed!"
fi
