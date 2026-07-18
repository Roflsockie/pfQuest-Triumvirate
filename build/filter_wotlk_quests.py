#!/usr/bin/env python3
"""
Filter quests-wotlk.lua: remove entries that overlap with vanilla/TBC quests.
Keeps only WotLK-exclusive quests (not present in quests.lua or quests-tbc.lua).
"""
import re
import sys
from pathlib import Path

DB_DIR = Path(__file__).resolve().parent.parent / "db"

def extract_quest_ids(filepath):
    """Extract all quest IDs from a pfDB quests data file."""
    text = filepath.read_text(encoding="utf-8")
    # Match [number]= patterns at the top level of the table
    ids = set()
    for m in re.finditer(r'\[(\d+)\]\s*=\s*\{', text):
        ids.add(int(m.group(1)))
    return ids

def main():
    vanilla_file = DB_DIR / "quests.lua"
    tbc_file = DB_DIR / "quests-tbc.lua"
    wotlk_file = DB_DIR / "quests-wotlk.lua"

    print("Extracting quest IDs...")
    vanilla_ids = extract_quest_ids(vanilla_file)
    tbc_ids = extract_quest_ids(tbc_file)
    wotlk_ids = extract_quest_ids(wotlk_file)

    print(f"  Vanilla: {len(vanilla_ids)} quests")
    print(f"  TBC:     {len(tbc_ids)} quests")
    print(f"  WotLK:   {len(wotlk_ids)} quests")

    # IDs to remove: present in vanilla OR tbc
    overlap_vanilla = wotlk_ids & vanilla_ids
    overlap_tbc = (wotlk_ids & tbc_ids) - overlap_vanilla
    keep_ids = wotlk_ids - vanilla_ids - tbc_ids

    print(f"\n  Overlap with vanilla: {len(overlap_vanilla)}")
    if overlap_vanilla:
        for qid in sorted(overlap_vanilla):
            print(f"    - {qid}")
    print(f"  Overlap with TBC only: {len(overlap_tbc)}")
    print(f"  Keeping (WotLK-only): {len(keep_ids)}")

    # Parse the wotlk file and extract each quest entry
    text = wotlk_file.read_text(encoding="utf-8")

    # Find the table content
    match = re.match(r'(pfDB\["quests"\]\["data-wotlk"\]\s*=\s*\{)(.*)(\})', text, re.DOTALL)
    if not match:
        print("ERROR: Could not parse quests-wotlk.lua")
        sys.exit(1)

    prefix = match.group(1)
    body = match.group(2)
    suffix = match.group(3)

    # Extract individual entries: [ID]={...}
    # Use a simple parser that tracks brace depth
    entries = []
    i = 0
    while i < len(body):
        # Find next [number]=
        m = re.search(r'\[(\d+)\]\s*=\s*\{', body[i:])
        if not m:
            break
        start = i + m.start()
        qid = int(m.group(1))
        # Find the matching closing brace
        brace_start = i + m.end() - 1  # position of {
        depth = 1
        j = brace_start + 1
        while j < len(body) and depth > 0:
            if body[j] == '{':
                depth += 1
            elif body[j] == '}':
                depth -= 1
            j += 1
        entry_text = body[start:j].rstrip(',').rstrip()
        entries.append((qid, entry_text))
        i = j

    # Filter: keep only entries not in vanilla or tbc
    kept = []
    removed = 0
    for qid, entry in entries:
        if qid in keep_ids:
            kept.append(entry)
        else:
            removed += 1

    # Rebuild the file
    new_body = ",".join(kept)
    new_text = prefix + new_body + suffix

    # Write back
    wotlk_file.write_text(new_text, encoding="utf-8")
    print(f"\nDone! Removed {removed} entries, kept {len(kept)} WotLK-exclusive quests.")
    print(f"File: {wotlk_file}")

if __name__ == "__main__":
    main()
