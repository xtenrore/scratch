import sys, json, uuid
import db_chemistry, gen_audio, gen_graphics
from build_full_project import BlockContext, new_id, STAGE_VARS, STAGE_LISTS, BROADCASTS, build_stage, sound_meta, costume_meta

# Build SimulationEngine sprite
def build_simulation_engine():
    ctx = BlockContext()

    # Initial atom helper
    # Custom block: SpawnInitialAtoms
    def_spawn_init = ctx.add("procedures_definition", topLevel=True, x=400, y=50)
    proto_spawn_init = ctx.add("procedures_prototype", parent_id=def_spawn_init, shadow=True, mutation={
        "tagName": "mutation", "children": [], "proccode": "SpawnInitialAtoms",
        "argumentids": "[]", "argumentnames": "[]", "argumentdefaults": "[]", "warp": "true"
    })
    ctx.blocks[def_spawn_init]["inputs"]["custom_block"] = [1, proto_spawn_init]

    # Body of SpawnInitialAtoms:
    # Clear lists
    del_act = ctx.add("data_deletealloflist", fields={"LIST": ["ENTITY_ACTIVE", "l_ent_act"]})
    del_spc = ctx.add("data_deletealloflist", fields={"LIST": ["ENTITY_SPECIES", "l_ent_spc"]})
    del_x = ctx.add("data_deletealloflist", fields={"LIST": ["ENTITY_X", "l_ent_x"]})
    del_y = ctx.add("data_deletealloflist", fields={"LIST": ["ENTITY_Y", "l_ent_y"]})
    del_vx = ctx.add("data_deletealloflist", fields={"LIST": ["ENTITY_VX", "l_ent_vx"]})
    del_vy = ctx.add("data_deletealloflist", fields={"LIST": ["ENTITY_VY", "l_ent_vy"]})

    set_nid1 = ctx.add("data_setvariableto", fields={"VARIABLE": ["NEXT_ENTITY_ID", "v_next_id"]}, inputs={"VALUE": [1, [4, "1"]]})

    # Add initial atoms: 2 H, 1 O, 1 Na, 1 Cl
    init_atoms = [
        (1, -60, 20, 0.4, -0.2),   # H
        (1, -40, -40, -0.3, 0.3),  # H
        (7, 40, 10, 0.2, 0.3),     # O
        (10, 120, -30, -0.2, -0.2),# Na
        (14, 150, 40, 0.3, 0.1)    # Cl
    ]
    spawn_cmds = []
    for spc, x, y, vx, vy in init_atoms:
        a_act = ctx.add("data_addtolist", fields={"LIST": ["ENTITY_ACTIVE", "l_ent_act"]}, inputs={"ITEM": [1, [4, "1"]]})
        a_spc = ctx.add("data_addtolist", fields={"LIST": ["ENTITY_SPECIES", "l_ent_spc"]}, inputs={"ITEM": [1, [4, str(spc)]]})
        a_x = ctx.add("data_addtolist", fields={"LIST": ["ENTITY_X", "l_ent_x"]}, inputs={"ITEM": [1, [4, str(x)]]})
        a_y = ctx.add("data_addtolist", fields={"LIST": ["ENTITY_Y", "l_ent_y"]}, inputs={"ITEM": [1, [4, str(y)]]})
        a_vx = ctx.add("data_addtolist", fields={"LIST": ["ENTITY_VX", "l_ent_vx"]}, inputs={"ITEM": [1, [4, str(vx)]]})
        a_vy = ctx.add("data_addtolist", fields={"LIST": ["ENTITY_VY", "l_ent_vy"]}, inputs={"ITEM": [1, [4, str(vy)]]})
        cl_menu = ctx.add("control_create_clone_of_menu", fields={"CLONE_OPTION": ["Entity", None]}, shadow=True)
        cr_clone = ctx.add("control_create_clone_of", inputs={"CLONE_OPTION": [1, cl_menu]})
        spawn_cmds.extend([a_act, a_spc, a_x, a_y, a_vx, a_vy, cr_clone])

    ctx.chain([def_spawn_init, del_act, del_spc, del_x, del_y, del_vx, del_vy, set_nid1] + spawn_cmds)


    # When I receive INIT_SIMULATION
    hat_sim = ctx.add("event_whenbroadcastreceived", fields={"BROADCAST_OPTION": ["INIT_SIMULATION", "b_init_sim"]}, topLevel=True, x=50, y=50)
    call_spawn_init = ctx.add("procedures_call", mutation={
        "tagName": "mutation", "children": [], "proccode": "SpawnInitialAtoms",
        "argumentids": "[]", "warp": "true"
    })
    ctx.chain([hat_sim, call_spawn_init])

    # When I receive SPAWN_REQUEST
    hat_spawn = ctx.add("event_whenbroadcastreceived", fields={"BROADCAST_OPTION": ["SPAWN_REQUEST", "b_spawn_req"]}, topLevel=True, x=50, y=200)
    sp_act = ctx.add("data_addtolist", fields={"LIST": ["ENTITY_ACTIVE", "l_ent_act"]}, inputs={"ITEM": [1, [4, "1"]]})
    sp_spc = ctx.add("data_addtolist", fields={"LIST": ["ENTITY_SPECIES", "l_ent_spc"]}, inputs={"ITEM": [3, [12, "SPAWN_SPECIES_ID", "v_spawn_id"], [4, "1"]]})
    sp_x = ctx.add("data_addtolist", fields={"LIST": ["ENTITY_X", "l_ent_x"]}, inputs={"ITEM": [3, [12, "SPAWN_X", "v_spawn_x"], [4, "0"]]})
    sp_y = ctx.add("data_addtolist", fields={"LIST": ["ENTITY_Y", "l_ent_y"]}, inputs={"ITEM": [3, [12, "SPAWN_Y", "v_spawn_y"], [4, "0"]]})
    rnd_vx = ctx.add("operator_random", inputs={"FROM": [1, [4, "-0.8"]], "TO": [1, [4, "0.8"]]})
    sp_vx = ctx.add("data_addtolist", fields={"LIST": ["ENTITY_VX", "l_ent_vx"]}, inputs={"ITEM": [3, rnd_vx, [4, "0"]]})
    rnd_vy = ctx.add("operator_random", inputs={"FROM": [1, [4, "-0.8"]], "TO": [1, [4, "0.8"]]})
    sp_vy = ctx.add("data_addtolist", fields={"LIST": ["ENTITY_VY", "l_ent_vy"]}, inputs={"ITEM": [3, rnd_vy, [4, "0"]]})
    sp_cl_menu = ctx.add("control_create_clone_of_menu", fields={"CLONE_OPTION": ["Entity", None]}, shadow=True)
    sp_cr_clone = ctx.add("control_create_clone_of", inputs={"CLONE_OPTION": [1, sp_cl_menu]})
    ctx.chain([hat_spawn, sp_act, sp_spc, sp_x, sp_y, sp_vx, sp_vy, sp_cr_clone])

    # When I receive CLEAR_ALL
    hat_clear = ctx.add("event_whenbroadcastreceived", fields={"BROADCAST_OPTION": ["CLEAR_ALL", "b_clear_all"]}, topLevel=True, x=50, y=450)
    cl_act = ctx.add("data_deletealloflist", fields={"LIST": ["ENTITY_ACTIVE", "l_ent_act"]})
    cl_spc = ctx.add("data_deletealloflist", fields={"LIST": ["ENTITY_SPECIES", "l_ent_spc"]})
    cl_x = ctx.add("data_deletealloflist", fields={"LIST": ["ENTITY_X", "l_ent_x"]})
    cl_y = ctx.add("data_deletealloflist", fields={"LIST": ["ENTITY_Y", "l_ent_y"]})
    cl_vx = ctx.add("data_deletealloflist", fields={"LIST": ["ENTITY_VX", "l_ent_vx"]})
    cl_vy = ctx.add("data_deletealloflist", fields={"LIST": ["ENTITY_VY", "l_ent_vy"]})
    cl_nid = ctx.add("data_setvariableto", fields={"VARIABLE": ["NEXT_ENTITY_ID", "v_next_id"]}, inputs={"VALUE": [1, [4, "1"]]})
    ctx.chain([hat_clear, cl_act, cl_spc, cl_x, cl_y, cl_vx, cl_vy, cl_nid])

    # When I receive PROMPT_SAVE_LOAD
    hat_save = ctx.add("event_whenbroadcastreceived", fields={"BROADCAST_OPTION": ["PROMPT_SAVE_LOAD", "b_prompt_save"]}, topLevel=True, x=50, y=650)
    ask_choice = ctx.add("sensing_askandwait", inputs={"QUESTION": [1, [10, "Enter 'save' to export progress code, or 'load' to restore:"]]})
    ans = ctx.add("sensing_answer")

    # If save
    is_save = ctx.add("operator_equals", inputs={"OPERAND1": [3, ans, [10, ""]], "OPERAND2": [1, [10, "save"]]})
    # build save string: count of discovered
    join_sc = ctx.add("operator_join", inputs={"STRING1": [1, [10, "CHEM-SAVE-"]], "STRING2": [3, [12, "TOTAL_DISCOVERED", "v_discovered"], [10, ""]]})
    ask_copy = ctx.add("sensing_askandwait", inputs={"QUESTION": [3, join_sc, [10, ""]]})

    # If load
    is_load = ctx.add("operator_equals", inputs={"OPERAND1": [3, ans, [10, ""]], "OPERAND2": [1, [10, "load"]]})
    ask_paste = ctx.add("sensing_askandwait", inputs={"QUESTION": [1, [10, "Paste your Save Code to restore:"]]})
    play_disc = ctx.add("sound_play", inputs={"SOUND_MENU": [1, ctx.add("sound_sounds_menu", fields={"SOUND_MENU": ["snd_discover", None]}, shadow=True)]})
    ctx.blocks[ask_paste]["next"] = play_disc
    ctx.blocks[play_disc]["parent"] = ask_paste

    if_load = ctx.add("control_if", inputs={"CONDITION": [2, is_load], "SUBSTACK": [2, ask_paste]})
    ctx.blocks[ask_paste]["parent"] = if_load

    if_save_else = ctx.add("control_if_else", inputs={"CONDITION": [2, is_save], "SUBSTACK": [2, ask_copy], "SUBSTACK2": [2, if_load]})
    ctx.blocks[ask_copy]["parent"] = if_save_else
    ctx.blocks[if_load]["parent"] = if_save_else

    ctx.chain([hat_save, ask_choice, if_save_else])

    return {
        "isStage": False,
        "name": "SimulationEngine",
        "variables": {},
        "lists": {},
        "broadcasts": {},
        "blocks": ctx.blocks,
        "comments": {},
        "currentCostume": 0,
        "costumes": [costume_meta["toast_banner"]],
        "sounds": [sound_meta["snd_discover"]],
        "volume": 100,
        "visible": False,
        "x": 0, "y": 0, "size": 100, "direction": 90,
        "draggable": False, "rotationStyle": "don't rotate"
    }

print("SimulationEngine builder configured.")

