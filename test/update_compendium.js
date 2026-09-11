const fs = require('fs');
const crypto = require('crypto');

function newId() {
  return crypto.randomBytes(8).toString('hex');
}

class BlockContext {
  constructor() {
    this.blocks = {};
  }

  add(opcode, options = {}) {
    const id = newId();
    const block = {
      opcode,
      next: options.next || null,
      parent: options.parent || null,
      inputs: options.inputs || {},
      fields: options.fields || {},
      shadow: !!options.shadow,
      topLevel: !!options.topLevel
    };
    if (options.topLevel) {
      block.x = options.x || 0;
      block.y = options.y || 0;
    }
    if (options.mutation) {
      block.mutation = options.mutation;
    }
    this.blocks[id] = block;

    // Set parent for child input blocks
    for (const inp of Object.values(block.inputs)) {
      if (Array.isArray(inp) && inp.length >= 2) {
        let childId = null;
        if ([1, 2, 3].includes(inp[0]) && typeof inp[1] === 'string') {
          childId = inp[1];
        }
        if (childId && this.blocks[childId]) {
          this.blocks[childId].parent = id;
        }
      }
    }
    return id;
  }

  chain(blockIds, parent = null) {
    for (let i = 0; i < blockIds.length - 1; i++) {
      const curr = blockIds[i];
      const next = blockIds[i + 1];
      this.blocks[curr].next = next;
      this.blocks[next].parent = curr;
    }
    if (parent && blockIds.length > 0) {
      this.blocks[blockIds[0]].parent = parent;
    }
  }
}

