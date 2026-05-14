# file: update_salvage_filtered.py
import os
import json
import shutil

# ======== USER CONFIG ========
TARGET_DIR = r"F:\Internet\Steam\steamapps\common\BATTLETECH\Mods\Missions"  # <-- your missions folder
BACKUP_DIR = os.path.join(TARGET_DIR, "backup_jsons")
NEW_VALUE = 55  # SalvagePotential value to set

# Mission filename prefixes to process
MISSION_PREFIXES = [
    "ambushconvoy", "assassinate", "attackdefend", "capturebase", "captureescort",
    "defendbase", "destroybase", "duoduel", "firemission", "rescue", "simplebattle",
    "testdrive", "threewaybattle", "fourwaybattle", "battleroyal", "battleroyale_v2",
    "blackout", "defenceindepth", "organizedretreat", "soloduel", "theswitch_assassinate",
    "warzone", "warzone_v2", "encounterLayers", "contracts", "contract_overide"
]
# =============================

# Make backup folder if it doesn't exist
os.makedirs(BACKUP_DIR, exist_ok=True)

# First, count total JSON files to process
total_files = 0
for dirpath, dirnames, filenames in os.walk(TARGET_DIR):
    for filename in filenames:
        if filename.lower().endswith(".json") and BACKUP_DIR not in os.path.join(dirpath, filename):
            if any(filename.lower().startswith(prefix.lower()) for prefix in MISSION_PREFIXES):
                total_files += 1

print(f"Found {total_files} mission JSON files to process...\n")

# Process files
processed_count = 0
updated_files = []

for dirpath, dirnames, filenames in os.walk(TARGET_DIR):
    for filename in filenames:
        if filename.lower().endswith(".json"):
            file_path = os.path.join(dirpath, filename)

            # Skip backup folder
            if BACKUP_DIR in file_path:
                continue

            # Only process files with prefixes
            if not any(filename.lower().startswith(prefix.lower()) for prefix in MISSION_PREFIXES):
                continue

            # Increment and print progress
            processed_count += 1
            print(f"[{processed_count}/{total_files}] Processing: {file_path}")

            # Backup original
            rel_path = os.path.relpath(file_path, TARGET_DIR)
            backup_path = os.path.join(BACKUP_DIR, rel_path)
            os.makedirs(os.path.dirname(backup_path), exist_ok=True)
            shutil.copy2(file_path, backup_path)

            try:
                # Load JSON
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Update SalvagePotential
                if isinstance(data, dict):
                    data["SalvagePotential"] = NEW_VALUE
                elif isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict):
                            item["SalvagePotential"] = NEW_VALUE

                # Save file back
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4)

                updated_files.append(file_path)
            except Exception as e:
                print(f"Error updating {file_path}: {e}")

print(f"\nUpdated SalvagePotential in {len(updated_files)} mission files.")
print(f"Backup of original JSONs saved in: {BACKUP_DIR}")