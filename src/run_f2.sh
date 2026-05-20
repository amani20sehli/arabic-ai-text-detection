#!/bin/bash
INPUT_PATH="/user/centos/output/ai_human_labeled/part-00000"
OUTPUT_PATH="/user/centos/output/feature2_periods"
RESULTS_DIR=~/mapreduce_results

echo "======================================"
echo " Feature 2: Number of Periods"
echo "======================================"

chmod +x f2_mapper.py f2_reducer.py
hdfs dfs -rm -r -f $OUTPUT_PATH

hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
    -files f2_mapper.py,f2_reducer.py \
    -mapper "python3 f2_mapper.py" \
    -reducer "python3 f2_reducer.py" \
    -input $INPUT_PATH \
    -output $OUTPUT_PATH

if [ $? -eq 0 ]; then
    mkdir -p $RESULTS_DIR
    hdfs dfs -getmerge $OUTPUT_PATH/part-* $RESULTS_DIR/feature2_periods.csv
    echo "======================================"
    echo " Saved: ~/mapreduce_results/feature2_periods.csv"
    echo "======================================"
else
    echo "ERROR: Job failed!"
fi
