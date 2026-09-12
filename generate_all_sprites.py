# generate_all_sprites.py
import sys, json, uuid
import db_chemistry, gen_audio, gen_graphics
from build_full_project import (
    BlockContext, new_id, STAGE_VARS, STAGE_LISTS, BROADCASTS,
    sound_meta, costume_meta
)

# Complete Modular Scratch 3.0 Sprite Architecture
import sys, json, uuid
import db_chemistry, gen_audio, gen_graphics
from build_full_project import (
    BlockContext, new_id, STAGE_VARS, STAGE_LISTS, BROADCASTS,
    sound_meta, costume_meta
)

# 1. Stage Builder
def build_stage():
    ctx = BlockContext()

    # Green flag
    flag_id = ctx.add('event_whenflagclicked', topLevel=True, x=50, y=50)
    s_vol = ctx.add('data_setvariableto', fields={'VARIABLE': ['MASTER_VOLUME', 'v_volume']}, inputs={'VALUE': [1, [4, '100']]})
    s_tool = ctx.add('data_setvariableto', fields={'VARIABLE': ['CURRENT_TOOL', 'v_tool']}, inputs={'VALUE': [1, [10, 'drag']]})
    s_uv = ctx.add('data_setvariableto', fields={'VARIABLE': ['UV_ACTIVE', 'v_uv']}, inputs={'VALUE': [1, [4, '0']]})
    s_frz = ctx.add('data_setvariableto', fields={'VARIABLE': ['TIME_FROZEN', 'v_freeze']}, inputs={'VALUE': [1, [4, '0']]})
    s_pal = ctx.add('data_setvariableto', fields={'VARIABLE': ['SHOW_PALETTE', 'v_palette']}, inputs={'VALUE': [1, [4, '0']]})
    s_comp = ctx.add('data_setvariableto', fields={'VARIABLE': ['SHOW_COMPENDIUM', 'v_compendium']}, inputs={'VALUE': [1, [4, '0']]})
    s_info = ctx.add('data_setvariableto', fields={'VARIABLE': ['SHOW_INFO', 'v_info']}, inputs={'VALUE': [1, [4, '0']]})
    s_onb = ctx.add('data_setvariableto', fields={'VARIABLE': ['SHOW_ONBOARDING', 'v_onboarding']}, inputs={'VALUE': [1, [4, '1']]})
    s_disc = ctx.add('data_setvariableto', fields={'VARIABLE': ['TOTAL_DISCOVERED', 'v_discovered']}, inputs={'VALUE': [1, [4, '19']]})
    s_tab = ctx.add('data_setvariableto', fields={'VARIABLE': ['COMPENDIUM_TAB', 'v_comp_tab']}, inputs={'VALUE': [1, [4, '1']]})

    bc_init_sim = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'INIT_SIMULATION', 'b_init_sim']]})
    bc_upd_bg = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'UPDATE_BACKDROP', 'b_update_bg']]})
    bc_init_ui = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'UPDATE_UI', 'b_update_ui']]})
    bc_onb = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'SHOW_ONBOARDING', 'b_show_onb']]})

    ctx.chain([flag_id, s_vol, s_tool, s_uv, s_frz, s_pal, s_comp, s_info, s_onb, s_disc, s_tab, bc_init_sim, bc_upd_bg, bc_init_ui, bc_onb])

    # Update backdrop on message
    bg_hat = ctx.add('event_whenbroadcastreceived', fields={'BROADCAST_OPTION': ['UPDATE_BACKDROP', 'b_update_bg']}, topLevel=True, x=50, y=420)
    eq_freeze = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'TIME_FROZEN', 'v_freeze'], [10, '']], 'OPERAND2': [1, [10, '1']]})
    bg_frozen_menu = ctx.add('looks_backdrops', fields={'BACKDROP': ['backdrop_frozen', None]}, shadow=True)
    sw_freeze = ctx.add('looks_switchbackdropto', inputs={'BACKDROP': [1, bg_frozen_menu]})

    eq_uv = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'UV_ACTIVE', 'v_uv'], [10, '']], 'OPERAND2': [1, [10, '1']]})
    bg_uv_menu = ctx.add('looks_backdrops', fields={'BACKDROP': ['backdrop_uv', None]}, shadow=True)
    sw_uv = ctx.add('looks_switchbackdropto', inputs={'BACKDROP': [1, bg_uv_menu]})

    bg_vac_menu = ctx.add('looks_backdrops', fields={'BACKDROP': ['backdrop_vacuum', None]}, shadow=True)
    sw_vac = ctx.add('looks_switchbackdropto', inputs={'BACKDROP': [1, bg_vac_menu]})

    if_uv_else = ctx.add('control_if_else', inputs={'CONDITION': [2, eq_uv], 'SUBSTACK': [2, sw_uv], 'SUBSTACK2': [2, sw_vac]})
    ctx.blocks[sw_uv]['parent'] = if_uv_else
    ctx.blocks[sw_vac]['parent'] = if_uv_else

    if_freeze_else = ctx.add('control_if_else', inputs={'CONDITION': [2, eq_freeze], 'SUBSTACK': [2, sw_freeze], 'SUBSTACK2': [2, if_uv_else]})
    ctx.blocks[sw_freeze]['parent'] = if_freeze_else
    ctx.blocks[if_uv_else]['parent'] = if_freeze_else

    ctx.chain([bg_hat, if_freeze_else])

    # Ambient Background Sound Loop (Forever loop respecting MASTER_VOLUME)
    hat_bg = ctx.add('event_whenflagclicked', topLevel=True, x=50, y=650)
    is_vol_pos = ctx.add('operator_gt', inputs={'OPERAND1': [3, [12, 'MASTER_VOLUME', 'v_volume'], [10, '']], 'OPERAND2': [1, [10, '0']]})
    snd_amb_menu = ctx.add('sound_sounds_menu', fields={'SOUND_MENU': ['snd_ambient', None]}, shadow=True)
    play_amb = ctx.add('sound_playuntildone', inputs={'SOUND_MENU': [1, snd_amb_menu]})
    wait_amb = ctx.add('control_wait', inputs={'DURATION': [1, [4, '0.3']]})
    if_amb = ctx.add('control_if_else', inputs={'CONDITION': [2, is_vol_pos], 'SUBSTACK': [2, play_amb], 'SUBSTACK2': [2, wait_amb]})
    ctx.blocks[play_amb]['parent'] = if_amb
    ctx.blocks[wait_amb]['parent'] = if_amb
    loop_amb = ctx.add('control_forever', inputs={'SUBSTACK': [2, if_amb]})
    ctx.blocks[if_amb]['parent'] = loop_amb
    ctx.chain([hat_bg, loop_amb])

    # Keyboard Shortcuts (Stage has 0 clones, guarantees clean single-fire handling)
    # Key 'a': Toggle Palette
    hat_ka = ctx.add('event_whenkeypressed', fields={'KEY_OPTION': ['a', None]}, topLevel=True, x=350, y=50)
    t_pal_k = ctx.add('data_setvariableto', fields={'VARIABLE': ['SHOW_PALETTE', 'v_palette']}, inputs={'VALUE': [3, ctx.add('operator_subtract', inputs={'NUM1': [1, [4, '1']], 'NUM2': [3, [12, 'SHOW_PALETTE', 'v_palette'], [4, '0']]}), [4, '0']]})
    bc_upd_ka = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'UPDATE_UI', 'b_update_ui']]})
    snd_clk_ka = ctx.add('sound_play', inputs={'SOUND_MENU': [1, ctx.add('sound_sounds_menu', fields={'SOUND_MENU': ['snd_click', None]}, shadow=True)]})
    ctx.chain([hat_ka, t_pal_k, bc_upd_ka, snd_clk_ka])

    # Key 'x': Toggle Delete Mode
    hat_kx = ctx.add('event_whenkeypressed', fields={'KEY_OPTION': ['x', None]}, topLevel=True, x=350, y=200)
    is_del_k = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'CURRENT_TOOL', 'v_tool'], [10, '']], 'OPERAND2': [1, [10, 'delete']]})
    set_drag_kx = ctx.add('data_setvariableto', fields={'VARIABLE': ['CURRENT_TOOL', 'v_tool']}, inputs={'VALUE': [1, [10, 'drag']]})
    set_del_kx = ctx.add('data_setvariableto', fields={'VARIABLE': ['CURRENT_TOOL', 'v_tool']}, inputs={'VALUE': [1, [10, 'delete']]})
    if_del_kx = ctx.add('control_if_else', inputs={'CONDITION': [2, is_del_k], 'SUBSTACK': [2, set_drag_kx], 'SUBSTACK2': [2, set_del_kx]})
    ctx.blocks[set_drag_kx]['parent'] = if_del_kx
    ctx.blocks[set_del_kx]['parent'] = if_del_kx
    bc_upd_kx = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'UPDATE_UI', 'b_update_ui']]})
    snd_clk_kx = ctx.add('sound_play', inputs={'SOUND_MENU': [1, ctx.add('sound_sounds_menu', fields={'SOUND_MENU': ['snd_click', None]}, shadow=True)]})
    ctx.chain([hat_kx, if_del_kx, bc_upd_kx, snd_clk_kx])

    # Key 'i': Toggle Inspect Mode
    hat_ki = ctx.add('event_whenkeypressed', fields={'KEY_OPTION': ['i', None]}, topLevel=True, x=350, y=380)
    is_insp_k = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'CURRENT_TOOL', 'v_tool'], [10, '']], 'OPERAND2': [1, [10, 'inspect']]})
    set_drag_ki = ctx.add('data_setvariableto', fields={'VARIABLE': ['CURRENT_TOOL', 'v_tool']}, inputs={'VALUE': [1, [10, 'drag']]})
    set_insp_ki = ctx.add('data_setvariableto', fields={'VARIABLE': ['CURRENT_TOOL', 'v_tool']}, inputs={'VALUE': [1, [10, 'inspect']]})
    if_insp_ki = ctx.add('control_if_else', inputs={'CONDITION': [2, is_insp_k], 'SUBSTACK': [2, set_drag_ki], 'SUBSTACK2': [2, set_insp_ki]})
    ctx.blocks[set_drag_ki]['parent'] = if_insp_ki
    ctx.blocks[set_insp_ki]['parent'] = if_insp_ki
    bc_upd_ki = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'UPDATE_UI', 'b_update_ui']]})
    snd_clk_ki = ctx.add('sound_play', inputs={'SOUND_MENU': [1, ctx.add('sound_sounds_menu', fields={'SOUND_MENU': ['snd_click', None]}, shadow=True)]})
    ctx.chain([hat_ki, if_insp_ki, bc_upd_ki, snd_clk_ki])

    # Key 'u': Toggle UV Light
    hat_ku = ctx.add('event_whenkeypressed', fields={'KEY_OPTION': ['u', None]}, topLevel=True, x=350, y=560)
    t_uv_k = ctx.add('data_setvariableto', fields={'VARIABLE': ['UV_ACTIVE', 'v_uv']}, inputs={'VALUE': [3, ctx.add('operator_subtract', inputs={'NUM1': [1, [4, '1']], 'NUM2': [3, [12, 'UV_ACTIVE', 'v_uv'], [4, '0']]}), [4, '0']]})
    bc_bg_ku = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'UPDATE_BACKDROP', 'b_update_bg']]})
    bc_upd_ku = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'UPDATE_UI', 'b_update_ui']]})
    snd_clk_ku = ctx.add('sound_play', inputs={'SOUND_MENU': [1, ctx.add('sound_sounds_menu', fields={'SOUND_MENU': ['snd_click', None]}, shadow=True)]})
    ctx.chain([hat_ku, t_uv_k, bc_bg_ku, bc_upd_ku, snd_clk_ku])

    # Key 'f': Toggle Cryo Freeze
    hat_kf = ctx.add('event_whenkeypressed', fields={'KEY_OPTION': ['f', None]}, topLevel=True, x=350, y=740)
    t_frz_kf = ctx.add('data_setvariableto', fields={'VARIABLE': ['TIME_FROZEN', 'v_freeze']}, inputs={'VALUE': [3, ctx.add('operator_subtract', inputs={'NUM1': [1, [4, '1']], 'NUM2': [3, [12, 'TIME_FROZEN', 'v_freeze'], [4, '0']]}), [4, '0']]})
    bc_bg_kf = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'UPDATE_BACKDROP', 'b_update_bg']]})
    bc_upd_kf = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'UPDATE_UI', 'b_update_ui']]})
    snd_frz_kf = ctx.add('sound_play', inputs={'SOUND_MENU': [1, ctx.add('sound_sounds_menu', fields={'SOUND_MENU': ['snd_freeze', None]}, shadow=True)]})
    ctx.chain([hat_kf, t_frz_kf, bc_bg_kf, bc_upd_kf, snd_frz_kf])

    # Key 'space': Toggle Cryo Freeze
    hat_ksp = ctx.add('event_whenkeypressed', fields={'KEY_OPTION': ['space', None]}, topLevel=True, x=350, y=920)
    t_frz_ksp = ctx.add('data_setvariableto', fields={'VARIABLE': ['TIME_FROZEN', 'v_freeze']}, inputs={'VALUE': [3, ctx.add('operator_subtract', inputs={'NUM1': [1, [4, '1']], 'NUM2': [3, [12, 'TIME_FROZEN', 'v_freeze'], [4, '0']]}), [4, '0']]})
    bc_bg_ksp = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'UPDATE_BACKDROP', 'b_update_bg']]})
    bc_upd_ksp = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'UPDATE_UI', 'b_update_ui']]})
    snd_frz_ksp = ctx.add('sound_play', inputs={'SOUND_MENU': [1, ctx.add('sound_sounds_menu', fields={'SOUND_MENU': ['snd_freeze', None]}, shadow=True)]})
    ctx.chain([hat_ksp, t_frz_ksp, bc_bg_ksp, bc_upd_ksp, snd_frz_ksp])

    # Key 'c': Toggle Compendium
    hat_kc = ctx.add('event_whenkeypressed', fields={'KEY_OPTION': ['c', None]}, topLevel=True, x=650, y=50)
    t_comp_kc = ctx.add('data_setvariableto', fields={'VARIABLE': ['SHOW_COMPENDIUM', 'v_compendium']}, inputs={'VALUE': [3, ctx.add('operator_subtract', inputs={'NUM1': [1, [4, '1']], 'NUM2': [3, [12, 'SHOW_COMPENDIUM', 'v_compendium'], [4, '0']]}), [4, '0']]})
    bc_upd_kc = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'UPDATE_UI', 'b_update_ui']]})
    snd_clk_kc = ctx.add('sound_play', inputs={'SOUND_MENU': [1, ctx.add('sound_sounds_menu', fields={'SOUND_MENU': ['snd_click', None]}, shadow=True)]})
    ctx.chain([hat_kc, t_comp_kc, bc_upd_kc, snd_clk_kc])

    # Key 'm': Toggle Master Audio
    hat_km = ctx.add('event_whenkeypressed', fields={'KEY_OPTION': ['m', None]}, topLevel=True, x=650, y=200)
    t_vol_km = ctx.add('data_setvariableto', fields={'VARIABLE': ['MASTER_VOLUME', 'v_volume']}, inputs={'VALUE': [3, ctx.add('operator_subtract', inputs={'NUM1': [1, [4, '100']], 'NUM2': [3, [12, 'MASTER_VOLUME', 'v_volume'], [4, '0']]}), [4, '0']]})
    bc_upd_km = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'UPDATE_UI', 'b_update_ui']]})
    snd_clk_km = ctx.add('sound_play', inputs={'SOUND_MENU': [1, ctx.add('sound_sounds_menu', fields={'SOUND_MENU': ['snd_click', None]}, shadow=True)]})
    ctx.chain([hat_km, t_vol_km, bc_upd_km, snd_clk_km])

    # Key 's': Prompt Save / Load
    hat_ks = ctx.add('event_whenkeypressed', fields={'KEY_OPTION': ['s', None]}, topLevel=True, x=650, y=380)
    bc_save_ks = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'PROMPT_SAVE_LOAD', 'b_prompt_save']]})
    ctx.chain([hat_ks, bc_save_ks])

    # Key 'h': Toggle Onboarding Help
    hat_kh = ctx.add('event_whenkeypressed', fields={'KEY_OPTION': ['h', None]}, topLevel=True, x=650, y=500)
    t_onb_kh = ctx.add('data_setvariableto', fields={'VARIABLE': ['SHOW_ONBOARDING', 'v_onboarding']}, inputs={'VALUE': [3, ctx.add('operator_subtract', inputs={'NUM1': [1, [4, '1']], 'NUM2': [3, [12, 'SHOW_ONBOARDING', 'v_onboarding'], [4, '0']]}), [4, '0']]})
    bc_onb_kh = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'SHOW_ONBOARDING', 'b_show_onb']]})
    snd_clk_kh = ctx.add('sound_play', inputs={'SOUND_MENU': [1, ctx.add('sound_sounds_menu', fields={'SOUND_MENU': ['snd_click', None]}, shadow=True)]})
    ctx.chain([hat_kh, t_onb_kh, bc_onb_kh, snd_clk_kh])

    # Key 'p': Purge Chamber
    hat_kp = ctx.add('event_whenkeypressed', fields={'KEY_OPTION': ['p', None]}, topLevel=True, x=650, y=650)
    bc_clear_kp = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'CLEAR_ALL', 'b_clear_all']]})
    snd_del_kp = ctx.add('sound_play', inputs={'SOUND_MENU': [1, ctx.add('sound_sounds_menu', fields={'SOUND_MENU': ['snd_delete', None]}, shadow=True)]})
    ctx.chain([hat_kp, bc_clear_kp, snd_del_kp])

    # Key 'd': Discovery Reset confirmation (Protected from accidental deletion)
    hat_kd = ctx.add('event_whenkeypressed', fields={'KEY_OPTION': ['d', None]}, topLevel=True, x=650, y=800)
    ask_rst = ctx.add('sensing_askandwait', inputs={'QUESTION': [1, [10, 'Type "RESET" to reset discovery catalog to base 19 elements:']]})
    is_rst = ctx.add('operator_equals', inputs={'OPERAND1': [3, ctx.add('sensing_answer'), [10, '']], 'OPERAND2': [1, [10, 'RESET']]})
    set_tot_19 = ctx.add('data_setvariableto', fields={'VARIABLE': ['TOTAL_DISCOVERED', 'v_discovered']}, inputs={'VALUE': [1, [4, '19']]})
    set_k20 = ctx.add('data_setvariableto', fields={'VARIABLE': ['SPAWN_SPECIES_ID', 'v_spawn_id']}, inputs={'VALUE': [1, [4, '20']]})
    rep_rst_item = ctx.add('data_replaceitemoflist', fields={'LIST': ['DB_DISCOVERED', 'l_db_disc']}, inputs={'INDEX': [3, [12, 'SPAWN_SPECIES_ID', 'v_spawn_id'], [7, '20']], 'ITEM': [1, [4, '0']]})
    inc_rst_k = ctx.add('data_changevariableby', fields={'VARIABLE': ['SPAWN_SPECIES_ID', 'v_spawn_id']}, inputs={'VALUE': [1, [4, '1']]})
    ctx.chain([rep_rst_item, inc_rst_k])
    rep_110 = ctx.add('control_repeat', inputs={'TIMES': [1, [6, '110']], 'SUBSTACK': [2, rep_rst_item]})
    ctx.blocks[rep_rst_item]['parent'] = rep_110
    rst_spc_id = ctx.add('data_setvariableto', fields={'VARIABLE': ['SPAWN_SPECIES_ID', 'v_spawn_id']}, inputs={'VALUE': [1, [4, '1']]})
    bc_rst_ui = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'UPDATE_UI', 'b_update_ui']]})
    snd_rst_m = ctx.add('sound_sounds_menu', fields={'SOUND_MENU': ['snd_delete', None]}, shadow=True)
    play_rst_snd = ctx.add('sound_play', inputs={'SOUND_MENU': [1, snd_rst_m]})
    ctx.chain([set_tot_19, set_k20, rep_110, rst_spc_id, bc_rst_ui, play_rst_snd])
    if_rst_conf = ctx.add('control_if', inputs={'CONDITION': [2, is_rst], 'SUBSTACK': [2, set_tot_19]})
    ctx.blocks[set_tot_19]['parent'] = if_rst_conf
    ctx.chain([hat_kd, ask_rst, if_rst_conf])

    stage_sounds = [
        sound_meta['snd_click'],
        sound_meta['snd_bond'],
        sound_meta['snd_exothermic'],
        sound_meta['snd_photon'],
        sound_meta['snd_cosmic'],
        sound_meta['snd_delete'],
        sound_meta['snd_freeze'],
        sound_meta['snd_discover'],
        sound_meta['snd_ambient']
    ]

    return {
        'isStage': True,
        'name': 'Stage',
        'variables': STAGE_VARS,
        'lists': STAGE_LISTS,
        'broadcasts': BROADCASTS,
        'blocks': ctx.blocks,
        'comments': {},
        'currentCostume': 0,
        'costumes': [
            costume_meta['backdrop_vacuum'],
            costume_meta['backdrop_uv'],
            costume_meta['backdrop_frozen']
        ],
        'sounds': stage_sounds,
        'volume': 100,
        'layerOrder': 0,
        'tempo': 60,
        'videoTransparency': 50,
        'videoState': 'on',
        'textToSpeechLanguage': None
    }

