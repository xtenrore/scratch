import os, sys, json, hashlib, zipfile, io
from clean_meta import clean_costume, clean_sound
import generate_all_sprites
from generate_all_sprites import (
    build_stage, build_simulation_engine, build_entity,
    build_cosmic_ray, build_photon, build_effects,
    build_tool_rail_ui, build_all_tool_buttons,
    build_palette_ui, build_all_palette_items,
    build_inspector_ui,
    build_compendium_ui, build_all_compendium_tabs,
    build_all_compendium_buttons, build_all_compendium_pagination,
    build_all_compendium_categories, build_all_compendium_element_cards,
    build_all_compendium_species_cards,
    build_onboarding_ui, build_telemetry_ui,
    costume_meta, sound_meta
)

print("Assembling Scratch 3.0 project targets...")

stage = build_stage()
sim_engine = build_simulation_engine()
entity = build_entity()
cosmic_ray = build_cosmic_ray()
photon = build_photon()
effects = build_effects()
telemetry = build_telemetry_ui()
tool_rail = build_tool_rail_ui()
tool_buttons = build_all_tool_buttons()
palette = build_palette_ui()
palette_items = build_all_palette_items()
compendium = build_compendium_ui()
comp_tabs = build_all_compendium_tabs()
comp_buttons = build_all_compendium_buttons()
comp_pagination = build_all_compendium_pagination()
comp_categories = build_all_compendium_categories()
comp_elem_cards = build_all_compendium_element_cards()
comp_species_cards = build_all_compendium_species_cards()
inspector = build_inspector_ui()
onboarding = build_onboarding_ui()

targets = [
    stage,
    sim_engine,
    entity,
    cosmic_ray,
    photon,
    effects,
    telemetry,
    tool_rail,
    *tool_buttons,
    palette,
    *palette_items,
    compendium,
    *comp_tabs,
    *comp_buttons,
    *comp_pagination,
    *comp_categories,
    *comp_elem_cards,
    *comp_species_cards,
    inspector,
    onboarding
]

for idx, t in enumerate(targets):
    t["layerOrder"] = idx

# Clean costumes and sounds in each target to remove "raw" bytes
for t in targets:
    t["costumes"] = [clean_costume(c) for c in t["costumes"]]
    t["sounds"] = [clean_sound(s) for s in t["sounds"]]

# Monitor for TOTAL_DISCOVERED in top right header strip
monitors = []

project_json = {
    "targets": targets,
    "monitors": monitors,
    "extensions": [],
    "meta": {
        "semver": "3.0.0",
        "vm": "0.2.0",
        "agent": "Mozilla/5.0 (Scratch 3.0 Advanced Chemistry Simulator)"
    }
}

# Collect all unique assets to write to zip
all_assets = {}

# Add costumes
for key, c in costume_meta.items():
    filename = c["md5ext"]
    all_assets[filename] = c["raw"]

# Add sounds
for key, s in sound_meta.items():
    filename = s["md5ext"]
    all_assets[filename] = s["raw"]

os.makedirs("/workspaces/scratch/sb3", exist_ok=True)
os.makedirs("/workspaces/scratch/assets", exist_ok=True)
os.makedirs("/workspaces/scratch/etc", exist_ok=True)

# Write project.json to disk for debugging/inspection
json_bytes = json.dumps(project_json, indent=2).encode("utf-8")
with open("/workspaces/scratch/etc/project.json", "wb") as f:
    f.write(json_bytes)

# Create .sb3 ZIP archive
sb3_path = "/workspaces/scratch/sb3/ChemistrySimulator.sb3"
with zipfile.ZipFile(sb3_path, "w", zipfile.ZIP_DEFLATED) as zf:
    zf.writestr("project.json", json_bytes)
    for filename, raw in all_assets.items():
        zf.writestr(filename, raw)
        # Also ensure saved to assets folder
        asset_disk_path = os.path.join("/workspaces/scratch/assets", filename)
        if not os.path.exists(asset_disk_path):
            with open(asset_disk_path, "wb") as f:
                f.write(raw)

# Also create lowercase alias
alias_path = "/workspaces/scratch/sb3/chemistry_simulator.sb3"
with open(sb3_path, "rb") as src, open(alias_path, "wb") as dst:
    dst.write(src.read())

sb3_size = os.path.getsize(sb3_path)
print(f"SUCCESS! .sb3 archive created at {sb3_path}")
print(f"Size: {sb3_size} bytes ({sb3_size / 1024:.1f} KB)")
print(f"Total assets in archive: {len(all_assets)} + project.json")