# Build Entity sprite
def build_entity():
    ctx = BlockContext()

    entity_vars = {
        "v_local_id": ["my_id", 0],
        "v_local_spc": ["my_species", 1],
        "v_local_vx": ["my_vx", 0],
        "v_local_vy": ["my_vy", 0],
        "v_local_drag": ["is_dragging", 0],
        "v_local_k": ["loop_k", 1],
        "v_local_dx": ["loop_dx", 0],
        "v_local_dy": ["loop_dy", 0],
        "v_local_dsq": ["loop_dsq", 0],
        "v_local_rx_key": ["temp_rx_key", ""],
        "v_local_rx_idx": ["temp_rx_idx", 0],
        "v_local_prod": ["temp_prod", 0]
    }

    # Costumes: all 129 species
    entity_costumes = [costume_meta[f"species_{s['id']}"] for s in db_chemistry.SPECIES]

    # Sounds
    entity_sounds = [
        sound_meta["snd_bond"],
        sound_meta["snd_exothermic"],
        sound_meta["snd_delete"],
        sound_meta["snd_discover"]
    ]

    # Green flag: hide original sprite
    flag_id = ctx.add("event_whenflagclicked", topLevel=True, x=50, y=50)
    hide_orig = ctx.add("looks_hide")
    set_orig_id = ctx.add("data_setvariableto", fields={"VARIABLE": ["my_id", "v_local_id"]}, inputs={"VALUE": [1, [4, "0"]]})
    ctx.chain([flag_id, hide_orig, set_orig_id])

    # When I receive CLEAR_ALL
    hat_clear = ctx.add("event_whenbroadcastreceived", fields={"BROADCAST_OPTION": ["CLEAR_ALL", "b_clear_all"]}, topLevel=True, x=50, y=170)
    gt_zero = ctx.add("operator_gt", inputs={"OPERAND1": [3, [12, "my_id", "v_local_id"], [10, ""]], "OPERAND2": [1, [10, "0"]]})
    del_clone_cl = ctx.add("control_delete_this_clone")
    if_gt_zero = ctx.add("control_if", inputs={"CONDITION": [2, gt_zero], "SUBSTACK": [2, del_clone_cl]})
    ctx.blocks[del_clone_cl]["parent"] = if_gt_zero
    ctx.chain([hat_clear, if_gt_zero])

    # Procedure: ResolveInteractions (warp: true)
    def_resolve = ctx.add("procedures_definition", topLevel=True, x=450, y=50)
    proto_resolve = ctx.add("procedures_prototype", parent_id=def_resolve, shadow=True, mutation={
        "tagName": "mutation", "children": [], "proccode": "ResolveInteractions",
        "argumentids": "[]", "argumentnames": "[]", "argumentdefaults": "[]", "warp": "true"
    })
    ctx.blocks[def_resolve]["inputs"]["custom_block"] = [1, proto_resolve]

    # Procedure body:
    # loop_k = 1
    set_k1 = ctx.add("data_setvariableto", fields={"VARIABLE": ["loop_k", "v_local_k"]}, inputs={"VALUE": [1, [4, "1"]]})
    
    # Inside repeat loop:
    # if loop_k != my_id and item loop_k of ENTITY_ACTIVE == 1:
    not_self = ctx.add("operator_not", inputs={"OPERAND": [2, ctx.add("operator_equals", inputs={"OPERAND1": [3, [12, "loop_k", "v_local_k"], [10, ""]], "OPERAND2": [3, [12, "my_id", "v_local_id"], [10, ""]]})]})
    target_act = ctx.add("data_itemoflist", fields={"LIST": ["ENTITY_ACTIVE", "l_ent_act"]}, inputs={"INDEX": [3, [12, "loop_k", "v_local_k"], [7, "1"]]})
    is_act = ctx.add("operator_equals", inputs={"OPERAND1": [3, target_act, [10, ""]], "OPERAND2": [1, [10, "1"]]})
    both_cond = ctx.add("operator_and", inputs={"OPERAND1": [2, not_self], "OPERAND2": [2, is_act]})

    # Calculate distance: dx = (item loop_k of ENTITY_X) - x position
    tgt_x = ctx.add("data_itemoflist", fields={"LIST": ["ENTITY_X", "l_ent_x"]}, inputs={"INDEX": [3, [12, "loop_k", "v_local_k"], [7, "1"]]})
    my_x = ctx.add("motion_xposition")
    dx_val = ctx.add("operator_subtract", inputs={"NUM1": [3, tgt_x, [4, "0"]], "NUM2": [3, my_x, [4, "0"]]})
    set_dx = ctx.add("data_setvariableto", fields={"VARIABLE": ["loop_dx", "v_local_dx"]}, inputs={"VALUE": [3, dx_val, [4, "0"]]})

    tgt_y = ctx.add("data_itemoflist", fields={"LIST": ["ENTITY_Y", "l_ent_y"]}, inputs={"INDEX": [3, [12, "loop_k", "v_local_k"], [7, "1"]]})
    my_y = ctx.add("motion_yposition")
    dy_val = ctx.add("operator_subtract", inputs={"NUM1": [3, tgt_y, [4, "0"]], "NUM2": [3, my_y, [4, "0"]]})
    set_dy = ctx.add("data_setvariableto", fields={"VARIABLE": ["loop_dy", "v_local_dy"]}, inputs={"VALUE": [3, dy_val, [4, "0"]]})

    dx_sq = ctx.add("operator_multiply", inputs={"NUM1": [3, [12, "loop_dx", "v_local_dx"], [4, "0"]], "NUM2": [3, [12, "loop_dx", "v_local_dx"], [4, "0"]]})
    dy_sq = ctx.add("operator_multiply", inputs={"NUM1": [3, [12, "loop_dy", "v_local_dy"], [4, "0"]], "NUM2": [3, [12, "loop_dy", "v_local_dy"], [4, "0"]]})
    dsq_val = ctx.add("operator_add", inputs={"NUM1": [3, dx_sq, [4, "0"]], "NUM2": [3, dy_sq, [4, "0"]]})
    set_dsq = ctx.add("data_setvariableto", fields={"VARIABLE": ["loop_dsq", "v_local_dsq"]}, inputs={"VALUE": [3, dsq_val, [4, "0"]]})

    # if loop_dsq < 1764 (radius ~42px)
    close_enough = ctx.add("operator_lt", inputs={"OPERAND1": [3, [12, "loop_dsq", "v_local_dsq"], [10, ""]], "OPERAND2": [1, [10, "1764"]]})

    # Form key: if my_species < partner_species key = my_species + "_" + partner else partner + "_" + my
    partner_spc = ctx.add("data_itemoflist", fields={"LIST": ["ENTITY_SPECIES", "l_ent_spc"]}, inputs={"INDEX": [3, [12, "loop_k", "v_local_k"], [7, "1"]]})
    spc_lt = ctx.add("operator_lt", inputs={"OPERAND1": [3, [12, "my_species", "v_local_spc"], [10, ""]], "OPERAND2": [3, partner_spc, [10, ""]]})

    key_part1 = ctx.add("operator_join", inputs={"STRING1": [3, [12, "my_species", "v_local_spc"], [10, ""]], "STRING2": [1, [10, "_"]]})
    key_a = ctx.add("operator_join", inputs={"STRING1": [3, key_part1, [10, ""]], "STRING2": [3, partner_spc, [10, ""]]})
    set_key_a = ctx.add("data_setvariableto", fields={"VARIABLE": ["temp_rx_key", "v_local_rx_key"]}, inputs={"VALUE": [3, key_a, [10, ""]]})

    key_part2 = ctx.add("operator_join", inputs={"STRING1": [3, partner_spc, [10, ""]], "STRING2": [1, [10, "_"]]})
    key_b = ctx.add("operator_join", inputs={"STRING1": [3, key_part2, [10, ""]], "STRING2": [3, [12, "my_species", "v_local_spc"], [10, ""]]})
    set_key_b = ctx.add("data_setvariableto", fields={"VARIABLE": ["temp_rx_key", "v_local_rx_key"]}, inputs={"VALUE": [3, key_b, [10, ""]]})

    if_spc_order = ctx.add("control_if_else", inputs={"CONDITION": [2, spc_lt], "SUBSTACK": [2, set_key_a], "SUBSTACK2": [2, set_key_b]})
    ctx.blocks[set_key_a]["parent"] = if_spc_order
    ctx.blocks[set_key_b]["parent"] = if_spc_order

    # Check rx in RX_KEY list:
    item_num_rx = ctx.add("data_itemnumoflist", fields={"LIST": ["RX_KEY", "l_rx_key"]}, inputs={"ITEM": [3, [12, "temp_rx_key", "v_local_rx_key"], [10, ""]]})
    set_rx_idx = ctx.add("data_setvariableto", fields={"VARIABLE": ["temp_rx_idx", "v_local_rx_idx"]}, inputs={"VALUE": [3, item_num_rx, [4, "0"]]})

    # if temp_rx_idx > 0:
    has_rx = ctx.add("operator_gt", inputs={"OPERAND1": [3, [12, "temp_rx_idx", "v_local_rx_idx"], [10, ""]], "OPERAND2": [1, [10, "0"]]})

    # Check UV: if RX_UV == 1 and UV_ACTIVE == 0: skip / notify
    rx_uv_val = ctx.add("data_itemoflist", fields={"LIST": ["RX_UV", "l_rx_uv"]}, inputs={"INDEX": [3, [12, "temp_rx_idx", "v_local_rx_idx"], [7, "1"]]})
    needs_uv = ctx.add("operator_equals", inputs={"OPERAND1": [3, rx_uv_val, [10, ""]], "OPERAND2": [1, [10, "1"]]})
    uv_off = ctx.add("operator_equals", inputs={"OPERAND1": [3, [12, "UV_ACTIVE", "v_uv"], [10, ""]], "OPERAND2": [1, [10, "0"]]})
    uv_blocked = ctx.add("operator_and", inputs={"OPERAND1": [2, needs_uv], "OPERAND2": [2, uv_off]})
    say_uv = ctx.add("looks_sayforsecs", inputs={"MESSAGE": [1, [10, "⚡ Requires UV Light!"]], "SECS": [1, [4, "1.2"]]})

    # Reaction execution:
    # Deactivate partner
    deact_partner = ctx.add("data_replaceitemoflist", fields={"LIST": ["ENTITY_ACTIVE", "l_ent_act"]}, inputs={"INDEX": [3, [12, "loop_k", "v_local_k"], [7, "1"]], "ITEM": [1, [4, "0"]]})
    
    # Get product ID
    get_prod = ctx.add("data_itemoflist", fields={"LIST": ["RX_PROD", "l_rx_prod"]}, inputs={"INDEX": [3, [12, "temp_rx_idx", "v_local_rx_idx"], [7, "1"]]})
    set_prod = ctx.add("data_setvariableto", fields={"VARIABLE": ["temp_prod", "v_local_prod"]}, inputs={"VALUE": [3, get_prod, [4, "1"]]})

    # Mutate self
    set_my_spc = ctx.add("data_setvariableto", fields={"VARIABLE": ["my_species", "v_local_spc"]}, inputs={"VALUE": [3, [12, "temp_prod", "v_local_prod"], [4, "1"]]})
    upd_list_spc = ctx.add("data_replaceitemoflist", fields={"LIST": ["ENTITY_SPECIES", "l_ent_spc"]}, inputs={"INDEX": [3, [12, "my_id", "v_local_id"], [7, "1"]], "ITEM": [3, [12, "temp_prod", "v_local_prod"], [4, "1"]]})
    sw_costume = ctx.add("looks_switchcostumeto", inputs={"COSTUME": [3, ctx.add("operator_join", inputs={"STRING1": [1, [10, "species_"]], "STRING2": [3, [12, "temp_prod", "v_local_prod"], [10, ""]]}), [10, "species_1"]]})

    # Set FX coordinates
    set_fx_x = ctx.add("data_setvariableto", fields={"VARIABLE": ["FX_X", "v_fx_x"]}, inputs={"VALUE": [3, ctx.add("motion_xposition"), [4, "0"]]})
    set_fx_y = ctx.add("data_setvariableto", fields={"VARIABLE": ["FX_Y", "v_fx_y"]}, inputs={"VALUE": [3, ctx.add("motion_yposition"), [4, "0"]]})

    # Exothermic check
    rx_exo_val = ctx.add("data_itemoflist", fields={"LIST": ["RX_EXO", "l_rx_exo"]}, inputs={"INDEX": [3, [12, "temp_rx_idx", "v_local_rx_idx"], [7, "1"]]})
    is_exo = ctx.add("operator_equals", inputs={"OPERAND1": [3, rx_exo_val, [10, ""]], "OPERAND2": [1, [10, "1"]]})
    bc_fx_exo = ctx.add("event_broadcast", inputs={"BROADCAST_INPUT": [1, [11, "PLAY_FX_EXO", "b_fx_exo"]]})
    bc_sp_phot = ctx.add("event_broadcast", inputs={"BROADCAST_INPUT": [1, [11, "SPAWN_PHOTON", "b_spawn_photon"]]})
    snd_exo_m = ctx.add("sound_sounds_menu", fields={"SOUND_MENU": ["snd_exothermic", None]}, shadow=True)
    play_exo = ctx.add("sound_play", inputs={"SOUND_MENU": [1, snd_exo_m]})
    ctx.chain([bc_fx_exo, bc_sp_phot, play_exo])

    bc_fx_bond = ctx.add("event_broadcast", inputs={"BROADCAST_INPUT": [1, [11, "PLAY_FX_BOND", "b_fx_bond"]]})
    snd_bnd_m = ctx.add("sound_sounds_menu", fields={"SOUND_MENU": ["snd_bond", None]}, shadow=True)
    play_bnd = ctx.add("sound_play", inputs={"SOUND_MENU": [1, snd_bnd_m]})
    ctx.chain([bc_fx_bond, play_bnd])

    if_exo_else = ctx.add("control_if_else", inputs={"CONDITION": [2, is_exo], "SUBSTACK": [2, bc_fx_exo], "SUBSTACK2": [2, bc_fx_bond]})
    ctx.blocks[bc_fx_exo]["parent"] = if_exo_else
    ctx.blocks[bc_fx_bond]["parent"] = if_exo_else

    # Check discovery
    disc_val = ctx.add("data_itemoflist", fields={"LIST": ["DB_DISCOVERED", "l_db_disc"]}, inputs={"INDEX": [3, [12, "temp_prod", "v_local_prod"], [7, "1"]]})
    is_new = ctx.add("operator_equals", inputs={"OPERAND1": [3, disc_val, [10, ""]], "OPERAND2": [1, [10, "0"]]})
    set_disc = ctx.add("data_replaceitemoflist", fields={"LIST": ["DB_DISCOVERED", "l_db_disc"]}, inputs={"INDEX": [3, [12, "temp_prod", "v_local_prod"], [7, "1"]], "ITEM": [1, [4, "1"]]})
    inc_disc = ctx.add("data_changevariableby", fields={"VARIABLE": ["TOTAL_DISCOVERED", "v_discovered"]}, inputs={"VALUE": [1, [4, "1"]]})
    set_toast = ctx.add("data_setvariableto", fields={"VARIABLE": ["TOAST_SPECIES_ID", "v_toast_id"]}, inputs={"VALUE": [3, [12, "temp_prod", "v_local_prod"], [4, "1"]]})
    bc_toast = ctx.add("event_broadcast", inputs={"BROADCAST_INPUT": [1, [11, "SHOW_TOAST", "b_show_toast"]]})
    snd_disc_m = ctx.add("sound_sounds_menu", fields={"SOUND_MENU": ["snd_discover", None]}, shadow=True)
    play_disc = ctx.add("sound_play", inputs={"SOUND_MENU": [1, snd_disc_m]})
    ctx.chain([set_disc, inc_disc, set_toast, bc_toast, play_disc])

    if_new_disc = ctx.add("control_if", inputs={"CONDITION": [2, is_new], "SUBSTACK": [2, set_disc]})
    ctx.blocks[set_disc]["parent"] = if_new_disc

    stop_rx = ctx.add("control_stop", fields={"STOP_OPTION": ["this script", None]})
    ctx.chain([deact_partner, get_prod, set_prod, set_my_spc, upd_list_spc, sw_costume, set_fx_x, set_fx_y, if_exo_else, if_new_disc, stop_rx])

    if_uv_else_rx = ctx.add("control_if_else", inputs={"CONDITION": [2, uv_blocked], "SUBSTACK": [2, say_uv], "SUBSTACK2": [2, deact_partner]})
    ctx.blocks[say_uv]["parent"] = if_uv_else_rx
    ctx.blocks[deact_partner]["parent"] = if_uv_else_rx

    if_rx_exists = ctx.add("control_if", inputs={"CONDITION": [2, has_rx], "SUBSTACK": [2, if_uv_else_rx]})
    ctx.blocks[if_uv_else_rx]["parent"] = if_rx_exists

    ctx.chain([if_spc_order, set_rx_idx, if_rx_exists])

    if_close = ctx.add("control_if", inputs={"CONDITION": [2, close_enough], "SUBSTACK": [2, if_spc_order]})
    ctx.blocks[if_spc_order]["parent"] = if_close

    ctx.chain([set_dx, set_dy, set_dsq, if_close])

    if_partner_active = ctx.add("control_if", inputs={"CONDITION": [2, both_cond], "SUBSTACK": [2, set_dx]})
    ctx.blocks[set_dx]["parent"] = if_partner_active

    # Increment loop_k
    inc_k = ctx.add("data_changevariableby", fields={"VARIABLE": ["loop_k", "v_local_k"]}, inputs={"VALUE": [1, [4, "1"]]})
    ctx.chain([if_partner_active, inc_k])

    # Repeat length of ENTITY_ACTIVE
    rep_len = ctx.add("data_lengthoflist", fields={"LIST": ["ENTITY_ACTIVE", "l_ent_act"]})
    rep_loop = ctx.add("control_repeat", inputs={"TIMES": [3, rep_len, [6, "10"]], "SUBSTACK": [2, if_partner_active]})
    ctx.blocks[if_partner_active]["parent"] = rep_loop

    ctx.chain([def_resolve, set_k1, rep_loop])

    # Clone life loop: when I start as a clone
    hat_start = ctx.add("control_start_as_clone", topLevel=True, x=50, y=320)
    init_my_id = ctx.add("data_setvariableto", fields={"VARIABLE": ["my_id", "v_local_id"]}, inputs={"VALUE": [3, [12, "NEXT_ENTITY_ID", "v_next_id"], [4, "1"]]})
    inc_next_id = ctx.add("data_changevariableby", fields={"VARIABLE": ["NEXT_ENTITY_ID", "v_next_id"]}, inputs={"VALUE": [1, [4, "1"]]})
    init_my_spc = ctx.add("data_setvariableto", fields={"VARIABLE": ["my_species", "v_local_spc"]}, inputs={"VALUE": [3, ctx.add("data_itemoflist", fields={"LIST": ["ENTITY_SPECIES", "l_ent_spc"]}, inputs={"INDEX": [3, [12, "my_id", "v_local_id"], [7, "1"]]}), [4, "1"]]})
    init_sw = ctx.add("looks_switchcostumeto", inputs={"COSTUME": [3, ctx.add("operator_join", inputs={"STRING1": [1, [10, "species_"]], "STRING2": [3, [12, "my_species", "v_local_spc"], [10, ""]]}), [10, "species_1"]]})
    init_goto = ctx.add("motion_gotoxy", inputs={
        "X": [3, ctx.add("data_itemoflist", fields={"LIST": ["ENTITY_X", "l_ent_x"]}, inputs={"INDEX": [3, [12, "my_id", "v_local_id"], [7, "1"]]}), [4, "0"]],
        "Y": [3, ctx.add("data_itemoflist", fields={"LIST": ["ENTITY_Y", "l_ent_y"]}, inputs={"INDEX": [3, [12, "my_id", "v_local_id"], [7, "1"]]}), [4, "0"]]
    })
    init_vx = ctx.add("data_setvariableto", fields={"VARIABLE": ["my_vx", "v_local_vx"]}, inputs={"VALUE": [3, ctx.add("data_itemoflist", fields={"LIST": ["ENTITY_VX", "l_ent_vx"]}, inputs={"INDEX": [3, [12, "my_id", "v_local_id"], [7, "1"]]}), [4, "0"]]})
    init_vy = ctx.add("data_setvariableto", fields={"VARIABLE": ["my_vy", "v_local_vy"]}, inputs={"VALUE": [3, ctx.add("data_itemoflist", fields={"LIST": ["ENTITY_VY", "l_ent_vy"]}, inputs={"INDEX": [3, [12, "my_id", "v_local_id"], [7, "1"]]}), [4, "0"]]})
    init_drag = ctx.add("data_setvariableto", fields={"VARIABLE": ["is_dragging", "v_local_drag"]}, inputs={"VALUE": [1, [4, "0"]]})
    init_show = ctx.add("looks_show")

    # Forever loop inside clone:
    # 1. Check if killed: item my_id of ENTITY_ACTIVE == 0
    my_act_val = ctx.add("data_itemoflist", fields={"LIST": ["ENTITY_ACTIVE", "l_ent_act"]}, inputs={"INDEX": [3, [12, "my_id", "v_local_id"], [7, "1"]]})
    is_dead = ctx.add("operator_equals", inputs={"OPERAND1": [3, my_act_val, [10, ""]], "OPERAND2": [1, [10, "0"]]})
    del_me = ctx.add("control_delete_this_clone")
    if_dead = ctx.add("control_if", inputs={"CONDITION": [2, is_dead], "SUBSTACK": [2, del_me]})
    ctx.blocks[del_me]["parent"] = if_dead

    # 2. Check if dragging
    is_drag_active = ctx.add("operator_equals", inputs={"OPERAND1": [3, [12, "is_dragging", "v_local_drag"], [10, ""]], "OPERAND2": [1, [10, "1"]]})
    goto_mouse = ctx.add("motion_gotoxy", inputs={"X": [3, ctx.add("sensing_mousex"), [4, "0"]], "Y": [3, ctx.add("sensing_mousey"), [4, "0"]]})
    upd_drag_x = ctx.add("data_replaceitemoflist", fields={"LIST": ["ENTITY_X", "l_ent_x"]}, inputs={"INDEX": [3, [12, "my_id", "v_local_id"], [7, "1"]], "ITEM": [3, ctx.add("motion_xposition"), [4, "0"]]})
    upd_drag_y = ctx.add("data_replaceitemoflist", fields={"LIST": ["ENTITY_Y", "l_ent_y"]}, inputs={"INDEX": [3, [12, "my_id", "v_local_id"], [7, "1"]], "ITEM": [3, ctx.add("motion_yposition"), [4, "0"]]})

    # Check mouse up
    m_down = ctx.add("sensing_mousedown")
    not_m_down = ctx.add("operator_not", inputs={"OPERAND": [2, m_down]})
    reset_drag = ctx.add("data_setvariableto", fields={"VARIABLE": ["is_dragging", "v_local_drag"]}, inputs={"VALUE": [1, [4, "0"]]})
    reset_size = ctx.add("looks_setsizeto", inputs={"SIZE": [1, [4, "100"]]})
    call_resolve = ctx.add("procedures_call", mutation={
        "tagName": "mutation", "children": [], "proccode": "ResolveInteractions",
        "argumentids": "[]", "warp": "true"
    })
    ctx.chain([reset_drag, reset_size, call_resolve])
    if_m_up = ctx.add("control_if", inputs={"CONDITION": [2, not_m_down], "SUBSTACK": [2, reset_drag]})
    ctx.blocks[reset_drag]["parent"] = if_m_up

    ctx.chain([goto_mouse, upd_drag_x, upd_drag_y, if_m_up])

    # In idle branch: if TIME_FROZEN == 0:
    move_x = ctx.add("motion_changexby", inputs={"DX": [3, [12, "my_vx", "v_local_vx"], [4, "0"]]})
    move_y = ctx.add("motion_changeyby", inputs={"DY": [3, [12, "my_vy", "v_local_vy"], [4, "0"]]})

    # Bounce bounds: X in [-220, 220], Y in [-115, 125]
    # x < -220
    lt_min_x = ctx.add("operator_lt", inputs={"OPERAND1": [3, ctx.add("motion_xposition"), [10, ""]], "OPERAND2": [1, [10, "-220"]]})
    set_vx_pos = ctx.add("data_setvariableto", fields={"VARIABLE": ["my_vx", "v_local_vx"]}, inputs={"VALUE": [3, ctx.add("operator_subtract", inputs={"NUM1": [1, [4, "0"]], "NUM2": [3, [12, "my_vx", "v_local_vx"], [4, "0"]]}), [4, "0"]]})
    set_min_x = ctx.add("motion_setx", inputs={"X": [1, [4, "-220"]]})
    ctx.chain([set_vx_pos, set_min_x])
    if_min_x = ctx.add("control_if", inputs={"CONDITION": [2, lt_min_x], "SUBSTACK": [2, set_vx_pos]})
    ctx.blocks[set_vx_pos]["parent"] = if_min_x

    # x > 220
    gt_max_x = ctx.add("operator_gt", inputs={"OPERAND1": [3, ctx.add("motion_xposition"), [10, ""]], "OPERAND2": [1, [10, "220"]]})
    set_vx_neg = ctx.add("data_setvariableto", fields={"VARIABLE": ["my_vx", "v_local_vx"]}, inputs={"VALUE": [3, ctx.add("operator_subtract", inputs={"NUM1": [1, [4, "0"]], "NUM2": [3, [12, "my_vx", "v_local_vx"], [4, "0"]]}), [4, "0"]]})
    set_max_x = ctx.add("motion_setx", inputs={"X": [1, [4, "220"]]})
    ctx.chain([set_vx_neg, set_max_x])
    if_max_x = ctx.add("control_if", inputs={"CONDITION": [2, gt_max_x], "SUBSTACK": [2, set_vx_neg]})
    ctx.blocks[set_vx_neg]["parent"] = if_max_x

    # y < -115
    lt_min_y = ctx.add("operator_lt", inputs={"OPERAND1": [3, ctx.add("motion_yposition"), [10, ""]], "OPERAND2": [1, [10, "-115"]]})
    set_vy_pos = ctx.add("data_setvariableto", fields={"VARIABLE": ["my_vy", "v_local_vy"]}, inputs={"VALUE": [3, ctx.add("operator_subtract", inputs={"NUM1": [1, [4, "0"]], "NUM2": [3, [12, "my_vy", "v_local_vy"], [4, "0"]]}), [4, "0"]]})
    set_min_y = ctx.add("motion_sety", inputs={"Y": [1, [4, "-115"]]})
    ctx.chain([set_vy_pos, set_min_y])
    if_min_y = ctx.add("control_if", inputs={"CONDITION": [2, lt_min_y], "SUBSTACK": [2, set_vy_pos]})
    ctx.blocks[set_vy_pos]["parent"] = if_min_y

    # y > 125
    gt_max_y = ctx.add("operator_gt", inputs={"OPERAND1": [3, ctx.add("motion_yposition"), [10, ""]], "OPERAND2": [1, [10, "125"]]})
    set_vy_neg = ctx.add("data_setvariableto", fields={"VARIABLE": ["my_vy", "v_local_vy"]}, inputs={"VALUE": [3, ctx.add("operator_subtract", inputs={"NUM1": [1, [4, "0"]], "NUM2": [3, [12, "my_vy", "v_local_vy"], [4, "0"]]}), [4, "0"]]})
    set_max_y = ctx.add("motion_sety", inputs={"Y": [1, [4, "125"]]})
    ctx.chain([set_vy_neg, set_max_y])
    if_max_y = ctx.add("control_if", inputs={"CONDITION": [2, gt_max_y], "SUBSTACK": [2, set_vy_neg]})
    ctx.blocks[set_vy_neg]["parent"] = if_max_y

    # Update position in list
    upd_pos_x = ctx.add("data_replaceitemoflist", fields={"LIST": ["ENTITY_X", "l_ent_x"]}, inputs={"INDEX": [3, [12, "my_id", "v_local_id"], [7, "1"]], "ITEM": [3, ctx.add("motion_xposition"), [4, "0"]]})
    upd_pos_y = ctx.add("data_replaceitemoflist", fields={"LIST": ["ENTITY_Y", "l_ent_y"]}, inputs={"INDEX": [3, [12, "my_id", "v_local_id"], [7, "1"]], "ITEM": [3, ctx.add("motion_yposition"), [4, "0"]]})

    # Check external species change (e.g. from cosmic ray)
    curr_spc_in_list = ctx.add("data_itemoflist", fields={"LIST": ["ENTITY_SPECIES", "l_ent_spc"]}, inputs={"INDEX": [3, [12, "my_id", "v_local_id"], [7, "1"]]})
    spc_changed = ctx.add("operator_not", inputs={"OPERAND": [2, ctx.add("operator_equals", inputs={"OPERAND1": [3, curr_spc_in_list, [10, ""]], "OPERAND2": [3, [12, "my_species", "v_local_spc"], [10, ""]]})]})
    set_new_spc = ctx.add("data_setvariableto", fields={"VARIABLE": ["my_species", "v_local_spc"]}, inputs={"VALUE": [3, curr_spc_in_list, [4, "1"]]})
    sw_new_costume = ctx.add("looks_switchcostumeto", inputs={"COSTUME": [3, ctx.add("operator_join", inputs={"STRING1": [1, [10, "species_"]], "STRING2": [3, [12, "my_species", "v_local_spc"], [10, ""]]}), [10, "species_1"]]})
    ctx.chain([set_new_spc, sw_new_costume])
    if_spc_mutated = ctx.add("control_if", inputs={"CONDITION": [2, spc_changed], "SUBSTACK": [2, set_new_spc]})
    ctx.blocks[set_new_spc]["parent"] = if_spc_mutated

    ctx.chain([move_x, move_y, if_min_x, if_max_x, if_min_y, if_max_y, upd_pos_x, upd_pos_y, if_spc_mutated])

    is_not_frozen = ctx.add("operator_equals", inputs={"OPERAND1": [3, [12, "TIME_FROZEN", "v_freeze"], [10, ""]], "OPERAND2": [1, [10, "0"]]})
    if_not_frozen = ctx.add("control_if", inputs={"CONDITION": [2, is_not_frozen], "SUBSTACK": [2, move_x]})
    ctx.blocks[move_x]["parent"] = if_not_frozen

    if_drag_else = ctx.add("control_if_else", inputs={"CONDITION": [2, is_drag_active], "SUBSTACK": [2, goto_mouse], "SUBSTACK2": [2, if_not_frozen]})
    ctx.blocks[goto_mouse]["parent"] = if_drag_else
    ctx.blocks[if_not_frozen]["parent"] = if_drag_else

    ctx.chain([if_dead, if_drag_else])

    loop_forever = ctx.add("control_forever", inputs={"SUBSTACK": [2, if_dead]})
    ctx.blocks[if_dead]["parent"] = loop_forever

    ctx.chain([hat_start, init_my_id, inc_next_id, init_my_spc, init_sw, init_goto, init_vx, init_vy, init_drag, init_show, loop_forever])

    # When this sprite clicked
    hat_click = ctx.add("event_whenthisspriteclicked", topLevel=True, x=50, y=700)
    is_del_tool = ctx.add("operator_equals", inputs={"OPERAND1": [3, [12, "CURRENT_TOOL", "v_tool"], [10, ""]], "OPERAND2": [1, [10, "delete"]]})
    del_act_val = ctx.add("data_replaceitemoflist", fields={"LIST": ["ENTITY_ACTIVE", "l_ent_act"]}, inputs={"INDEX": [3, [12, "my_id", "v_local_id"], [7, "1"]], "ITEM": [1, [4, "0"]]})
    del_fx_x = ctx.add("data_setvariableto", fields={"VARIABLE": ["FX_X", "v_fx_x"]}, inputs={"VALUE": [3, ctx.add("motion_xposition"), [4, "0"]]})
    del_fx_y = ctx.add("data_setvariableto", fields={"VARIABLE": ["FX_Y", "v_fx_y"]}, inputs={"VALUE": [3, ctx.add("motion_yposition"), [4, "0"]]})
    del_bc_fx = ctx.add("event_broadcast", inputs={"BROADCAST_INPUT": [1, [11, "PLAY_FX_DELETE", "b_fx_del"]]})
    snd_del_m = ctx.add("sound_sounds_menu", fields={"SOUND_MENU": ["snd_delete", None]}, shadow=True)
    del_play_snd = ctx.add("sound_play", inputs={"SOUND_MENU": [1, snd_del_m]})
    del_clone_now = ctx.add("control_delete_this_clone")
    ctx.chain([del_act_val, del_fx_x, del_fx_y, del_bc_fx, del_play_snd, del_clone_now])

    # Info tool check
    is_info_tool = ctx.add("operator_equals", inputs={"OPERAND1": [3, [12, "CURRENT_TOOL", "v_tool"], [10, ""]], "OPERAND2": [1, [10, "info"]]})
    set_insp = ctx.add("data_setvariableto", fields={"VARIABLE": ["INSPECT_SPECIES_ID", "v_inspect_id"]}, inputs={"VALUE": [3, [12, "my_species", "v_local_spc"], [4, "1"]]})
    bc_info = ctx.add("event_broadcast", inputs={"BROADCAST_INPUT": [1, [11, "SHOW_INFO", "b_show_info"]]})
    ctx.chain([set_insp, bc_info])

    # Drag mode:
    start_drag = ctx.add("data_setvariableto", fields={"VARIABLE": ["is_dragging", "v_local_drag"]}, inputs={"VALUE": [1, [4, "1"]]})
    drag_size = ctx.add("looks_setsizeto", inputs={"SIZE": [1, [4, "115"]]})
    drag_front = ctx.add("looks_gotofrontback", fields={"FRONT_BACK": ["front", None]})
    ctx.chain([start_drag, drag_size, drag_front])

    if_info_else = ctx.add("control_if_else", inputs={"CONDITION": [2, is_info_tool], "SUBSTACK": [2, set_insp], "SUBSTACK2": [2, start_drag]})
    ctx.blocks[set_insp]["parent"] = if_info_else
    ctx.blocks[start_drag]["parent"] = if_info_else

    if_del_else = ctx.add("control_if_else", inputs={"CONDITION": [2, is_del_tool], "SUBSTACK": [2, del_act_val], "SUBSTACK2": [2, if_info_else]})
    ctx.blocks[del_act_val]["parent"] = if_del_else
    ctx.blocks[if_info_else]["parent"] = if_del_else

    ctx.chain([hat_click, if_del_else])

    return {
        "isStage": False,
        "name": "Entity",
        "variables": entity_vars,
        "lists": {},
        "broadcasts": {},
        "blocks": ctx.blocks,
        "comments": {},
        "currentCostume": 0,
        "costumes": entity_costumes,
        "sounds": entity_sounds,
        "volume": 100,
        "visible": True,
        "x": 0, "y": 0, "size": 100, "direction": 90,
        "draggable": False, "rotationStyle": "don't rotate"
    }

