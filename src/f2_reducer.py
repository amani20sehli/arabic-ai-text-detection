#!/usr/bin/env python3
import sys

def reducer():
    rows = []
    ai_total = 0
    human_total = 0
    seen = set()

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        parts = line.split('\t')
        if len(parts) < 3:
            continue
        label = parts[0]
        count = int(parts[1])
        sentence = parts[2]

        if label == 'ai':
            ai_total += count
        elif label == 'human':
            human_total += count

        key = f"{label}_{sentence[:50]}"
        if key not in seen:
            seen.add(key)
            sentence = sentence.replace('"', '""')
            rows.append(f'{label},{count},"{sentence}"')

    # Print header and all rows
    print("label,period_count,sentence_sample")
    for row in rows:
        print(row)

    # Print summary at end
    print("")
    print("=== SUMMARY ===")
    print(f"label,total_periods")
    print(f"ai,{ai_total}")
    print(f"human,{human_total}")

if __name__ == '__main__':
    reducer()
