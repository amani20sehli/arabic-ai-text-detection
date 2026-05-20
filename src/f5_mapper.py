#!/usr/bin/env python3
import sys
import csv
from camel_tools.morphology.database import MorphologyDB
from camel_tools.morphology.analyzer import Analyzer

# Initialize camel-tools
db = MorphologyDB.builtin_db()
analyzer = Analyzer(db)

def get_entities(text):
    words = text.split()
    entities = []
    for word in words:
        try:
            analyses = analyzer.analyze(word)
            for analysis in analyses:
                if analysis.get('pos') in ('noun_prop', 'NOUN_PROP'):
                    entities.append(word)
                    break
        except:
            pass
    return entities

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

        entities = get_entities(text)
        total = len(entities)
        unique = len(set(entities))

        if total == 0:
            ratio = 0.0
        else:
            ratio = round(unique / total, 4)

        for entity in set(entities):
            print(f"{label}\t{total}\t{unique}\t{ratio}\t{entity}")

if __name__ == '__main__':
    mapper()
