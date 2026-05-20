#!/bin/bash
INPUT_PATH="/user/centos/output/ai_human_labeled/part-00000"
OUTPUT_PATH="/user/centos/output/feature5_entity"
RESULTS_DIR=~/mapreduce_results

echo "======================================"
echo " Feature 5: Entity Diversity"
echo "======================================"

chmod +x f5_mapper.py f5_reducer.py
hdfs dfs -rm -r -f $OUTPUT_PATH

hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar \
    -files f5_mapper.py,f5_reducer.py \
    -mapper "python3 f5_mapper.py" \
    -reducer "python3 f5_reducer.py" \
    -input $INPUT_PATH \
    -output $OUTPUT_PATH

if [ $? -eq 0 ]; then
    mkdir -p $RESULTS_DIR
    hdfs dfs -getmerge $OUTPUT_PATH/part-* $RESULTS_DIR/feature5_entity.csv
    echo "======================================"
    echo " Saved: ~/mapreduce_results/feature5_entity.csv"
    echo "======================================"
else
    echo "ERROR: Job failed!"
fi
