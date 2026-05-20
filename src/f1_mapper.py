#!/usr/bin/env python3
import sys
import csv
import re

def get_elongated_words(text):
    # Match Arabic words with repeated characters 3+ times
    pattern = re.compile(r'\b[\u0600-\u06FF]*?([\u0600-\u06FF])\1{2,}[\u0600-\u06FF]*\b')
    return pattern.findall(text), [m.group() for m in pattern.finditer(text)]

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

        _, words = get_elongated_words(text)
        for word in words:
            print(f"{label}\t{word}")

if __name__ == '__main__':
    mapper()