# 2. SimulationEngine Builder
def build_simulation_engine():
    ctx = BlockContext()

    def_spawn_init = ctx.add('procedures_definition', topLevel=True, x=400, y=50)
    proto_spawn_init = ctx.add('procedures_prototype', parent_id=def_spawn_init, shadow=True, mutation={
        'tagName': 'mutation', 'children': [], 'proccode': 'SpawnInitialAtoms',
        'argumentids': '[]', 'argumentnames': '[]', 'argumentdefaults': '[]', 'warp': 'true'
    })
    ctx.blocks[def_spawn_init]['inputs']['custom_block'] = [1, proto_spawn_init]

    del_act = ctx.add('data_deletealloflist', fields={'LIST': ['ENTITY_ACTIVE', 'l_ent_act']})
    del_spc = ctx.add('data_deletealloflist', fields={'LIST': ['ENTITY_SPECIES', 'l_ent_spc']})
    del_x = ctx.add('data_deletealloflist', fields={'LIST': ['ENTITY_X', 'l_ent_x']})
    del_y = ctx.add('data_deletealloflist', fields={'LIST': ['ENTITY_Y', 'l_ent_y']})
    del_vx = ctx.add('data_deletealloflist', fields={'LIST': ['ENTITY_VX', 'l_ent_vx']})
    del_vy = ctx.add('data_deletealloflist', fields={'LIST': ['ENTITY_VY', 'l_ent_vy']})
    set_nid1 = ctx.add('data_setvariableto', fields={'VARIABLE': ['NEXT_ENTITY_ID', 'v_next_id']}, inputs={'VALUE': [1, [4, '1']]})

    init_atoms = [
        (1, -60, 20, 0.4, -0.2),
        (1, -40, -40, -0.3, 0.3),
        (7, 40, 10, 0.2, 0.3),
        (10, 120, -30, -0.2, -0.2),
        (14, 150, 40, 0.3, 0.1)
    ]
    spawn_cmds = []
    for spc, x, y, vx, vy in init_atoms:
        a_act = ctx.add('data_addtolist', fields={'LIST': ['ENTITY_ACTIVE', 'l_ent_act']}, inputs={'ITEM': [1, [4, '1']]})
        a_spc = ctx.add('data_addtolist', fields={'LIST': ['ENTITY_SPECIES', 'l_ent_spc']}, inputs={'ITEM': [1, [4, str(spc)]]})
        a_x = ctx.add('data_addtolist', fields={'LIST': ['ENTITY_X', 'l_ent_x']}, inputs={'ITEM': [1, [4, str(x)]]})
        a_y = ctx.add('data_addtolist', fields={'LIST': ['ENTITY_Y', 'l_ent_y']}, inputs={'ITEM': [1, [4, str(y)]]})
        a_vx = ctx.add('data_addtolist', fields={'LIST': ['ENTITY_VX', 'l_ent_vx']}, inputs={'ITEM': [1, [4, str(vx)]]})
        a_vy = ctx.add('data_addtolist', fields={'LIST': ['ENTITY_VY', 'l_ent_vy']}, inputs={'ITEM': [1, [4, str(vy)]]})
        cl_menu = ctx.add('control_create_clone_of_menu', fields={'CLONE_OPTION': ['Entity', None]}, shadow=True)
        cr_clone = ctx.add('control_create_clone_of', inputs={'CLONE_OPTION': [1, cl_menu]})
        spawn_cmds.extend([a_act, a_spc, a_x, a_y, a_vx, a_vy, cr_clone])

    ctx.chain([def_spawn_init, del_act, del_spc, del_x, del_y, del_vx, del_vy, set_nid1] + spawn_cmds)

    hat_sim = ctx.add('event_whenbroadcastreceived', fields={'BROADCAST_OPTION': ['INIT_SIMULATION', 'b_init_sim']}, topLevel=True, x=50, y=50)
    call_spawn_init = ctx.add('procedures_call', mutation={
        'tagName': 'mutation', 'children': [], 'proccode': 'SpawnInitialAtoms',
        'argumentids': '[]', 'warp': 'true'
    })
    ctx.chain([hat_sim, call_spawn_init])

    hat_spawn = ctx.add('event_whenbroadcastreceived', fields={'BROADCAST_OPTION': ['SPAWN_REQUEST', 'b_spawn_req']}, topLevel=True, x=50, y=200)
    sp_act = ctx.add('data_addtolist', fields={'LIST': ['ENTITY_ACTIVE', 'l_ent_act']}, inputs={'ITEM': [1, [4, '1']]})
    sp_spc = ctx.add('data_addtolist', fields={'LIST': ['ENTITY_SPECIES', 'l_ent_spc']}, inputs={'ITEM': [3, [12, 'SPAWN_SPECIES_ID', 'v_spawn_id'], [4, '1']]})
    sp_x = ctx.add('data_addtolist', fields={'LIST': ['ENTITY_X', 'l_ent_x']}, inputs={'ITEM': [3, [12, 'SPAWN_X', 'v_spawn_x'], [4, '0']]})
    sp_y = ctx.add('data_addtolist', fields={'LIST': ['ENTITY_Y', 'l_ent_y']}, inputs={'ITEM': [3, [12, 'SPAWN_Y', 'v_spawn_y'], [4, '0']]})
    rnd_vx = ctx.add('operator_random', inputs={'FROM': [1, [4, '-0.7']], 'TO': [1, [4, '0.7']]})
    sp_vx = ctx.add('data_addtolist', fields={'LIST': ['ENTITY_VX', 'l_ent_vx']}, inputs={'ITEM': [3, rnd_vx, [4, '0']]})
    rnd_vy = ctx.add('operator_random', inputs={'FROM': [1, [4, '-0.7']], 'TO': [1, [4, '0.7']]})
    sp_vy = ctx.add('data_addtolist', fields={'LIST': ['ENTITY_VY', 'l_ent_vy']}, inputs={'ITEM': [3, rnd_vy, [4, '0']]})
    sp_cl_menu = ctx.add('control_create_clone_of_menu', fields={'CLONE_OPTION': ['Entity', None]}, shadow=True)
    sp_cr_clone = ctx.add('control_create_clone_of', inputs={'CLONE_OPTION': [1, sp_cl_menu]})
    ctx.chain([hat_spawn, sp_act, sp_spc, sp_x, sp_y, sp_vx, sp_vy, sp_cr_clone])

    hat_clear = ctx.add('event_whenbroadcastreceived', fields={'BROADCAST_OPTION': ['CLEAR_ALL', 'b_clear_all']}, topLevel=True, x=50, y=450)
    cl_act = ctx.add('data_deletealloflist', fields={'LIST': ['ENTITY_ACTIVE', 'l_ent_act']})
    cl_spc = ctx.add('data_deletealloflist', fields={'LIST': ['ENTITY_SPECIES', 'l_ent_spc']})
    cl_x = ctx.add('data_deletealloflist', fields={'LIST': ['ENTITY_X', 'l_ent_x']})
    cl_y = ctx.add('data_deletealloflist', fields={'LIST': ['ENTITY_Y', 'l_ent_y']})
    cl_vx = ctx.add('data_deletealloflist', fields={'LIST': ['ENTITY_VX', 'l_ent_vx']})
    cl_vy = ctx.add('data_deletealloflist', fields={'LIST': ['ENTITY_VY', 'l_ent_vy']})
    cl_nid = ctx.add('data_setvariableto', fields={'VARIABLE': ['NEXT_ENTITY_ID', 'v_next_id']}, inputs={'VALUE': [1, [4, '1']]})
    ctx.chain([hat_clear, cl_act, cl_spc, cl_x, cl_y, cl_vx, cl_vy, cl_nid])

    hat_save = ctx.add('event_whenbroadcastreceived', fields={'BROADCAST_OPTION': ['PROMPT_SAVE_LOAD', 'b_prompt_save']}, topLevel=True, x=50, y=650)
    ask_choice = ctx.add('sensing_askandwait', inputs={'QUESTION': [1, [10, 'Enter "save" to export progress code, or "load" to restore:']]})
    ans = ctx.add('sensing_answer')

    is_save = ctx.add('operator_equals', inputs={'OPERAND1': [3, ans, [10, '']], 'OPERAND2': [1, [10, 'save']]})
    # Save logic
    set_sc_init = ctx.add('data_setvariableto', fields={'VARIABLE': ['SAVE_CODE', 'v_save_code']}, inputs={'VALUE': [1, [10, 'CHEM:_']]})
    set_sk20 = ctx.add('data_setvariableto', fields={'VARIABLE': ['SPAWN_SPECIES_ID', 'v_spawn_id']}, inputs={'VALUE': [1, [4, '20']]})
    disc_item = ctx.add('data_itemoflist', fields={'LIST': ['DB_DISCOVERED', 'l_db_disc']}, inputs={'INDEX': [3, [12, 'SPAWN_SPECIES_ID', 'v_spawn_id'], [7, '20']]})
    is_disc_1 = ctx.add('operator_equals', inputs={'OPERAND1': [3, disc_item, [10, '']], 'OPERAND2': [1, [10, '1']]})
    join_id = ctx.add('operator_join', inputs={'STRING1': [3, [12, 'SPAWN_SPECIES_ID', 'v_spawn_id'], [10, '']], 'STRING2': [1, [10, '_']]})
    append_sc = ctx.add('data_setvariableto', fields={'VARIABLE': ['SAVE_CODE', 'v_save_code']}, inputs={'VALUE': [3, ctx.add('operator_join', inputs={'STRING1': [3, [12, 'SAVE_CODE', 'v_save_code'], [10, '']], 'STRING2': [3, join_id, [10, '']]}), [10, '']]})
    if_disc_append = ctx.add('control_if', inputs={'CONDITION': [2, is_disc_1], 'SUBSTACK': [2, append_sc]})
    ctx.blocks[append_sc]['parent'] = if_disc_append
    inc_sk = ctx.add('data_changevariableby', fields={'VARIABLE': ['SPAWN_SPECIES_ID', 'v_spawn_id']}, inputs={'VALUE': [1, [4, '1']]})
    ctx.chain([if_disc_append, inc_sk])
    rep_save = ctx.add('control_repeat', inputs={'TIMES': [1, [6, '110']], 'SUBSTACK': [2, if_disc_append]})
    ctx.blocks[if_disc_append]['parent'] = rep_save
    rst_spc_s = ctx.add('data_setvariableto', fields={'VARIABLE': ['SPAWN_SPECIES_ID', 'v_spawn_id']}, inputs={'VALUE': [1, [4, '1']]})
    prompt_show_sc = ctx.add('sensing_askandwait', inputs={'QUESTION': [3, ctx.add('operator_join', inputs={'STRING1': [1, [10, 'Save Code (Ctrl+C to copy): ']], 'STRING2': [3, [12, 'SAVE_CODE', 'v_save_code'], [10, '']]}), [10, '']]})
    ctx.chain([set_sc_init, set_sk20, rep_save, rst_spc_s, prompt_show_sc])

    # Load logic
    is_load = ctx.add('operator_equals', inputs={'OPERAND1': [3, ans, [10, '']], 'OPERAND2': [1, [10, 'load']]})
    ask_paste = ctx.add('sensing_askandwait', inputs={'QUESTION': [1, [10, 'Paste your Save Code (CHEM:_...) to restore:']]})
    ans_load = ctx.add('sensing_answer')
    code_valid = ctx.add('operator_contains', inputs={'STRING1': [3, ans_load, [10, '']], 'STRING2': [1, [10, 'CHEM:']]})

    set_tot_19_l = ctx.add('data_setvariableto', fields={'VARIABLE': ['TOTAL_DISCOVERED', 'v_discovered']}, inputs={'VALUE': [1, [4, '19']]})
    set_lk20 = ctx.add('data_setvariableto', fields={'VARIABLE': ['SPAWN_SPECIES_ID', 'v_spawn_id']}, inputs={'VALUE': [1, [4, '20']]})

    pat_mid = ctx.add('operator_join', inputs={'STRING1': [3, [12, 'SPAWN_SPECIES_ID', 'v_spawn_id'], [10, '']], 'STRING2': [1, [10, '_']]})
    pat_str = ctx.add('operator_join', inputs={'STRING1': [1, [10, '_']], 'STRING2': [3, pat_mid, [10, '']]})
    has_pat = ctx.add('operator_contains', inputs={'STRING1': [3, ans_load, [10, '']], 'STRING2': [3, pat_str, [10, '']]})

    set_disc_1 = ctx.add('data_replaceitemoflist', fields={'LIST': ['DB_DISCOVERED', 'l_db_disc']}, inputs={'INDEX': [3, [12, 'SPAWN_SPECIES_ID', 'v_spawn_id'], [7, '20']], 'ITEM': [1, [4, '1']]})
    inc_tot = ctx.add('data_changevariableby', fields={'VARIABLE': ['TOTAL_DISCOVERED', 'v_discovered']}, inputs={'VALUE': [1, [4, '1']]})
    ctx.chain([set_disc_1, inc_tot])

    set_disc_0 = ctx.add('data_replaceitemoflist', fields={'LIST': ['DB_DISCOVERED', 'l_db_disc']}, inputs={'INDEX': [3, [12, 'SPAWN_SPECIES_ID', 'v_spawn_id'], [7, '20']], 'ITEM': [1, [4, '0']]})

    if_has_pat = ctx.add('control_if_else', inputs={'CONDITION': [2, has_pat], 'SUBSTACK': [2, set_disc_1], 'SUBSTACK2': [2, set_disc_0]})
    ctx.blocks[set_disc_1]['parent'] = if_has_pat
    ctx.blocks[set_disc_0]['parent'] = if_has_pat

    inc_lk = ctx.add('data_changevariableby', fields={'VARIABLE': ['SPAWN_SPECIES_ID', 'v_spawn_id']}, inputs={'VALUE': [1, [4, '1']]})
    ctx.chain([if_has_pat, inc_lk])
    rep_load = ctx.add('control_repeat', inputs={'TIMES': [1, [6, '110']], 'SUBSTACK': [2, if_has_pat]})
    ctx.blocks[if_has_pat]['parent'] = rep_load
    rst_spc_l = ctx.add('data_setvariableto', fields={'VARIABLE': ['SPAWN_SPECIES_ID', 'v_spawn_id']}, inputs={'VALUE': [1, [4, '1']]})
    bc_load_ui = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'UPDATE_UI', 'b_update_ui']]})
    snd_disc_m = ctx.add('sound_sounds_menu', fields={'SOUND_MENU': ['snd_discover', None]}, shadow=True)
    play_load_snd = ctx.add('sound_play', inputs={'SOUND_MENU': [1, snd_disc_m]})
    say_load_ok = ctx.add('looks_sayforsecs', inputs={'MESSAGE': [1, [10, 'Discoveries successfully restored!']], 'SECS': [1, [4, '2']]})
    ctx.chain([set_tot_19_l, set_lk20, rep_load, rst_spc_l, bc_load_ui, play_load_snd, say_load_ok])

    say_invalid = ctx.add('looks_sayforsecs', inputs={'MESSAGE': [1, [10, 'Invalid Save Code! Must contain CHEM:']], 'SECS': [1, [4, '2']]})
    if_code_valid = ctx.add('control_if_else', inputs={'CONDITION': [2, code_valid], 'SUBSTACK': [2, set_tot_19_l], 'SUBSTACK2': [2, say_invalid]})
    ctx.blocks[set_tot_19_l]['parent'] = if_code_valid
    ctx.blocks[say_invalid]['parent'] = if_code_valid
    ctx.chain([ask_paste, if_code_valid])

    if_load = ctx.add('control_if', inputs={'CONDITION': [2, is_load], 'SUBSTACK': [2, ask_paste]})
    ctx.blocks[ask_paste]['parent'] = if_load

    if_save_else = ctx.add('control_if_else', inputs={'CONDITION': [2, is_save], 'SUBSTACK': [2, set_sc_init], 'SUBSTACK2': [2, if_load]})
    ctx.blocks[set_sc_init]['parent'] = if_save_else
    ctx.blocks[if_load]['parent'] = if_save_else

    ctx.chain([hat_save, ask_choice, if_save_else])

    return {
        'isStage': False,
        'name': 'SimulationEngine',
        'variables': {},
        'lists': {},
        'broadcasts': {},
        'blocks': ctx.blocks,
        'comments': {},
        'currentCostume': 0,
        'costumes': [costume_meta['toast_banner']],
        'sounds': [sound_meta['snd_discover']],
        'volume': 100,
        'visible': False,
        'x': 0, 'y': 0, 'size': 100, 'direction': 90,
        'draggable': False, 'rotationStyle': "don't rotate"
    }

