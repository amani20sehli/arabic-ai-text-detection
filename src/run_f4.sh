#!/bin/bash
INPUT_PATH="/user/centos/output/ai_human_labeled/part-00000"
OUTPUT_PATH="/user/centos/output/feature4_dual"
RESULTS_DIR=~/mapreduce_results

echo "======================================"
echo " Feature 4: Number of Dual Words"
echo "======================================"

chmod +x f4_mapper.py f4_reducer.py
hdfs dfs -rm -r -f $OUTPUT_PATH

hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
    -files f4_mapper.py,f4_reducer.py \
    -mapper "python3 f4_mapper.py" \
    -reducer "python3 f4_reducer.py" \
    -input $INPUT_PATH \
    -output $OUTPUT_PATH

if [ $? -eq 0 ]; then
    mkdir -p $RESULTS_DIR
    hdfs dfs -getmerge $OUTPUT_PATH/part-* $RESULTS_DIR/feature4_dual.csv
    echo "======================================"
    echo " Saved: ~/mapreduce_results/feature4_dual.csv"
    echo "======================================"
else
    echo "ERROR: Job failed!"
fi
