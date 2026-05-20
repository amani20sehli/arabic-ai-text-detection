#!/usr/bin/env python3
import sys
import csv
import re

def get_dual_words(text):
    # Arabic dual: words ending with ان or ين
    pattern = re.compile(r'\b[\u0600-\u06FF]+(?:\u0627\u0646|\u064a\u0646)\b')
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

        count, dual_words = get_dual_words(text)
        for word in dual_words:
            print(f"{label}\t{count}\t{word}")

if __name__ == '__main__':
    mapper()