# 3. Entity Sprite Builder
def build_entity():
    ctx = BlockContext()

    entity_vars = {
        'v_local_id': ['my_id', 0],
        'v_local_spc': ['my_species', 1],
        'v_local_vx': ['my_vx', 0],
        'v_local_vy': ['my_vy', 0],
        'v_local_drag': ['is_dragging', 0],
        'v_local_k': ['loop_k', 1],
        'v_local_dx': ['loop_dx', 0],
        'v_local_dy': ['loop_dy', 0],
        'v_local_dsq': ['loop_dsq', 0],
        'v_local_rx_key': ['temp_rx_key', ''],
        'v_local_rx_idx': ['temp_rx_idx', 0],
        'v_local_prod': ['temp_prod', 0]
    }

    entity_costumes = [costume_meta[f'species_{s["id"]}'] for s in db_chemistry.SPECIES]
    entity_sounds = [
        sound_meta['snd_bond'],
        sound_meta['snd_exothermic'],
        sound_meta['snd_delete'],
        sound_meta['snd_discover']
    ]

    flag_id = ctx.add('event_whenflagclicked', topLevel=True, x=50, y=50)
    hide_orig = ctx.add('looks_hide')
    set_orig_id = ctx.add('data_setvariableto', fields={'VARIABLE': ['my_id', 'v_local_id']}, inputs={'VALUE': [1, [4, '0']]})
    ctx.chain([flag_id, hide_orig, set_orig_id])

    hat_clear = ctx.add('event_whenbroadcastreceived', fields={'BROADCAST_OPTION': ['CLEAR_ALL', 'b_clear_all']}, topLevel=True, x=50, y=170)
    gt_zero = ctx.add('operator_gt', inputs={'OPERAND1': [3, [12, 'my_id', 'v_local_id'], [10, '']], 'OPERAND2': [1, [10, '0']]})
    del_clone_cl = ctx.add('control_delete_this_clone')
    if_gt_zero = ctx.add('control_if', inputs={'CONDITION': [2, gt_zero], 'SUBSTACK': [2, del_clone_cl]})
    ctx.blocks[del_clone_cl]['parent'] = if_gt_zero
    ctx.chain([hat_clear, if_gt_zero])

    # Procedure: ResolveInteractions (warp: true)
    def_resolve = ctx.add('procedures_definition', topLevel=True, x=450, y=50)
    proto_resolve = ctx.add('procedures_prototype', parent_id=def_resolve, shadow=True, mutation={
        'tagName': 'mutation', 'children': [], 'proccode': 'ResolveInteractions',
        'argumentids': '[]', 'argumentnames': '[]', 'argumentdefaults': '[]', 'warp': 'true'
    })
    ctx.blocks[def_resolve]['inputs']['custom_block'] = [1, proto_resolve]

    set_k1 = ctx.add('data_setvariableto', fields={'VARIABLE': ['loop_k', 'v_local_k']}, inputs={'VALUE': [1, [4, '1']]})

    not_self = ctx.add('operator_not', inputs={'OPERAND': [2, ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'loop_k', 'v_local_k'], [10, '']], 'OPERAND2': [3, [12, 'my_id', 'v_local_id'], [10, '']]})]})
    target_act = ctx.add('data_itemoflist', fields={'LIST': ['ENTITY_ACTIVE', 'l_ent_act']}, inputs={'INDEX': [3, [12, 'loop_k', 'v_local_k'], [7, '1']]})
    is_act = ctx.add('operator_equals', inputs={'OPERAND1': [3, target_act, [10, '']], 'OPERAND2': [1, [10, '1']]})
    both_cond = ctx.add('operator_and', inputs={'OPERAND1': [2, not_self], 'OPERAND2': [2, is_act]})

    tgt_x = ctx.add('data_itemoflist', fields={'LIST': ['ENTITY_X', 'l_ent_x']}, inputs={'INDEX': [3, [12, 'loop_k', 'v_local_k'], [7, '1']]})
    my_x = ctx.add('motion_xposition')
    dx_val = ctx.add('operator_subtract', inputs={'NUM1': [3, tgt_x, [4, '0']], 'NUM2': [3, my_x, [4, '0']]})
    set_dx = ctx.add('data_setvariableto', fields={'VARIABLE': ['loop_dx', 'v_local_dx']}, inputs={'VALUE': [3, dx_val, [4, '0']]})

    tgt_y = ctx.add('data_itemoflist', fields={'LIST': ['ENTITY_Y', 'l_ent_y']}, inputs={'INDEX': [3, [12, 'loop_k', 'v_local_k'], [7, '1']]})
    my_y = ctx.add('motion_yposition')
    dy_val = ctx.add('operator_subtract', inputs={'NUM1': [3, tgt_y, [4, '0']], 'NUM2': [3, my_y, [4, '0']]})
    set_dy = ctx.add('data_setvariableto', fields={'VARIABLE': ['loop_dy', 'v_local_dy']}, inputs={'VALUE': [3, dy_val, [4, '0']]})

    dx_sq = ctx.add('operator_multiply', inputs={'NUM1': [3, [12, 'loop_dx', 'v_local_dx'], [4, '0']], 'NUM2': [3, [12, 'loop_dx', 'v_local_dx'], [4, '0']]})
    dy_sq = ctx.add('operator_multiply', inputs={'NUM1': [3, [12, 'loop_dy', 'v_local_dy'], [4, '0']], 'NUM2': [3, [12, 'loop_dy', 'v_local_dy'], [4, '0']]})
    dsq_val = ctx.add('operator_add', inputs={'NUM1': [3, dx_sq, [4, '0']], 'NUM2': [3, dy_sq, [4, '0']]})
    set_dsq = ctx.add('data_setvariableto', fields={'VARIABLE': ['loop_dsq', 'v_local_dsq']}, inputs={'VALUE': [3, dsq_val, [4, '0']]})

    close_enough = ctx.add('operator_lt', inputs={'OPERAND1': [3, [12, 'loop_dsq', 'v_local_dsq'], [10, '']], 'OPERAND2': [1, [10, '1764']]})

    partner_spc = ctx.add('data_itemoflist', fields={'LIST': ['ENTITY_SPECIES', 'l_ent_spc']}, inputs={'INDEX': [3, [12, 'loop_k', 'v_local_k'], [7, '1']]})
    spc_lt = ctx.add('operator_lt', inputs={'OPERAND1': [3, [12, 'my_species', 'v_local_spc'], [10, '']], 'OPERAND2': [3, partner_spc, [10, '']]})

    key_part1 = ctx.add('operator_join', inputs={'STRING1': [3, [12, 'my_species', 'v_local_spc'], [10, '']], 'STRING2': [1, [10, '_']]})
    key_a = ctx.add('operator_join', inputs={'STRING1': [3, key_part1, [10, '']], 'STRING2': [3, partner_spc, [10, '']]})
    set_key_a = ctx.add('data_setvariableto', fields={'VARIABLE': ['temp_rx_key', 'v_local_rx_key']}, inputs={'VALUE': [3, key_a, [10, '']]})

    key_part2 = ctx.add('operator_join', inputs={'STRING1': [3, partner_spc, [10, '']], 'STRING2': [1, [10, '_']]})
    key_b = ctx.add('operator_join', inputs={'STRING1': [3, key_part2, [10, '']], 'STRING2': [3, [12, 'my_species', 'v_local_spc'], [10, '']]})
    set_key_b = ctx.add('data_setvariableto', fields={'VARIABLE': ['temp_rx_key', 'v_local_rx_key']}, inputs={'VALUE': [3, key_b, [10, '']]})

    if_spc_order = ctx.add('control_if_else', inputs={'CONDITION': [2, spc_lt], 'SUBSTACK': [2, set_key_a], 'SUBSTACK2': [2, set_key_b]})
    ctx.blocks[set_key_a]['parent'] = if_spc_order
    ctx.blocks[set_key_b]['parent'] = if_spc_order

    item_num_rx = ctx.add('data_itemnumoflist', fields={'LIST': ['RX_KEY', 'l_rx_key']}, inputs={'ITEM': [3, [12, 'temp_rx_key', 'v_local_rx_key'], [10, '']]})
    set_rx_idx = ctx.add('data_setvariableto', fields={'VARIABLE': ['temp_rx_idx', 'v_local_rx_idx']}, inputs={'VALUE': [3, item_num_rx, [4, '0']]})

    has_rx = ctx.add('operator_gt', inputs={'OPERAND1': [3, [12, 'temp_rx_idx', 'v_local_rx_idx'], [10, '']], 'OPERAND2': [1, [10, '0']]})

    rx_uv_val = ctx.add('data_itemoflist', fields={'LIST': ['RX_UV', 'l_rx_uv']}, inputs={'INDEX': [3, [12, 'temp_rx_idx', 'v_local_rx_idx'], [7, '1']]})
    needs_uv = ctx.add('operator_equals', inputs={'OPERAND1': [3, rx_uv_val, [10, '']], 'OPERAND2': [1, [10, '1']]})
    uv_off = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'UV_ACTIVE', 'v_uv'], [10, '']], 'OPERAND2': [1, [10, '0']]})
    uv_blocked = ctx.add('operator_and', inputs={'OPERAND1': [2, needs_uv], 'OPERAND2': [2, uv_off]})
    say_uv = ctx.add('looks_sayforsecs', inputs={'MESSAGE': [1, [10, '⚡ Requires UV Light!']], 'SECS': [1, [4, '1.2']]})

    deact_partner = ctx.add('data_replaceitemoflist', fields={'LIST': ['ENTITY_ACTIVE', 'l_ent_act']}, inputs={'INDEX': [3, [12, 'loop_k', 'v_local_k'], [7, '1']], 'ITEM': [1, [4, '0']]})
    get_prod = ctx.add('data_itemoflist', fields={'LIST': ['RX_PROD', 'l_rx_prod']}, inputs={'INDEX': [3, [12, 'temp_rx_idx', 'v_local_rx_idx'], [7, '1']]})
    set_prod = ctx.add('data_setvariableto', fields={'VARIABLE': ['temp_prod', 'v_local_prod']}, inputs={'VALUE': [3, get_prod, [4, '1']]})

    set_my_spc = ctx.add('data_setvariableto', fields={'VARIABLE': ['my_species', 'v_local_spc']}, inputs={'VALUE': [3, [12, 'temp_prod', 'v_local_prod'], [4, '1']]})
    upd_list_spc = ctx.add('data_replaceitemoflist', fields={'LIST': ['ENTITY_SPECIES', 'l_ent_spc']}, inputs={'INDEX': [3, [12, 'my_id', 'v_local_id'], [7, '1']], 'ITEM': [3, [12, 'temp_prod', 'v_local_prod'], [4, '1']]})
    sw_costume = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [3, ctx.add('operator_join', inputs={'STRING1': [1, [10, 'species_']], 'STRING2': [3, [12, 'temp_prod', 'v_local_prod'], [10, '']]}), [10, 'species_1']]})

    set_fx_x = ctx.add('data_setvariableto', fields={'VARIABLE': ['FX_X', 'v_fx_x']}, inputs={'VALUE': [3, ctx.add('motion_xposition'), [4, '0']]})
    set_fx_y = ctx.add('data_setvariableto', fields={'VARIABLE': ['FX_Y', 'v_fx_y']}, inputs={'VALUE': [3, ctx.add('motion_yposition'), [4, '0']]})

    rx_exo_val = ctx.add('data_itemoflist', fields={'LIST': ['RX_EXO', 'l_rx_exo']}, inputs={'INDEX': [3, [12, 'temp_rx_idx', 'v_local_rx_idx'], [7, '1']]})
    is_exo = ctx.add('operator_equals', inputs={'OPERAND1': [3, rx_exo_val, [10, '']], 'OPERAND2': [1, [10, '1']]})
    bc_fx_exo = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'PLAY_FX_EXO', 'b_fx_exo']]})
    bc_sp_phot = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'SPAWN_PHOTON', 'b_spawn_photon']]})
    snd_exo_m = ctx.add('sound_sounds_menu', fields={'SOUND_MENU': ['snd_exothermic', None]}, shadow=True)
    play_exo = ctx.add('sound_play', inputs={'SOUND_MENU': [1, snd_exo_m]})
    ctx.chain([bc_fx_exo, bc_sp_phot, play_exo])

    bc_fx_bond = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'PLAY_FX_BOND', 'b_fx_bond']]})
    snd_bnd_m = ctx.add('sound_sounds_menu', fields={'SOUND_MENU': ['snd_bond', None]}, shadow=True)
    play_bnd = ctx.add('sound_play', inputs={'SOUND_MENU': [1, snd_bnd_m]})
    ctx.chain([bc_fx_bond, play_bnd])

    if_exo_else = ctx.add('control_if_else', inputs={'CONDITION': [2, is_exo], 'SUBSTACK': [2, bc_fx_exo], 'SUBSTACK2': [2, bc_fx_bond]})
    ctx.blocks[bc_fx_exo]['parent'] = if_exo_else
    ctx.blocks[bc_fx_bond]['parent'] = if_exo_else

    disc_val = ctx.add('data_itemoflist', fields={'LIST': ['DB_DISCOVERED', 'l_db_disc']}, inputs={'INDEX': [3, [12, 'temp_prod', 'v_local_prod'], [7, '1']]})
    is_new = ctx.add('operator_equals', inputs={'OPERAND1': [3, disc_val, [10, '']], 'OPERAND2': [1, [10, '0']]})
    set_disc = ctx.add('data_replaceitemoflist', fields={'LIST': ['DB_DISCOVERED', 'l_db_disc']}, inputs={'INDEX': [3, [12, 'temp_prod', 'v_local_prod'], [7, '1']], 'ITEM': [1, [4, '1']]})
    inc_disc = ctx.add('data_changevariableby', fields={'VARIABLE': ['TOTAL_DISCOVERED', 'v_discovered']}, inputs={'VALUE': [1, [4, '1']]})
    set_toast = ctx.add('data_setvariableto', fields={'VARIABLE': ['TOAST_SPECIES_ID', 'v_toast_id']}, inputs={'VALUE': [3, [12, 'temp_prod', 'v_local_prod'], [4, '1']]})
    bc_toast = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'SHOW_TOAST', 'b_show_toast']]})
    snd_disc_m = ctx.add('sound_sounds_menu', fields={'SOUND_MENU': ['snd_discover', None]}, shadow=True)
    play_disc = ctx.add('sound_play', inputs={'SOUND_MENU': [1, snd_disc_m]})
    ctx.chain([set_disc, inc_disc, set_toast, bc_toast, play_disc])

    if_new_disc = ctx.add('control_if', inputs={'CONDITION': [2, is_new], 'SUBSTACK': [2, set_disc]})
    ctx.blocks[set_disc]['parent'] = if_new_disc

    stop_rx = ctx.add('control_stop', fields={'STOP_OPTION': ['this script', None]})
    ctx.chain([deact_partner, get_prod, set_prod, set_my_spc, upd_list_spc, sw_costume, set_fx_x, set_fx_y, if_exo_else, if_new_disc, stop_rx])

    if_uv_else_rx = ctx.add('control_if_else', inputs={'CONDITION': [2, uv_blocked], 'SUBSTACK': [2, say_uv], 'SUBSTACK2': [2, deact_partner]})
    ctx.blocks[say_uv]['parent'] = if_uv_else_rx
    ctx.blocks[deact_partner]['parent'] = if_uv_else_rx

    if_rx_exists = ctx.add('control_if', inputs={'CONDITION': [2, has_rx], 'SUBSTACK': [2, if_uv_else_rx]})
    ctx.blocks[if_uv_else_rx]['parent'] = if_rx_exists

    ctx.chain([if_spc_order, set_rx_idx, if_rx_exists])

    if_close = ctx.add('control_if', inputs={'CONDITION': [2, close_enough], 'SUBSTACK': [2, if_spc_order]})
    ctx.blocks[if_spc_order]['parent'] = if_close

    ctx.chain([set_dx, set_dy, set_dsq, if_close])

    if_partner_active = ctx.add('control_if', inputs={'CONDITION': [2, both_cond], 'SUBSTACK': [2, set_dx]})
    ctx.blocks[set_dx]['parent'] = if_partner_active

    inc_k = ctx.add('data_changevariableby', fields={'VARIABLE': ['loop_k', 'v_local_k']}, inputs={'VALUE': [1, [4, '1']]})
    ctx.chain([if_partner_active, inc_k])

    rep_len = ctx.add('data_lengthoflist', fields={'LIST': ['ENTITY_ACTIVE', 'l_ent_act']})
    rep_loop = ctx.add('control_repeat', inputs={'TIMES': [3, rep_len, [6, '10']], 'SUBSTACK': [2, if_partner_active]})
    ctx.blocks[if_partner_active]['parent'] = rep_loop

    ctx.chain([def_resolve, set_k1, rep_loop])

    # Clone life loop
    hat_start = ctx.add('control_start_as_clone', topLevel=True, x=50, y=320)
    init_my_id = ctx.add('data_setvariableto', fields={'VARIABLE': ['my_id', 'v_local_id']}, inputs={'VALUE': [3, [12, 'NEXT_ENTITY_ID', 'v_next_id'], [4, '1']]})
    inc_next_id = ctx.add('data_changevariableby', fields={'VARIABLE': ['NEXT_ENTITY_ID', 'v_next_id']}, inputs={'VALUE': [1, [4, '1']]})
    init_my_spc = ctx.add('data_setvariableto', fields={'VARIABLE': ['my_species', 'v_local_spc']}, inputs={'VALUE': [3, ctx.add('data_itemoflist', fields={'LIST': ['ENTITY_SPECIES', 'l_ent_spc']}, inputs={'INDEX': [3, [12, 'my_id', 'v_local_id'], [7, '1']]}), [4, '1']]})
    init_sw = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [3, ctx.add('operator_join', inputs={'STRING1': [1, [10, 'species_']], 'STRING2': [3, [12, 'my_species', 'v_local_spc'], [10, '']]}), [10, 'species_1']]})
    init_goto = ctx.add('motion_gotoxy', inputs={
        'X': [3, ctx.add('data_itemoflist', fields={'LIST': ['ENTITY_X', 'l_ent_x']}, inputs={'INDEX': [3, [12, 'my_id', 'v_local_id'], [7, '1']]}), [4, '0']],
        'Y': [3, ctx.add('data_itemoflist', fields={'LIST': ['ENTITY_Y', 'l_ent_y']}, inputs={'INDEX': [3, [12, 'my_id', 'v_local_id'], [7, '1']]}), [4, '0']]
    })
    init_vx = ctx.add('data_setvariableto', fields={'VARIABLE': ['my_vx', 'v_local_vx']}, inputs={'VALUE': [3, ctx.add('data_itemoflist', fields={'LIST': ['ENTITY_VX', 'l_ent_vx']}, inputs={'INDEX': [3, [12, 'my_id', 'v_local_id'], [7, '1']]}), [4, '0']]})
    init_vy = ctx.add('data_setvariableto', fields={'VARIABLE': ['my_vy', 'v_local_vy']}, inputs={'VALUE': [3, ctx.add('data_itemoflist', fields={'LIST': ['ENTITY_VY', 'l_ent_vy']}, inputs={'INDEX': [3, [12, 'my_id', 'v_local_id'], [7, '1']]}), [4, '0']]})
    init_drag = ctx.add('data_setvariableto', fields={'VARIABLE': ['is_dragging', 'v_local_drag']}, inputs={'VALUE': [1, [4, '0']]})
    init_show = ctx.add('looks_show')

    my_act_val = ctx.add('data_itemoflist', fields={'LIST': ['ENTITY_ACTIVE', 'l_ent_act']}, inputs={'INDEX': [3, [12, 'my_id', 'v_local_id'], [7, '1']]})
    is_dead = ctx.add('operator_equals', inputs={'OPERAND1': [3, my_act_val, [10, '']], 'OPERAND2': [1, [10, '0']]})
    del_me = ctx.add('control_delete_this_clone')
    if_dead = ctx.add('control_if', inputs={'CONDITION': [2, is_dead], 'SUBSTACK': [2, del_me]})
    ctx.blocks[del_me]['parent'] = if_dead

    is_drag_active = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'is_dragging', 'v_local_drag'], [10, '']], 'OPERAND2': [1, [10, '1']]})
    goto_mouse = ctx.add('motion_gotoxy', inputs={'X': [3, ctx.add('sensing_mousex'), [4, '0']], 'Y': [3, ctx.add('sensing_mousey'), [4, '0']]})
    upd_drag_x = ctx.add('data_replaceitemoflist', fields={'LIST': ['ENTITY_X', 'l_ent_x']}, inputs={'INDEX': [3, [12, 'my_id', 'v_local_id'], [7, '1']], 'ITEM': [3, ctx.add('motion_xposition'), [4, '0']]})
    upd_drag_y = ctx.add('data_replaceitemoflist', fields={'LIST': ['ENTITY_Y', 'l_ent_y']}, inputs={'INDEX': [3, [12, 'my_id', 'v_local_id'], [7, '1']], 'ITEM': [3, ctx.add('motion_yposition'), [4, '0']]})

    m_down = ctx.add('sensing_mousedown')
    not_m_down = ctx.add('operator_not', inputs={'OPERAND': [2, m_down]})
    reset_drag = ctx.add('data_setvariableto', fields={'VARIABLE': ['is_dragging', 'v_local_drag']}, inputs={'VALUE': [1, [4, '0']]})
    reset_size = ctx.add('looks_setsizeto', inputs={'SIZE': [1, [4, '100']]})
    call_resolve = ctx.add('procedures_call', mutation={
        'tagName': 'mutation', 'children': [], 'proccode': 'ResolveInteractions',
        'argumentids': '[]', 'warp': 'true'
    })
    ctx.chain([reset_drag, reset_size, call_resolve])
    if_m_up = ctx.add('control_if', inputs={'CONDITION': [2, not_m_down], 'SUBSTACK': [2, reset_drag]})
    ctx.blocks[reset_drag]['parent'] = if_m_up
    ctx.chain([goto_mouse, upd_drag_x, upd_drag_y, if_m_up])

    move_x = ctx.add('motion_changexby', inputs={'DX': [3, [12, 'my_vx', 'v_local_vx'], [4, '0']]})
    move_y = ctx.add('motion_changeyby', inputs={'DY': [3, [12, 'my_vy', 'v_local_vy'], [4, '0']]})

    lt_min_x = ctx.add('operator_lt', inputs={'OPERAND1': [3, ctx.add('motion_xposition'), [10, '']], 'OPERAND2': [1, [10, '-220']]})
    set_vx_pos = ctx.add('data_setvariableto', fields={'VARIABLE': ['my_vx', 'v_local_vx']}, inputs={'VALUE': [3, ctx.add('operator_subtract', inputs={'NUM1': [1, [4, '0']], 'NUM2': [3, [12, 'my_vx', 'v_local_vx'], [4, '0']]}), [4, '0']]})
    set_min_x = ctx.add('motion_setx', inputs={'X': [1, [4, '-220']]})
    ctx.chain([set_vx_pos, set_min_x])
    if_min_x = ctx.add('control_if', inputs={'CONDITION': [2, lt_min_x], 'SUBSTACK': [2, set_vx_pos]})
    ctx.blocks[set_vx_pos]['parent'] = if_min_x

    gt_max_x = ctx.add('operator_gt', inputs={'OPERAND1': [3, ctx.add('motion_xposition'), [10, '']], 'OPERAND2': [1, [10, '220']]})
    set_vx_neg = ctx.add('data_setvariableto', fields={'VARIABLE': ['my_vx', 'v_local_vx']}, inputs={'VALUE': [3, ctx.add('operator_subtract', inputs={'NUM1': [1, [4, '0']], 'NUM2': [3, [12, 'my_vx', 'v_local_vx'], [4, '0']]}), [4, '0']]})
    set_max_x = ctx.add('motion_setx', inputs={'X': [1, [4, '220']]})
    ctx.chain([set_vx_neg, set_max_x])
    if_max_x = ctx.add('control_if', inputs={'CONDITION': [2, gt_max_x], 'SUBSTACK': [2, set_vx_neg]})
    ctx.blocks[set_vx_neg]['parent'] = if_max_x

    lt_min_y = ctx.add('operator_lt', inputs={'OPERAND1': [3, ctx.add('motion_yposition'), [10, '']], 'OPERAND2': [1, [10, '-115']]})
    set_vy_pos = ctx.add('data_setvariableto', fields={'VARIABLE': ['my_vy', 'v_local_vy']}, inputs={'VALUE': [3, ctx.add('operator_subtract', inputs={'NUM1': [1, [4, '0']], 'NUM2': [3, [12, 'my_vy', 'v_local_vy'], [4, '0']]}), [4, '0']]})
    set_min_y = ctx.add('motion_sety', inputs={'Y': [1, [4, '-115']]})
    ctx.chain([set_vy_pos, set_min_y])
    if_min_y = ctx.add('control_if', inputs={'CONDITION': [2, lt_min_y], 'SUBSTACK': [2, set_vy_pos]})
    ctx.blocks[set_vy_pos]['parent'] = if_min_y

    gt_max_y = ctx.add('operator_gt', inputs={'OPERAND1': [3, ctx.add('motion_yposition'), [10, '']], 'OPERAND2': [1, [10, '120']]})
    set_vy_neg = ctx.add('data_setvariableto', fields={'VARIABLE': ['my_vy', 'v_local_vy']}, inputs={'VALUE': [3, ctx.add('operator_subtract', inputs={'NUM1': [1, [4, '0']], 'NUM2': [3, [12, 'my_vy', 'v_local_vy'], [4, '0']]}), [4, '0']]})
    set_max_y = ctx.add('motion_sety', inputs={'Y': [1, [4, '120']]})
    ctx.chain([set_vy_neg, set_max_y])
    if_max_y = ctx.add('control_if', inputs={'CONDITION': [2, gt_max_y], 'SUBSTACK': [2, set_vy_neg]})
    ctx.blocks[set_vy_neg]['parent'] = if_max_y

    upd_pos_x = ctx.add('data_replaceitemoflist', fields={'LIST': ['ENTITY_X', 'l_ent_x']}, inputs={'INDEX': [3, [12, 'my_id', 'v_local_id'], [7, '1']], 'ITEM': [3, ctx.add('motion_xposition'), [4, '0']]})
    upd_pos_y = ctx.add('data_replaceitemoflist', fields={'LIST': ['ENTITY_Y', 'l_ent_y']}, inputs={'INDEX': [3, [12, 'my_id', 'v_local_id'], [7, '1']], 'ITEM': [3, ctx.add('motion_yposition'), [4, '0']]})

    curr_spc_in_list = ctx.add('data_itemoflist', fields={'LIST': ['ENTITY_SPECIES', 'l_ent_spc']}, inputs={'INDEX': [3, [12, 'my_id', 'v_local_id'], [7, '1']]})
    spc_changed = ctx.add('operator_not', inputs={'OPERAND': [2, ctx.add('operator_equals', inputs={'OPERAND1': [3, curr_spc_in_list, [10, '']], 'OPERAND2': [3, [12, 'my_species', 'v_local_spc'], [10, '']]})]})
    set_new_spc = ctx.add('data_setvariableto', fields={'VARIABLE': ['my_species', 'v_local_spc']}, inputs={'VALUE': [3, curr_spc_in_list, [4, '1']]})
    sw_new_costume = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [3, ctx.add('operator_join', inputs={'STRING1': [1, [10, 'species_']], 'STRING2': [3, [12, 'my_species', 'v_local_spc'], [10, '']]}), [10, 'species_1']]})
    ctx.chain([set_new_spc, sw_new_costume])
    if_spc_mutated = ctx.add('control_if', inputs={'CONDITION': [2, spc_changed], 'SUBSTACK': [2, set_new_spc]})
    ctx.blocks[set_new_spc]['parent'] = if_spc_mutated

    ctx.chain([move_x, move_y, if_min_x, if_max_x, if_min_y, if_max_y, upd_pos_x, upd_pos_y, if_spc_mutated])

    is_not_frozen = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'TIME_FROZEN', 'v_freeze'], [10, '']], 'OPERAND2': [1, [10, '0']]})
    if_not_frozen = ctx.add('control_if', inputs={'CONDITION': [2, is_not_frozen], 'SUBSTACK': [2, move_x]})
    ctx.blocks[move_x]['parent'] = if_not_frozen

    if_drag_else = ctx.add('control_if_else', inputs={'CONDITION': [2, is_drag_active], 'SUBSTACK': [2, goto_mouse], 'SUBSTACK2': [2, if_not_frozen]})
    ctx.blocks[goto_mouse]['parent'] = if_drag_else
    ctx.blocks[if_not_frozen]['parent'] = if_drag_else

    ctx.chain([if_dead, if_drag_else])
    loop_forever = ctx.add('control_forever', inputs={'SUBSTACK': [2, if_dead]})
    ctx.blocks[if_dead]['parent'] = loop_forever

    ctx.chain([hat_start, init_my_id, inc_next_id, init_my_spc, init_sw, init_goto, init_vx, init_vy, init_drag, init_show, loop_forever])

    # Click handling
    hat_click = ctx.add('event_whenthisspriteclicked', topLevel=True, x=50, y=700)
    is_del_tool = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'CURRENT_TOOL', 'v_tool'], [10, '']], 'OPERAND2': [1, [10, 'delete']]})
    del_act_val = ctx.add('data_replaceitemoflist', fields={'LIST': ['ENTITY_ACTIVE', 'l_ent_act']}, inputs={'INDEX': [3, [12, 'my_id', 'v_local_id'], [7, '1']], 'ITEM': [1, [4, '0']]})
    del_fx_x = ctx.add('data_setvariableto', fields={'VARIABLE': ['FX_X', 'v_fx_x']}, inputs={'VALUE': [3, ctx.add('motion_xposition'), [4, '0']]})
    del_fx_y = ctx.add('data_setvariableto', fields={'VARIABLE': ['FX_Y', 'v_fx_y']}, inputs={'VALUE': [3, ctx.add('motion_yposition'), [4, '0']]})
    del_bc_fx = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'PLAY_FX_DELETE', 'b_fx_del']]})
    snd_del_m = ctx.add('sound_sounds_menu', fields={'SOUND_MENU': ['snd_delete', None]}, shadow=True)
    del_play_snd = ctx.add('sound_play', inputs={'SOUND_MENU': [1, snd_del_m]})
    del_clone_now = ctx.add('control_delete_this_clone')
    ctx.chain([del_act_val, del_fx_x, del_fx_y, del_bc_fx, del_play_snd, del_clone_now])

    is_info_tool = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'CURRENT_TOOL', 'v_tool'], [10, '']], 'OPERAND2': [1, [10, 'inspect']]})
    set_insp = ctx.add('data_setvariableto', fields={'VARIABLE': ['INSPECT_SPECIES_ID', 'v_inspect_id']}, inputs={'VALUE': [3, [12, 'my_species', 'v_local_spc'], [4, '1']]})
    set_show_inf = ctx.add('data_setvariableto', fields={'VARIABLE': ['SHOW_INFO', 'v_info']}, inputs={'VALUE': [1, [4, '1']]})
    bc_info = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'SHOW_INFO', 'b_show_info']]})
    bc_upd_info = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'UPDATE_UI', 'b_update_ui']]})
    ctx.chain([set_insp, set_show_inf, bc_info, bc_upd_info])

    start_drag = ctx.add('data_setvariableto', fields={'VARIABLE': ['is_dragging', 'v_local_drag']}, inputs={'VALUE': [1, [4, '1']]})
    drag_size = ctx.add('looks_setsizeto', inputs={'SIZE': [1, [4, '115']]})
    drag_front = ctx.add('looks_gotofrontback', fields={'FRONT_BACK': ['front', None]})
    ctx.chain([start_drag, drag_size, drag_front])

    if_info_else = ctx.add('control_if_else', inputs={'CONDITION': [2, is_info_tool], 'SUBSTACK': [2, set_insp], 'SUBSTACK2': [2, start_drag]})
    ctx.blocks[set_insp]['parent'] = if_info_else
    ctx.blocks[start_drag]['parent'] = if_info_else

    if_del_else = ctx.add('control_if_else', inputs={'CONDITION': [2, is_del_tool], 'SUBSTACK': [2, del_act_val], 'SUBSTACK2': [2, if_info_else]})
    ctx.blocks[del_act_val]['parent'] = if_del_else
    ctx.blocks[if_info_else]['parent'] = if_del_else

    ctx.chain([hat_click, if_del_else])

    return {
        'isStage': False,
        'name': 'Entity',
        'variables': entity_vars,
        'lists': {},
        'broadcasts': {},
        'blocks': ctx.blocks,
        'comments': {},
        'currentCostume': 0,
        'costumes': entity_costumes,
        'sounds': entity_sounds,
        'volume': 100,
        'visible': True,
        'x': 0, 'y': 0, 'size': 100, 'direction': 90,
        'draggable': False, 'rotationStyle': "don't rotate"
    }