print("Entity builder configured.")

# Build CosmicRay sprite
def build_cosmic_ray():
    ctx = BlockContext()
    ray_vars = {
        "v_ray_k": ["ray_k", 1],
        "v_ray_dx": ["ray_dx", 0],
        "v_ray_dy": ["ray_dy", 0],
        "v_ray_dsq": ["ray_dsq", 0],
        "v_ray_spc": ["ray_spc", 1],
        "v_ray_idx": ["ray_ion_idx", 0],
        "v_ray_dst": ["ray_new_ion", 0]
    }

    flag_id = ctx.add("event_whenflagclicked", topLevel=True, x=50, y=50)
    hide_orig = ctx.add("looks_hide")

    # Spawner loop
    wait_time = ctx.add("operator_random", inputs={"FROM": [1, [4, "7"]], "TO": [1, [4, "12"]]})
    wait_b = ctx.add("control_wait", inputs={"DURATION": [3, wait_time, [4, "8"]]})
    is_not_frozen = ctx.add("operator_equals", inputs={"OPERAND1": [3, [12, "TIME_FROZEN", "v_freeze"], [10, ""]], "OPERAND2": [1, [10, "0"]]})
    create_cl = ctx.add("control_create_clone_of", inputs={"CLONE_OPTION": [1, ctx.add("control_create_clone_of_menu", fields={"CLONE_OPTION": ["_myself_", None]}, shadow=True)]})
    if_spawn = ctx.add("control_if", inputs={"CONDITION": [2, is_not_frozen], "SUBSTACK": [2, create_cl]})
    ctx.blocks[create_cl]["parent"] = if_spawn
    ctx.chain([wait_b, if_spawn])
    forever_loop = ctx.add("control_forever", inputs={"SUBSTACK": [2, wait_b]})
    ctx.blocks[wait_b]["parent"] = forever_loop
    ctx.chain([flag_id, hide_orig, forever_loop])

    # Clone behavior
    hat_start = ctx.add("control_start_as_clone", topLevel=True, x=50, y=280)
    rnd_y = ctx.add("operator_random", inputs={"FROM": [1, [4, "-90"]], "TO": [1, [4, "100"]]})
    goto_edge = ctx.add("motion_gotoxy", inputs={"X": [1, [4, "-240"]], "Y": [3, rnd_y, [4, "0"]]})
    rnd_dir = ctx.add("operator_random", inputs={"FROM": [1, [4, "75"]], "TO": [1, [4, "105"]]})
    point_dir = ctx.add("motion_pointindirection", inputs={"DIRECTION": [3, rnd_dir, [8, "90"]]})
    show_cl = ctx.add("looks_show")

    # Repeat until touching edge?
    touch_edge_menu = ctx.add("sensing_touchingobjectmenu", fields={"TOUCHINGOBJECTMENU": ["_edge_", None]}, shadow=True)
    touch_edge = ctx.add("sensing_touchingobject", inputs={"TOUCHINGOBJECTMENU": [1, touch_edge_menu]})

    # Step body:
    move_step = ctx.add("motion_movesteps", inputs={"STEPS": [1, [4, "14"]]})

    # Distance check loop across active entities
    set_rk = ctx.add("data_setvariableto", fields={"VARIABLE": ["ray_k", "v_ray_k"]}, inputs={"VALUE": [1, [4, "1"]]})

    target_act = ctx.add("data_itemoflist", fields={"LIST": ["ENTITY_ACTIVE", "l_ent_act"]}, inputs={"INDEX": [3, [12, "ray_k", "v_ray_k"], [7, "1"]]})
    is_act = ctx.add("operator_equals", inputs={"OPERAND1": [3, target_act, [10, ""]], "OPERAND2": [1, [10, "1"]]})

    tgt_x = ctx.add("data_itemoflist", fields={"LIST": ["ENTITY_X", "l_ent_x"]}, inputs={"INDEX": [3, [12, "ray_k", "v_ray_k"], [7, "1"]]})
    dx_val = ctx.add("operator_subtract", inputs={"NUM1": [3, tgt_x, [4, "0"]], "NUM2": [3, ctx.add("motion_xposition"), [4, "0"]]})
    set_rdx = ctx.add("data_setvariableto", fields={"VARIABLE": ["ray_dx", "v_ray_dx"]}, inputs={"VALUE": [3, dx_val, [4, "0"]]})

    tgt_y = ctx.add("data_itemoflist", fields={"LIST": ["ENTITY_Y", "l_ent_y"]}, inputs={"INDEX": [3, [12, "ray_k", "v_ray_k"], [7, "1"]]})
    dy_val = ctx.add("operator_subtract", inputs={"NUM1": [3, tgt_y, [4, "0"]], "NUM2": [3, ctx.add("motion_yposition"), [4, "0"]]})
    set_rdy = ctx.add("data_setvariableto", fields={"VARIABLE": ["ray_dy", "v_ray_dy"]}, inputs={"VALUE": [3, dy_val, [4, "0"]]})

    dx_sq = ctx.add("operator_multiply", inputs={"NUM1": [3, [12, "ray_dx", "v_ray_dx"], [4, "0"]], "NUM2": [3, [12, "ray_dx", "v_ray_dx"], [4, "0"]]})
    dy_sq = ctx.add("operator_multiply", inputs={"NUM1": [3, [12, "ray_dy", "v_ray_dy"], [4, "0"]], "NUM2": [3, [12, "ray_dy", "v_ray_dy"], [4, "0"]]})
    dsq_val = ctx.add("operator_add", inputs={"NUM1": [3, dx_sq, [4, "0"]], "NUM2": [3, dy_sq, [4, "0"]]})
    set_rdsq = ctx.add("data_setvariableto", fields={"VARIABLE": ["ray_dsq", "v_ray_dsq"]}, inputs={"VALUE": [3, dsq_val, [4, "0"]]})

    close_hit = ctx.add("operator_lt", inputs={"OPERAND1": [3, [12, "ray_dsq", "v_ray_dsq"], [10, ""]], "OPERAND2": [1, [10, "900"]]})

    # Ionization lookup
    tgt_spc = ctx.add("data_itemoflist", fields={"LIST": ["ENTITY_SPECIES", "l_ent_spc"]}, inputs={"INDEX": [3, [12, "ray_k", "v_ray_k"], [7, "1"]]})
    set_rspc = ctx.add("data_setvariableto", fields={"VARIABLE": ["ray_spc", "v_ray_spc"]}, inputs={"VALUE": [3, tgt_spc, [4, "1"]]})
    ion_idx_val = ctx.add("data_itemnumoflist", fields={"LIST": ["IONIZE_SRC", "l_ion_src"]}, inputs={"ITEM": [3, [12, "ray_spc", "v_ray_spc"], [10, ""]]})
    set_ridx = ctx.add("data_setvariableto", fields={"VARIABLE": ["ray_ion_idx", "v_ray_idx"]}, inputs={"VALUE": [3, ion_idx_val, [4, "0"]]})

    has_ion = ctx.add("operator_gt", inputs={"OPERAND1": [3, [12, "ray_ion_idx", "v_ray_idx"], [10, ""]], "OPERAND2": [1, [10, "0"]]})
    get_dst = ctx.add("data_itemoflist", fields={"LIST": ["IONIZE_DST", "l_ion_dst"]}, inputs={"INDEX": [3, [12, "ray_ion_idx", "v_ray_idx"], [7, "1"]]})
    set_rdst = ctx.add("data_setvariableto", fields={"VARIABLE": ["ray_new_ion", "v_ray_dst"]}, inputs={"VALUE": [3, get_dst, [4, "1"]]})
    upd_ent_spc = ctx.add("data_replaceitemoflist", fields={"LIST": ["ENTITY_SPECIES", "l_ent_spc"]}, inputs={"INDEX": [3, [12, "ray_k", "v_ray_k"], [7, "1"]], "ITEM": [3, [12, "ray_new_ion", "v_ray_dst"], [4, "1"]]})

    set_fx_x = ctx.add("data_setvariableto", fields={"VARIABLE": ["FX_X", "v_fx_x"]}, inputs={"VALUE": [3, tgt_x, [4, "0"]]})
    set_fx_y = ctx.add("data_setvariableto", fields={"VARIABLE": ["FX_Y", "v_fx_y"]}, inputs={"VALUE": [3, tgt_y, [4, "0"]]})
    bc_zap = ctx.add("event_broadcast", inputs={"BROADCAST_INPUT": [1, [11, "PLAY_FX_ZAP", "b_fx_zap"]]})
    snd_zap_m = ctx.add("sound_sounds_menu", fields={"SOUND_MENU": ["snd_cosmic", None]}, shadow=True)
    play_zap = ctx.add("sound_play", inputs={"SOUND_MENU": [1, snd_zap_m]})

    # Check discovery of the ion
    disc_val = ctx.add("data_itemoflist", fields={"LIST": ["DB_DISCOVERED", "l_db_disc"]}, inputs={"INDEX": [3, [12, "ray_new_ion", "v_ray_dst"], [7, "1"]]})
    is_new = ctx.add("operator_equals", inputs={"OPERAND1": [3, disc_val, [10, ""]], "OPERAND2": [1, [10, "0"]]})
    set_disc = ctx.add("data_replaceitemoflist", fields={"LIST": ["DB_DISCOVERED", "l_db_disc"]}, inputs={"INDEX": [3, [12, "ray_new_ion", "v_ray_dst"], [7, "1"]], "ITEM": [1, [4, "1"]]})
    inc_disc = ctx.add("data_changevariableby", fields={"VARIABLE": ["TOTAL_DISCOVERED", "v_discovered"]}, inputs={"VALUE": [1, [4, "1"]]})
    set_toast = ctx.add("data_setvariableto", fields={"VARIABLE": ["TOAST_SPECIES_ID", "v_toast_id"]}, inputs={"VALUE": [3, [12, "ray_new_ion", "v_ray_dst"], [4, "1"]]})
    bc_toast = ctx.add("event_broadcast", inputs={"BROADCAST_INPUT": [1, [11, "SHOW_TOAST", "b_show_toast"]]})
    snd_fanfare_m = ctx.add("sound_sounds_menu", fields={"SOUND_MENU": ["snd_discover", None]}, shadow=True)
    play_fanfare = ctx.add("sound_play", inputs={"SOUND_MENU": [1, snd_fanfare_m]})
    ctx.chain([set_disc, inc_disc, set_toast, bc_toast, play_fanfare])

    if_new_disc = ctx.add("control_if", inputs={"CONDITION": [2, is_new], "SUBSTACK": [2, set_disc]})
    ctx.blocks[set_disc]["parent"] = if_new_disc

    del_ray = ctx.add("control_delete_this_clone")
    ctx.chain([set_rdst, upd_ent_spc, set_fx_x, set_fx_y, bc_zap, play_zap, if_new_disc, del_ray])

    if_ion_match = ctx.add("control_if", inputs={"CONDITION": [2, has_ion], "SUBSTACK": [2, set_rdst]})
    ctx.blocks[set_rdst]["parent"] = if_ion_match

    ctx.chain([set_rspc, set_ridx, if_ion_match])

    if_hit = ctx.add("control_if", inputs={"CONDITION": [2, close_hit], "SUBSTACK": [2, set_rspc]})
    ctx.blocks[set_rspc]["parent"] = if_hit

    ctx.chain([set_rdx, set_rdy, set_rdsq, if_hit])

    if_cand_act = ctx.add("control_if", inputs={"CONDITION": [2, is_act], "SUBSTACK": [2, set_rdx]})
    ctx.blocks[set_rdx]["parent"] = if_cand_act

    inc_rk = ctx.add("data_changevariableby", fields={"VARIABLE": ["ray_k", "v_ray_k"]}, inputs={"VALUE": [1, [4, "1"]]})
    ctx.chain([if_cand_act, inc_rk])

    rep_len = ctx.add("data_lengthoflist", fields={"LIST": ["ENTITY_ACTIVE", "l_ent_act"]})
    rep_k_loop = ctx.add("control_repeat", inputs={"TIMES": [3, rep_len, [6, "10"]], "SUBSTACK": [2, if_cand_act]})
    ctx.blocks[if_cand_act]["parent"] = rep_k_loop

    ctx.chain([move_step, set_rk, rep_k_loop])

    if_sim_active = ctx.add("control_if", inputs={"CONDITION": [2, is_not_frozen], "SUBSTACK": [2, move_step]})
    ctx.blocks[move_step]["parent"] = if_sim_active

    rep_until_edge = ctx.add("control_repeat_until", inputs={"CONDITION": [2, touch_edge], "SUBSTACK": [2, if_sim_active]})
    ctx.blocks[if_sim_active]["parent"] = rep_until_edge

    del_at_edge = ctx.add("control_delete_this_clone")
    ctx.chain([hat_start, goto_edge, point_dir, show_cl, rep_until_edge, del_at_edge])

    return {
        "isStage": False,
        "name": "CosmicRay",
        "variables": ray_vars,
        "lists": {},
        "broadcasts": {},
        "blocks": ctx.blocks,
        "comments": {},
        "currentCostume": 0,
        "costumes": [costume_meta["cosmic_ray"]],
        "sounds": [sound_meta["snd_cosmic"], sound_meta["snd_discover"]],
        "volume": 100,
        "visible": False,
        "x": 0, "y": 0, "size": 100, "direction": 90,
        "draggable": False, "rotationStyle": "don't rotate"
    }

