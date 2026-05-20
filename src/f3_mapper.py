#!/usr/bin/env python3
import sys
import csv
from camel_tools.morphology.database import MorphologyDB
from camel_tools.morphology.analyzer import Analyzer

# Initialize camel-tools
db = MorphologyDB.builtin_db()
analyzer = Analyzer(db)

def get_verbs(text):
    words = text.split()
    verbs = []
    for word in words:
        try:
            analyses = analyzer.analyze(word)
            for analysis in analyses:
                if analysis.get('pos') in ('verb', 'VERB'):
                    verbs.append(word)
                    break
        except:
            pass
    return verbs

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

        verbs = get_verbs(text)
        count = len(verbs)
        for verb in verbs:
            print(f"{label}\t{count}\t{verb}")

if __name__ == '__main__':
    mapper()