# 4. CosmicRay Sprite Builder
def build_cosmic_ray():
    ctx = BlockContext()
    ray_vars = {
        'v_ray_k': ['ray_k', 1],
        'v_ray_dx': ['ray_dx', 0],
        'v_ray_dy': ['ray_dy', 0],
        'v_ray_dsq': ['ray_dsq', 0],
        'v_ray_spc': ['ray_spc', 1],
        'v_ray_idx': ['ray_ion_idx', 0],
        'v_ray_dst': ['ray_new_ion', 0]
    }

    flag_id = ctx.add('event_whenflagclicked', topLevel=True, x=50, y=50)
    hide_orig = ctx.add('looks_hide')

    wait_time = ctx.add('operator_random', inputs={'FROM': [1, [4, '7']], 'TO': [1, [4, '12']]})
    wait_b = ctx.add('control_wait', inputs={'DURATION': [3, wait_time, [4, '8']]})
    is_not_frozen = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'TIME_FROZEN', 'v_freeze'], [10, '']], 'OPERAND2': [1, [10, '0']]})
    create_cl = ctx.add('control_create_clone_of', inputs={'CLONE_OPTION': [1, ctx.add('control_create_clone_of_menu', fields={'CLONE_OPTION': ['_myself_', None]}, shadow=True)]})
    if_spawn = ctx.add('control_if', inputs={'CONDITION': [2, is_not_frozen], 'SUBSTACK': [2, create_cl]})
    ctx.blocks[create_cl]['parent'] = if_spawn
    ctx.chain([wait_b, if_spawn])
    forever_loop = ctx.add('control_forever', inputs={'SUBSTACK': [2, wait_b]})
    ctx.blocks[wait_b]['parent'] = forever_loop
    ctx.chain([flag_id, hide_orig, forever_loop])

    hat_start = ctx.add('control_start_as_clone', topLevel=True, x=50, y=280)
    rnd_y = ctx.add('operator_random', inputs={'FROM': [1, [4, '-90']], 'TO': [1, [4, '100']]})
    goto_edge = ctx.add('motion_gotoxy', inputs={'X': [1, [4, '-240']], 'Y': [3, rnd_y, [4, '0']]})
    rnd_dir = ctx.add('operator_random', inputs={'FROM': [1, [4, '75']], 'TO': [1, [4, '105']]})
    point_dir = ctx.add('motion_pointindirection', inputs={'DIRECTION': [3, rnd_dir, [8, '90']]})
    show_cl = ctx.add('looks_show')

    touch_edge_menu = ctx.add('sensing_touchingobjectmenu', fields={'TOUCHINGOBJECTMENU': ['_edge_', None]}, shadow=True)
    touch_edge = ctx.add('sensing_touchingobject', inputs={'TOUCHINGOBJECTMENU': [1, touch_edge_menu]})

    move_step = ctx.add('motion_movesteps', inputs={'STEPS': [1, [4, '14']]})
    set_rk = ctx.add('data_setvariableto', fields={'VARIABLE': ['ray_k', 'v_ray_k']}, inputs={'VALUE': [1, [4, '1']]})

    target_act = ctx.add('data_itemoflist', fields={'LIST': ['ENTITY_ACTIVE', 'l_ent_act']}, inputs={'INDEX': [3, [12, 'ray_k', 'v_ray_k'], [7, '1']]})
    is_act = ctx.add('operator_equals', inputs={'OPERAND1': [3, target_act, [10, '']], 'OPERAND2': [1, [10, '1']]})

    tgt_x = ctx.add('data_itemoflist', fields={'LIST': ['ENTITY_X', 'l_ent_x']}, inputs={'INDEX': [3, [12, 'ray_k', 'v_ray_k'], [7, '1']]})
    dx_val = ctx.add('operator_subtract', inputs={'NUM1': [3, tgt_x, [4, '0']], 'NUM2': [3, ctx.add('motion_xposition'), [4, '0']]})
    set_rdx = ctx.add('data_setvariableto', fields={'VARIABLE': ['ray_dx', 'v_ray_dx']}, inputs={'VALUE': [3, dx_val, [4, '0']]})

    tgt_y = ctx.add('data_itemoflist', fields={'LIST': ['ENTITY_Y', 'l_ent_y']}, inputs={'INDEX': [3, [12, 'ray_k', 'v_ray_k'], [7, '1']]})
    dy_val = ctx.add('operator_subtract', inputs={'NUM1': [3, tgt_y, [4, '0']], 'NUM2': [3, ctx.add('motion_yposition'), [4, '0']]})
    set_rdy = ctx.add('data_setvariableto', fields={'VARIABLE': ['ray_dy', 'v_ray_dy']}, inputs={'VALUE': [3, dy_val, [4, '0']]})

    dx_sq = ctx.add('operator_multiply', inputs={'NUM1': [3, [12, 'ray_dx', 'v_ray_dx'], [4, '0']], 'NUM2': [3, [12, 'ray_dx', 'v_ray_dx'], [4, '0']]})
    dy_sq = ctx.add('operator_multiply', inputs={'NUM1': [3, [12, 'ray_dy', 'v_ray_dy'], [4, '0']], 'NUM2': [3, [12, 'ray_dy', 'v_ray_dy'], [4, '0']]})
    dsq_val = ctx.add('operator_add', inputs={'NUM1': [3, dx_sq, [4, '0']], 'NUM2': [3, dy_sq, [4, '0']]})
    set_rdsq = ctx.add('data_setvariableto', fields={'VARIABLE': ['ray_dsq', 'v_ray_dsq']}, inputs={'VALUE': [3, dsq_val, [4, '0']]})

    close_hit = ctx.add('operator_lt', inputs={'OPERAND1': [3, [12, 'ray_dsq', 'v_ray_dsq'], [10, '']], 'OPERAND2': [1, [10, '900']]})

    tgt_spc = ctx.add('data_itemoflist', fields={'LIST': ['ENTITY_SPECIES', 'l_ent_spc']}, inputs={'INDEX': [3, [12, 'ray_k', 'v_ray_k'], [7, '1']]})
    set_rspc = ctx.add('data_setvariableto', fields={'VARIABLE': ['ray_spc', 'v_ray_spc']}, inputs={'VALUE': [3, tgt_spc, [4, '1']]})
    ion_idx_val = ctx.add('data_itemnumoflist', fields={'LIST': ['IONIZE_SRC', 'l_ion_src']}, inputs={'ITEM': [3, [12, 'ray_spc', 'v_ray_spc'], [10, '']]})
    set_ridx = ctx.add('data_setvariableto', fields={'VARIABLE': ['ray_ion_idx', 'v_ray_idx']}, inputs={'VALUE': [3, ion_idx_val, [4, '0']]})

    has_ion = ctx.add('operator_gt', inputs={'OPERAND1': [3, [12, 'ray_ion_idx', 'v_ray_idx'], [10, '']], 'OPERAND2': [1, [10, '0']]})
    get_dst = ctx.add('data_itemoflist', fields={'LIST': ['IONIZE_DST', 'l_ion_dst']}, inputs={'INDEX': [3, [12, 'ray_ion_idx', 'v_ray_idx'], [7, '1']]})
    set_rdst = ctx.add('data_setvariableto', fields={'VARIABLE': ['ray_new_ion', 'v_ray_dst']}, inputs={'VALUE': [3, get_dst, [4, '1']]})
    upd_ent_spc = ctx.add('data_replaceitemoflist', fields={'LIST': ['ENTITY_SPECIES', 'l_ent_spc']}, inputs={'INDEX': [3, [12, 'ray_k', 'v_ray_k'], [7, '1']], 'ITEM': [3, [12, 'ray_new_ion', 'v_ray_dst'], [4, '1']]})

    set_fx_x = ctx.add('data_setvariableto', fields={'VARIABLE': ['FX_X', 'v_fx_x']}, inputs={'VALUE': [3, tgt_x, [4, '0']]})
    set_fx_y = ctx.add('data_setvariableto', fields={'VARIABLE': ['FX_Y', 'v_fx_y']}, inputs={'VALUE': [3, tgt_y, [4, '0']]})
    bc_zap = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'PLAY_FX_ZAP', 'b_fx_zap']]})
    snd_zap_m = ctx.add('sound_sounds_menu', fields={'SOUND_MENU': ['snd_cosmic', None]}, shadow=True)
    play_zap = ctx.add('sound_play', inputs={'SOUND_MENU': [1, snd_zap_m]})

    disc_val = ctx.add('data_itemoflist', fields={'LIST': ['DB_DISCOVERED', 'l_db_disc']}, inputs={'INDEX': [3, [12, 'ray_new_ion', 'v_ray_dst'], [7, '1']]})
    is_new = ctx.add('operator_equals', inputs={'OPERAND1': [3, disc_val, [10, '']], 'OPERAND2': [1, [10, '0']]})
    set_disc = ctx.add('data_replaceitemoflist', fields={'LIST': ['DB_DISCOVERED', 'l_db_disc']}, inputs={'INDEX': [3, [12, 'ray_new_ion', 'v_ray_dst'], [7, '1']], 'ITEM': [1, [4, '1']]})
    inc_disc = ctx.add('data_changevariableby', fields={'VARIABLE': ['TOTAL_DISCOVERED', 'v_discovered']}, inputs={'VALUE': [1, [4, '1']]})
    set_toast = ctx.add('data_setvariableto', fields={'VARIABLE': ['TOAST_SPECIES_ID', 'v_toast_id']}, inputs={'VALUE': [3, [12, 'ray_new_ion', 'v_ray_dst'], [4, '1']]})
    bc_toast = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'SHOW_TOAST', 'b_show_toast']]})
    snd_fanfare_m = ctx.add('sound_sounds_menu', fields={'SOUND_MENU': ['snd_discover', None]}, shadow=True)
    play_fanfare = ctx.add('sound_play', inputs={'SOUND_MENU': [1, snd_fanfare_m]})
    ctx.chain([set_disc, inc_disc, set_toast, bc_toast, play_fanfare])

    if_new_disc = ctx.add('control_if', inputs={'CONDITION': [2, is_new], 'SUBSTACK': [2, set_disc]})
    ctx.blocks[set_disc]['parent'] = if_new_disc

    del_ray = ctx.add('control_delete_this_clone')
    ctx.chain([set_rdst, upd_ent_spc, set_fx_x, set_fx_y, bc_zap, play_zap, if_new_disc, del_ray])

    if_ion_match = ctx.add('control_if', inputs={'CONDITION': [2, has_ion], 'SUBSTACK': [2, set_rdst]})
    ctx.blocks[set_rdst]['parent'] = if_ion_match

    ctx.chain([set_rspc, set_ridx, if_ion_match])
    if_hit = ctx.add('control_if', inputs={'CONDITION': [2, close_hit], 'SUBSTACK': [2, set_rspc]})
    ctx.blocks[set_rspc]['parent'] = if_hit

    ctx.chain([set_rdx, set_rdy, set_rdsq, if_hit])
    if_cand_act = ctx.add('control_if', inputs={'CONDITION': [2, is_act], 'SUBSTACK': [2, set_rdx]})
    ctx.blocks[set_rdx]['parent'] = if_cand_act

    inc_rk = ctx.add('data_changevariableby', fields={'VARIABLE': ['ray_k', 'v_ray_k']}, inputs={'VALUE': [1, [4, '1']]})
    ctx.chain([if_cand_act, inc_rk])

    rep_len = ctx.add('data_lengthoflist', fields={'LIST': ['ENTITY_ACTIVE', 'l_ent_act']})
    rep_k_loop = ctx.add('control_repeat', inputs={'TIMES': [3, rep_len, [6, '10']], 'SUBSTACK': [2, if_cand_act]})
    ctx.blocks[if_cand_act]['parent'] = rep_k_loop

    ctx.chain([move_step, set_rk, rep_k_loop])
    if_sim_active = ctx.add('control_if', inputs={'CONDITION': [2, is_not_frozen], 'SUBSTACK': [2, move_step]})
    ctx.blocks[move_step]['parent'] = if_sim_active

    rep_until_edge = ctx.add('control_repeat_until', inputs={'CONDITION': [2, touch_edge], 'SUBSTACK': [2, if_sim_active]})
    ctx.blocks[if_sim_active]['parent'] = rep_until_edge

    del_at_edge = ctx.add('control_delete_this_clone')
    ctx.chain([hat_start, goto_edge, point_dir, show_cl, rep_until_edge, del_at_edge])

    return {
        'isStage': False,
        'name': 'CosmicRay',
        'variables': ray_vars,
        'lists': {},
        'broadcasts': {},
        'blocks': ctx.blocks,
        'comments': {},
        'currentCostume': 0,
        'costumes': [costume_meta['cosmic_ray']],
        'sounds': [sound_meta['snd_cosmic'], sound_meta['snd_discover']],
        'volume': 100,
        'visible': False,
        'x': 0, 'y': 0, 'size': 100, 'direction': 90,
        'draggable': False, 'rotationStyle': "don't rotate"
    }

# 5. Photon Sprite Builder
def build_photon():
    ctx = BlockContext()
    photon_vars = {'v_ph_life': ['life', 50]}

    hat_rec = ctx.add('event_whenbroadcastreceived', fields={'BROADCAST_OPTION': ['SPAWN_PHOTON', 'b_spawn_photon']}, topLevel=True, x=50, y=50)
    create_cl = ctx.add('control_create_clone_of', inputs={'CLONE_OPTION': [1, ctx.add('control_create_clone_of_menu', fields={'CLONE_OPTION': ['_myself_', None]}, shadow=True)]})
    ctx.chain([hat_rec, create_cl])

    hat_start = ctx.add('control_start_as_clone', topLevel=True, x=50, y=200)
    goto_fx = ctx.add('motion_gotoxy', inputs={'X': [3, [12, 'FX_X', 'v_fx_x'], [4, '0']], 'Y': [3, [12, 'FX_Y', 'v_fx_y'], [4, '0']]})
    rnd_dir = ctx.add('operator_random', inputs={'FROM': [1, [4, '0']], 'TO': [1, [4, '360']]})
    point_dir = ctx.add('motion_pointindirection', inputs={'DIRECTION': [3, rnd_dir, [8, '90']]})
    set_life = ctx.add('data_setvariableto', fields={'VARIABLE': ['life', 'v_ph_life']}, inputs={'VALUE': [1, [4, '50']]})
    set_ghost = ctx.add('looks_seteffectto', fields={'EFFECT': ['GHOST', None]}, inputs={'VALUE': [1, [4, '0']]})
    show_ph = ctx.add('looks_show')
    snd_ph_m = ctx.add('sound_sounds_menu', fields={'SOUND_MENU': ['snd_photon', None]}, shadow=True)
    play_ph = ctx.add('sound_play', inputs={'SOUND_MENU': [1, snd_ph_m]})

    life_done = ctx.add('operator_lt', inputs={'OPERAND1': [3, [12, 'life', 'v_ph_life'], [10, '']], 'OPERAND2': [1, [10, '1']]})
    is_not_frozen = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'TIME_FROZEN', 'v_freeze'], [10, '']], 'OPERAND2': [1, [10, '0']]})

    mv_step = ctx.add('motion_movesteps', inputs={'STEPS': [1, [4, '8']]})
    bounce_edge = ctx.add('motion_ifonedgebounce')
    dec_life = ctx.add('data_changevariableby', fields={'VARIABLE': ['life', 'v_ph_life']}, inputs={'VALUE': [1, [4, '-1']]})
    inc_ghost = ctx.add('looks_changeeffectby', fields={'EFFECT': ['GHOST', None]}, inputs={'VALUE': [1, [4, '2']]})
    ctx.chain([mv_step, bounce_edge, dec_life, inc_ghost])

    if_active = ctx.add('control_if', inputs={'CONDITION': [2, is_not_frozen], 'SUBSTACK': [2, mv_step]})
    ctx.blocks[mv_step]['parent'] = if_active

    rep_loop = ctx.add('control_repeat_until', inputs={'CONDITION': [2, life_done], 'SUBSTACK': [2, if_active]})
    ctx.blocks[if_active]['parent'] = rep_loop

    del_ph = ctx.add('control_delete_this_clone')
    ctx.chain([hat_start, goto_fx, point_dir, set_life, set_ghost, show_ph, play_ph, rep_loop, del_ph])

    return {
        'isStage': False,
        'name': 'Photon',
        'variables': photon_vars,
        'lists': {},
        'broadcasts': {},
        'blocks': ctx.blocks,
        'comments': {},
        'currentCostume': 0,
        'costumes': [costume_meta['photon_wave']],
        'sounds': [sound_meta['snd_photon']],
        'volume': 100,
        'visible': False,
        'x': 0, 'y': 0, 'size': 100, 'direction': 90,
        'draggable': False, 'rotationStyle': "don't rotate"
    }