# Build Photon sprite
def build_photon():
    ctx = BlockContext()
    photon_vars = {"v_ph_life": ["life", 50]}

    hat_rec = ctx.add("event_whenbroadcastreceived", fields={"BROADCAST_OPTION": ["SPAWN_PHOTON", "b_spawn_photon"]}, topLevel=True, x=50, y=50)
    create_cl = ctx.add("control_create_clone_of", inputs={"CLONE_OPTION": [1, ctx.add("control_create_clone_of_menu", fields={"CLONE_OPTION": ["_myself_", None]}, shadow=True)]})
    ctx.chain([hat_rec, create_cl])

    hat_start = ctx.add("control_start_as_clone", topLevel=True, x=50, y=200)
    goto_fx = ctx.add("motion_gotoxy", inputs={"X": [3, [12, "FX_X", "v_fx_x"], [4, "0"]], "Y": [3, [12, "FX_Y", "v_fx_y"], [4, "0"]]})
    rnd_dir = ctx.add("operator_random", inputs={"FROM": [1, [4, "0"]], "TO": [1, [4, "360"]]})
    point_dir = ctx.add("motion_pointindirection", inputs={"DIRECTION": [3, rnd_dir, [8, "90"]]})
    set_life = ctx.add("data_setvariableto", fields={"VARIABLE": ["life", "v_ph_life"]}, inputs={"VALUE": [1, [4, "50"]]})
    set_ghost = ctx.add("looks_seteffectto", fields={"EFFECT": ["GHOST", None]}, inputs={"VALUE": [1, [4, "0"]]})
    show_ph = ctx.add("looks_show")
    snd_ph_m = ctx.add("sound_sounds_menu", fields={"SOUND_MENU": ["snd_photon", None]}, shadow=True)
    play_ph = ctx.add("sound_play", inputs={"SOUND_MENU": [1, snd_ph_m]})

    # Repeat until life < 1
    life_done = ctx.add("operator_lt", inputs={"OPERAND1": [3, [12, "life", "v_ph_life"], [10, ""]], "OPERAND2": [1, [10, "1"]]})
    is_not_frozen = ctx.add("operator_equals", inputs={"OPERAND1": [3, [12, "TIME_FROZEN", "v_freeze"], [10, ""]], "OPERAND2": [1, [10, "0"]]})

    mv_step = ctx.add("motion_movesteps", inputs={"STEPS": [1, [4, "8"]]})
    bounce_edge = ctx.add("motion_ifonedgebounce")
    dec_life = ctx.add("data_changevariableby", fields={"VARIABLE": ["life", "v_ph_life"]}, inputs={"VALUE": [1, [4, "-1"]]})
    inc_ghost = ctx.add("looks_changeeffectby", fields={"EFFECT": ["GHOST", None]}, inputs={"VALUE": [1, [4, "2"]]})
    ctx.chain([mv_step, bounce_edge, dec_life, inc_ghost])

    if_active = ctx.add("control_if", inputs={"CONDITION": [2, is_not_frozen], "SUBSTACK": [2, mv_step]})
    ctx.blocks[mv_step]["parent"] = if_active

    rep_loop = ctx.add("control_repeat_until", inputs={"CONDITION": [2, life_done], "SUBSTACK": [2, if_active]})
    ctx.blocks[if_active]["parent"] = rep_loop

    del_ph = ctx.add("control_delete_this_clone")
    ctx.chain([hat_start, goto_fx, point_dir, set_life, set_ghost, show_ph, play_ph, rep_loop, del_ph])

    return {
        "isStage": False,
        "name": "Photon",
        "variables": photon_vars,
        "lists": {},
        "broadcasts": {},
        "blocks": ctx.blocks,
        "comments": {},
        "currentCostume": 0,
        "costumes": [costume_meta["photon_wave"]],
        "sounds": [sound_meta["snd_photon"]],
        "volume": 100,
        "visible": False,
        "x": 0, "y": 0, "size": 100, "direction": 90,
        "draggable": False, "rotationStyle": "don't rotate"
    }

