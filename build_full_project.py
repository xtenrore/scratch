import os, sys, json, hashlib, zipfile, io, uuid
import db_chemistry, gen_audio, gen_graphics

print("Starting full build of Chemistry Simulator Scratch 3.0...")

# 1. Generate audio assets
sound_meta = gen_audio.generate_all_sounds()

# 2. Generate graphic assets
costume_meta = gen_graphics.generate_all_assets()

# Helper for unique block IDs
def new_id():
    return uuid.uuid4().hex[:16]

# Global lists and variables definitions
STAGE_VARS = {
    "v_tool": ["CURRENT_TOOL", "drag"],
    "v_uv": ["UV_ACTIVE", 0],
    "v_freeze": ["TIME_FROZEN", 0],
    "v_palette": ["SHOW_PALETTE", 0],
    "v_compendium": ["SHOW_COMPENDIUM", 0],
    "v_info": ["SHOW_INFO", 0],
    "v_onboarding": ["SHOW_ONBOARDING", 1],
    "v_volume": ["MASTER_VOLUME", 100],
    "v_discovered": ["TOTAL_DISCOVERED", 19],
    "v_spawn_id": ["SPAWN_SPECIES_ID", 1],
    "v_spawn_x": ["SPAWN_X", 0],
    "v_spawn_y": ["SPAWN_Y", 0],
    "v_inspect_id": ["INSPECT_SPECIES_ID", 1],
    "v_toast_id": ["TOAST_SPECIES_ID", 1],
    "v_fx_x": ["FX_X", 0],
    "v_fx_y": ["FX_Y", 0],
    "v_next_id": ["NEXT_ENTITY_ID", 1],
    "v_save_code": ["SAVE_CODE", ""],
    "v_comp_tab": ["COMPENDIUM_TAB", 1]
}

STAGE_LISTS = {
    "l_db_id": ["DB_ID", [s["id"] for s in db_chemistry.SPECIES]],
    "l_db_formula": ["DB_FORMULA", [s["symbol"] for s in db_chemistry.SPECIES]],
    "l_db_name": ["DB_NAME", [s["name"] for s in db_chemistry.SPECIES]],
    "l_db_charge": ["DB_CHARGE", [s["charge"] for s in db_chemistry.SPECIES]],
    "l_db_type": ["DB_TYPE", [s["type"] for s in db_chemistry.SPECIES]],
    "l_db_atoms": ["DB_ATOMS", [s["atoms"] for s in db_chemistry.SPECIES]],
    "l_db_desc": ["DB_DESC", [s["desc"] for s in db_chemistry.SPECIES]],
    "l_db_disc": ["DB_DISCOVERED", [1 if s["id"] <= 19 else 0 for s in db_chemistry.SPECIES]],
    "l_rx_key": ["RX_KEY", [rx["key"] for rx in db_chemistry.REACTIONS]],
    "l_rx_prod": ["RX_PROD", [rx["product_id"] for rx in db_chemistry.REACTIONS]],
    "l_rx_exo": ["RX_EXO", [rx["is_exo"] for rx in db_chemistry.REACTIONS]],
    "l_rx_uv": ["RX_UV", [rx["req_uv"] for rx in db_chemistry.REACTIONS]],
    "l_rx_desc": ["RX_DESC", [rx["desc"] for rx in db_chemistry.REACTIONS]],
    "l_ion_src": ["IONIZE_SRC", [rule["src_id"] for rule in db_chemistry.IONIZE_RULES]],
    "l_ion_dst": ["IONIZE_DST", [rule["dst_id"] for rule in db_chemistry.IONIZE_RULES]],
    "l_ent_act": ["ENTITY_ACTIVE", []],
    "l_ent_spc": ["ENTITY_SPECIES", []],
    "l_ent_x": ["ENTITY_X", []],
    "l_ent_y": ["ENTITY_Y", []],
    "l_ent_vx": ["ENTITY_VX", []],
    "l_ent_vy": ["ENTITY_VY", []]
}

BROADCASTS = {
    "b_init_sim": "INIT_SIMULATION",
    "b_update_ui": "UPDATE_UI",
    "b_update_bg": "UPDATE_BACKDROP",
    "b_spawn_req": "SPAWN_REQUEST",
    "b_clear_all": "CLEAR_ALL",
    "b_fx_exo": "PLAY_FX_EXO",
    "b_fx_bond": "PLAY_FX_BOND",
    "b_fx_zap": "PLAY_FX_ZAP",
    "b_fx_del": "PLAY_FX_DELETE",
    "b_spawn_photon": "SPAWN_PHOTON",
    "b_show_info": "SHOW_INFO",
    "b_show_toast": "SHOW_TOAST",
    "b_show_onb": "SHOW_ONBOARDING",
    "b_prompt_save": "PROMPT_SAVE_LOAD"
}