# 6. Effects Sprite Builder
def build_effects():
    ctx = BlockContext()
    fx_costumes = [
        costume_meta['fx_exo_1'], costume_meta['fx_exo_2'], costume_meta['fx_exo_3'],
        costume_meta['fx_bond_1'], costume_meta['fx_bond_2'],
        costume_meta['fx_zap_1'], costume_meta['fx_zap_2'],
        costume_meta['fx_poof_1'], costume_meta['fx_poof_2'],
        costume_meta['toast_banner']
    ]

    flag_id = ctx.add('event_whenflagclicked', topLevel=True, x=50, y=50)
    hide_orig = ctx.add('looks_hide')
    ctx.chain([flag_id, hide_orig])

    hat_exo = ctx.add('event_whenbroadcastreceived', fields={'BROADCAST_OPTION': ['PLAY_FX_EXO', 'b_fx_exo']}, topLevel=True, x=50, y=150)
    goto_exo = ctx.add('motion_gotoxy', inputs={'X': [3, [12, 'FX_X', 'v_fx_x'], [4, '0']], 'Y': [3, [12, 'FX_Y', 'v_fx_y'], [4, '0']]})
    sw_exo1 = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, ctx.add('looks_costume', fields={'COSTUME': ['fx_exo_1', None]}, shadow=True)]})
    show_exo = ctx.add('looks_show')
    w1 = ctx.add('control_wait', inputs={'DURATION': [1, [4, '0.05']]})
    sw_exo2 = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, ctx.add('looks_costume', fields={'COSTUME': ['fx_exo_2', None]}, shadow=True)]})
    w2 = ctx.add('control_wait', inputs={'DURATION': [1, [4, '0.05']]})
    sw_exo3 = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, ctx.add('looks_costume', fields={'COSTUME': ['fx_exo_3', None]}, shadow=True)]})
    w3 = ctx.add('control_wait', inputs={'DURATION': [1, [4, '0.05']]})
    hide_exo = ctx.add('looks_hide')
    ctx.chain([hat_exo, goto_exo, sw_exo1, show_exo, w1, sw_exo2, w2, sw_exo3, w3, hide_exo])

    hat_bnd = ctx.add('event_whenbroadcastreceived', fields={'BROADCAST_OPTION': ['PLAY_FX_BOND', 'b_fx_bond']}, topLevel=True, x=50, y=420)
    goto_bnd = ctx.add('motion_gotoxy', inputs={'X': [3, [12, 'FX_X', 'v_fx_x'], [4, '0']], 'Y': [3, [12, 'FX_Y', 'v_fx_y'], [4, '0']]})
    sw_bnd1 = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, ctx.add('looks_costume', fields={'COSTUME': ['fx_bond_1', None]}, shadow=True)]})
    show_bnd = ctx.add('looks_show')
    wb1 = ctx.add('control_wait', inputs={'DURATION': [1, [4, '0.06']]})
    sw_bnd2 = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, ctx.add('looks_costume', fields={'COSTUME': ['fx_bond_2', None]}, shadow=True)]})
    wb2 = ctx.add('control_wait', inputs={'DURATION': [1, [4, '0.06']]})
    hide_bnd = ctx.add('looks_hide')
    ctx.chain([hat_bnd, goto_bnd, sw_bnd1, show_bnd, wb1, sw_bnd2, wb2, hide_bnd])

    hat_zap = ctx.add('event_whenbroadcastreceived', fields={'BROADCAST_OPTION': ['PLAY_FX_ZAP', 'b_fx_zap']}, topLevel=True, x=450, y=150)
    goto_zap = ctx.add('motion_gotoxy', inputs={'X': [3, [12, 'FX_X', 'v_fx_x'], [4, '0']], 'Y': [3, [12, 'FX_Y', 'v_fx_y'], [4, '0']]})
    sw_zap1 = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, ctx.add('looks_costume', fields={'COSTUME': ['fx_zap_1', None]}, shadow=True)]})
    show_zap = ctx.add('looks_show')
    wz1 = ctx.add('control_wait', inputs={'DURATION': [1, [4, '0.05']]})
    sw_zap2 = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, ctx.add('looks_costume', fields={'COSTUME': ['fx_zap_2', None]}, shadow=True)]})
    wz2 = ctx.add('control_wait', inputs={'DURATION': [1, [4, '0.05']]})
    hide_zap = ctx.add('looks_hide')
    ctx.chain([hat_zap, goto_zap, sw_zap1, show_zap, wz1, sw_zap2, wz2, hide_zap])

    hat_del = ctx.add('event_whenbroadcastreceived', fields={'BROADCAST_OPTION': ['PLAY_FX_DELETE', 'b_fx_del']}, topLevel=True, x=450, y=420)
    goto_del = ctx.add('motion_gotoxy', inputs={'X': [3, [12, 'FX_X', 'v_fx_x'], [4, '0']], 'Y': [3, [12, 'FX_Y', 'v_fx_y'], [4, '0']]})
    sw_poof1 = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, ctx.add('looks_costume', fields={'COSTUME': ['fx_poof_1', None]}, shadow=True)]})
    show_del = ctx.add('looks_show')
    wd1 = ctx.add('control_wait', inputs={'DURATION': [1, [4, '0.06']]})
    sw_poof2 = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, ctx.add('looks_costume', fields={'COSTUME': ['fx_poof_2', None]}, shadow=True)]})
    wd2 = ctx.add('control_wait', inputs={'DURATION': [1, [4, '0.06']]})
    hide_del = ctx.add('looks_hide')
    ctx.chain([hat_del, goto_del, sw_poof1, show_del, wd1, sw_poof2, wd2, hide_del])

    hat_toast = ctx.add('event_whenbroadcastreceived', fields={'BROADCAST_OPTION': ['SHOW_TOAST', 'b_show_toast']}, topLevel=True, x=450, y=650)
    goto_toast = ctx.add('motion_gotoxy', inputs={'X': [1, [4, '0']], 'Y': [1, [4, '115']]})
    sw_toast = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, ctx.add('looks_costume', fields={'COSTUME': ['toast_banner', None]}, shadow=True)]})
    show_toast = ctx.add('looks_show')
    front_toast = ctx.add('looks_gotofrontback', fields={'FRONT_BACK': ['front', None]})
    wt = ctx.add('control_wait', inputs={'DURATION': [1, [4, '2.5']]})
    hide_toast = ctx.add('looks_hide')
    ctx.chain([hat_toast, goto_toast, sw_toast, show_toast, front_toast, wt, hide_toast])

    return {
        'isStage': False,
        'name': 'Effects',
        'variables': {},
        'lists': {},
        'broadcasts': {},
        'blocks': ctx.blocks,
        'comments': {},
        'currentCostume': 0,
        'costumes': fx_costumes,
        'sounds': [],
        'volume': 100,
        'visible': False,
        'x': 0, 'y': 0, 'size': 100, 'direction': 90,
        'draggable': False, 'rotationStyle': "don't rotate"
    }

def make_sprite(name, costumes, sounds, blocks, visible=True, x=0, y=0, variables=None, lists=None):
    return {
        'isStage': False,
        'name': name,
        'variables': variables or {},
        'lists': lists or {},
        'broadcasts': {},
        'blocks': blocks,
        'comments': {},
        'currentCostume': 0,
        'costumes': costumes,
        'sounds': sounds,
        'volume': 100,
        'visible': visible,
        'x': x, 'y': y, 'size': 100, 'direction': 90,
        'draggable': False, 'rotationStyle': "don't rotate"
    }

# 7. ToolRailUI Chassis Builder & 10 Independent Tool Button Sprites
def build_tool_rail_ui(ASSETS=costume_meta):
    ctx = BlockContext()
    hat_gf = ctx.add('event_whenflagclicked', topLevel=True, x=50, y=50)
    goto_pos = ctx.add('motion_gotoxy', inputs={'X': [1, [4, '0']], 'Y': [1, [4, '144']]})
    show_it = ctx.add('looks_show')
    ctx.chain([hat_gf, goto_pos, show_it])
    costume = ASSETS.get('tool_rail_bar', ASSETS['btn_add'])
    return make_sprite('ToolRailUI', [costume], [], ctx.blocks, visible=True, x=0, y=144)

def build_all_tool_buttons(ASSETS=costume_meta):
    btn_defs = [
        ('ToolBtn_Add', -207, 'btn_add', 'btn_add_active', 'v_palette', 'toggle_palette', 'snd_click'),
        ('ToolBtn_Delete', -161, 'btn_del', 'btn_del_active', 'v_tool', 'toggle_delete', 'snd_click'),
        ('ToolBtn_Inspect', -115, 'btn_insp', 'btn_insp_active', 'v_tool', 'toggle_inspect', 'snd_click'),
        ('ToolBtn_UV', -69, 'btn_uv', 'btn_uv_active', 'v_uv', 'toggle_uv', 'snd_click'),
        ('ToolBtn_Freeze', -23, 'btn_freeze', 'btn_freeze_active', 'v_freeze', 'toggle_freeze', 'snd_freeze'),
        ('ToolBtn_Catalog', 23, 'btn_catalog', 'btn_catalog_active', 'v_compendium', 'toggle_compendium', 'snd_click'),
        ('ToolBtn_Audio', 69, 'btn_audio', 'btn_audio_muted', 'v_volume', 'toggle_audio', 'snd_click'),
        ('ToolBtn_Save', 115, 'btn_save', 'btn_save_active', None, 'broadcast_save', 'snd_click'),
        ('ToolBtn_Help', 161, 'btn_help', 'btn_help_active', 'v_onboarding', 'toggle_onboarding', 'snd_click'),
        ('ToolBtn_Purge', 207, 'btn_purge', 'btn_purge_active', None, 'broadcast_purge', 'snd_delete')
    ]
    sprites = []
    for name, x, c_norm, c_act, var_name, act_type, snd_name in btn_defs:
        ctx = BlockContext()
        # 1. Flag clicked
        f_hat = ctx.add('event_whenflagclicked', topLevel=True, x=50, y=50)
        f_goto = ctx.add('motion_gotoxy', inputs={'X': [1, [4, str(x)]], 'Y': [1, [4, '144']]})
        f_front = ctx.add('looks_gotofrontback', fields={'FRONT_BACK': ['front']})
        f_show = ctx.add('looks_show')
        ctx.chain([f_hat, f_goto, f_front, f_show])

        # 2. UPDATE_UI
        u_hat = ctx.add('event_whenbroadcastreceived', fields={'BROADCAST_OPTION': ['UPDATE_UI', 'b_update_ui']}, topLevel=True, x=50, y=200)
        u_front = ctx.add('looks_gotofrontback', fields={'FRONT_BACK': ['front']})
        u_show = ctx.add('looks_show')
        if var_name == 'v_palette':
            cond = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'SHOW_PALETTE', 'v_palette'], [10, '']], 'OPERAND2': [1, [10, '1']]})
            c1 = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, [4, c_act]]})
            c2 = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, [4, c_norm]]})
            if_block = ctx.add('control_if_else', inputs={'CONDITION': [2, cond], 'SUBSTACK': [2, c1], 'SUBSTACK2': [2, c2]})
            ctx.blocks[c1]['parent'] = if_block
            ctx.blocks[c2]['parent'] = if_block
            ctx.chain([u_hat, if_block, u_front, u_show])
        elif var_name == 'v_tool' and act_type == 'toggle_delete':
            cond = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'CURRENT_TOOL', 'v_tool'], [10, '']], 'OPERAND2': [1, [10, 'delete']]})
            c1 = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, [4, c_act]]})
            c2 = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, [4, c_norm]]})
            if_block = ctx.add('control_if_else', inputs={'CONDITION': [2, cond], 'SUBSTACK': [2, c1], 'SUBSTACK2': [2, c2]})
            ctx.blocks[c1]['parent'] = if_block
            ctx.blocks[c2]['parent'] = if_block
            ctx.chain([u_hat, if_block, u_front, u_show])
        elif var_name == 'v_tool' and act_type == 'toggle_inspect':
            cond = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'CURRENT_TOOL', 'v_tool'], [10, '']], 'OPERAND2': [1, [10, 'inspect']]})
            c1 = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, [4, c_act]]})
            c2 = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, [4, c_norm]]})
            if_block = ctx.add('control_if_else', inputs={'CONDITION': [2, cond], 'SUBSTACK': [2, c1], 'SUBSTACK2': [2, c2]})
            ctx.blocks[c1]['parent'] = if_block
            ctx.blocks[c2]['parent'] = if_block
            ctx.chain([u_hat, if_block, u_front, u_show])
        elif var_name == 'v_uv':
            cond = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'UV_ACTIVE', 'v_uv'], [10, '']], 'OPERAND2': [1, [10, '1']]})
            c1 = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, [4, c_act]]})
            c2 = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, [4, c_norm]]})
            if_block = ctx.add('control_if_else', inputs={'CONDITION': [2, cond], 'SUBSTACK': [2, c1], 'SUBSTACK2': [2, c2]})
            ctx.blocks[c1]['parent'] = if_block
            ctx.blocks[c2]['parent'] = if_block
            ctx.chain([u_hat, if_block, u_front, u_show])
        elif var_name == 'v_freeze':
            cond = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'TIME_FROZEN', 'v_freeze'], [10, '']], 'OPERAND2': [1, [10, '1']]})
            c1 = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, [4, c_act]]})
            c2 = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, [4, c_norm]]})
            if_block = ctx.add('control_if_else', inputs={'CONDITION': [2, cond], 'SUBSTACK': [2, c1], 'SUBSTACK2': [2, c2]})
            ctx.blocks[c1]['parent'] = if_block
            ctx.blocks[c2]['parent'] = if_block
            ctx.chain([u_hat, if_block, u_front, u_show])
        elif var_name == 'v_compendium':
            cond = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'SHOW_COMPENDIUM', 'v_compendium'], [10, '']], 'OPERAND2': [1, [10, '1']]})
            c1 = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, [4, c_act]]})
            c2 = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, [4, c_norm]]})
            if_block = ctx.add('control_if_else', inputs={'CONDITION': [2, cond], 'SUBSTACK': [2, c1], 'SUBSTACK2': [2, c2]})
            ctx.blocks[c1]['parent'] = if_block
            ctx.blocks[c2]['parent'] = if_block
            ctx.chain([u_hat, if_block, u_front, u_show])
        elif var_name == 'v_volume':
            cond = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'MASTER_VOLUME', 'v_volume'], [10, '']], 'OPERAND2': [1, [10, '0']]})
            c1 = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, [4, c_act]]})
            c2 = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, [4, c_norm]]})
            if_block = ctx.add('control_if_else', inputs={'CONDITION': [2, cond], 'SUBSTACK': [2, c1], 'SUBSTACK2': [2, c2]})
            ctx.blocks[c1]['parent'] = if_block
            ctx.blocks[c2]['parent'] = if_block
            ctx.chain([u_hat, if_block, u_front, u_show])
        elif var_name == 'v_onboarding':
            cond = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'SHOW_ONBOARDING', 'v_onboarding'], [10, '']], 'OPERAND2': [1, [10, '1']]})
            c1 = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, [4, c_act]]})
            c2 = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, [4, c_norm]]})
            if_block = ctx.add('control_if_else', inputs={'CONDITION': [2, cond], 'SUBSTACK': [2, c1], 'SUBSTACK2': [2, c2]})
            ctx.blocks[c1]['parent'] = if_block
            ctx.blocks[c2]['parent'] = if_block
            ctx.chain([u_hat, if_block, u_front, u_show])
        else:
            c1 = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, [4, c_norm]]})
            ctx.chain([u_hat, c1, u_front, u_show])

        # 3. Click
        c_hat = ctx.add('event_whenthisspriteclicked', topLevel=True, x=50, y=450)
        snd_m = ctx.add('sound_sounds_menu', fields={'SOUND_MENU': [snd_name, None]}, shadow=True)
        p_snd = ctx.add('sound_play', inputs={'SOUND_MENU': [1, snd_m]})
        if act_type == 'toggle_palette':
            inv_p = ctx.add('operator_subtract', inputs={'NUM1': [1, [4, '1']], 'NUM2': [3, [12, 'SHOW_PALETTE', 'v_palette'], [4, '0']]})
            s_p = ctx.add('data_setvariableto', fields={'VARIABLE': ['SHOW_PALETTE', 'v_palette']}, inputs={'VALUE': [3, inv_p, [4, '0']]})
            bc = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'UPDATE_UI', 'b_update_ui']]})
            ctx.chain([c_hat, s_p, bc, p_snd])
        elif act_type == 'toggle_delete':
            is_d = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'CURRENT_TOOL', 'v_tool'], [10, '']], 'OPERAND2': [1, [10, 'delete']]})
            s_drag = ctx.add('data_setvariableto', fields={'VARIABLE': ['CURRENT_TOOL', 'v_tool']}, inputs={'VALUE': [1, [10, 'drag']]})
            s_del = ctx.add('data_setvariableto', fields={'VARIABLE': ['CURRENT_TOOL', 'v_tool']}, inputs={'VALUE': [1, [10, 'delete']]})
            if_d = ctx.add('control_if_else', inputs={'CONDITION': [2, is_d], 'SUBSTACK': [2, s_drag], 'SUBSTACK2': [2, s_del]})
            ctx.blocks[s_drag]['parent'] = if_d
            ctx.blocks[s_del]['parent'] = if_d
            bc = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'UPDATE_UI', 'b_update_ui']]})
            ctx.chain([c_hat, if_d, bc, p_snd])
        elif act_type == 'toggle_inspect':
            is_i = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'CURRENT_TOOL', 'v_tool'], [10, '']], 'OPERAND2': [1, [10, 'inspect']]})
            s_drag = ctx.add('data_setvariableto', fields={'VARIABLE': ['CURRENT_TOOL', 'v_tool']}, inputs={'VALUE': [1, [10, 'drag']]})
            s_insp = ctx.add('data_setvariableto', fields={'VARIABLE': ['CURRENT_TOOL', 'v_tool']}, inputs={'VALUE': [1, [10, 'inspect']]})
            if_i = ctx.add('control_if_else', inputs={'CONDITION': [2, is_i], 'SUBSTACK': [2, s_drag], 'SUBSTACK2': [2, s_insp]})
            ctx.blocks[s_drag]['parent'] = if_i
            ctx.blocks[s_insp]['parent'] = if_i
            bc = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'UPDATE_UI', 'b_update_ui']]})
            ctx.chain([c_hat, if_i, bc, p_snd])
        elif act_type == 'toggle_uv':
            inv_u = ctx.add('operator_subtract', inputs={'NUM1': [1, [4, '1']], 'NUM2': [3, [12, 'UV_ACTIVE', 'v_uv'], [4, '0']]})
            s_u = ctx.add('data_setvariableto', fields={'VARIABLE': ['UV_ACTIVE', 'v_uv']}, inputs={'VALUE': [3, inv_u, [4, '0']]})
            bc_bg = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'UPDATE_BACKDROP', 'b_update_bg']]})
            bc_u = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'UPDATE_UI', 'b_update_ui']]})
            ctx.chain([c_hat, s_u, bc_bg, bc_u, p_snd])
        elif act_type == 'toggle_freeze':
            inv_f = ctx.add('operator_subtract', inputs={'NUM1': [1, [4, '1']], 'NUM2': [3, [12, 'TIME_FROZEN', 'v_freeze'], [4, '0']]})
            s_f = ctx.add('data_setvariableto', fields={'VARIABLE': ['TIME_FROZEN', 'v_freeze']}, inputs={'VALUE': [3, inv_f, [4, '0']]})
            bc_bg = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'UPDATE_BACKDROP', 'b_update_bg']]})
            bc_u = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'UPDATE_UI', 'b_update_ui']]})
            ctx.chain([c_hat, s_f, bc_bg, bc_u, p_snd])
        elif act_type == 'toggle_compendium':
            inv_c = ctx.add('operator_subtract', inputs={'NUM1': [1, [4, '1']], 'NUM2': [3, [12, 'SHOW_COMPENDIUM', 'v_compendium'], [4, '0']]})
            s_c = ctx.add('data_setvariableto', fields={'VARIABLE': ['SHOW_COMPENDIUM', 'v_compendium']}, inputs={'VALUE': [3, inv_c, [4, '0']]})
            bc = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'UPDATE_UI', 'b_update_ui']]})
            ctx.chain([c_hat, s_c, bc, p_snd])
        elif act_type == 'toggle_audio':
            is_z = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'MASTER_VOLUME', 'v_volume'], [10, '']], 'OPERAND2': [1, [10, '0']]})
            s_100 = ctx.add('data_setvariableto', fields={'VARIABLE': ['MASTER_VOLUME', 'v_volume']}, inputs={'VALUE': [1, [4, '100']]})
            s_0 = ctx.add('data_setvariableto', fields={'VARIABLE': ['MASTER_VOLUME', 'v_volume']}, inputs={'VALUE': [1, [4, '0']]})
            if_v = ctx.add('control_if_else', inputs={'CONDITION': [2, is_z], 'SUBSTACK': [2, s_100], 'SUBSTACK2': [2, s_0]})
            ctx.blocks[s_100]['parent'] = if_v
            ctx.blocks[s_0]['parent'] = if_v
            bc = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'UPDATE_UI', 'b_update_ui']]})
            ctx.chain([c_hat, if_v, bc, p_snd])
        elif act_type == 'broadcast_save':
            bc = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'PROMPT_SAVE_LOAD', 'b_prompt_save']]})
            ctx.chain([c_hat, bc, p_snd])
        elif act_type == 'toggle_onboarding':
            inv_o = ctx.add('operator_subtract', inputs={'NUM1': [1, [4, '1']], 'NUM2': [3, [12, 'SHOW_ONBOARDING', 'v_onboarding'], [4, '0']]})
            s_o = ctx.add('data_setvariableto', fields={'VARIABLE': ['SHOW_ONBOARDING', 'v_onboarding']}, inputs={'VALUE': [3, inv_o, [4, '0']]})
            bc_o = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'SHOW_ONBOARDING', 'b_show_onb']]})
            bc_u = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'UPDATE_UI', 'b_update_ui']]})
            ctx.chain([c_hat, s_o, bc_o, bc_u, p_snd])
        elif act_type == 'broadcast_purge':
            bc = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'CLEAR_ALL', 'b_clear_all']]})
            ctx.chain([c_hat, bc, p_snd])

        costumes = [ASSETS[c_norm], ASSETS[c_act]]
        sounds = [sound_meta[snd_name]]
        sprites.append(make_sprite(name, costumes, sounds, ctx.blocks, visible=True, x=x, y=144))
    return sprites