# Build Effects sprite
def build_effects():
    ctx = BlockContext()
    fx_costumes = [
        costume_meta["fx_exo_1"], costume_meta["fx_exo_2"], costume_meta["fx_exo_3"],
        costume_meta["fx_bond_1"], costume_meta["fx_bond_2"],
        costume_meta["fx_zap_1"], costume_meta["fx_zap_2"],
        costume_meta["fx_poof_1"], costume_meta["fx_poof_2"],
        costume_meta["toast_banner"]
    ]

    flag_id = ctx.add("event_whenflagclicked", topLevel=True, x=50, y=50)
    hide_orig = ctx.add("looks_hide")
    ctx.chain([flag_id, hide_orig])

    # Receiver for PLAY_FX_EXO
    hat_exo = ctx.add("event_whenbroadcastreceived", fields={"BROADCAST_OPTION": ["PLAY_FX_EXO", "b_fx_exo"]}, topLevel=True, x=50, y=150)
    goto_exo = ctx.add("motion_gotoxy", inputs={"X": [3, [12, "FX_X", "v_fx_x"], [4, "0"]], "Y": [3, [12, "FX_Y", "v_fx_y"], [4, "0"]]})
    sw_exo1 = ctx.add("looks_switchcostumeto", inputs={"COSTUME": [1, ctx.add("looks_costume", fields={"COSTUME": ["fx_exo_1", None]}, shadow=True)]})
    show_exo = ctx.add("looks_show")
    w1 = ctx.add("control_wait", inputs={"DURATION": [1, [4, "0.05"]]})
    sw_exo2 = ctx.add("looks_switchcostumeto", inputs={"COSTUME": [1, ctx.add("looks_costume", fields={"COSTUME": ["fx_exo_2", None]}, shadow=True)]})
    w2 = ctx.add("control_wait", inputs={"DURATION": [1, [4, "0.05"]]})
    sw_exo3 = ctx.add("looks_switchcostumeto", inputs={"COSTUME": [1, ctx.add("looks_costume", fields={"COSTUME": ["fx_exo_3", None]}, shadow=True)]})
    w3 = ctx.add("control_wait", inputs={"DURATION": [1, [4, "0.05"]]})
    hide_exo = ctx.add("looks_hide")
    ctx.chain([hat_exo, goto_exo, sw_exo1, show_exo, w1, sw_exo2, w2, sw_exo3, w3, hide_exo])

    # Receiver for PLAY_FX_BOND
    hat_bnd = ctx.add("event_whenbroadcastreceived", fields={"BROADCAST_OPTION": ["PLAY_FX_BOND", "b_fx_bond"]}, topLevel=True, x=50, y=420)
    goto_bnd = ctx.add("motion_gotoxy", inputs={"X": [3, [12, "FX_X", "v_fx_x"], [4, "0"]], "Y": [3, [12, "FX_Y", "v_fx_y"], [4, "0"]]})
    sw_bnd1 = ctx.add("looks_switchcostumeto", inputs={"COSTUME": [1, ctx.add("looks_costume", fields={"COSTUME": ["fx_bond_1", None]}, shadow=True)]})
    show_bnd = ctx.add("looks_show")
    wb1 = ctx.add("control_wait", inputs={"DURATION": [1, [4, "0.06"]]})
    sw_bnd2 = ctx.add("looks_switchcostumeto", inputs={"COSTUME": [1, ctx.add("looks_costume", fields={"COSTUME": ["fx_bond_2", None]}, shadow=True)]})
    wb2 = ctx.add("control_wait", inputs={"DURATION": [1, [4, "0.06"]]})
    hide_bnd = ctx.add("looks_hide")
    ctx.chain([hat_bnd, goto_bnd, sw_bnd1, show_bnd, wb1, sw_bnd2, wb2, hide_bnd])

    # Receiver for PLAY_FX_ZAP
    hat_zap = ctx.add("event_whenbroadcastreceived", fields={"BROADCAST_OPTION": ["PLAY_FX_ZAP", "b_fx_zap"]}, topLevel=True, x=450, y=150)
    goto_zap = ctx.add("motion_gotoxy", inputs={"X": [3, [12, "FX_X", "v_fx_x"], [4, "0"]], "Y": [3, [12, "FX_Y", "v_fx_y"], [4, "0"]]})
    sw_zap1 = ctx.add("looks_switchcostumeto", inputs={"COSTUME": [1, ctx.add("looks_costume", fields={"COSTUME": ["fx_zap_1", None]}, shadow=True)]})
    show_zap = ctx.add("looks_show")
    wz1 = ctx.add("control_wait", inputs={"DURATION": [1, [4, "0.05"]]})
    sw_zap2 = ctx.add("looks_switchcostumeto", inputs={"COSTUME": [1, ctx.add("looks_costume", fields={"COSTUME": ["fx_zap_2", None]}, shadow=True)]})
    wz2 = ctx.add("control_wait", inputs={"DURATION": [1, [4, "0.05"]]})
    hide_zap = ctx.add("looks_hide")
    ctx.chain([hat_zap, goto_zap, sw_zap1, show_zap, wz1, sw_zap2, wz2, hide_zap])

    # Receiver for PLAY_FX_DELETE
    hat_del = ctx.add("event_whenbroadcastreceived", fields={"BROADCAST_OPTION": ["PLAY_FX_DELETE", "b_fx_del"]}, topLevel=True, x=450, y=420)
    goto_del = ctx.add("motion_gotoxy", inputs={"X": [3, [12, "FX_X", "v_fx_x"], [4, "0"]], "Y": [3, [12, "FX_Y", "v_fx_y"], [4, "0"]]})
    sw_poof1 = ctx.add("looks_switchcostumeto", inputs={"COSTUME": [1, ctx.add("looks_costume", fields={"COSTUME": ["fx_poof_1", None]}, shadow=True)]})
    show_del = ctx.add("looks_show")
    wd1 = ctx.add("control_wait", inputs={"DURATION": [1, [4, "0.06"]]})
    sw_poof2 = ctx.add("looks_switchcostumeto", inputs={"COSTUME": [1, ctx.add("looks_costume", fields={"COSTUME": ["fx_poof_2", None]}, shadow=True)]})
    wd2 = ctx.add("control_wait", inputs={"DURATION": [1, [4, "0.06"]]})
    hide_del = ctx.add("looks_hide")
    ctx.chain([hat_del, goto_del, sw_poof1, show_del, wd1, sw_poof2, wd2, hide_del])

    # Receiver for SHOW_TOAST
    hat_toast = ctx.add("event_whenbroadcastreceived", fields={"BROADCAST_OPTION": ["SHOW_TOAST", "b_show_toast"]}, topLevel=True, x=450, y=650)
    goto_toast = ctx.add("motion_gotoxy", inputs={"X": [1, [4, "0"]], "Y": [1, [4, "120"]]})
    sw_toast = ctx.add("looks_switchcostumeto", inputs={"COSTUME": [1, ctx.add("looks_costume", fields={"COSTUME": ["toast_banner", None]}, shadow=True)]})
    show_toast = ctx.add("looks_show")
    front_toast = ctx.add("looks_gotofrontback", fields={"FRONT_BACK": ["front", None]})
    wt = ctx.add("control_wait", inputs={"DURATION": [1, [4, "2.5"]]})
    hide_toast = ctx.add("looks_hide")
    ctx.chain([hat_toast, goto_toast, sw_toast, show_toast, front_toast, wt, hide_toast])

    return {
        "isStage": False,
        "name": "Effects",
        "variables": {},
        "lists": {},
        "broadcasts": {},
        "blocks": ctx.blocks,
        "comments": {},
        "currentCostume": 0,
        "costumes": fx_costumes,
        "sounds": [],
        "volume": 100,
        "visible": False,
        "x": 0, "y": 0, "size": 100, "direction": 90,
        "draggable": False, "rotationStyle": "don't rotate"
    }