# Scratch block builder helper
class BlockContext:
    def __init__(self):
        self.blocks = {}

    def add(self, opcode, inputs=None, fields=None, shadow=False, topLevel=False, next_id=None, parent_id=None, mutation=None, x=0, y=0):
        b_id = new_id()
        block = {
            "opcode": opcode,
            "next": next_id,
            "parent": parent_id,
            "inputs": inputs or {},
            "fields": fields or {},
            "shadow": shadow,
            "topLevel": topLevel
        }
        if topLevel:
            block["x"] = x
            block["y"] = y
        if mutation:
            block["mutation"] = mutation
        self.blocks[b_id] = block

        # Auto-set parent for child input blocks
        for inp_name, inp_val in (inputs or {}).items():
            if isinstance(inp_val, list) and len(inp_val) >= 2:
                child_id = None
                if inp_val[0] in (1, 2, 3) and isinstance(inp_val[1], str):
                    child_id = inp_val[1]
                if child_id and child_id in self.blocks:
                    self.blocks[child_id]["parent"] = b_id

        return b_id

    def chain(self, block_ids, parent=None):
        for i in range(len(block_ids) - 1):
            curr_id = block_ids[i]
            nxt_id = block_ids[i+1]
            self.blocks[curr_id]["next"] = nxt_id
            self.blocks[nxt_id]["parent"] = curr_id
        if parent and len(block_ids) > 0:
            self.blocks[block_ids[0]]["parent"] = parent

# Build Stage
def build_stage():
    ctx = BlockContext()

    # Flag clicked script
    flag_id = ctx.add("event_whenflagclicked", topLevel=True, x=50, y=50)
    bc_init_sim = ctx.add("event_broadcast", inputs={"BROADCAST_INPUT": [1, [11, "INIT_SIMULATION", "b_init_sim"]]})
    bc_upd_bg = ctx.add("event_broadcast", inputs={"BROADCAST_INPUT": [1, [11, "UPDATE_BACKDROP", "b_update_bg"]]})
    bc_init_ui = ctx.add("event_broadcast", inputs={"BROADCAST_INPUT": [1, [11, "UPDATE_UI", "b_update_ui"]]})
    ctx.chain([flag_id, bc_init_sim, bc_upd_bg, bc_init_ui])

    # Update backdrop on message
    bg_hat = ctx.add("event_whenbroadcastreceived", fields={"BROADCAST_OPTION": ["UPDATE_BACKDROP", "b_update_bg"]}, topLevel=True, x=50, y=220)
    eq_freeze = ctx.add("operator_equals", inputs={"OPERAND1": [3, [12, "TIME_FROZEN", "v_freeze"], [10, ""]], "OPERAND2": [1, [10, "1"]]})
    bg_frozen_menu = ctx.add("looks_backdrops", fields={"BACKDROP": ["backdrop_frozen", None]}, shadow=True)
    sw_freeze = ctx.add("looks_switchbackdropto", inputs={"BACKDROP": [1, bg_frozen_menu]})

    eq_uv = ctx.add("operator_equals", inputs={"OPERAND1": [3, [12, "UV_ACTIVE", "v_uv"], [10, ""]], "OPERAND2": [1, [10, "1"]]})
    bg_uv_menu = ctx.add("looks_backdrops", fields={"BACKDROP": ["backdrop_uv", None]}, shadow=True)
    sw_uv = ctx.add("looks_switchbackdropto", inputs={"BACKDROP": [1, bg_uv_menu]})

    bg_vac_menu = ctx.add("looks_backdrops", fields={"BACKDROP": ["backdrop_vacuum", None]}, shadow=True)
    sw_vac = ctx.add("looks_switchbackdropto", inputs={"BACKDROP": [1, bg_vac_menu]})

    if_uv_else = ctx.add("control_if_else", inputs={"CONDITION": [2, eq_uv], "SUBSTACK": [2, sw_uv], "SUBSTACK2": [2, sw_vac]})
    ctx.blocks[sw_uv]["parent"] = if_uv_else
    ctx.blocks[sw_vac]["parent"] = if_uv_else

    if_freeze_else = ctx.add("control_if_else", inputs={"CONDITION": [2, eq_freeze], "SUBSTACK": [2, sw_freeze], "SUBSTACK2": [2, if_uv_else]})
    ctx.blocks[sw_freeze]["parent"] = if_freeze_else
    ctx.blocks[if_uv_else]["parent"] = if_freeze_else

    ctx.chain([bg_hat, if_freeze_else])

    # Stage sound list
    stage_sounds = [
        sound_meta["snd_click"],
        sound_meta["snd_bond"],
        sound_meta["snd_exothermic"],
        sound_meta["snd_photon"],
        sound_meta["snd_cosmic"],
        sound_meta["snd_delete"],
        sound_meta["snd_freeze"],
        sound_meta["snd_discover"],
        sound_meta["snd_ambient"]
    ]

    return {
        "isStage": True,
        "name": "Stage",
        "variables": STAGE_VARS,
        "lists": STAGE_LISTS,
        "broadcasts": BROADCASTS,
        "blocks": ctx.blocks,
        "comments": {},
        "currentCostume": 0,
        "costumes": [
            costume_meta["backdrop_vacuum"],
            costume_meta["backdrop_uv"],
            costume_meta["backdrop_frozen"]
        ],
        "sounds": stage_sounds,
        "volume": 100,
        "layerOrder": 0,
        "tempo": 60,
        "videoTransparency": 50,
        "videoState": "on",
        "textToSpeechLanguage": None
    }

print("Stage builder configured.")
