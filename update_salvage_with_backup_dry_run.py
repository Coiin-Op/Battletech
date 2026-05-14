# file: update_salvage_dryrun.py
import os
import json

# ======== USER CONFIG ========
TARGET_DIR = r"F:\Internet\Steam\steamapps\common\BATTLETECH\Mods\Missions"
NEW_VALUE = 55  # SalvagePotential value you would set
MISSION_PREFIXES = [
    "ambushconvoy", "assassinate", "attackdefend", "capturebase", "captureescort",
    "defendbase", "destroybase", "duoduel", "firemission", "rescue", "simplebattle",
    "testdrive", "threewaybattle", "fourwaybattle", "battleroyal", "battleroyale_v2",
    "blackout", "defenceindepth", "organizedretreat", "soloduel", "theswitch_assassinate",
    "warzone", "warzone_v2", "encounterLayers", "contracts", "contract_overide"
]
# =============================

# First, count total JSON files to process
total_files = 0
for dirpath, dirnames, filenames in os.walk(TARGET_DIR):
    for filename in filenames:
        if filename.lower().endswith(".json") and any(filename.lower().startswith(prefix.lower()) for prefix in MISSION_PREFIXES):
            total_files += 1

print(f"Dry-run mode: Found {total_files} mission JSON files to process...\n")

# Process files in dry-run mode
processed_count = 0
for dirpath, dirnames, filenames in os.walk(TARGET_DIR):
    for filename in filenames:
        if filename.lower().endswith(".json"):
            if not any(filename.lower().startswith(prefix.lower()) for prefix in MISSION_PREFIXES):
                continue

            file_path = os.path.join(dirpath, filename)
            processed_count += 1
            print(f"[{processed_count}/{total_files}] Would process: {file_path}")

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Show current SalvagePotential without changing
                if isinstance(data, dict):
                    current = data.get("SalvagePotential", "Not set")
                elif isinstance(data, list):
                    current = [item.get("SalvagePotential", "Not set") for item in data if isinstance(item, dict)]
                else:
                    current = "Unknown format"

                print(f"    Current SalvagePotential: {current} --> Would set to {NEW_VALUE}")
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

print("\nDry-run complete. No files were modified.")