# 8. PaletteUI Chassis & 19 Independent Element Selector Sprites
def build_palette_ui(ASSETS=costume_meta):
    ctx = BlockContext()
    hat_gf = ctx.add('event_whenflagclicked', topLevel=True, x=50, y=50)
    goto_pos = ctx.add('motion_gotoxy', inputs={'X': [1, [4, '0']], 'Y': [1, [4, '-125']]})
    hide_it = ctx.add('looks_hide')
    ctx.chain([hat_gf, goto_pos, hide_it])

    hat_upd = ctx.add('event_whenbroadcastreceived', fields={'BROADCAST_OPTION': ['UPDATE_UI', 'b_update_ui']}, topLevel=True, x=50, y=200)
    pal_act = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'SHOW_PALETTE', 'v_palette'], [10, '']], 'OPERAND2': [1, [10, '1']]})
    front_b = ctx.add('looks_gotofrontback', fields={'FRONT_BACK': ['front']})
    show_b = ctx.add('looks_show')
    ctx.chain([front_b, show_b])
    hide_upd = ctx.add('looks_hide')
    if_pal = ctx.add('control_if_else', inputs={'CONDITION': [2, pal_act], 'SUBSTACK': [2, front_b], 'SUBSTACK2': [2, hide_upd]})
    ctx.blocks[front_b]['parent'] = if_pal
    ctx.blocks[hide_upd]['parent'] = if_pal
    ctx.chain([hat_upd, if_pal])

    # Fallback coordinate check handler on drawer chassis for compatibility
    hat_click = ctx.add('event_whenthisspriteclicked', topLevel=True, x=50, y=400)
    mx = ctx.add('sensing_mousex')
    calc_c1 = ctx.add('operator_divide', inputs={'NUM1': [3, ctx.add('operator_add', inputs={'NUM1': [3, mx, [10, '0']], 'NUM2': [1, [4, '216']]}), [4, '0']], 'NUM2': [1, [4, '44']]})
    flr1 = ctx.add('operator_mathop', fields={'OPERATOR': ['floor', None]}, inputs={'NUM': [3, calc_c1, [4, '0']]})
    col1 = ctx.add('operator_add', inputs={'NUM1': [3, flr1, [4, '0']], 'NUM2': [1, [4, '1']]})
    s_col = ctx.add('data_setvariableto', fields={'VARIABLE': ['calc_col', 'v_pal_col']}, inputs={'VALUE': [3, col1, [4, '1']]})

    my = ctx.add('sensing_mousey')
    is_r1 = ctx.add('operator_gt', inputs={'OPERAND1': [3, my, [10, '0']], 'OPERAND2': [1, [10, '-135']]})
    s_sp1 = ctx.add('data_setvariableto', fields={'VARIABLE': ['SPAWN_SPECIES_ID', 'v_spawn_id']}, inputs={'VALUE': [3, [12, 'calc_col', 'v_pal_col'], [4, '1']]})

    calc_c2 = ctx.add('operator_divide', inputs={'NUM1': [3, ctx.add('operator_add', inputs={'NUM1': [3, mx, [10, '0']], 'NUM2': [1, [4, '194']]}), [4, '0']], 'NUM2': [1, [4, '44']]})
    flr2 = ctx.add('operator_mathop', fields={'OPERATOR': ['floor', None]}, inputs={'NUM': [3, calc_c2, [4, '0']]})
    col2 = ctx.add('operator_add', inputs={'NUM1': [3, flr2, [4, '0']], 'NUM2': [1, [4, '11']]})
    s_sp2 = ctx.add('data_setvariableto', fields={'VARIABLE': ['SPAWN_SPECIES_ID', 'v_spawn_id']}, inputs={'VALUE': [3, col2, [4, '11']]})

    if_row = ctx.add('control_if_else', inputs={'CONDITION': [2, is_r1], 'SUBSTACK': [2, s_sp1], 'SUBSTACK2': [2, s_sp2]})
    ctx.blocks[s_sp1]['parent'] = if_row
    ctx.blocks[s_sp2]['parent'] = if_row

    rx = ctx.add('operator_random', inputs={'FROM': [1, [4, '-100']], 'TO': [1, [4, '100']]})
    s_rx = ctx.add('data_setvariableto', fields={'VARIABLE': ['SPAWN_X', 'v_spawn_x']}, inputs={'VALUE': [3, rx, [4, '0']]})
    ry = ctx.add('operator_random', inputs={'FROM': [1, [4, '-60']], 'TO': [1, [4, '40']]})
    s_ry = ctx.add('data_setvariableto', fields={'VARIABLE': ['SPAWN_Y', 'v_spawn_y']}, inputs={'VALUE': [3, ry, [4, '0']]})
    bc_sp = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'SPAWN_REQUEST', 'b_spawn_req']]})
    snd_m = ctx.add('sound_sounds_menu', fields={'SOUND_MENU': ['snd_click', None]}, shadow=True)
    p_snd = ctx.add('sound_play', inputs={'SOUND_MENU': [1, snd_m]})
    ctx.chain([hat_click, s_col, if_row, s_rx, s_ry, bc_sp, p_snd])

    pal_vars = {'v_pal_col': ['calc_col', 1]}
    pal_costume = ASSETS.get('palette_drawer', ASSETS.get('palette_drawer_frame'))
    return {
        'isStage': False,
        'name': 'PaletteUI',
        'variables': pal_vars,
        'lists': {},
        'broadcasts': {},
        'blocks': ctx.blocks,
        'comments': {},
        'currentCostume': 0,
        'costumes': [pal_costume],
        'sounds': [sound_meta['snd_click']],
        'volume': 100,
        'visible': False,
        'x': 0, 'y': -125, 'size': 100, 'direction': 90,
        'draggable': False, 'rotationStyle': "don't rotate"
    }

def build_all_palette_items(ASSETS=costume_meta):
    sprites = []
    for i in range(19):
        sid = i + 1
        if i < 10:
            x = -196 + i * 44
            y = -116
        else:
            x = -174 + (i - 10) * 44
            y = -154

        ctx = BlockContext()
        f_hat = ctx.add('event_whenflagclicked', topLevel=True, x=50, y=50)
        f_goto = ctx.add('motion_gotoxy', inputs={'X': [1, [4, str(x)]], 'Y': [1, [4, str(y)]]})
        f_hide = ctx.add('looks_hide')
        ctx.chain([f_hat, f_goto, f_hide])

        u_hat = ctx.add('event_whenbroadcastreceived', fields={'BROADCAST_OPTION': ['UPDATE_UI', 'b_update_ui']}, topLevel=True, x=50, y=200)
        pal_act = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'SHOW_PALETTE', 'v_palette'], [10, '']], 'OPERAND2': [1, [10, '1']]})
        u_front = ctx.add('looks_gotofrontback', fields={'FRONT_BACK': ['front']})
        u_show = ctx.add('looks_show')
        ctx.chain([u_front, u_show])
        u_hide = ctx.add('looks_hide')
        if_pal = ctx.add('control_if_else', inputs={'CONDITION': [2, pal_act], 'SUBSTACK': [2, u_front], 'SUBSTACK2': [2, u_hide]})
        ctx.blocks[u_front]['parent'] = if_pal
        ctx.blocks[u_hide]['parent'] = if_pal
        ctx.chain([u_hat, if_pal])

        c_hat = ctx.add('event_whenthisspriteclicked', topLevel=True, x=50, y=400)
        s_sid = ctx.add('data_setvariableto', fields={'VARIABLE': ['SPAWN_SPECIES_ID', 'v_spawn_id']}, inputs={'VALUE': [1, [4, str(sid)]]})
        rx = ctx.add('operator_random', inputs={'FROM': [1, [4, '-100']], 'TO': [1, [4, '100']]})
        s_rx = ctx.add('data_setvariableto', fields={'VARIABLE': ['SPAWN_X', 'v_spawn_x']}, inputs={'VALUE': [3, rx, [4, '0']]})
        ry = ctx.add('operator_random', inputs={'FROM': [1, [4, '-60']], 'TO': [1, [4, '40']]})
        s_ry = ctx.add('data_setvariableto', fields={'VARIABLE': ['SPAWN_Y', 'v_spawn_y']}, inputs={'VALUE': [3, ry, [4, '0']]})
        bc_sp = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'SPAWN_REQUEST', 'b_spawn_req']]})
        snd_m = ctx.add('sound_sounds_menu', fields={'SOUND_MENU': ['snd_click', None]}, shadow=True)
        p_snd = ctx.add('sound_play', inputs={'SOUND_MENU': [1, snd_m]})
        ctx.chain([c_hat, s_sid, s_rx, s_ry, bc_sp, p_snd])

        costume = ASSETS[f'pal_card_{sid}']
        sprites.append(make_sprite(f'PalItem_{sid}', [costume], [sound_meta['snd_click']], ctx.blocks, visible=False, x=x, y=y))
    return sprites

# 9. InspectorUI Builder (Selected Entity Inspector)
def build_inspector_ui():
    ctx = BlockContext()
    card_costumes = [costume_meta[f'card_{s["id"]}'] for s in db_chemistry.SPECIES]

    flag_id = ctx.add('event_whenflagclicked', topLevel=True, x=50, y=50)
    hide_info = ctx.add('looks_hide')
    goto_pos = ctx.add('motion_gotoxy', inputs={'X': [1, [4, '135']], 'Y': [1, [4, '10']]})
    ctx.chain([flag_id, hide_info, goto_pos])

    hat_info = ctx.add('event_whenbroadcastreceived', fields={'BROADCAST_OPTION': ['SHOW_INFO', 'b_show_info']}, topLevel=True, x=50, y=180)
    sw_card = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [3, ctx.add('operator_join', inputs={'STRING1': [1, [10, 'card_']], 'STRING2': [3, [12, 'INSPECT_SPECIES_ID', 'v_inspect_id'], [10, '']]}), [10, 'card_1']]})
    show_card = ctx.add('looks_show')
    front_card = ctx.add('looks_gotofrontback', fields={'FRONT_BACK': ['front', None]})
    ctx.chain([hat_info, sw_card, show_card, front_card])

    hat_upd = ctx.add('event_whenbroadcastreceived', fields={'BROADCAST_OPTION': ['UPDATE_UI', 'b_update_ui']}, topLevel=True, x=50, y=340)
    is_show = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'SHOW_INFO', 'v_info'], [10, '']], 'OPERAND2': [1, [10, '1']]})
    sw_card_u = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [3, ctx.add('operator_join', inputs={'STRING1': [1, [10, 'card_']], 'STRING2': [3, [12, 'INSPECT_SPECIES_ID', 'v_inspect_id'], [10, '']]}), [10, 'card_1']]})
    show_card_u = ctx.add('looks_show')
    ctx.chain([sw_card_u, show_card_u])
    hide_card_u = ctx.add('looks_hide')
    if_show_else = ctx.add('control_if_else', inputs={'CONDITION': [2, is_show], 'SUBSTACK': [2, sw_card_u], 'SUBSTACK2': [2, hide_card_u]})
    ctx.blocks[sw_card_u]['parent'] = if_show_else
    ctx.blocks[hide_card_u]['parent'] = if_show_else
    ctx.chain([hat_upd, if_show_else])

    # Click card to dismiss
    hat_click = ctx.add('event_whenthisspriteclicked', topLevel=True, x=50, y=520)
    set_hide = ctx.add('data_setvariableto', fields={'VARIABLE': ['SHOW_INFO', 'v_info']}, inputs={'VALUE': [1, [4, '0']]})
    hide_it = ctx.add('looks_hide')
    bc_upd = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'UPDATE_UI', 'b_update_ui']]})
    ctx.chain([hat_click, set_hide, hide_it, bc_upd])

    return {
        'isStage': False,
        'name': 'InspectorUI',
        'variables': {},
        'lists': {},
        'broadcasts': {},
        'blocks': ctx.blocks,
        'comments': {},
        'currentCostume': 0,
        'costumes': card_costumes,
        'sounds': [],
        'volume': 100,
        'visible': False,
        'x': 135, 'y': 10, 'size': 100, 'direction': 90,
        'draggable': False, 'rotationStyle': "don't rotate"
    }