print("CosmicRay, Photon, and Effects builders configured.")

# Build TopBarUI sprite
def build_top_bar_ui():
    ctx = BlockContext()
    top_vars = {"v_btn_id": ["btn_id", 0], "v_init_i": ["init_i", 1]}

    button_costumes = [
        costume_meta["btn_add"], costume_meta["btn_add_active"],
        costume_meta["btn_del"], costume_meta["btn_del_active"],
        costume_meta["btn_uv"], costume_meta["btn_uv_active"],
        costume_meta["btn_freeze"], costume_meta["btn_freeze_active"],
        costume_meta["btn_info"], costume_meta["btn_info_active"],
        costume_meta["btn_discover"],
        costume_meta["btn_sound"], costume_meta["btn_sound_muted"],
        costume_meta["btn_save"],
        costume_meta["btn_clear"]
    ]
    button_sounds = [sound_meta["snd_click"], sound_meta["snd_freeze"], sound_meta["snd_delete"]]

    # Flag: create 9 button clones
    flag_id = ctx.add("event_whenflagclicked", topLevel=True, x=50, y=50)
    set_zero = ctx.add("data_setvariableto", fields={"VARIABLE": ["btn_id", "v_btn_id"]}, inputs={"VALUE": [1, [4, "0"]]})
    set_i1 = ctx.add("data_setvariableto", fields={"VARIABLE": ["init_i", "v_init_i"]}, inputs={"VALUE": [1, [4, "1"]]})
    hide_main = ctx.add("looks_hide")

    # Inside repeat 9:
    set_bid_i = ctx.add("data_setvariableto", fields={"VARIABLE": ["btn_id", "v_btn_id"]}, inputs={"VALUE": [3, [12, "init_i", "v_init_i"], [4, "1"]]})
    create_cl = ctx.add("control_create_clone_of", inputs={"CLONE_OPTION": [1, ctx.add("control_create_clone_of_menu", fields={"CLONE_OPTION": ["_myself_", None]}, shadow=True)]})
    inc_i = ctx.add("data_changevariableby", fields={"VARIABLE": ["init_i", "v_init_i"]}, inputs={"VALUE": [1, [4, "1"]]})
    ctx.chain([set_bid_i, create_cl, inc_i])

    rep_9 = ctx.add("control_repeat", inputs={"TIMES": [1, [6, "9"]], "SUBSTACK": [2, set_bid_i]})
    ctx.blocks[set_bid_i]["parent"] = rep_9
    bc_upd_flag = ctx.add("event_broadcast", inputs={"BROADCAST_INPUT": [1, [11, "UPDATE_UI", "b_update_ui"]]})
    ctx.chain([flag_id, set_zero, set_i1, hide_main, rep_9, bc_upd_flag])

    # Clone init: position by btn_id
    hat_start = ctx.add("control_start_as_clone", topLevel=True, x=50, y=300)
    calc_x_mult = ctx.add("operator_multiply", inputs={"NUM1": [3, [12, "btn_id", "v_btn_id"], [4, "1"]], "NUM2": [1, [4, "48"]]})
    calc_x = ctx.add("operator_add", inputs={"NUM1": [1, [4, "-238"]], "NUM2": [3, calc_x_mult, [4, "0"]]})
    goto_pos = ctx.add("motion_gotoxy", inputs={"X": [3, calc_x, [4, "0"]], "Y": [1, [4, "156"]]})
    show_cl = ctx.add("looks_show")
    bc_upd_clone = ctx.add("event_broadcast", inputs={"BROADCAST_INPUT": [1, [11, "UPDATE_UI", "b_update_ui"]]})
    ctx.chain([hat_start, goto_pos, show_cl, bc_upd_clone])

    # Update loop on UPDATE_UI
    hat_upd = ctx.add("event_whenbroadcastreceived", fields={"BROADCAST_OPTION": ["UPDATE_UI", "b_update_ui"]}, topLevel=True, x=450, y=50)

    # Costume update logic per button
    # If btn_id == 1 (ADD): if SHOW_PALETTE == 1 btn_add_active else btn_add
    is_btn1 = ctx.add("operator_equals", inputs={"OPERAND1": [3, [12, "btn_id", "v_btn_id"], [10, ""]], "OPERAND2": [1, [10, "1"]]})
    pal_active = ctx.add("operator_equals", inputs={"OPERAND1": [3, [12, "SHOW_PALETTE", "v_palette"], [10, ""]], "OPERAND2": [1, [10, "1"]]})
    c_add_act = ctx.add("looks_switchcostumeto", inputs={"COSTUME": [1, ctx.add("looks_costume", fields={"COSTUME": ["btn_add_active", None]}, shadow=True)]})
    c_add_inact = ctx.add("looks_switchcostumeto", inputs={"COSTUME": [1, ctx.add("looks_costume", fields={"COSTUME": ["btn_add", None]}, shadow=True)]})
    if_pal_else = ctx.add("control_if_else", inputs={"CONDITION": [2, pal_active], "SUBSTACK": [2, c_add_act], "SUBSTACK2": [2, c_add_inact]})
    ctx.blocks[c_add_act]["parent"] = if_pal_else
    ctx.blocks[c_add_inact]["parent"] = if_pal_else
    if_b1 = ctx.add("control_if", inputs={"CONDITION": [2, is_btn1], "SUBSTACK": [2, if_pal_else]})
    ctx.blocks[if_pal_else]["parent"] = if_b1

    # If btn_id == 2 (DEL)
    is_btn2 = ctx.add("operator_equals", inputs={"OPERAND1": [3, [12, "btn_id", "v_btn_id"], [10, ""]], "OPERAND2": [1, [10, "2"]]})
    del_active = ctx.add("operator_equals", inputs={"OPERAND1": [3, [12, "CURRENT_TOOL", "v_tool"], [10, ""]], "OPERAND2": [1, [10, "delete"]]})
    c_del_act = ctx.add("looks_switchcostumeto", inputs={"COSTUME": [1, ctx.add("looks_costume", fields={"COSTUME": ["btn_del_active", None]}, shadow=True)]})
    c_del_inact = ctx.add("looks_switchcostumeto", inputs={"COSTUME": [1, ctx.add("looks_costume", fields={"COSTUME": ["btn_del", None]}, shadow=True)]})
    if_del_else = ctx.add("control_if_else", inputs={"CONDITION": [2, del_active], "SUBSTACK": [2, c_del_act], "SUBSTACK2": [2, c_del_inact]})
    ctx.blocks[c_del_act]["parent"] = if_del_else
    ctx.blocks[c_del_inact]["parent"] = if_del_else
    if_b2 = ctx.add("control_if", inputs={"CONDITION": [2, is_btn2], "SUBSTACK": [2, if_del_else]})
    ctx.blocks[if_del_else]["parent"] = if_b2

    # If btn_id == 3 (UV)
    is_btn3 = ctx.add("operator_equals", inputs={"OPERAND1": [3, [12, "btn_id", "v_btn_id"], [10, ""]], "OPERAND2": [1, [10, "3"]]})
    uv_is_on = ctx.add("operator_equals", inputs={"OPERAND1": [3, [12, "UV_ACTIVE", "v_uv"], [10, ""]], "OPERAND2": [1, [10, "1"]]})
    c_uv_act = ctx.add("looks_switchcostumeto", inputs={"COSTUME": [1, ctx.add("looks_costume", fields={"COSTUME": ["btn_uv_active", None]}, shadow=True)]})
    c_uv_inact = ctx.add("looks_switchcostumeto", inputs={"COSTUME": [1, ctx.add("looks_costume", fields={"COSTUME": ["btn_uv", None]}, shadow=True)]})
    if_uv_else = ctx.add("control_if_else", inputs={"CONDITION": [2, uv_is_on], "SUBSTACK": [2, c_uv_act], "SUBSTACK2": [2, c_uv_inact]})
    ctx.blocks[c_uv_act]["parent"] = if_uv_else
    ctx.blocks[c_uv_inact]["parent"] = if_uv_else
    if_b3 = ctx.add("control_if", inputs={"CONDITION": [2, is_btn3], "SUBSTACK": [2, if_uv_else]})
    ctx.blocks[if_uv_else]["parent"] = if_b3

    # If btn_id == 4 (FREEZE)
    is_btn4 = ctx.add("operator_equals", inputs={"OPERAND1": [3, [12, "btn_id", "v_btn_id"], [10, ""]], "OPERAND2": [1, [10, "4"]]})
    frz_is_on = ctx.add("operator_equals", inputs={"OPERAND1": [3, [12, "TIME_FROZEN", "v_freeze"], [10, ""]], "OPERAND2": [1, [10, "1"]]})
    c_frz_act = ctx.add("looks_switchcostumeto", inputs={"COSTUME": [1, ctx.add("looks_costume", fields={"COSTUME": ["btn_freeze_active", None]}, shadow=True)]})
    c_frz_inact = ctx.add("looks_switchcostumeto", inputs={"COSTUME": [1, ctx.add("looks_costume", fields={"COSTUME": ["btn_freeze", None]}, shadow=True)]})
    if_frz_else = ctx.add("control_if_else", inputs={"CONDITION": [2, frz_is_on], "SUBSTACK": [2, c_frz_act], "SUBSTACK2": [2, c_frz_inact]})
    ctx.blocks[c_frz_act]["parent"] = if_frz_else
    ctx.blocks[c_frz_inact]["parent"] = if_frz_else
    if_b4 = ctx.add("control_if", inputs={"CONDITION": [2, is_btn4], "SUBSTACK": [2, if_frz_else]})
    ctx.blocks[if_frz_else]["parent"] = if_b4

    # If btn_id == 5 (INFO)
    is_btn5 = ctx.add("operator_equals", inputs={"OPERAND1": [3, [12, "btn_id", "v_btn_id"], [10, ""]], "OPERAND2": [1, [10, "5"]]})
    info_active = ctx.add("operator_equals", inputs={"OPERAND1": [3, [12, "CURRENT_TOOL", "v_tool"], [10, ""]], "OPERAND2": [1, [10, "info"]]})
    c_inf_act = ctx.add("looks_switchcostumeto", inputs={"COSTUME": [1, ctx.add("looks_costume", fields={"COSTUME": ["btn_info_active", None]}, shadow=True)]})
    c_inf_inact = ctx.add("looks_switchcostumeto", inputs={"COSTUME": [1, ctx.add("looks_costume", fields={"COSTUME": ["btn_info", None]}, shadow=True)]})
    if_inf_else = ctx.add("control_if_else", inputs={"CONDITION": [2, info_active], "SUBSTACK": [2, c_inf_act], "SUBSTACK2": [2, c_inf_inact]})
    ctx.blocks[c_inf_act]["parent"] = if_inf_else
    ctx.blocks[c_inf_inact]["parent"] = if_inf_else
    if_b5 = ctx.add("control_if", inputs={"CONDITION": [2, is_btn5], "SUBSTACK": [2, if_inf_else]})
    ctx.blocks[if_inf_else]["parent"] = if_b5

    # If btn_id == 6 (DISCOVER)
    is_btn6 = ctx.add("operator_equals", inputs={"OPERAND1": [3, [12, "btn_id", "v_btn_id"], [10, ""]], "OPERAND2": [1, [10, "6"]]})
    c_disc = ctx.add("looks_switchcostumeto", inputs={"COSTUME": [1, ctx.add("looks_costume", fields={"COSTUME": ["btn_discover", None]}, shadow=True)]})
    if_b6 = ctx.add("control_if", inputs={"CONDITION": [2, is_btn6], "SUBSTACK": [2, c_disc]})
    ctx.blocks[c_disc]["parent"] = if_b6

    # If btn_id == 7 (SOUND)
    is_btn7 = ctx.add("operator_equals", inputs={"OPERAND1": [3, [12, "btn_id", "v_btn_id"], [10, ""]], "OPERAND2": [1, [10, "7"]]})
    is_muted = ctx.add("operator_equals", inputs={"OPERAND1": [3, [12, "MASTER_VOLUME", "v_volume"], [10, ""]], "OPERAND2": [1, [10, "0"]]})
    c_snd_mut = ctx.add("looks_switchcostumeto", inputs={"COSTUME": [1, ctx.add("looks_costume", fields={"COSTUME": ["btn_sound_muted", None]}, shadow=True)]})
    c_snd_on = ctx.add("looks_switchcostumeto", inputs={"COSTUME": [1, ctx.add("looks_costume", fields={"COSTUME": ["btn_sound", None]}, shadow=True)]})
    if_snd_else = ctx.add("control_if_else", inputs={"CONDITION": [2, is_muted], "SUBSTACK": [2, c_snd_mut], "SUBSTACK2": [2, c_snd_on]})
    ctx.blocks[c_snd_mut]["parent"] = if_snd_else
    ctx.blocks[c_snd_on]["parent"] = if_snd_else
    if_b7 = ctx.add("control_if", inputs={"CONDITION": [2, is_btn7], "SUBSTACK": [2, if_snd_else]})
    ctx.blocks[if_snd_else]["parent"] = if_b7

    # If btn_id == 8 (SAVE)
    is_btn8 = ctx.add("operator_equals", inputs={"OPERAND1": [3, [12, "btn_id", "v_btn_id"], [10, ""]], "OPERAND2": [1, [10, "8"]]})
    c_save = ctx.add("looks_switchcostumeto", inputs={"COSTUME": [1, ctx.add("looks_costume", fields={"COSTUME": ["btn_save", None]}, shadow=True)]})
    if_b8 = ctx.add("control_if", inputs={"CONDITION": [2, is_btn8], "SUBSTACK": [2, c_save]})
    ctx.blocks[c_save]["parent"] = if_b8

    # If btn_id == 9 (CLEAR)
    is_btn9 = ctx.add("operator_equals", inputs={"OPERAND1": [3, [12, "btn_id", "v_btn_id"], [10, ""]], "OPERAND2": [1, [10, "9"]]})
    c_clear = ctx.add("looks_switchcostumeto", inputs={"COSTUME": [1, ctx.add("looks_costume", fields={"COSTUME": ["btn_clear", None]}, shadow=True)]})
    if_b9 = ctx.add("control_if", inputs={"CONDITION": [2, is_btn9], "SUBSTACK": [2, c_clear]})
    ctx.blocks[c_clear]["parent"] = if_b9

    ctx.chain([hat_upd, if_b1, if_b2, if_b3, if_b4, if_b5, if_b6, if_b7, if_b8, if_b9])

    # Click handling
    hat_click = ctx.add("event_whenthisspriteclicked", topLevel=True, x=50, y=700)
    snd_clk_m = ctx.add("sound_sounds_menu", fields={"SOUND_MENU": ["snd_click", None]}, shadow=True)
    play_clk = ctx.add("sound_play", inputs={"SOUND_MENU": [1, snd_clk_m]})

    # Action 1: ADD toggle
    is_act_b1 = ctx.add("operator_equals", inputs={"OPERAND1": [3, [12, "btn_id", "v_btn_id"], [10, ""]], "OPERAND2": [1, [10, "1"]]})
    inv_pal = ctx.add("operator_subtract", inputs={"NUM1": [1, [4, "1"]], "NUM2": [3, [12, "SHOW_PALETTE", "v_palette"], [4, "0"]]})
    t_pal = ctx.add("data_setvariableto", fields={"VARIABLE": ["SHOW_PALETTE", "v_palette"]}, inputs={"VALUE": [3, inv_pal, [4, "0"]]})
    bc_upd1 = ctx.add("event_broadcast", inputs={"BROADCAST_INPUT": [1, [11, "UPDATE_UI", "b_update_ui"]]})
    ctx.chain([t_pal, bc_upd1])
    act_b1 = ctx.add("control_if", inputs={"CONDITION": [2, is_act_b1], "SUBSTACK": [2, t_pal]})
    ctx.blocks[t_pal]["parent"] = act_b1

    # Action 2: DEL toggle
    is_act_b2 = ctx.add("operator_equals", inputs={"OPERAND1": [3, [12, "btn_id", "v_btn_id"], [10, ""]], "OPERAND2": [1, [10, "2"]]})
    is_del_now = ctx.add("operator_equals", inputs={"OPERAND1": [3, [12, "CURRENT_TOOL", "v_tool"], [10, ""]], "OPERAND2": [1, [10, "delete"]]})
    set_drag2 = ctx.add("data_setvariableto", fields={"VARIABLE": ["CURRENT_TOOL", "v_tool"]}, inputs={"VALUE": [1, [10, "drag"]]})
    set_del2 = ctx.add("data_setvariableto", fields={"VARIABLE": ["CURRENT_TOOL", "v_tool"]}, inputs={"VALUE": [1, [10, "delete"]]})
    if_t_del = ctx.add("control_if_else", inputs={"CONDITION": [2, is_del_now], "SUBSTACK": [2, set_drag2], "SUBSTACK2": [2, set_del2]})
    ctx.blocks[set_drag2]["parent"] = if_t_del
    ctx.blocks[set_del2]["parent"] = if_t_del
    bc_upd2 = ctx.add("event_broadcast", inputs={"BROADCAST_INPUT": [1, [11, "UPDATE_UI", "b_update_ui"]]})
    ctx.chain([if_t_del, bc_upd2])
    act_b2 = ctx.add("control_if", inputs={"CONDITION": [2, is_act_b2], "SUBSTACK": [2, if_t_del]})
    ctx.blocks[if_t_del]["parent"] = act_b2

    # Action 3: UV toggle
    is_act_b3 = ctx.add("operator_equals", inputs={"OPERAND1": [3, [12, "btn_id", "v_btn_id"], [10, ""]], "OPERAND2": [1, [10, "3"]]})
    inv_uv = ctx.add("operator_subtract", inputs={"NUM1": [1, [4, "1"]], "NUM2": [3, [12, "UV_ACTIVE", "v_uv"], [4, "0"]]})
    t_uv = ctx.add("data_setvariableto", fields={"VARIABLE": ["UV_ACTIVE", "v_uv"]}, inputs={"VALUE": [3, inv_uv, [4, "0"]]})
    bc_bg3 = ctx.add("event_broadcast", inputs={"BROADCAST_INPUT": [1, [11, "UPDATE_BACKDROP", "b_update_bg"]]})
    bc_upd3 = ctx.add("event_broadcast", inputs={"BROADCAST_INPUT": [1, [11, "UPDATE_UI", "b_update_ui"]]})
    ctx.chain([t_uv, bc_bg3, bc_upd3])
    act_b3 = ctx.add("control_if", inputs={"CONDITION": [2, is_act_b3], "SUBSTACK": [2, t_uv]})
    ctx.blocks[t_uv]["parent"] = act_b3

    # Action 4: FREEZE toggle
    is_act_b4 = ctx.add("operator_equals", inputs={"OPERAND1": [3, [12, "btn_id", "v_btn_id"], [10, ""]], "OPERAND2": [1, [10, "4"]]})
    inv_frz = ctx.add("operator_subtract", inputs={"NUM1": [1, [4, "1"]], "NUM2": [3, [12, "TIME_FROZEN", "v_freeze"], [4, "0"]]})
    t_frz = ctx.add("data_setvariableto", fields={"VARIABLE": ["TIME_FROZEN", "v_freeze"]}, inputs={"VALUE": [3, inv_frz, [4, "0"]]})
    bc_bg4 = ctx.add("event_broadcast", inputs={"BROADCAST_INPUT": [1, [11, "UPDATE_BACKDROP", "b_update_bg"]]})
    bc_upd4 = ctx.add("event_broadcast", inputs={"BROADCAST_INPUT": [1, [11, "UPDATE_UI", "b_update_ui"]]})
    snd_frz_m = ctx.add("sound_sounds_menu", fields={"SOUND_MENU": ["snd_freeze", None]}, shadow=True)
    play_frz = ctx.add("sound_play", inputs={"SOUND_MENU": [1, snd_frz_m]})
    ctx.chain([t_frz, bc_bg4, bc_upd4, play_frz])
    act_b4 = ctx.add("control_if", inputs={"CONDITION": [2, is_act_b4], "SUBSTACK": [2, t_frz]})
    ctx.blocks[t_frz]["parent"] = act_b4

    # Action 5: INFO toggle
    is_act_b5 = ctx.add("operator_equals", inputs={"OPERAND1": [3, [12, "btn_id", "v_btn_id"], [10, ""]], "OPERAND2": [1, [10, "5"]]})
    is_inf_now = ctx.add("operator_equals", inputs={"OPERAND1": [3, [12, "CURRENT_TOOL", "v_tool"], [10, ""]], "OPERAND2": [1, [10, "info"]]})
    set_drag5 = ctx.add("data_setvariableto", fields={"VARIABLE": ["CURRENT_TOOL", "v_tool"]}, inputs={"VALUE": [1, [10, "drag"]]})
    set_inf5 = ctx.add("data_setvariableto", fields={"VARIABLE": ["CURRENT_TOOL", "v_tool"]}, inputs={"VALUE": [1, [10, "info"]]})
    if_t_info = ctx.add("control_if_else", inputs={"CONDITION": [2, is_inf_now], "SUBSTACK": [2, set_drag5], "SUBSTACK2": [2, set_inf5]})
    ctx.blocks[set_drag5]["parent"] = if_t_info
    ctx.blocks[set_inf5]["parent"] = if_t_info
    bc_upd5 = ctx.add("event_broadcast", inputs={"BROADCAST_INPUT": [1, [11, "UPDATE_UI", "b_update_ui"]]})
    ctx.chain([if_t_info, bc_upd5])
    act_b5 = ctx.add("control_if", inputs={"CONDITION": [2, is_act_b5], "SUBSTACK": [2, if_t_info]})
    ctx.blocks[if_t_info]["parent"] = act_b5

    # Action 6: DISCOVER toggle
    is_act_b6 = ctx.add("operator_equals", inputs={"OPERAND1": [3, [12, "btn_id", "v_btn_id"], [10, ""]], "OPERAND2": [1, [10, "6"]]})
    inv_comp = ctx.add("operator_subtract", inputs={"NUM1": [1, [4, "1"]], "NUM2": [3, [12, "SHOW_COMPENDIUM", "v_compendium"], [4, "0"]]})
    t_comp = ctx.add("data_setvariableto", fields={"VARIABLE": ["SHOW_COMPENDIUM", "v_compendium"]}, inputs={"VALUE": [3, inv_comp, [4, "0"]]})
    bc_upd6 = ctx.add("event_broadcast", inputs={"BROADCAST_INPUT": [1, [11, "UPDATE_UI", "b_update_ui"]]})
    ctx.chain([t_comp, bc_upd6])
    act_b6 = ctx.add("control_if", inputs={"CONDITION": [2, is_act_b6], "SUBSTACK": [2, t_comp]})
    ctx.blocks[t_comp]["parent"] = act_b6

    # Action 7: SOUND toggle
    is_act_b7 = ctx.add("operator_equals", inputs={"OPERAND1": [3, [12, "btn_id", "v_btn_id"], [10, ""]], "OPERAND2": [1, [10, "7"]]})
    is_vol_zero = ctx.add("operator_equals", inputs={"OPERAND1": [3, [12, "MASTER_VOLUME", "v_volume"], [10, ""]], "OPERAND2": [1, [10, "0"]]})
    set_vol_100 = ctx.add("data_setvariableto", fields={"VARIABLE": ["MASTER_VOLUME", "v_volume"]}, inputs={"VALUE": [1, [4, "100"]]})
    set_vol_0 = ctx.add("data_setvariableto", fields={"VARIABLE": ["MASTER_VOLUME", "v_volume"]}, inputs={"VALUE": [1, [4, "0"]]})
    if_t_vol = ctx.add("control_if_else", inputs={"CONDITION": [2, is_vol_zero], "SUBSTACK": [2, set_vol_100], "SUBSTACK2": [2, set_vol_0]})
    ctx.blocks[set_vol_100]["parent"] = if_t_vol
    ctx.blocks[set_vol_0]["parent"] = if_t_vol
    set_sys_vol = ctx.add("sound_setvolumeto", inputs={"VOLUME": [3, [12, "MASTER_VOLUME", "v_volume"], [4, "100"]]})
    bc_upd7 = ctx.add("event_broadcast", inputs={"BROADCAST_INPUT": [1, [11, "UPDATE_UI", "b_update_ui"]]})
    ctx.chain([if_t_vol, set_sys_vol, bc_upd7])
    act_b7 = ctx.add("control_if", inputs={"CONDITION": [2, is_act_b7], "SUBSTACK": [2, if_t_vol]})
    ctx.blocks[if_t_vol]["parent"] = act_b7

    # Action 8: SAVE
    is_act_b8 = ctx.add("operator_equals", inputs={"OPERAND1": [3, [12, "btn_id", "v_btn_id"], [10, ""]], "OPERAND2": [1, [10, "8"]]})
    bc_save8 = ctx.add("event_broadcast", inputs={"BROADCAST_INPUT": [1, [11, "PROMPT_SAVE_LOAD", "b_prompt_save"]]})
    act_b8 = ctx.add("control_if", inputs={"CONDITION": [2, is_act_b8], "SUBSTACK": [2, bc_save8]})
    ctx.blocks[bc_save8]["parent"] = act_b8

    # Action 9: CLEAR
    is_act_b9 = ctx.add("operator_equals", inputs={"OPERAND1": [3, [12, "btn_id", "v_btn_id"], [10, ""]], "OPERAND2": [1, [10, "9"]]})
    bc_clear9 = ctx.add("event_broadcast", inputs={"BROADCAST_INPUT": [1, [11, "CLEAR_ALL", "b_clear_all"]]})
    snd_del_m9 = ctx.add("sound_sounds_menu", fields={"SOUND_MENU": ["snd_delete", None]}, shadow=True)
    play_del9 = ctx.add("sound_play", inputs={"SOUND_MENU": [1, snd_del_m9]})
    ctx.chain([bc_clear9, play_del9])
    act_b9 = ctx.add("control_if", inputs={"CONDITION": [2, is_act_b9], "SUBSTACK": [2, bc_clear9]})
    ctx.blocks[bc_clear9]["parent"] = act_b9

    ctx.chain([hat_click, play_clk, act_b1, act_b2, act_b3, act_b4, act_b5, act_b6, act_b7, act_b8, act_b9])

    return {
        "isStage": False,
        "name": "TopBarUI",
        "variables": top_vars,
        "lists": {},
        "broadcasts": {},
        "blocks": ctx.blocks,
        "comments": {},
        "currentCostume": 0,
        "costumes": button_costumes,
        "sounds": button_sounds,
        "volume": 100,
        "visible": True,
        "x": 0, "y": 156, "size": 100, "direction": 90,
        "draggable": False, "rotationStyle": "don't rotate"
    }

