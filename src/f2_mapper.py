#!/usr/bin/env python3
import sys
import csv
import re

def get_periods(text):
    # Match sentences ending with period
    pattern = re.compile(r'[^.!؟]+[.!؟]+')
    matches = pattern.findall(text)
    return len(matches), matches

def mapper():
    reader = csv.reader(sys.stdin)
    first_line = True
    for row in reader:
        if first_line:
            first_line = False
            continue
        if len(row) < 2:
            continue

        label = row[0].strip()
        text = row[1].strip().strip('"')

        if not text or label not in ('ai', 'human'):
            continue

        count, sentences = get_periods(text)
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                print(f"{label}\t{count}\t{sentence}")

if __name__ == '__main__':
    mapper()