# ==============================================================================
# 9. Compendium UI Sprite Builder
# ==============================================================================
def build_compendium_ui(ASSETS=costume_meta):
    ctx = BlockContext()

    comp_costumes = [
        ASSETS['comp_summary'],
        ASSETS['comp_elements'],
        ASSETS['comp_molecules_1'],
        ASSETS['comp_molecules_2'],
        ASSETS['comp_radicals'],
        ASSETS['comp_ions']
    ]
    comp_sounds = [sound_meta['snd_click'], sound_meta['snd_bond'], sound_meta['snd_delete']]

    # Green flag
    hat_gf = ctx.add('event_whenflagclicked', topLevel=True, x=50, y=50)
    set_comp_var = ctx.add('data_setvariableto', fields={'VARIABLE': ['SHOW_COMPENDIUM', 'v_compendium']}, inputs={'VALUE': [1, [4, '0']]})
    set_tab_var = ctx.add('data_setvariableto', fields={'VARIABLE': ['COMPENDIUM_TAB', 'v_comp_tab']}, inputs={'VALUE': [1, [4, '1']]})
    goto_center = ctx.add('motion_gotoxy', inputs={'X': [1, [4, '0']], 'Y': [1, [4, '0']]})
    set_size = ctx.add('looks_setsizeto', inputs={'SIZE': [1, [4, '100']]})
    hide_it = ctx.add('looks_hide')
    ctx.chain([hat_gf, set_comp_var, set_tab_var, goto_center, set_size, hide_it])

    # UPDATE_UI receiver: switch costume based on COMPENDIUM_TAB
    hat_upd = ctx.add('event_whenbroadcastreceived', fields={'BROADCAST_OPTION': ['UPDATE_UI', 'b_update_ui']}, topLevel=True, x=50, y=240)
    is_show = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'SHOW_COMPENDIUM', 'v_compendium'], [10, '']], 'OPERAND2': [1, [10, '1']]})

    c_sum = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, [4, 'comp_summary']]})
    c_elem = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, [4, 'comp_elements']]})
    c_mol1 = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, [4, 'comp_molecules_1']]})
    c_mol2 = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, [4, 'comp_molecules_2']]})
    c_rad = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, [4, 'comp_radicals']]})
    c_ion = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, [4, 'comp_ions']]})

    eq_5 = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'COMPENDIUM_TAB', 'v_comp_tab'], [10, '']], 'OPERAND2': [1, [10, '5']]})
    if_5 = ctx.add('control_if_else', inputs={'CONDITION': [2, eq_5], 'SUBSTACK': [2, c_rad], 'SUBSTACK2': [2, c_ion]})
    ctx.blocks[c_rad]['parent'] = if_5
    ctx.blocks[c_ion]['parent'] = if_5

    eq_4 = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'COMPENDIUM_TAB', 'v_comp_tab'], [10, '']], 'OPERAND2': [1, [10, '4']]})
    if_4 = ctx.add('control_if_else', inputs={'CONDITION': [2, eq_4], 'SUBSTACK': [2, c_mol2], 'SUBSTACK2': [2, if_5]})
    ctx.blocks[c_mol2]['parent'] = if_4
    ctx.blocks[if_5]['parent'] = if_4

    eq_3 = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'COMPENDIUM_TAB', 'v_comp_tab'], [10, '']], 'OPERAND2': [1, [10, '3']]})
    if_3 = ctx.add('control_if_else', inputs={'CONDITION': [2, eq_3], 'SUBSTACK': [2, c_mol1], 'SUBSTACK2': [2, if_4]})
    ctx.blocks[c_mol1]['parent'] = if_3
    ctx.blocks[if_4]['parent'] = if_3

    eq_2 = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'COMPENDIUM_TAB', 'v_comp_tab'], [10, '']], 'OPERAND2': [1, [10, '2']]})
    if_2 = ctx.add('control_if_else', inputs={'CONDITION': [2, eq_2], 'SUBSTACK': [2, c_elem], 'SUBSTACK2': [2, if_3]})
    ctx.blocks[c_elem]['parent'] = if_2
    ctx.blocks[if_3]['parent'] = if_2

    eq_1 = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'COMPENDIUM_TAB', 'v_comp_tab'], [10, '']], 'OPERAND2': [1, [10, '1']]})
    if_1 = ctx.add('control_if_else', inputs={'CONDITION': [2, eq_1], 'SUBSTACK': [2, c_sum], 'SUBSTACK2': [2, if_2]})
    ctx.blocks[c_sum]['parent'] = if_1
    ctx.blocks[if_2]['parent'] = if_1

    goto_front = ctx.add('looks_gotofrontback', fields={'FRONT_BACK': ['front']})
    show_it = ctx.add('looks_show')
    ctx.chain([if_1, goto_front, show_it])

    hide_comp = ctx.add('looks_hide')
    if_show_all = ctx.add('control_if_else', inputs={'CONDITION': [2, is_show], 'SUBSTACK': [2, if_1], 'SUBSTACK2': [2, hide_comp]})
    ctx.blocks[if_1]['parent'] = if_show_all
    ctx.blocks[hide_comp]['parent'] = if_show_all
    ctx.chain([hat_upd, if_show_all])

    # Interactive Click Handler: handles Close, Reset, Tab Bar, Category Jump, and Species Injections
    hat_click = ctx.add('event_whenthisspriteclicked', topLevel=True, x=50, y=600)
    mx_b = ctx.add('sensing_mousex')
    set_cx = ctx.add('data_setvariableto', fields={'VARIABLE': ['CLICK_X', 'v_click_x']}, inputs={'VALUE': [2, mx_b]})
    my_b = ctx.add('sensing_mousey')
    set_cy = ctx.add('data_setvariableto', fields={'VARIABLE': ['CLICK_Y', 'v_click_y']}, inputs={'VALUE': [2, my_b]})

    vx = [3, [12, 'CLICK_X', 'v_click_x'], [10, '']]
    vy = [3, [12, 'CLICK_Y', 'v_click_y'], [10, '']]

    # Close checks (Top-right [x] or Bottom-right [CLOSE CATALOG])
    gt_x180 = ctx.add('operator_gt', inputs={'OPERAND1': vx, 'OPERAND2': [1, [10, '180']]})
    gt_y95 = ctx.add('operator_gt', inputs={'OPERAND1': vy, 'OPERAND2': [1, [10, '95']]})
    is_top_close = ctx.add('operator_and', inputs={'OPERAND1': [2, gt_x180], 'OPERAND2': [2, gt_y95]})

    gt_x80 = ctx.add('operator_gt', inputs={'OPERAND1': vx, 'OPERAND2': [1, [10, '80']]})
    lt_y_m95 = ctx.add('operator_lt', inputs={'OPERAND1': vy, 'OPERAND2': [1, [10, '-95']]})
    is_bot_close = ctx.add('operator_and', inputs={'OPERAND1': [2, gt_x80], 'OPERAND2': [2, lt_y_m95]})

    is_close = ctx.add('operator_or', inputs={'OPERAND1': [2, is_top_close], 'OPERAND2': [2, is_bot_close]})

    set_hide_var = ctx.add('data_setvariableto', fields={'VARIABLE': ['SHOW_COMPENDIUM', 'v_compendium']}, inputs={'VALUE': [1, [4, '0']]})
    hide_sprite = ctx.add('looks_hide')
    bc_upd_c = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'UPDATE_UI', 'b_update_ui']]})
    snd_clk_m = ctx.add('sound_sounds_menu', fields={'SOUND_MENU': ['snd_click', None]}, shadow=True)
    play_clk_c = ctx.add('sound_play', inputs={'SOUND_MENU': [1, snd_clk_m]})
    ctx.chain([set_hide_var, hide_sprite, bc_upd_c, play_clk_c])

    # Reset button check (mouse x < -80 and mouse y < -95)
    lt_xm80 = ctx.add('operator_lt', inputs={'OPERAND1': vx, 'OPERAND2': [1, [10, '-80']]})
    is_reset_btn = ctx.add('operator_and', inputs={'OPERAND1': [2, lt_xm80], 'OPERAND2': [2, lt_y_m95]})
    bc_clear_r = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'CLEAR_ALL', 'b_clear_all']]})
    bc_upd_r = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'UPDATE_UI', 'b_update_ui']]})
    snd_del_m = ctx.add('sound_sounds_menu', fields={'SOUND_MENU': ['snd_delete', None]}, shadow=True)
    play_del_r = ctx.add('sound_play', inputs={'SOUND_MENU': [1, snd_del_m]})
    ctx.chain([bc_clear_r, bc_upd_r, play_del_r])

    # Tab Bar check (my > 65 and my < 95)
    gt_y65 = ctx.add('operator_gt', inputs={'OPERAND1': vy, 'OPERAND2': [1, [10, '65']]})
    lt_y95 = ctx.add('operator_lt', inputs={'OPERAND1': vy, 'OPERAND2': [1, [10, '95']]})
    is_tab_bar = ctx.add('operator_and', inputs={'OPERAND1': [2, gt_y65], 'OPERAND2': [2, lt_y95]})

    set_tab1 = ctx.add('data_setvariableto', fields={'VARIABLE': ['COMPENDIUM_TAB', 'v_comp_tab']}, inputs={'VALUE': [1, [4, '1']]})
    set_tab2 = ctx.add('data_setvariableto', fields={'VARIABLE': ['COMPENDIUM_TAB', 'v_comp_tab']}, inputs={'VALUE': [1, [4, '2']]})
    set_tab3 = ctx.add('data_setvariableto', fields={'VARIABLE': ['COMPENDIUM_TAB', 'v_comp_tab']}, inputs={'VALUE': [1, [4, '3']]})
    set_tab5 = ctx.add('data_setvariableto', fields={'VARIABLE': ['COMPENDIUM_TAB', 'v_comp_tab']}, inputs={'VALUE': [1, [4, '5']]})
    set_tab6 = ctx.add('data_setvariableto', fields={'VARIABLE': ['COMPENDIUM_TAB', 'v_comp_tab']}, inputs={'VALUE': [1, [4, '6']]})

    lt_x135 = ctx.add('operator_lt', inputs={'OPERAND1': vx, 'OPERAND2': [1, [10, '135']]})
    if_t5_6 = ctx.add('control_if_else', inputs={'CONDITION': [2, lt_x135], 'SUBSTACK': [2, set_tab5], 'SUBSTACK2': [2, set_tab6]})
    ctx.blocks[set_tab5]['parent'] = if_t5_6
    ctx.blocks[set_tab6]['parent'] = if_t5_6

    lt_x50 = ctx.add('operator_lt', inputs={'OPERAND1': vx, 'OPERAND2': [1, [10, '50']]})
    if_t3_4 = ctx.add('control_if_else', inputs={'CONDITION': [2, lt_x50], 'SUBSTACK': [2, set_tab3], 'SUBSTACK2': [2, if_t5_6]})
    ctx.blocks[set_tab3]['parent'] = if_t3_4
    ctx.blocks[if_t5_6]['parent'] = if_t3_4

    lt_xm40 = ctx.add('operator_lt', inputs={'OPERAND1': vx, 'OPERAND2': [1, [10, '-40']]})
    if_t2_3 = ctx.add('control_if_else', inputs={'CONDITION': [2, lt_xm40], 'SUBSTACK': [2, set_tab2], 'SUBSTACK2': [2, if_t3_4]})
    ctx.blocks[set_tab2]['parent'] = if_t2_3
    ctx.blocks[if_t3_4]['parent'] = if_t2_3

    lt_xm125 = ctx.add('operator_lt', inputs={'OPERAND1': vx, 'OPERAND2': [1, [10, '-125']]})
    if_t1_2 = ctx.add('control_if_else', inputs={'CONDITION': [2, lt_xm125], 'SUBSTACK': [2, set_tab1], 'SUBSTACK2': [2, if_t2_3]})
    ctx.blocks[set_tab1]['parent'] = if_t1_2
    ctx.blocks[if_t2_3]['parent'] = if_t1_2

    bc_upd_t = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'UPDATE_UI', 'b_update_ui']]})
    snd_clk_m2 = ctx.add('sound_sounds_menu', fields={'SOUND_MENU': ['snd_click', None]}, shadow=True)
    play_clk_t = ctx.add('sound_play', inputs={'SOUND_MENU': [1, snd_clk_m2]})
    ctx.chain([if_t1_2, bc_upd_t, play_clk_t])

    # Category jump in Tab 1 (Summary)
    is_tab_1 = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'COMPENDIUM_TAB', 'v_comp_tab'], [10, '']], 'OPERAND2': [1, [10, '1']]})
    gt_ym60 = ctx.add('operator_gt', inputs={'OPERAND1': vy, 'OPERAND2': [1, [10, '-60']]})
    lt_y45 = ctx.add('operator_lt', inputs={'OPERAND1': vy, 'OPERAND2': [1, [10, '45']]})
    in_cat_y = ctx.add('operator_and', inputs={'OPERAND1': [2, gt_ym60], 'OPERAND2': [2, lt_y45]})
    is_cat_jump = ctx.add('operator_and', inputs={'OPERAND1': [2, is_tab_1], 'OPERAND2': [2, in_cat_y]})

    set_cj2 = ctx.add('data_setvariableto', fields={'VARIABLE': ['COMPENDIUM_TAB', 'v_comp_tab']}, inputs={'VALUE': [1, [4, '2']]})
    set_cj3 = ctx.add('data_setvariableto', fields={'VARIABLE': ['COMPENDIUM_TAB', 'v_comp_tab']}, inputs={'VALUE': [1, [4, '3']]})
    set_cj5 = ctx.add('data_setvariableto', fields={'VARIABLE': ['COMPENDIUM_TAB', 'v_comp_tab']}, inputs={'VALUE': [1, [4, '5']]})
    set_cj6 = ctx.add('data_setvariableto', fields={'VARIABLE': ['COMPENDIUM_TAB', 'v_comp_tab']}, inputs={'VALUE': [1, [4, '6']]})

    lt_x110 = ctx.add('operator_lt', inputs={'OPERAND1': vx, 'OPERAND2': [1, [10, '110']]})
    if_cj5_6 = ctx.add('control_if_else', inputs={'CONDITION': [2, lt_x110], 'SUBSTACK': [2, set_cj5], 'SUBSTACK2': [2, set_cj6]})
    ctx.blocks[set_cj5]['parent'] = if_cj5_6
    ctx.blocks[set_cj6]['parent'] = if_cj5_6

    lt_x0 = ctx.add('operator_lt', inputs={'OPERAND1': vx, 'OPERAND2': [1, [10, '0']]})
    if_cj3_5 = ctx.add('control_if_else', inputs={'CONDITION': [2, lt_x0], 'SUBSTACK': [2, set_cj3], 'SUBSTACK2': [2, if_cj5_6]})
    ctx.blocks[set_cj3]['parent'] = if_cj3_5
    ctx.blocks[if_cj5_6]['parent'] = if_cj3_5

    lt_xm110 = ctx.add('operator_lt', inputs={'OPERAND1': vx, 'OPERAND2': [1, [10, '-110']]})
    if_cj2_3 = ctx.add('control_if_else', inputs={'CONDITION': [2, lt_xm110], 'SUBSTACK': [2, set_cj2], 'SUBSTACK2': [2, if_cj3_5]})
    ctx.blocks[set_cj2]['parent'] = if_cj2_3
    ctx.blocks[if_cj3_5]['parent'] = if_cj2_3

    bc_upd_cj = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'UPDATE_UI', 'b_update_ui']]})
    snd_clk_m3 = ctx.add('sound_sounds_menu', fields={'SOUND_MENU': ['snd_click', None]}, shadow=True)
    play_clk_cj = ctx.add('sound_play', inputs={'SOUND_MENU': [1, snd_clk_m3]})
    ctx.chain([if_cj2_3, bc_upd_cj, play_clk_cj])

    # Element Spawning in Tab 2 (Atoms)
    is_tab_2 = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'COMPENDIUM_TAB', 'v_comp_tab'], [10, '']], 'OPERAND2': [1, [10, '2']]})
    gt_y_m15 = ctx.add('operator_gt', inputs={'OPERAND1': vy, 'OPERAND2': [1, [10, '-15']]})
    lt_y53 = ctx.add('operator_lt', inputs={'OPERAND1': vy, 'OPERAND2': [1, [10, '53']]})
    in_r1_y = ctx.add('operator_and', inputs={'OPERAND1': [2, gt_y_m15], 'OPERAND2': [2, lt_y53]})
    is_el_r1 = ctx.add('operator_and', inputs={'OPERAND1': [2, is_tab_2], 'OPERAND2': [2, in_r1_y]})

    mx_s205 = ctx.add('operator_add', inputs={'NUM1': vx, 'NUM2': [1, [4, '205']]})
    col_raw1 = ctx.add('operator_divide', inputs={'NUM1': [3, mx_s205, [4, '0']], 'NUM2': [1, [4, '41']]})
    col_f1 = ctx.add('operator_mathop', fields={'OPERATOR': ['floor', None]}, inputs={'NUM': [3, col_raw1, [4, '0']]})
    col_id1 = ctx.add('operator_add', inputs={'NUM1': [3, col_f1, [4, '0']], 'NUM2': [1, [4, '1']]})

    gt_ym87 = ctx.add('operator_gt', inputs={'OPERAND1': vy, 'OPERAND2': [1, [10, '-87']]})
    lt_ym19 = ctx.add('operator_lt', inputs={'OPERAND1': vy, 'OPERAND2': [1, [10, '-19']]})
    in_r2_y = ctx.add('operator_and', inputs={'OPERAND1': [2, gt_ym87], 'OPERAND2': [2, lt_ym19]})
    is_el_r2 = ctx.add('operator_and', inputs={'OPERAND1': [2, is_tab_2], 'OPERAND2': [2, in_r2_y]})

    mx_s185 = ctx.add('operator_add', inputs={'NUM1': vx, 'NUM2': [1, [4, '185']]})
    col_raw2 = ctx.add('operator_divide', inputs={'NUM1': [3, mx_s185, [4, '0']], 'NUM2': [1, [4, '41']]})
    col_f2 = ctx.add('operator_mathop', fields={'OPERATOR': ['floor', None]}, inputs={'NUM': [3, col_raw2, [4, '0']]})
    col_id2 = ctx.add('operator_add', inputs={'NUM1': [3, col_f2, [4, '0']], 'NUM2': [1, [4, '11']]})

    set_spc_r1 = ctx.add('data_setvariableto', fields={'VARIABLE': ['SPAWN_SPECIES_ID', 'v_spawn_id']}, inputs={'VALUE': [3, col_id1, [4, '1']]})
    set_spc_r2 = ctx.add('data_setvariableto', fields={'VARIABLE': ['SPAWN_SPECIES_ID', 'v_spawn_id']}, inputs={'VALUE': [3, col_id2, [4, '11']]})

    rnd_sx1 = ctx.add('operator_random', inputs={'FROM': [1, [4, '-70']], 'TO': [1, [4, '70']]})
    set_sx1 = ctx.add('data_setvariableto', fields={'VARIABLE': ['SPAWN_X', 'v_spawn_x']}, inputs={'VALUE': [3, rnd_sx1, [4, '0']]})
    rnd_sy1 = ctx.add('operator_random', inputs={'FROM': [1, [4, '-20']], 'TO': [1, [4, '30']]})
    set_sy1 = ctx.add('data_setvariableto', fields={'VARIABLE': ['SPAWN_Y', 'v_spawn_y']}, inputs={'VALUE': [3, rnd_sy1, [4, '0']]})
    bc_spawn1 = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'SPAWN_REQUEST', 'b_spawn_req']]})
    set_insp1 = ctx.add('data_setvariableto', fields={'VARIABLE': ['INSPECT_SPECIES_ID', 'v_inspect_id']}, inputs={'VALUE': [3, [12, 'SPAWN_SPECIES_ID', 'v_spawn_id'], [4, '1']]})
    set_show_info1 = ctx.add('data_setvariableto', fields={'VARIABLE': ['SHOW_INFO', 'v_info']}, inputs={'VALUE': [1, [4, '1']]})
    bc_upd_s1 = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'UPDATE_UI', 'b_update_ui']]})
    snd_bnd_m1 = ctx.add('sound_sounds_menu', fields={'SOUND_MENU': ['snd_bond', None]}, shadow=True)
    play_bnd1 = ctx.add('sound_play', inputs={'SOUND_MENU': [1, snd_bnd_m1]})

    ctx.chain([set_spc_r1, set_sx1, set_sy1, bc_spawn1, set_insp1, set_show_info1, bc_upd_s1, play_bnd1])

    # Row 2 chain clone
    rnd_sx2 = ctx.add('operator_random', inputs={'FROM': [1, [4, '-70']], 'TO': [1, [4, '70']]})
    set_sx2 = ctx.add('data_setvariableto', fields={'VARIABLE': ['SPAWN_X', 'v_spawn_x']}, inputs={'VALUE': [3, rnd_sx2, [4, '0']]})
    rnd_sy2 = ctx.add('operator_random', inputs={'FROM': [1, [4, '-20']], 'TO': [1, [4, '30']]})
    set_sy2 = ctx.add('data_setvariableto', fields={'VARIABLE': ['SPAWN_Y', 'v_spawn_y']}, inputs={'VALUE': [3, rnd_sy2, [4, '0']]})
    bc_spawn2 = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'SPAWN_REQUEST', 'b_spawn_req']]})
    set_insp2 = ctx.add('data_setvariableto', fields={'VARIABLE': ['INSPECT_SPECIES_ID', 'v_inspect_id']}, inputs={'VALUE': [3, [12, 'SPAWN_SPECIES_ID', 'v_spawn_id'], [4, '11']]})
    set_show_info2 = ctx.add('data_setvariableto', fields={'VARIABLE': ['SHOW_INFO', 'v_info']}, inputs={'VALUE': [1, [4, '1']]})
    bc_upd_s2 = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'UPDATE_UI', 'b_update_ui']]})
    snd_bnd_m2 = ctx.add('sound_sounds_menu', fields={'SOUND_MENU': ['snd_bond', None]}, shadow=True)
    play_bnd2 = ctx.add('sound_play', inputs={'SOUND_MENU': [1, snd_bnd_m2]})
    ctx.chain([set_spc_r2, set_sx2, set_sy2, bc_spawn2, set_insp2, set_show_info2, bc_upd_s2, play_bnd2])

    if_r2_act = ctx.add('control_if', inputs={'CONDITION': [2, is_el_r2], 'SUBSTACK': [2, set_spc_r2]})
    ctx.blocks[set_spc_r2]['parent'] = if_r2_act

    if_el_act = ctx.add('control_if_else', inputs={'CONDITION': [2, is_el_r1], 'SUBSTACK': [2, set_spc_r1], 'SUBSTACK2': [2, if_r2_act]})
    ctx.blocks[set_spc_r1]['parent'] = if_el_act
    ctx.blocks[if_r2_act]['parent'] = if_el_act

    # Assemble master click dispatcher:
    # if is_close -> close
    # else if is_reset -> reset
    # else if is_tab_bar -> change tab
    # else if is_cat_jump -> jump category
    # else -> element actions
    if_action_cat = ctx.add('control_if_else', inputs={'CONDITION': [2, is_cat_jump], 'SUBSTACK': [2, if_cj2_3], 'SUBSTACK2': [2, if_el_act]})
    ctx.blocks[if_cj2_3]['parent'] = if_action_cat
    ctx.blocks[if_el_act]['parent'] = if_action_cat

    if_action_tb = ctx.add('control_if_else', inputs={'CONDITION': [2, is_tab_bar], 'SUBSTACK': [2, if_t1_2], 'SUBSTACK2': [2, if_action_cat]})
    ctx.blocks[if_t1_2]['parent'] = if_action_tb
    ctx.blocks[if_action_cat]['parent'] = if_action_tb

    if_action_rst = ctx.add('control_if_else', inputs={'CONDITION': [2, is_reset_btn], 'SUBSTACK': [2, bc_clear_r], 'SUBSTACK2': [2, if_action_tb]})
    ctx.blocks[bc_clear_r]['parent'] = if_action_rst
    ctx.blocks[if_action_tb]['parent'] = if_action_rst

    if_master_click = ctx.add('control_if_else', inputs={'CONDITION': [2, is_close], 'SUBSTACK': [2, set_hide_var], 'SUBSTACK2': [2, if_action_rst]})
    ctx.blocks[set_hide_var]['parent'] = if_master_click
    ctx.blocks[if_action_rst]['parent'] = if_master_click

    ctx.chain([hat_click, set_cx, set_cy, if_master_click])

    comp_vars = {
        'v_click_x': ['CLICK_X', 0],
        'v_click_y': ['CLICK_Y', 0]
    }

    return {
        'isStage': False,
        'name': 'CompendiumUI',
        'variables': comp_vars,
        'lists': {},
        'broadcasts': {},
        'blocks': ctx.blocks,
        'comments': {},
        'currentCostume': 0,
        'costumes': comp_costumes,
        'sounds': comp_sounds,
        'volume': 100,
        'visible': False,
        'x': 0, 'y': 0, 'size': 100, 'direction': 90,
        'draggable': False, 'rotationStyle': "don't rotate"
    }


# 9b. Compendium Independent Navigation Tab Sprites
def build_all_compendium_tabs(ASSETS=costume_meta):
    tab_defs = [
        ('CompTab_Overview', -167, 88, 1, 'tab_overview_inactive', 'tab_overview_active'),
        ('CompTab_Elements', -85, 88, 2, 'tab_elements_inactive', 'tab_elements_active'),
        ('CompTab_Molecules', 1, 88, 3, 'tab_molecules_inactive', 'tab_molecules_active'),
        ('CompTab_Radicals', 88, 88, 5, 'tab_radicals_inactive', 'tab_radicals_active'),
        ('CompTab_Ions', 169, 88, 6, 'tab_ions_inactive', 'tab_ions_active')
    ]
    sprites = []
    for name, x, y, tab_id, c_inact_name, c_act_name in tab_defs:
        ctx = BlockContext()
        f_hat = ctx.add('event_whenflagclicked', topLevel=True, x=50, y=50)
        f_goto = ctx.add('motion_gotoxy', inputs={'X': [1, [4, str(x)]], 'Y': [1, [4, str(y)]]})
        f_hide = ctx.add('looks_hide')
        ctx.chain([f_hat, f_goto, f_hide])

        u_hat = ctx.add('event_whenbroadcastreceived', fields={'BROADCAST_OPTION': ['UPDATE_UI', 'b_update_ui']}, topLevel=True, x=50, y=200)
        is_comp = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'SHOW_COMPENDIUM', 'v_compendium'], [10, '']], 'OPERAND2': [1, [10, '1']]})
        if tab_id == 3:
            is_t3 = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'COMPENDIUM_TAB', 'v_comp_tab'], [10, '']], 'OPERAND2': [1, [10, '3']]})
            is_t4 = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'COMPENDIUM_TAB', 'v_comp_tab'], [10, '']], 'OPERAND2': [1, [10, '4']]})
            is_act = ctx.add('operator_or', inputs={'OPERAND1': [2, is_t3], 'OPERAND2': [2, is_t4]})
        else:
            is_act = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'COMPENDIUM_TAB', 'v_comp_tab'], [10, '']], 'OPERAND2': [1, [10, str(tab_id)]]})

        c_act = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, [4, c_act_name]]})
        c_inact = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, [4, c_inact_name]]})
        if_act = ctx.add('control_if_else', inputs={'CONDITION': [2, is_act], 'SUBSTACK': [2, c_act], 'SUBSTACK2': [2, c_inact]})
        ctx.blocks[c_act]['parent'] = if_act
        ctx.blocks[c_inact]['parent'] = if_act

        u_front = ctx.add('looks_gotofrontback', fields={'FRONT_BACK': ['front']})
        u_show = ctx.add('looks_show')
        ctx.chain([if_act, u_front, u_show])

        u_hide = ctx.add('looks_hide')
        if_comp = ctx.add('control_if_else', inputs={'CONDITION': [2, is_comp], 'SUBSTACK': [2, if_act], 'SUBSTACK2': [2, u_hide]})
        ctx.blocks[if_act]['parent'] = if_comp
        ctx.blocks[u_hide]['parent'] = if_comp
        ctx.chain([u_hat, if_comp])

        c_hat = ctx.add('event_whenthisspriteclicked', topLevel=True, x=50, y=450)
        s_tab = ctx.add('data_setvariableto', fields={'VARIABLE': ['COMPENDIUM_TAB', 'v_comp_tab']}, inputs={'VALUE': [1, [4, str(tab_id)]]})
        bc_u = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'UPDATE_UI', 'b_update_ui']]})
        snd_m = ctx.add('sound_sounds_menu', fields={'SOUND_MENU': ['snd_click', None]}, shadow=True)
        p_snd = ctx.add('sound_play', inputs={'SOUND_MENU': [1, snd_m]})
        ctx.chain([c_hat, s_tab, bc_u, p_snd])

        costumes = [ASSETS[c_inact_name], ASSETS[c_act_name]]
        sprites.append(make_sprite(name, costumes, [sound_meta['snd_click']], ctx.blocks, visible=False, x=x, y=y))
    return sprites


# 9c. Compendium Action Buttons (Close X, Close Bottom, Reset)
def build_all_compendium_buttons(ASSETS=costume_meta):
    btn_defs = [
        ('CompBtn_CloseX', 197, 112, 'comp_btn_close_x', 'close', 'snd_click'),
        ('CompBtn_CloseBottom', 151, -111, 'comp_btn_close_bottom', 'close', 'snd_click'),
        ('CompBtn_Reset', -151, -111, 'comp_btn_reset', 'reset', 'snd_delete')
    ]
    sprites = []
    for name, x, y, c_name, action, snd_name in btn_defs:
        ctx = BlockContext()
        f_hat = ctx.add('event_whenflagclicked', topLevel=True, x=50, y=50)
        f_goto = ctx.add('motion_gotoxy', inputs={'X': [1, [4, str(x)]], 'Y': [1, [4, str(y)]]})
        f_hide = ctx.add('looks_hide')
        ctx.chain([f_hat, f_goto, f_hide])

        u_hat = ctx.add('event_whenbroadcastreceived', fields={'BROADCAST_OPTION': ['UPDATE_UI', 'b_update_ui']}, topLevel=True, x=50, y=200)
        is_comp = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'SHOW_COMPENDIUM', 'v_compendium'], [10, '']], 'OPERAND2': [1, [10, '1']]})
        u_front = ctx.add('looks_gotofrontback', fields={'FRONT_BACK': ['front']})
        u_show = ctx.add('looks_show')
        ctx.chain([u_front, u_show])
        u_hide = ctx.add('looks_hide')
        if_comp = ctx.add('control_if_else', inputs={'CONDITION': [2, is_comp], 'SUBSTACK': [2, u_front], 'SUBSTACK2': [2, u_hide]})
        ctx.blocks[u_front]['parent'] = if_comp
        ctx.blocks[u_hide]['parent'] = if_comp
        ctx.chain([u_hat, if_comp])

        c_hat = ctx.add('event_whenthisspriteclicked', topLevel=True, x=50, y=450)
        snd_m = ctx.add('sound_sounds_menu', fields={'SOUND_MENU': [snd_name, None]}, shadow=True)
        p_snd = ctx.add('sound_play', inputs={'SOUND_MENU': [1, snd_m]})
        if action == 'close':
            s_close = ctx.add('data_setvariableto', fields={'VARIABLE': ['SHOW_COMPENDIUM', 'v_compendium']}, inputs={'VALUE': [1, [4, '0']]})
            u_hide2 = ctx.add('looks_hide')
            bc_u = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'UPDATE_UI', 'b_update_ui']]})
            ctx.chain([c_hat, s_close, u_hide2, bc_u, p_snd])
        elif action == 'reset':
            bc_clr = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'CLEAR_ALL', 'b_clear_all']]})
            bc_u = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'UPDATE_UI', 'b_update_ui']]})
            ctx.chain([c_hat, bc_clr, bc_u, p_snd])

        sprites.append(make_sprite(name, [ASSETS[c_name]], [sound_meta[snd_name]], ctx.blocks, visible=False, x=x, y=y))
    return sprites