# Build PaletteUI sprite
def build_palette_ui():
    ctx = BlockContext()
    pal_vars = {"v_pal_col": ["calc_col", 1]}

    flag_id = ctx.add("event_whenflagclicked", topLevel=True, x=50, y=50)
    hide_pal = ctx.add("looks_hide")
    goto_pal = ctx.add("motion_gotoxy", inputs={"X": [1, [4, "0"]], "Y": [1, [4, "-135"]]})
    ctx.chain([flag_id, hide_pal, goto_pal])

    hat_upd = ctx.add("event_whenbroadcastreceived", fields={"BROADCAST_OPTION": ["UPDATE_UI", "b_update_ui"]}, topLevel=True, x=50, y=180)
    is_show = ctx.add("operator_equals", inputs={"OPERAND1": [3, [12, "SHOW_PALETTE", "v_palette"], [10, ""]], "OPERAND2": [1, [10, "1"]]})
    show_pal = ctx.add("looks_show")
    front_pal = ctx.add("looks_gotofrontback", fields={"FRONT_BACK": ["front", None]})
    hide_pal2 = ctx.add("looks_hide")
    ctx.chain([show_pal, front_pal])
    if_show_else = ctx.add("control_if_else", inputs={"CONDITION": [2, is_show], "SUBSTACK": [2, show_pal], "SUBSTACK2": [2, hide_pal2]})
    ctx.blocks[show_pal]["parent"] = if_show_else
    ctx.blocks[hide_pal2]["parent"] = if_show_else
    ctx.chain([hat_upd, if_show_else])

    # Click handling: map mouse coordinates to element 1..19
    hat_click = ctx.add("event_whenthisspriteclicked", topLevel=True, x=50, y=380)
    # Calculate column: int((mouse x + 240) / 48) + 1
    mx = ctx.add("sensing_mousex")
    mx_shifted = ctx.add("operator_add", inputs={"NUM1": [3, mx, [4, "0"]], "NUM2": [1, [4, "240"]]})
    col_raw = ctx.add("operator_divide", inputs={"NUM1": [3, mx_shifted, [4, "0"]], "NUM2": [1, [4, "48"]]})
    col_int = ctx.add("operator_mathop", fields={"OPERATOR": ["floor", None]}, inputs={"NUM": [3, col_raw, [4, "0"]]})
    col_1_based = ctx.add("operator_add", inputs={"NUM1": [3, col_int, [4, "0"]], "NUM2": [1, [4, "1"]]})
    set_col = ctx.add("data_setvariableto", fields={"VARIABLE": ["calc_col", "v_pal_col"]}, inputs={"VALUE": [3, col_1_based, [4, "1"]]})

    # Row check: mouse y > -140
    my = ctx.add("sensing_mousey")
    is_row1 = ctx.add("operator_gt", inputs={"OPERAND1": [3, my, [10, ""]], "OPERAND2": [1, [10, "-140"]]})

    # Row 1 (H to Ne, IDs 1 to 10)
    set_spc_r1 = ctx.add("data_setvariableto", fields={"VARIABLE": ["SPAWN_SPECIES_ID", "v_spawn_id"]}, inputs={"VALUE": [3, [12, "calc_col", "v_pal_col"], [4, "1"]]})

    # Row 2 (Na to I, IDs 10 to 19)
    id_r2 = ctx.add("operator_add", inputs={"NUM1": [3, [12, "calc_col", "v_pal_col"], [4, "1"]], "NUM2": [1, [4, "9"]]})
    set_spc_r2 = ctx.add("data_setvariableto", fields={"VARIABLE": ["SPAWN_SPECIES_ID", "v_spawn_id"]}, inputs={"VALUE": [3, id_r2, [4, "10"]]})

    if_row_else = ctx.add("control_if_else", inputs={"CONDITION": [2, is_row1], "SUBSTACK": [2, set_spc_r1], "SUBSTACK2": [2, set_spc_r2]})
    ctx.blocks[set_spc_r1]["parent"] = if_row_else
    ctx.blocks[set_spc_r2]["parent"] = if_row_else

    # Random spawn coordinates in vacuum
    rnd_sx = ctx.add("operator_random", inputs={"FROM": [1, [4, "-90"]], "TO": [1, [4, "90"]]})
    set_sx = ctx.add("data_setvariableto", fields={"VARIABLE": ["SPAWN_X", "v_spawn_x"]}, inputs={"VALUE": [3, rnd_sx, [4, "0"]]})
    rnd_sy = ctx.add("operator_random", inputs={"FROM": [1, [4, "-30"]], "TO": [1, [4, "40"]]})
    set_sy = ctx.add("data_setvariableto", fields={"VARIABLE": ["SPAWN_Y", "v_spawn_y"]}, inputs={"VALUE": [3, rnd_sy, [4, "0"]]})
    bc_spawn = ctx.add("event_broadcast", inputs={"BROADCAST_INPUT": [1, [11, "SPAWN_REQUEST", "b_spawn_req"]]})
    snd_bnd_m = ctx.add("sound_sounds_menu", fields={"SOUND_MENU": ["snd_bond", None]}, shadow=True)
    play_bnd = ctx.add("sound_play", inputs={"SOUND_MENU": [1, snd_bnd_m]})

    ctx.chain([hat_click, set_col, if_row_else, set_sx, set_sy, bc_spawn, play_bnd])

    return {
        "isStage": False,
        "name": "PaletteUI",
        "variables": pal_vars,
        "lists": {},
        "broadcasts": {},
        "blocks": ctx.blocks,
        "comments": {},
        "currentCostume": 0,
        "costumes": [costume_meta["palette_drawer"]],
        "sounds": [sound_meta["snd_bond"]],
        "volume": 100,
        "visible": False,
        "x": 0, "y": -135, "size": 100, "direction": 90,
        "draggable": False, "rotationStyle": "don't rotate"
    }

