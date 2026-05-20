#!/usr/bin/env python3
# Task 4.1: Simulate live stream of Arabic abstracts
import csv, time, os, random

INPUT  = "/home/centos/hf_data/test.csv"
STREAM = "/home/centos/stream_input"
os.makedirs(STREAM, exist_ok=True)

rows = []
with open(INPUT) as f:
    reader = csv.reader(f)
    next(reader)
    rows = list(reader)

print(f"Streaming {len(rows)} records...")
batch = 1
for i in range(0, len(rows), 10):
    chunk = rows[i:i+10]
    path  = f"{STREAM}/batch_{batch:04d}.csv"
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["label","text"])
        writer.writerows(chunk)
    print(f"Sent batch {batch} ({len(chunk)} records)")
    batch += 1
    time.sleep(5)

print("Stream simulation complete!")