function updateProject() {
  const projectPath = './etc/project.json';
  const project = JSON.parse(fs.readFileSync(projectPath, 'utf8'));

  const comp = project.targets.find(t => t.name === 'CompendiumUI');
  if (!comp) throw new Error('CompendiumUI target not found');

  // 1. Costumes
  comp.costumes = [
    {
      name: 'comp_summary',
      assetId: '2f696cb87bbd10223c2bbf1713a80f4a',
      dataFormat: 'svg',
      md5ext: '2f696cb87bbd10223c2bbf1713a80f4a.svg',
      rotationCenterX: 220,
      rotationCenterY: 125
    },
    {
      name: 'comp_elements',
      assetId: '3b27276fdb69294f659218f976d7d63b',
      dataFormat: 'svg',
      md5ext: '3b27276fdb69294f659218f976d7d63b.svg',
      rotationCenterX: 220,
      rotationCenterY: 125
    },
    {
      name: 'comp_molecules_1',
      assetId: '1bb82093c12ce6d7e1ec7b3f7312f46e',
      dataFormat: 'svg',
      md5ext: '1bb82093c12ce6d7e1ec7b3f7312f46e.svg',
      rotationCenterX: 220,
      rotationCenterY: 125
    },
    {
      name: 'comp_molecules_2',
      assetId: '41cba68d6d4aa53b09b193d04f1630e9',
      dataFormat: 'svg',
      md5ext: '41cba68d6d4aa53b09b193d04f1630e9.svg',
      rotationCenterX: 220,
      rotationCenterY: 125
    },
    {
      name: 'comp_radicals',
      assetId: 'f3b4452313338bf28e8ca10a0e2a10fc',
      dataFormat: 'svg',
      md5ext: 'f3b4452313338bf28e8ca10a0e2a10fc.svg',
      rotationCenterX: 220,
      rotationCenterY: 125
    },
    {
      name: 'comp_ions',
      assetId: '5367d4b2abecf90421d410a6c74b8d7e',
      dataFormat: 'svg',
      md5ext: '5367d4b2abecf90421d410a6c74b8d7e.svg',
      rotationCenterX: 220,
      rotationCenterY: 125
    }
  ];

  // 2. Build block tree
  const ctx = new BlockContext();

  function numVx() {
    return [3, [12, 'CLICK_X', 'v_click_x'], [10, '0']];
  }
  function numVy() {
    return [3, [12, 'CLICK_Y', 'v_click_y'], [10, '0']];
  }
  function varTab() {
    return [3, [12, 'COMPENDIUM_TAB', 'v_comp_tab'], [10, '1']];
  }

  function makeEqTab(tabNum) {
    return ctx.add('operator_equals', {
      inputs: {
        OPERAND1: varTab(),
        OPERAND2: [1, [10, String(tabNum)]]
      }
    });
  }

  function makeInRange(valFn, minVal, maxVal) {
    const gt = ctx.add('operator_gt', {
      inputs: {
        OPERAND1: valFn(),
        OPERAND2: [1, [10, String(minVal)]]
      }
    });
    const lt = ctx.add('operator_lt', {
      inputs: {
        OPERAND1: valFn(),
        OPERAND2: [1, [10, String(maxVal)]]
      }
    });
    return ctx.add('operator_and', {
      inputs: {
        OPERAND1: [2, gt],
        OPERAND2: [2, lt]
      }
    });
  }

  // Green flag: initialize
  const hatGf = ctx.add('event_whenflagclicked', { topLevel: true, x: 50, y: 50 });
  const setCompVar = ctx.add('data_setvariableto', { fields: { VARIABLE: ['SHOW_COMPENDIUM', 'v_compendium'] }, inputs: { VALUE: [1, [4, '0']] } });
  const setTabVar = ctx.add('data_setvariableto', { fields: { VARIABLE: ['COMPENDIUM_TAB', 'v_comp_tab'] }, inputs: { VALUE: [1, [4, '1']] } });
  const gotoCenter = ctx.add('motion_gotoxy', { inputs: { X: [1, [4, '0']], Y: [1, [4, '0']] } });
  const setSize = ctx.add('looks_setsizeto', { inputs: { SIZE: [1, [4, '100']] } });
  const hideIt = ctx.add('looks_hide');
  ctx.chain([hatGf, setCompVar, setTabVar, gotoCenter, setSize, hideIt]);

  // UPDATE_UI receiver
  const hatUpd = ctx.add('event_whenbroadcastreceived', { fields: { BROADCAST_OPTION: ['UPDATE_UI', 'b_update_ui'] }, topLevel: true, x: 50, y: 240 });
  const isShow = ctx.add('operator_equals', { inputs: { OPERAND1: [3, [12, 'SHOW_COMPENDIUM', 'v_compendium'], [10, '']], OPERAND2: [1, [10, '1']] } });

  const cSum = ctx.add('looks_switchcostumeto', { inputs: { COSTUME: [1, [4, 'comp_summary']] } });
  const cElem = ctx.add('looks_switchcostumeto', { inputs: { COSTUME: [1, [4, 'comp_elements']] } });
  const cMol1 = ctx.add('looks_switchcostumeto', { inputs: { COSTUME: [1, [4, 'comp_molecules_1']] } });
  const cMol2 = ctx.add('looks_switchcostumeto', { inputs: { COSTUME: [1, [4, 'comp_molecules_2']] } });
  const cRad = ctx.add('looks_switchcostumeto', { inputs: { COSTUME: [1, [4, 'comp_radicals']] } });
  const cIon = ctx.add('looks_switchcostumeto', { inputs: { COSTUME: [1, [4, 'comp_ions']] } });

  const eq5 = ctx.add('operator_equals', { inputs: { OPERAND1: varTab(), OPERAND2: [1, [10, '5']] } });
  const if5 = ctx.add('control_if_else', { inputs: { CONDITION: [2, eq5], SUBSTACK: [2, cRad], SUBSTACK2: [2, cIon] } });
  ctx.blocks[cRad].parent = if5; ctx.blocks[cIon].parent = if5;

  const eq4 = ctx.add('operator_equals', { inputs: { OPERAND1: varTab(), OPERAND2: [1, [10, '4']] } });
  const if4 = ctx.add('control_if_else', { inputs: { CONDITION: [2, eq4], SUBSTACK: [2, cMol2], SUBSTACK2: [2, if5] } });
  ctx.blocks[cMol2].parent = if4; ctx.blocks[if5].parent = if4;

  const eq3 = ctx.add('operator_equals', { inputs: { OPERAND1: varTab(), OPERAND2: [1, [10, '3']] } });
  const if3 = ctx.add('control_if_else', { inputs: { CONDITION: [2, eq3], SUBSTACK: [2, cMol1], SUBSTACK2: [2, if4] } });
  ctx.blocks[cMol1].parent = if3; ctx.blocks[if4].parent = if3;

  const eq2 = ctx.add('operator_equals', { inputs: { OPERAND1: varTab(), OPERAND2: [1, [10, '2']] } });
  const if2 = ctx.add('control_if_else', { inputs: { CONDITION: [2, eq2], SUBSTACK: [2, cElem], SUBSTACK2: [2, if3] } });
  ctx.blocks[cElem].parent = if2; ctx.blocks[if3].parent = if2;

  const eq1 = ctx.add('operator_equals', { inputs: { OPERAND1: varTab(), OPERAND2: [1, [10, '1']] } });
  const if1 = ctx.add('control_if_else', { inputs: { CONDITION: [2, eq1], SUBSTACK: [2, cSum], SUBSTACK2: [2, if2] } });
  ctx.blocks[cSum].parent = if1; ctx.blocks[if2].parent = if1;

  const gotoFront = ctx.add('looks_gotofrontback', { fields: { FRONT_BACK: ['front'] } });
  const showIt = ctx.add('looks_show');
  ctx.chain([if1, gotoFront, showIt]);

  const hideComp = ctx.add('looks_hide');
  const ifShowAll = ctx.add('control_if_else', { inputs: { CONDITION: [2, isShow], SUBSTACK: [2, if1], SUBSTACK2: [2, hideComp] } });
  ctx.blocks[if1].parent = ifShowAll; ctx.blocks[hideComp].parent = ifShowAll;
  ctx.chain([hatUpd, ifShowAll]);

  // Master Click Handler
  const hatClick = ctx.add('event_whenthisspriteclicked', { topLevel: true, x: 50, y: 600 });
  const mxB = ctx.add('sensing_mousex');
  const setCx = ctx.add('data_setvariableto', { fields: { VARIABLE: ['CLICK_X', 'v_click_x'] }, inputs: { VALUE: [2, mxB] } });
  const myB = ctx.add('sensing_mousey');
  const setCy = ctx.add('data_setvariableto', { fields: { VARIABLE: ['CLICK_Y', 'v_click_y'] }, inputs: { VALUE: [2, myB] } });

  // Helper to build a spawn sequence for species ID
  function buildSpawnChain(speciesValInput) {
    const setSpc = ctx.add('data_setvariableto', { fields: { VARIABLE: ['SPAWN_SPECIES_ID', 'v_spawn_id'] }, inputs: { VALUE: speciesValInput } });
    const rndX = ctx.add('operator_random', { inputs: { FROM: [1, [4, '-70']], TO: [1, [4, '70']] } });
    const setSx = ctx.add('data_setvariableto', { fields: { VARIABLE: ['SPAWN_X', 'v_spawn_x'] }, inputs: { VALUE: [3, rndX, [4, '0']] } });
    const rndY = ctx.add('operator_random', { inputs: { FROM: [1, [4, '-20']], TO: [1, [4, '30']] } });
    const setSy = ctx.add('data_setvariableto', { fields: { VARIABLE: ['SPAWN_Y', 'v_spawn_y'] }, inputs: { VALUE: [3, rndY, [4, '0']] } });
    const bcSpawn = ctx.add('event_broadcast', { inputs: { BROADCAST_INPUT: [1, [11, 'SPAWN_REQUEST', 'b_spawn_req']] } });
    const setInsp = ctx.add('data_setvariableto', { fields: { VARIABLE: ['INSPECT_SPECIES_ID', 'v_inspect_id'] }, inputs: { VALUE: [3, [12, 'SPAWN_SPECIES_ID', 'v_spawn_id'], [4, '1']] } });
    const setShowInfo = ctx.add('data_setvariableto', { fields: { VARIABLE: ['SHOW_INFO', 'v_info'] }, inputs: { VALUE: [1, [4, '1']] } });
    const bcUpd = ctx.add('event_broadcast', { inputs: { BROADCAST_INPUT: [1, [11, 'UPDATE_UI', 'b_update_ui']] } });
    const sndBondM = ctx.add('sound_sounds_menu', { fields: { SOUND_MENU: ['snd_bond', null] }, shadow: true });
    const playBond = ctx.add('sound_play', { inputs: { SOUND_MENU: [1, sndBondM] } });

    ctx.chain([setSpc, setSx, setSy, bcSpawn, setInsp, setShowInfo, bcUpd, playBond]);
    return setSpc;
  }

  // 1. Close Action: Top-right [x] or Bottom-right [CLOSE CATALOG]
  const gtX180 = ctx.add('operator_gt', { inputs: { OPERAND1: numVx(), OPERAND2: [1, [10, '180']] } });
  const gtY95 = ctx.add('operator_gt', { inputs: { OPERAND1: numVy(), OPERAND2: [1, [10, '95']] } });
  const isTopClose = ctx.add('operator_and', { inputs: { OPERAND1: [2, gtX180], OPERAND2: [2, gtY95] } });

  const gtX80 = ctx.add('operator_gt', { inputs: { OPERAND1: numVx(), OPERAND2: [1, [10, '80']] } });
  const ltYm95 = ctx.add('operator_lt', { inputs: { OPERAND1: numVy(), OPERAND2: [1, [10, '-95']] } });
  const isBotClose = ctx.add('operator_and', { inputs: { OPERAND1: [2, gtX80], OPERAND2: [2, ltYm95] } });

  const isClose = ctx.add('operator_or', { inputs: { OPERAND1: [2, isTopClose], OPERAND2: [2, isBotClose] } });

  const setHideVar = ctx.add('data_setvariableto', { fields: { VARIABLE: ['SHOW_COMPENDIUM', 'v_compendium'] }, inputs: { VALUE: [1, [4, '0']] } });
  const hideSprite = ctx.add('looks_hide');
  const bcUpdC = ctx.add('event_broadcast', { inputs: { BROADCAST_INPUT: [1, [11, 'UPDATE_UI', 'b_update_ui']] } });
  const sndClkM = ctx.add('sound_sounds_menu', { fields: { SOUND_MENU: ['snd_click', null] }, shadow: true });
  const playClkC = ctx.add('sound_play', { inputs: { SOUND_MENU: [1, sndClkM] } });
  ctx.chain([setHideVar, hideSprite, bcUpdC, playClkC]);

  const ifClose = ctx.add('control_if', { inputs: { CONDITION: [2, isClose], SUBSTACK: [2, setHideVar] } });
  ctx.blocks[setHideVar].parent = ifClose;

  // 2. Reset Action: bottom-left (x < -80 and y < -95)
  const ltXm80 = ctx.add('operator_lt', { inputs: { OPERAND1: numVx(), OPERAND2: [1, [10, '-80']] } });
  const ltYm95R = ctx.add('operator_lt', { inputs: { OPERAND1: numVy(), OPERAND2: [1, [10, '-95']] } });
  const isResetBtn = ctx.add('operator_and', { inputs: { OPERAND1: [2, ltXm80], OPERAND2: [2, ltYm95R] } });

  const bcClearR = ctx.add('event_broadcast', { inputs: { BROADCAST_INPUT: [1, [11, 'CLEAR_ALL', 'b_clear_all']] } });
  const bcUpdR = ctx.add('event_broadcast', { inputs: { BROADCAST_INPUT: [1, [11, 'UPDATE_UI', 'b_update_ui']] } });
  const sndDelM = ctx.add('sound_sounds_menu', { fields: { SOUND_MENU: ['snd_delete', null] }, shadow: true });
  const playDelR = ctx.add('sound_play', { inputs: { SOUND_MENU: [1, sndDelM] } });
  ctx.chain([bcClearR, bcUpdR, playDelR]);

  const ifReset = ctx.add('control_if', { inputs: { CONDITION: [2, isResetBtn], SUBSTACK: [2, bcClearR] } });
  ctx.blocks[bcClearR].parent = ifReset;

  // 3. Tab Bar Action: (y > 65 and y < 95)
  const isTabBar = makeInRange(numVy, 65, 95);

  const setTab1 = ctx.add('data_setvariableto', { fields: { VARIABLE: ['COMPENDIUM_TAB', 'v_comp_tab'] }, inputs: { VALUE: [1, [4, '1']] } });
  const setTab2 = ctx.add('data_setvariableto', { fields: { VARIABLE: ['COMPENDIUM_TAB', 'v_comp_tab'] }, inputs: { VALUE: [1, [4, '2']] } });
  const setTab3 = ctx.add('data_setvariableto', { fields: { VARIABLE: ['COMPENDIUM_TAB', 'v_comp_tab'] }, inputs: { VALUE: [1, [4, '3']] } });
  const setTab5 = ctx.add('data_setvariableto', { fields: { VARIABLE: ['COMPENDIUM_TAB', 'v_comp_tab'] }, inputs: { VALUE: [1, [4, '5']] } });
  const setTab6 = ctx.add('data_setvariableto', { fields: { VARIABLE: ['COMPENDIUM_TAB', 'v_comp_tab'] }, inputs: { VALUE: [1, [4, '6']] } });

  const ltX135 = ctx.add('operator_lt', { inputs: { OPERAND1: numVx(), OPERAND2: [1, [10, '135']] } });
  const ifT5_6 = ctx.add('control_if_else', { inputs: { CONDITION: [2, ltX135], SUBSTACK: [2, setTab5], SUBSTACK2: [2, setTab6] } });
  ctx.blocks[setTab5].parent = ifT5_6; ctx.blocks[setTab6].parent = ifT5_6;

  const ltX50 = ctx.add('operator_lt', { inputs: { OPERAND1: numVx(), OPERAND2: [1, [10, '50']] } });
  const ifT3_4 = ctx.add('control_if_else', { inputs: { CONDITION: [2, ltX50], SUBSTACK: [2, setTab3], SUBSTACK2: [2, ifT5_6] } });
  ctx.blocks[setTab3].parent = ifT3_4; ctx.blocks[ifT5_6].parent = ifT3_4;

  const ltXm40 = ctx.add('operator_lt', { inputs: { OPERAND1: numVx(), OPERAND2: [1, [10, '-40']] } });
  const ifT2_3 = ctx.add('control_if_else', { inputs: { CONDITION: [2, ltXm40], SUBSTACK: [2, setTab2], SUBSTACK2: [2, ifT3_4] } });
  ctx.blocks[setTab2].parent = ifT2_3; ctx.blocks[ifT3_4].parent = ifT2_3;

  const ltXm125 = ctx.add('operator_lt', { inputs: { OPERAND1: numVx(), OPERAND2: [1, [10, '-125']] } });
  const ifT1_2 = ctx.add('control_if_else', { inputs: { CONDITION: [2, ltXm125], SUBSTACK: [2, setTab1], SUBSTACK2: [2, ifT2_3] } });
  ctx.blocks[setTab1].parent = ifT1_2; ctx.blocks[ifT2_3].parent = ifT1_2;

  const bcUpdT = ctx.add('event_broadcast', { inputs: { BROADCAST_INPUT: [1, [11, 'UPDATE_UI', 'b_update_ui']] } });
  const sndClkM2 = ctx.add('sound_sounds_menu', { fields: { SOUND_MENU: ['snd_click', null] }, shadow: true });
  const playClkT = ctx.add('sound_play', { inputs: { SOUND_MENU: [1, sndClkM2] } });
  ctx.chain([ifT1_2, bcUpdT, playClkT]);

  const ifTabBar = ctx.add('control_if', { inputs: { CONDITION: [2, isTabBar], SUBSTACK: [2, ifT1_2] } });
  ctx.blocks[ifT1_2].parent = ifTabBar;

  // 4. Tab 1 Action (Summary Category Cards)
  const isTab1 = makeEqTab(1);
  const inCatY = makeInRange(numVy, -60, 45);

  const setCj2 = ctx.add('data_setvariableto', { fields: { VARIABLE: ['COMPENDIUM_TAB', 'v_comp_tab'] }, inputs: { VALUE: [1, [4, '2']] } });
  const setCj3 = ctx.add('data_setvariableto', { fields: { VARIABLE: ['COMPENDIUM_TAB', 'v_comp_tab'] }, inputs: { VALUE: [1, [4, '3']] } });
  const setCj5 = ctx.add('data_setvariableto', { fields: { VARIABLE: ['COMPENDIUM_TAB', 'v_comp_tab'] }, inputs: { VALUE: [1, [4, '5']] } });
  const setCj6 = ctx.add('data_setvariableto', { fields: { VARIABLE: ['COMPENDIUM_TAB', 'v_comp_tab'] }, inputs: { VALUE: [1, [4, '6']] } });

  const ltCj110 = ctx.add('operator_lt', { inputs: { OPERAND1: numVx(), OPERAND2: [1, [10, '110']] } });
  const ifCj5_6 = ctx.add('control_if_else', { inputs: { CONDITION: [2, ltCj110], SUBSTACK: [2, setCj5], SUBSTACK2: [2, setCj6] } });
  ctx.blocks[setCj5].parent = ifCj5_6; ctx.blocks[setCj6].parent = ifCj5_6;

  const ltCj0 = ctx.add('operator_lt', { inputs: { OPERAND1: numVx(), OPERAND2: [1, [10, '0']] } });
  const ifCj3_5 = ctx.add('control_if_else', { inputs: { CONDITION: [2, ltCj0], SUBSTACK: [2, setCj3], SUBSTACK2: [2, ifCj5_6] } });
  ctx.blocks[setCj3].parent = ifCj3_5; ctx.blocks[ifCj5_6].parent = ifCj3_5;

  const ltCjm110 = ctx.add('operator_lt', { inputs: { OPERAND1: numVx(), OPERAND2: [1, [10, '-110']] } });
  const ifCj2_3 = ctx.add('control_if_else', { inputs: { CONDITION: [2, ltCjm110], SUBSTACK: [2, setCj2], SUBSTACK2: [2, ifCj3_5] } });
  ctx.blocks[setCj2].parent = ifCj2_3; ctx.blocks[ifCj3_5].parent = ifCj2_3;

  const bcUpdCj = ctx.add('event_broadcast', { inputs: { BROADCAST_INPUT: [1, [11, 'UPDATE_UI', 'b_update_ui']] } });
  const sndClkM5 = ctx.add('sound_sounds_menu', { fields: { SOUND_MENU: ['snd_click', null] }, shadow: true });
  const playClkCj = ctx.add('sound_play', { inputs: { SOUND_MENU: [1, sndClkM5] } });
  ctx.chain([ifCj2_3, bcUpdCj, playClkCj]);

  const ifCatContent = ctx.add('control_if', { inputs: { CONDITION: [2, inCatY], SUBSTACK: [2, ifCj2_3] } });
  ctx.blocks[ifCj2_3].parent = ifCatContent;

  const ifTab1 = ctx.add('control_if', { inputs: { CONDITION: [2, isTab1], SUBSTACK: [2, ifCatContent] } });
  ctx.blocks[ifCatContent].parent = ifTab1;

  // 5. Tab 2 Action: 19 Atoms
  const isTab2 = makeEqTab(2);
  const inElR1 = makeInRange(numVy, -15, 53);

  const mxS205 = ctx.add('operator_add', { inputs: { NUM1: numVx(), NUM2: [1, [4, '205']] } });
  const colRaw1 = ctx.add('operator_divide', { inputs: { NUM1: [3, mxS205, [4, '0']], NUM2: [1, [4, '41']] } });
  const colF1 = ctx.add('operator_mathop', { fields: { OPERATOR: ['floor', null] }, inputs: { NUM: [3, colRaw1, [4, '0']] } });
  const colId1 = ctx.add('operator_add', { inputs: { NUM1: [3, colF1, [4, '0']], NUM2: [1, [4, '1']] } });
  const spawnChainR1 = buildSpawnChain([3, colId1, [4, '1']]);

  const ifElR1 = ctx.add('control_if', { inputs: { CONDITION: [2, inElR1], SUBSTACK: [2, spawnChainR1] } });
  ctx.blocks[spawnChainR1].parent = ifElR1;

  const inElR2 = makeInRange(numVy, -87, -19);
  const mxS185 = ctx.add('operator_add', { inputs: { NUM1: numVx(), NUM2: [1, [4, '185']] } });
  const colRaw2 = ctx.add('operator_divide', { inputs: { NUM1: [3, mxS185, [4, '0']], NUM2: [1, [4, '41']] } });
  const colF2 = ctx.add('operator_mathop', { fields: { OPERATOR: ['floor', null] }, inputs: { NUM: [3, colRaw2, [4, '0']] } });
  const colId2 = ctx.add('operator_add', { inputs: { NUM1: [3, colF2, [4, '0']], NUM2: [1, [4, '11']] } });
  const spawnChainR2 = buildSpawnChain([3, colId2, [4, '11']]);

  const ifElR2 = ctx.add('control_if', { inputs: { CONDITION: [2, inElR2], SUBSTACK: [2, spawnChainR2] } });
  ctx.blocks[spawnChainR2].parent = ifElR2;

  ctx.chain([ifElR1, ifElR2]);
  const ifTab2 = ctx.add('control_if', { inputs: { CONDITION: [2, isTab2], SUBSTACK: [2, ifElR1] } });
  ctx.blocks[ifElR1].parent = ifTab2;

  // Helper for 8-Card Grid Tabs (Tabs 3, 4, 5, 6)
  function build8GridTab(tabNum, ids, paginationConfig) {
    const isThisTab = makeEqTab(tabNum);
    const substackBlocks = [];

    // Optional pagination button
    if (paginationConfig) {
      const inPageY = makeInRange(numVy, 52, 73);
      let inPageX;
      if (paginationConfig.maxX !== null && paginationConfig.maxX !== undefined) {
        inPageX = makeInRange(numVx, paginationConfig.minX, paginationConfig.maxX);
      } else {
        inPageX = ctx.add('operator_gt', { inputs: { OPERAND1: numVx(), OPERAND2: [1, [10, String(paginationConfig.minX)]] } });
      }
      const isPageBtn = ctx.add('operator_and', { inputs: { OPERAND1: [2, inPageY], OPERAND2: [2, inPageX] } });

      const setT = ctx.add('data_setvariableto', { fields: { VARIABLE: ['COMPENDIUM_TAB', 'v_comp_tab'] }, inputs: { VALUE: [1, [4, String(paginationConfig.targetTab)]] } });
      const bcUpdP = ctx.add('event_broadcast', { inputs: { BROADCAST_INPUT: [1, [11, 'UPDATE_UI', 'b_update_ui']] } });
      const sndClkMP = ctx.add('sound_sounds_menu', { fields: { SOUND_MENU: ['snd_click', null] }, shadow: true });
      const playClkP = ctx.add('sound_play', { inputs: { SOUND_MENU: [1, sndClkMP] } });
      ctx.chain([setT, bcUpdP, playClkP]);

      const ifPageBtn = ctx.add('control_if', { inputs: { CONDITION: [2, isPageBtn], SUBSTACK: [2, setT] } });
      ctx.blocks[setT].parent = ifPageBtn;
      substackBlocks.push(ifPageBtn);
    }

    function build4ColDispatcher(id0, id1, id2, id3) {
      const set0 = buildSpawnChain([1, [4, String(id0)]]);
      const set1 = buildSpawnChain([1, [4, String(id1)]]);
      const set2 = buildSpawnChain([1, [4, String(id2)]]);
      const set3 = buildSpawnChain([1, [4, String(id3)]]);

      const ltC3 = ctx.add('operator_lt', { inputs: { OPERAND1: numVx(), OPERAND2: [1, [10, '110']] } });
      const ifC2_3 = ctx.add('control_if_else', { inputs: { CONDITION: [2, ltC3], SUBSTACK: [2, set2], SUBSTACK2: [2, set3] } });
      ctx.blocks[set2].parent = ifC2_3; ctx.blocks[set3].parent = ifC2_3;

      const ltC2 = ctx.add('operator_lt', { inputs: { OPERAND1: numVx(), OPERAND2: [1, [10, '0']] } });
      const ifC1_2 = ctx.add('control_if_else', { inputs: { CONDITION: [2, ltC2], SUBSTACK: [2, set1], SUBSTACK2: [2, ifC2_3] } });
      ctx.blocks[set1].parent = ifC1_2; ctx.blocks[ifC2_3].parent = ifC1_2;

      const ltC1 = ctx.add('operator_lt', { inputs: { OPERAND1: numVx(), OPERAND2: [1, [10, '-105']] } });
      const ifC0_1 = ctx.add('control_if_else', { inputs: { CONDITION: [2, ltC1], SUBSTACK: [2, set0], SUBSTACK2: [2, ifC1_2] } });
      ctx.blocks[set0].parent = ifC0_1; ctx.blocks[ifC1_2].parent = ifC0_1;

      return ifC0_1;
    }

    // Row 1
    const inRow1 = makeInRange(numVy, -15, 51);
    const row1Disp = build4ColDispatcher(ids[0], ids[1], ids[2], ids[3]);
    const ifRow1 = ctx.add('control_if', { inputs: { CONDITION: [2, inRow1], SUBSTACK: [2, row1Disp] } });
    ctx.blocks[row1Disp].parent = ifRow1;
    substackBlocks.push(ifRow1);

    // Row 2
    const inRow2 = makeInRange(numVy, -87, -21);
    const row2Disp = build4ColDispatcher(ids[4], ids[5], ids[6], ids[7]);
    const ifRow2 = ctx.add('control_if', { inputs: { CONDITION: [2, inRow2], SUBSTACK: [2, row2Disp] } });
    ctx.blocks[row2Disp].parent = ifRow2;
    substackBlocks.push(ifRow2);

    ctx.chain(substackBlocks);
    const ifTab = ctx.add('control_if', { inputs: { CONDITION: [2, isThisTab], SUBSTACK: [2, substackBlocks[0]] } });
    ctx.blocks[substackBlocks[0]].parent = ifTab;
    return ifTab;
  }

  // 6. Tab 3: Molecules Page 1
  const ifTab3 = build8GridTab(3, [20, 21, 22, 25, 39, 40, 44, 47], { targetTab: 4, minX: 120 });

  // 7. Tab 4: Molecules Page 2
  const ifTab4 = build8GridTab(4, [30, 32, 57, 58, 60, 71, 85, 106], { targetTab: 3, minX: 40, maxX: 120 });

  // 8. Tab 5: Radicals
  const ifTab5 = build8GridTab(5, [41, 42, 43, 28, 46, 29, 27, 56], null);

  // 9. Tab 6: Ions
  const ifTab6 = build8GridTab(6, [109, 111, 118, 117, 123, 124, 119, 129], null);

  // Master click chain: hatClick -> setCx -> setCy -> ifClose -> ifReset -> ifTabBar -> ifTab1 -> ifTab2 -> ifTab3 -> ifTab4 -> ifTab5 -> ifTab6
  ctx.chain([
    hatClick,
    setCx,
    setCy,
    ifClose,
    ifReset,
    ifTabBar,
    ifTab1,
    ifTab2,
    ifTab3,
    ifTab4,
    ifTab5,
    ifTab6
  ]);

  comp.blocks = ctx.blocks;

  fs.writeFileSync(projectPath, JSON.stringify(project, null, 2));
  console.log('Successfully updated CompendiumUI blocks and costumes in project.json!');
}

updateProject();