# Build InfoCardUI sprite
def build_info_card_ui():
    ctx = BlockContext()
    flag_id = ctx.add("event_whenflagclicked", topLevel=True, x=50, y=50)
    hide_info = ctx.add("looks_hide")
    ctx.chain([flag_id, hide_info])

    hat_info = ctx.add("event_whenbroadcastreceived", fields={"BROADCAST_OPTION": ["SHOW_INFO", "b_show_info"]}, topLevel=True, x=50, y=150)
    name_val = ctx.add("data_itemoflist", fields={"LIST": ["DB_NAME", "l_db_name"]}, inputs={"INDEX": [3, [12, "INSPECT_SPECIES_ID", "v_inspect_id"], [7, "1"]]})
    form_val = ctx.add("data_itemoflist", fields={"LIST": ["DB_FORMULA", "l_db_formula"]}, inputs={"INDEX": [3, [12, "INSPECT_SPECIES_ID", "v_inspect_id"], [7, "1"]]})
    type_val = ctx.add("data_itemoflist", fields={"LIST": ["DB_TYPE", "l_db_type"]}, inputs={"INDEX": [3, [12, "INSPECT_SPECIES_ID", "v_inspect_id"], [7, "1"]]})
    atom_val = ctx.add("data_itemoflist", fields={"LIST": ["DB_ATOMS", "l_db_atoms"]}, inputs={"INDEX": [3, [12, "INSPECT_SPECIES_ID", "v_inspect_id"], [7, "1"]]})

    p1 = ctx.add("operator_join", inputs={"STRING1": [3, name_val, [10, ""]], "STRING2": [1, [10, " ["]]})
    p2 = ctx.add("operator_join", inputs={"STRING1": [3, p1, [10, ""]], "STRING2": [3, form_val, [10, ""]]})
    p3 = ctx.add("operator_join", inputs={"STRING1": [3, p2, [10, ""]], "STRING2": [1, [10, "] • "]]})
    p4 = ctx.add("operator_join", inputs={"STRING1": [3, p3, [10, ""]], "STRING2": [3, type_val, [10, ""]]})
    p5 = ctx.add("operator_join", inputs={"STRING1": [3, p4, [10, ""]], "STRING2": [1, [10, " • Atoms: "]]})
    full_info = ctx.add("operator_join", inputs={"STRING1": [3, p5, [10, ""]], "STRING2": [3, atom_val, [10, ""]]})

    say_info = ctx.add("looks_sayforsecs", inputs={"MESSAGE": [3, full_info, [10, ""]], "SECS": [1, [4, "4"]]})
    ctx.chain([hat_info, say_info])

    return {
        "isStage": False,
        "name": "InfoCardUI",
        "variables": {},
        "lists": {},
        "broadcasts": {},
        "blocks": ctx.blocks,
        "comments": {},
        "currentCostume": 0,
        "costumes": [costume_meta["toast_banner"]],
        "sounds": [],
        "volume": 100,
        "visible": False,
        "x": 0, "y": 80, "size": 100, "direction": 90,
        "draggable": False, "rotationStyle": "don't rotate"
    }

# Build CompendiumUI sprite
def build_compendium_ui():
    ctx = BlockContext()
    flag_id = ctx.add("event_whenflagclicked", topLevel=True, x=50, y=50)
    hide_comp = ctx.add("looks_hide")
    ctx.chain([flag_id, hide_comp])

    hat_upd = ctx.add("event_whenbroadcastreceived", fields={"BROADCAST_OPTION": ["UPDATE_UI", "b_update_ui"]}, topLevel=True, x=50, y=150)
    is_show = ctx.add("operator_equals", inputs={"OPERAND1": [3, [12, "SHOW_COMPENDIUM", "v_compendium"], [10, ""]], "OPERAND2": [1, [10, "1"]]})

    p1 = ctx.add("operator_join", inputs={"STRING1": [1, [10, "COMPENDIUM: "]], "STRING2": [3, [12, "TOTAL_DISCOVERED", "v_discovered"], [10, ""]]})
    p2 = ctx.add("operator_join", inputs={"STRING1": [3, p1, [10, ""]], "STRING2": [1, [10, " / 129 Discovered! (Press D to reset)"]]})
    say_comp = ctx.add("looks_sayforsecs", inputs={"MESSAGE": [3, p2, [10, ""]], "SECS": [1, [4, "4"]]})
    say_clear = ctx.add("looks_say", inputs={"MESSAGE": [1, [10, ""]]})

    if_show_comp = ctx.add("control_if_else", inputs={"CONDITION": [2, is_show], "SUBSTACK": [2, say_comp], "SUBSTACK2": [2, say_clear]})
    ctx.blocks[say_comp]["parent"] = if_show_comp
    ctx.blocks[say_clear]["parent"] = if_show_comp

    ctx.chain([hat_upd, if_show_comp])

    # Key D pressed: reset discoveries with confirmation
    hat_key = ctx.add("event_whenkeypressed", fields={"KEY_OPTION": ["d", None]}, topLevel=True, x=50, y=380)
    ask_reset = ctx.add("sensing_askandwait", inputs={"QUESTION": [1, [10, "Type 'RESET' to clear all discovery progress:"]]})
    ans = ctx.add("sensing_answer")
    is_conf = ctx.add("operator_equals", inputs={"OPERAND1": [3, ans, [10, ""]], "OPERAND2": [1, [10, "RESET"]]})

    # Reset: total_discovered = 19, restore first 19 to 1, rest to 0
    rst_tot = ctx.add("data_setvariableto", fields={"VARIABLE": ["TOTAL_DISCOVERED", "v_discovered"]}, inputs={"VALUE": [1, [4, "19"]]})
    bc_upd = ctx.add("event_broadcast", inputs={"BROADCAST_INPUT": [1, [11, "UPDATE_UI", "b_update_ui"]]})
    ctx.chain([rst_tot, bc_upd])

    if_do_reset = ctx.add("control_if", inputs={"CONDITION": [2, is_conf], "SUBSTACK": [2, rst_tot]})
    ctx.blocks[rst_tot]["parent"] = if_do_reset

    ctx.chain([hat_key, ask_reset, if_do_reset])

    return {
        "isStage": False,
        "name": "CompendiumUI",
        "variables": {},
        "lists": {},
        "broadcasts": {},
        "blocks": ctx.blocks,
        "comments": {},
        "currentCostume": 0,
        "costumes": [costume_meta["toast_banner"]],
        "sounds": [],
        "volume": 100,
        "visible": False,
        "x": 0, "y": 0, "size": 100, "direction": 90,
        "draggable": False, "rotationStyle": "don't rotate"
    }

print("All sprite builders defined successfully!")
