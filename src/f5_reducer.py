#!/usr/bin/env python3
import sys

def reducer():
    rows = []
    ai_total_entities = 0
    ai_unique_entities = 0
    human_total_entities = 0
    human_unique_entities = 0
    seen = set()

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        parts = line.split('\t')
        if len(parts) < 5:
            continue
        label   = parts[0]
        total   = int(parts[1])
        unique  = int(parts[2])
        ratio   = parts[3]
        entity  = parts[4]

        if label == 'ai':
            ai_total_entities += total
            ai_unique_entities += unique
        elif label == 'human':
            human_total_entities += total
            human_unique_entities += unique

        key = f"{label}_{entity}"
        if key not in seen:
            seen.add(key)
            rows.append(f'{label},{total},{unique},{ratio},{entity}')

    # Print header and all rows
    print("label,total_entities,unique_entities,diversity_ratio,entity")
    for row in rows:
        print(row)

    # Print summary
    ai_ratio = round(ai_unique_entities / ai_total_entities, 4) if ai_total_entities > 0 else 0
    human_ratio = round(human_unique_entities / human_total_entities, 4) if human_total_entities > 0 else 0

    print("")
    print("=== SUMMARY ===")
    print("label,total_entities,unique_entities,overall_diversity_ratio")
    print(f"ai,{ai_total_entities},{ai_unique_entities},{ai_ratio}")
    print(f"human,{human_total_entities},{human_unique_entities},{human_ratio}")

if __name__ == '__main__':
    reducer()