# 9d. Compendium Pagination Buttons (Next Page, Prev Page)
def build_all_compendium_pagination(ASSETS=costume_meta):
    p_defs = [
        ('CompBtn_NextPage', 163, 64, 'comp_btn_next', 3, 4),
        ('CompBtn_PrevPage', 85, 64, 'comp_btn_prev', 4, 3)
    ]
    sprites = []
    for name, x, y, c_name, active_tab, target_tab in p_defs:
        ctx = BlockContext()
        f_hat = ctx.add('event_whenflagclicked', topLevel=True, x=50, y=50)
        f_goto = ctx.add('motion_gotoxy', inputs={'X': [1, [4, str(x)]], 'Y': [1, [4, str(y)]]})
        f_hide = ctx.add('looks_hide')
        ctx.chain([f_hat, f_goto, f_hide])

        u_hat = ctx.add('event_whenbroadcastreceived', fields={'BROADCAST_OPTION': ['UPDATE_UI', 'b_update_ui']}, topLevel=True, x=50, y=200)
        is_comp = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'SHOW_COMPENDIUM', 'v_compendium'], [10, '']], 'OPERAND2': [1, [10, '1']]})
        is_tab = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'COMPENDIUM_TAB', 'v_comp_tab'], [10, '']], 'OPERAND2': [1, [10, str(active_tab)]]})
        both = ctx.add('operator_and', inputs={'OPERAND1': [2, is_comp], 'OPERAND2': [2, is_tab]})
        u_front = ctx.add('looks_gotofrontback', fields={'FRONT_BACK': ['front']})
        u_show = ctx.add('looks_show')
        ctx.chain([u_front, u_show])
        u_hide = ctx.add('looks_hide')
        if_show = ctx.add('control_if_else', inputs={'CONDITION': [2, both], 'SUBSTACK': [2, u_front], 'SUBSTACK2': [2, u_hide]})
        ctx.blocks[u_front]['parent'] = if_show
        ctx.blocks[u_hide]['parent'] = if_show
        ctx.chain([u_hat, if_show])

        c_hat = ctx.add('event_whenthisspriteclicked', topLevel=True, x=50, y=450)
        s_tab = ctx.add('data_setvariableto', fields={'VARIABLE': ['COMPENDIUM_TAB', 'v_comp_tab']}, inputs={'VALUE': [1, [4, str(target_tab)]]})
        bc_u = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'UPDATE_UI', 'b_update_ui']]})
        snd_m = ctx.add('sound_sounds_menu', fields={'SOUND_MENU': ['snd_click', None]}, shadow=True)
        p_snd = ctx.add('sound_play', inputs={'SOUND_MENU': [1, snd_m]})
        ctx.chain([c_hat, s_tab, bc_u, p_snd])

        sprites.append(make_sprite(name, [ASSETS[c_name]], [sound_meta['snd_click']], ctx.blocks, visible=False, x=x, y=y))
    return sprites


# 9e. Compendium Category Jump Cards (Overview Tab 1)
def build_all_compendium_categories(ASSETS=costume_meta):
    cat_defs = [
        ('CompCatCard_Atoms', -157, -27, 'comp_cat_atoms', 2),
        ('CompCatCard_Molecules', -53, -27, 'comp_cat_molecules', 3),
        ('CompCatCard_Radicals', 51, -27, 'comp_cat_radicals', 5),
        ('CompCatCard_Ions', 155, -27, 'comp_cat_ions', 6)
    ]
    sprites = []
    for name, x, y, c_name, target_tab in cat_defs:
        ctx = BlockContext()
        f_hat = ctx.add('event_whenflagclicked', topLevel=True, x=50, y=50)
        f_goto = ctx.add('motion_gotoxy', inputs={'X': [1, [4, str(x)]], 'Y': [1, [4, str(y)]]})
        f_hide = ctx.add('looks_hide')
        ctx.chain([f_hat, f_goto, f_hide])

        u_hat = ctx.add('event_whenbroadcastreceived', fields={'BROADCAST_OPTION': ['UPDATE_UI', 'b_update_ui']}, topLevel=True, x=50, y=200)
        is_comp = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'SHOW_COMPENDIUM', 'v_compendium'], [10, '']], 'OPERAND2': [1, [10, '1']]})
        is_tab1 = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'COMPENDIUM_TAB', 'v_comp_tab'], [10, '']], 'OPERAND2': [1, [10, '1']]})
        both = ctx.add('operator_and', inputs={'OPERAND1': [2, is_comp], 'OPERAND2': [2, is_tab1]})
        u_front = ctx.add('looks_gotofrontback', fields={'FRONT_BACK': ['front']})
        u_show = ctx.add('looks_show')
        ctx.chain([u_front, u_show])
        u_hide = ctx.add('looks_hide')
        if_show = ctx.add('control_if_else', inputs={'CONDITION': [2, both], 'SUBSTACK': [2, u_front], 'SUBSTACK2': [2, u_hide]})
        ctx.blocks[u_front]['parent'] = if_show
        ctx.blocks[u_hide]['parent'] = if_show
        ctx.chain([u_hat, if_show])

        c_hat = ctx.add('event_whenthisspriteclicked', topLevel=True, x=50, y=450)
        s_tab = ctx.add('data_setvariableto', fields={'VARIABLE': ['COMPENDIUM_TAB', 'v_comp_tab']}, inputs={'VALUE': [1, [4, str(target_tab)]]})
        bc_u = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'UPDATE_UI', 'b_update_ui']]})
        snd_m = ctx.add('sound_sounds_menu', fields={'SOUND_MENU': ['snd_click', None]}, shadow=True)
        p_snd = ctx.add('sound_play', inputs={'SOUND_MENU': [1, snd_m]})
        ctx.chain([c_hat, s_tab, bc_u, p_snd])

        sprites.append(make_sprite(name, [ASSETS[c_name]], [sound_meta['snd_click']], ctx.blocks, visible=False, x=x, y=y))
    return sprites


# 9f. Compendium Base Element Cards (Elements Tab 2)
def build_all_compendium_element_cards(ASSETS=costume_meta):
    sprites = []
    for sid in range(1, 20):
        if sid <= 10:
            x = -185 + (sid - 1) * 41
            y = 19
        else:
            x = -164 + (sid - 11) * 41
            y = -53

        ctx = BlockContext()
        f_hat = ctx.add('event_whenflagclicked', topLevel=True, x=50, y=50)
        f_goto = ctx.add('motion_gotoxy', inputs={'X': [1, [4, str(x)]], 'Y': [1, [4, str(y)]]})
        f_hide = ctx.add('looks_hide')
        ctx.chain([f_hat, f_goto, f_hide])

        u_hat = ctx.add('event_whenbroadcastreceived', fields={'BROADCAST_OPTION': ['UPDATE_UI', 'b_update_ui']}, topLevel=True, x=50, y=200)
        is_comp = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'SHOW_COMPENDIUM', 'v_compendium'], [10, '']], 'OPERAND2': [1, [10, '1']]})
        is_tab2 = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'COMPENDIUM_TAB', 'v_comp_tab'], [10, '']], 'OPERAND2': [1, [10, '2']]})
        both = ctx.add('operator_and', inputs={'OPERAND1': [2, is_comp], 'OPERAND2': [2, is_tab2]})
        u_front = ctx.add('looks_gotofrontback', fields={'FRONT_BACK': ['front']})
        u_show = ctx.add('looks_show')
        ctx.chain([u_front, u_show])
        u_hide = ctx.add('looks_hide')
        if_show = ctx.add('control_if_else', inputs={'CONDITION': [2, both], 'SUBSTACK': [2, u_front], 'SUBSTACK2': [2, u_hide]})
        ctx.blocks[u_front]['parent'] = if_show
        ctx.blocks[u_hide]['parent'] = if_show
        ctx.chain([u_hat, if_show])

        c_hat = ctx.add('event_whenthisspriteclicked', topLevel=True, x=50, y=450)
        s_sid = ctx.add('data_setvariableto', fields={'VARIABLE': ['SPAWN_SPECIES_ID', 'v_spawn_id']}, inputs={'VALUE': [1, [4, str(sid)]]})
        rx = ctx.add('operator_random', inputs={'FROM': [1, [4, '-70']], 'TO': [1, [4, '70']]})
        s_rx = ctx.add('data_setvariableto', fields={'VARIABLE': ['SPAWN_X', 'v_spawn_x']}, inputs={'VALUE': [3, rx, [4, '0']]})
        ry = ctx.add('operator_random', inputs={'FROM': [1, [4, '-20']], 'TO': [1, [4, '30']]})
        s_ry = ctx.add('data_setvariableto', fields={'VARIABLE': ['SPAWN_Y', 'v_spawn_y']}, inputs={'VALUE': [3, ry, [4, '0']]})
        bc_sp = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'SPAWN_REQUEST', 'b_spawn_req']]})
        s_insp = ctx.add('data_setvariableto', fields={'VARIABLE': ['INSPECT_SPECIES_ID', 'v_inspect_id']}, inputs={'VALUE': [1, [4, str(sid)]]})
        s_info = ctx.add('data_setvariableto', fields={'VARIABLE': ['SHOW_INFO', 'v_info']}, inputs={'VALUE': [1, [4, '1']]})
        bc_u = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'UPDATE_UI', 'b_update_ui']]})
        snd_m = ctx.add('sound_sounds_menu', fields={'SOUND_MENU': ['snd_bond', None]}, shadow=True)
        p_snd = ctx.add('sound_play', inputs={'SOUND_MENU': [1, snd_m]})
        ctx.chain([c_hat, s_sid, s_rx, s_ry, bc_sp, s_insp, s_info, bc_u, p_snd])

        c_name = f'comp_elem_card_{sid}'
        sprites.append(make_sprite(f'CompCard_Elem_{sid}', [ASSETS[c_name]], [sound_meta['snd_bond']], ctx.blocks, visible=False, x=x, y=y))
    return sprites


# 9g. Compendium Chemical Species Cards (Molecules, Radicals, Ions)
def build_all_compendium_species_cards(ASSETS=costume_meta):
    tab_configs = [
        ("mol1", [20, 21, 22, 25, 39, 40, 44, 47], 3),
        ("mol2", [30, 32, 57, 58, 60, 71, 85, 106], 4),
        ("rad", [41, 42, 43, 28, 46, 29, 27, 56], 5),
        ("ion", [109, 111, 118, 117, 123, 124, 119, 129], 6)
    ]
    card_cols = [-157, -53, 51, 155]
    card_rows = [17, -55]
    sprites = []
    for prefix, ids, target_tab in tab_configs:
        for idx, sid in enumerate(ids):
            x = card_cols[idx % 4]
            y = card_rows[idx // 4]

            ctx = BlockContext()
            f_hat = ctx.add('event_whenflagclicked', topLevel=True, x=50, y=50)
            f_goto = ctx.add('motion_gotoxy', inputs={'X': [1, [4, str(x)]], 'Y': [1, [4, str(y)]]})
            f_hide = ctx.add('looks_hide')
            ctx.chain([f_hat, f_goto, f_hide])

            u_hat = ctx.add('event_whenbroadcastreceived', fields={'BROADCAST_OPTION': ['UPDATE_UI', 'b_update_ui']}, topLevel=True, x=50, y=200)
            is_comp = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'SHOW_COMPENDIUM', 'v_compendium'], [10, '']], 'OPERAND2': [1, [10, '1']]})
            is_tab = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'COMPENDIUM_TAB', 'v_comp_tab'], [10, '']], 'OPERAND2': [1, [10, str(target_tab)]]})
            both = ctx.add('operator_and', inputs={'OPERAND1': [2, is_comp], 'OPERAND2': [2, is_tab]})
            u_front = ctx.add('looks_gotofrontback', fields={'FRONT_BACK': ['front']})
            u_show = ctx.add('looks_show')
            ctx.chain([u_front, u_show])
            u_hide = ctx.add('looks_hide')
            if_show = ctx.add('control_if_else', inputs={'CONDITION': [2, both], 'SUBSTACK': [2, u_front], 'SUBSTACK2': [2, u_hide]})
            ctx.blocks[u_front]['parent'] = if_show
            ctx.blocks[u_hide]['parent'] = if_show
            ctx.chain([u_hat, if_show])

            c_hat = ctx.add('event_whenthisspriteclicked', topLevel=True, x=50, y=450)
            s_sid = ctx.add('data_setvariableto', fields={'VARIABLE': ['SPAWN_SPECIES_ID', 'v_spawn_id']}, inputs={'VALUE': [1, [4, str(sid)]]})
            rx = ctx.add('operator_random', inputs={'FROM': [1, [4, '-70']], 'TO': [1, [4, '70']]})
            s_rx = ctx.add('data_setvariableto', fields={'VARIABLE': ['SPAWN_X', 'v_spawn_x']}, inputs={'VALUE': [3, rx, [4, '0']]})
            ry = ctx.add('operator_random', inputs={'FROM': [1, [4, '-20']], 'TO': [1, [4, '30']]})
            s_ry = ctx.add('data_setvariableto', fields={'VARIABLE': ['SPAWN_Y', 'v_spawn_y']}, inputs={'VALUE': [3, ry, [4, '0']]})
            bc_sp = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'SPAWN_REQUEST', 'b_spawn_req']]})
            s_insp = ctx.add('data_setvariableto', fields={'VARIABLE': ['INSPECT_SPECIES_ID', 'v_inspect_id']}, inputs={'VALUE': [1, [4, str(sid)]]})
            s_info = ctx.add('data_setvariableto', fields={'VARIABLE': ['SHOW_INFO', 'v_info']}, inputs={'VALUE': [1, [4, '1']]})
            bc_u = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'UPDATE_UI', 'b_update_ui']]})
            snd_m = ctx.add('sound_sounds_menu', fields={'SOUND_MENU': ['snd_bond', None]}, shadow=True)
            p_snd = ctx.add('sound_play', inputs={'SOUND_MENU': [1, snd_m]})
            ctx.chain([c_hat, s_sid, s_rx, s_ry, bc_sp, s_insp, s_info, bc_u, p_snd])

            c_name = f'comp_{prefix}_card_{sid}'
            sprite_name = f'CompCard_{prefix.capitalize()}_{sid}'
            sprites.append(make_sprite(sprite_name, [ASSETS[c_name]], [sound_meta['snd_bond']], ctx.blocks, visible=False, x=x, y=y))
    return sprites


# ==============================================================================
# 10. Onboarding UI Sprite Builder
# ==============================================================================
def build_onboarding_ui(ASSETS=costume_meta):
    ctx = BlockContext()

    onb_costume = [ASSETS['onboarding_card']]

    # Green flag
    hat_gf = ctx.add('event_whenflagclicked', topLevel=True, x=50, y=50)
    goto_center = ctx.add('motion_gotoxy', inputs={'X': [1, [4, '0']], 'Y': [1, [4, '0']]})
    set_size = ctx.add('looks_setsizeto', inputs={'SIZE': [1, [4, '100']]})
    is_show = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'SHOW_ONBOARDING', 'v_onboarding'], [10, '']], 'OPERAND2': [1, [10, '1']]})
    sw_card = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, [4, 'onboarding_card']]})
    goto_front = ctx.add('looks_gotofrontback', fields={'FRONT_BACK': ['front']})
    show_card = ctx.add('looks_show')
    ctx.chain([sw_card, goto_front, show_card])
    hide_card = ctx.add('looks_hide')
    if_show = ctx.add('control_if_else', inputs={'CONDITION': [2, is_show], 'SUBSTACK': [2, sw_card], 'SUBSTACK2': [2, hide_card]})
    ctx.blocks[sw_card]['parent'] = if_show
    ctx.blocks[hide_card]['parent'] = if_show
    ctx.chain([hat_gf, goto_center, set_size, if_show])

    # SHOW_ONBOARDING broadcast receiver
    hat_show_onb = ctx.add('event_whenbroadcastreceived', fields={'BROADCAST_OPTION': ['SHOW_ONBOARDING', 'b_show_onb']}, topLevel=True, x=50, y=280)
    set_onb_1 = ctx.add('data_setvariableto', fields={'VARIABLE': ['SHOW_ONBOARDING', 'v_onboarding']}, inputs={'VALUE': [1, [4, '1']]})
    sw_card2 = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, [4, 'onboarding_card']]})
    goto_front2 = ctx.add('looks_gotofrontback', fields={'FRONT_BACK': ['front']})
    show_card2 = ctx.add('looks_show')
    ctx.chain([hat_show_onb, set_onb_1, sw_card2, goto_front2, show_card2])

    # UPDATE_UI broadcast receiver
    hat_upd = ctx.add('event_whenbroadcastreceived', fields={'BROADCAST_OPTION': ['UPDATE_UI', 'b_update_ui']}, topLevel=True, x=50, y=480)
    is_show_u = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'SHOW_ONBOARDING', 'v_onboarding'], [10, '']], 'OPERAND2': [1, [10, '1']]})
    sw_card_u = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, [4, 'onboarding_card']]})
    goto_front_u = ctx.add('looks_gotofrontback', fields={'FRONT_BACK': ['front']})
    show_card_u = ctx.add('looks_show')
    ctx.chain([sw_card_u, goto_front_u, show_card_u])
    hide_card_u = ctx.add('looks_hide')
    if_show_u = ctx.add('control_if_else', inputs={'CONDITION': [2, is_show_u], 'SUBSTACK': [2, sw_card_u], 'SUBSTACK2': [2, hide_card_u]})
    ctx.blocks[sw_card_u]['parent'] = if_show_u
    ctx.blocks[hide_card_u]['parent'] = if_show_u
    ctx.chain([hat_upd, if_show_u])

    # Click to dismiss
    hat_click = ctx.add('event_whenthisspriteclicked', topLevel=True, x=50, y=720)
    set_hide = ctx.add('data_setvariableto', fields={'VARIABLE': ['SHOW_ONBOARDING', 'v_onboarding']}, inputs={'VALUE': [1, [4, '0']]})
    hide_click = ctx.add('looks_hide')
    bc_upd = ctx.add('event_broadcast', inputs={'BROADCAST_INPUT': [1, [11, 'UPDATE_UI', 'b_update_ui']]})
    ctx.chain([hat_click, set_hide, hide_click, bc_upd])

    return {
        'isStage': False,
        'name': 'OnboardingUI',
        'variables': {},
        'lists': {},
        'broadcasts': {},
        'blocks': ctx.blocks,
        'comments': {},
        'currentCostume': 0,
        'costumes': onb_costume,
        'sounds': [],
        'volume': 100,
        'visible': True,
        'x': 0, 'y': 0, 'size': 100, 'direction': 90,
        'draggable': False, 'rotationStyle': "don't rotate"
    }


# ==============================================================================
# 11. Telemetry UI Sprite Builder
# ==============================================================================
def build_telemetry_ui(ASSETS=costume_meta):
    ctx = BlockContext()

    telem_costume_names = [
        'telem_ready', 'telem_react', 'telem_exo', 'telem_uv_req',
        'telem_cosmic', 'telem_inert', 'telem_discover', 'telem_frozen',
        'telem_save', 'telem_load', 'telem_purge'
    ]
    telem_costumes = [ASSETS[c] for c in telem_costume_names]

    # Green flag
    hat_gf = ctx.add('event_whenflagclicked', topLevel=True, x=50, y=50)
    goto_bar = ctx.add('motion_gotoxy', inputs={'X': [1, [4, '0']], 'Y': [1, [4, '-164']]})
    set_size = ctx.add('looks_setsizeto', inputs={'SIZE': [1, [4, '100']]})
    sw_ready = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, [4, 'telem_ready']]})
    show_bar = ctx.add('looks_show')
    ctx.chain([hat_gf, goto_bar, set_size, sw_ready, show_bar])

    # INIT_SIMULATION
    hat_init = ctx.add('event_whenbroadcastreceived', fields={'BROADCAST_OPTION': ['INIT_SIMULATION', 'b_init_sim']}, topLevel=True, x=50, y=220)
    sw_ready_init = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, [4, 'telem_ready']]})
    ctx.chain([hat_init, sw_ready_init])

    # UPDATE_UI: check freeze
    hat_upd = ctx.add('event_whenbroadcastreceived', fields={'BROADCAST_OPTION': ['UPDATE_UI', 'b_update_ui']}, topLevel=True, x=50, y=340)
    is_frz = ctx.add('operator_equals', inputs={'OPERAND1': [3, [12, 'TIME_FROZEN', 'v_freeze'], [10, '']], 'OPERAND2': [1, [10, '1']]})
    sw_frz = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, [4, 'telem_frozen']]})
    if_frz = ctx.add('control_if', inputs={'CONDITION': [2, is_frz], 'SUBSTACK': [2, sw_frz]})
    ctx.blocks[sw_frz]['parent'] = if_frz
    ctx.chain([hat_upd, if_frz])

    # FX_EXOTHERMIC
    hat_exo = ctx.add('event_whenbroadcastreceived', fields={'BROADCAST_OPTION': ['PLAY_FX_EXO', 'b_fx_exo']}, topLevel=True, x=50, y=480)
    sw_exo = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, [4, 'telem_exo']]})
    ctx.chain([hat_exo, sw_exo])

    # FX_BOND
    hat_bond = ctx.add('event_whenbroadcastreceived', fields={'BROADCAST_OPTION': ['PLAY_FX_BOND', 'b_fx_bond']}, topLevel=True, x=50, y=580)
    sw_bond = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, [4, 'telem_react']]})
    ctx.chain([hat_bond, sw_bond])

    # FX_ZAP
    hat_zap = ctx.add('event_whenbroadcastreceived', fields={'BROADCAST_OPTION': ['PLAY_FX_ZAP', 'b_fx_zap']}, topLevel=True, x=50, y=680)
    sw_zap = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, [4, 'telem_cosmic']]})
    ctx.chain([hat_zap, sw_zap])

    # CLEAR_ALL / FX_DELETE
    hat_del = ctx.add('event_whenbroadcastreceived', fields={'BROADCAST_OPTION': ['CLEAR_ALL', 'b_clear_all']}, topLevel=True, x=50, y=780)
    sw_purge = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, [4, 'telem_purge']]})
    ctx.chain([hat_del, sw_purge])

    hat_del2 = ctx.add('event_whenbroadcastreceived', fields={'BROADCAST_OPTION': ['PLAY_FX_DELETE', 'b_fx_del']}, topLevel=True, x=250, y=780)
    sw_purge2 = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, [4, 'telem_purge']]})
    ctx.chain([hat_del2, sw_purge2])

    # SHOW_TOAST
    hat_toast = ctx.add('event_whenbroadcastreceived', fields={'BROADCAST_OPTION': ['SHOW_TOAST', 'b_show_toast']}, topLevel=True, x=50, y=880)
    sw_disc = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, [4, 'telem_discover']]})
    ctx.chain([hat_toast, sw_disc])

    # PROMPT_SAVE_LOAD
    hat_save = ctx.add('event_whenbroadcastreceived', fields={'BROADCAST_OPTION': ['PROMPT_SAVE_LOAD', 'b_prompt_save']}, topLevel=True, x=50, y=980)
    sw_save = ctx.add('looks_switchcostumeto', inputs={'COSTUME': [1, [4, 'telem_save']]})
    ctx.chain([hat_save, sw_save])

    return {
        'isStage': False,
        'name': 'TelemetryUI',
        'variables': {},
        'lists': {},
        'broadcasts': {},
        'blocks': ctx.blocks,
        'comments': {},
        'currentCostume': 0,
        'costumes': telem_costumes,
        'sounds': [],
        'volume': 100,
        'visible': True,
        'x': 0, 'y': -164, 'size': 100, 'direction': 90,
        'draggable': False, 'rotationStyle': "don't rotate"
    }
