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
        word = parts[2]

        if label == 'ai':
            ai_total += count
        elif label == 'human':
            human_total += count

        key = f"{label}_{word}"
        if key not in seen:
            seen.add(key)
            rows.append(f'{label},{count},{word}')

    # Print header and all rows
    print("label,dual_count,dual_word")
    for row in rows:
        print(row)

    # Print summary
    print("")
    print("=== SUMMARY ===")
    print("label,total_dual_words")
    print(f"ai,{ai_total}")
    print(f"human,{human_total}")

if __name__ == '__main__':
    reducer()
