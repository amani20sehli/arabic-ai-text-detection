#!/usr/bin/env python3
import sys

def reducer():
    print("label,elongated_word")
    
    seen = set()
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        parts = line.split('\t')
        if len(parts) < 2:
            continue
        label = parts[0]
        word = parts[1]
        
        key = f"{label}_{word}"
        if key not in seen:
            seen.add(key)
            print(f"{label},{word}")

if __name__ == '__main__':
    reducer()
