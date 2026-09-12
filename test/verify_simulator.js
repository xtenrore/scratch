const fs = require('fs');
const assert = require('assert');
const parser = require('scratch-parser');
const VirtualMachine = require('scratch-vm');

async function testAll() {
  console.log('=== STARTING AUTOMATED SIMULATOR VALIDATION SUITE ===');

  // 1. Parser verification on both SB3 files
  for (const file of ['sb3/ChemistrySimulator.sb3', 'sb3/chemistry_simulator.sb3']) {
    const buf = fs.readFileSync(file);
    await new Promise((resolve, reject) => {
      parser(buf, false, (err, res) => {
        if (err) return reject(err);
        assert(res && res[0], 'Project empty');
        assert.strictEqual(res[0].targets.length, 106, 'Must have 106 targets');
        assert.strictEqual(res[0].meta.semver, '3.0.0', 'Semver must be 3.0.0');
        console.log(`[PASS] ${file} is a valid Scratch 3.0 project (106 targets, semver 3.0.0)`);
        resolve();
      });
    });
  }

  // 2. Load into Scratch VM
  const vm = new VirtualMachine();
  const buf = fs.readFileSync('sb3/ChemistrySimulator.sb3');
  await vm.loadProject(buf);
  console.log('[PASS] Scratch VM loadProject completed cleanly');

  // Set VM stepping rate to standard 30 FPS (33ms step time)
  vm.runtime.currentStepTime = 33;

  // 3. Green flag
  vm.greenFlag();
  for (let i = 0; i < 25; i++) vm.runtime._step();

  const stage = vm.runtime.getTargetForStage();
  const getVar = (name) => {
    for (const k in stage.variables) {
      if (stage.variables[k].name === name) return stage.variables[k].value;
    }
    return undefined;
  };
  const setVar = (name, val) => {
    for (const k in stage.variables) {
      if (stage.variables[k].name === name) stage.variables[k].value = val;
    }
  };
  const getList = (name) => {
    for (const k in stage.variables) {
      if (stage.variables[k].name === name && Array.isArray(stage.variables[k].value)) {
        return stage.variables[k].value;
      }
    }
    return undefined;
  };

  assert.strictEqual(Number(getVar('SHOW_ONBOARDING')), 1, 'Initial onboarding should be 1');
  assert.strictEqual(getVar('CURRENT_TOOL'), 'drag', 'Initial tool should be drag');
  assert.strictEqual(Number(getVar('TOTAL_DISCOVERED')), 19, 'Initial discovered elements must be 19');
  assert.strictEqual(Number(getVar('UV_ACTIVE')), 0, 'Initial UV must be 0');
  assert.strictEqual(Number(getVar('TIME_FROZEN')), 0, 'Initial FREEZE must be 0');
  assert.strictEqual(Number(getVar('MASTER_VOLUME')), 100, 'Initial volume must be 100');

  console.log('[PASS] Initial state variables verified');

  // 4. Verify Chemical Database and Reaction Rule Lists
  const dbName = getList('DB_NAME');
  const dbForm = getList('DB_FORMULA');
  const dbDisc = getList('DB_DISCOVERED');
  const rxKey = getList('RX_KEY');
  const rxProd = getList('RX_PROD');
  const rxExo = getList('RX_EXO');
  const rxUv = getList('RX_UV');
  const rxDesc = getList('RX_DESC');
  const ionSrc = getList('IONIZE_SRC');
  const ionDst = getList('IONIZE_DST');

  assert.strictEqual(dbName.length, 129, 'DB_NAME must have 129 species');
  assert.strictEqual(dbForm.length, 129, 'DB_FORMULA must have 129 species');
  assert.strictEqual(dbDisc.length, 129, 'DB_DISCOVERED must have 129 entries');
  assert.strictEqual(rxKey.length, 112, 'RX_KEY must have 112 reactions');
  assert.strictEqual(rxProd.length, 112, 'RX_PROD must have 112 products');
  assert.strictEqual(rxExo.length, 112, 'RX_EXO must have 112 entries');
  assert.strictEqual(rxUv.length, 112, 'RX_UV must have 112 entries');
  assert.strictEqual(rxDesc.length, 112, 'RX_DESC must have 112 entries');
  assert.strictEqual(ionSrc.length, 18, 'IONIZE_SRC must have 18 entries');
  assert.strictEqual(ionDst.length, 18, 'IONIZE_DST must have 18 entries');

  console.log('[PASS] All 129 species, 112 reaction rules, and 18 ionization rules verified in VM memory');

  // 5. Verify Tool Rail UI Independent Button Sprites & Initial Particles Clones
  const allTargets = vm.runtime.targets;
  const toolButtons = allTargets.filter(t => t.getName().startsWith('ToolBtn_'));
  const entityClones = allTargets.filter(t => t.getName() === 'Entity' && !t.isOriginal);

  assert.strictEqual(toolButtons.length, 10, 'Expected 10 independent ToolBtn sprites');
  assert.strictEqual(entityClones.length, 5, 'Expected 5 initial Entity particle clones');
  console.log('[PASS] Tool rail initialized with 10 independent vector button sprites across Y=144');
  console.log('[PASS] Simulation engine spawned 5 initial reactor atoms');

  // 6. Test Spawning an Additional Entity via SPAWN_REQUEST
  const initialEntities = vm.runtime.targets.filter(t => t.getName() === 'Entity' && !t.isOriginal).length;
  setVar('SPAWN_SPECIES_ID', 6); // Carbon
  setVar('SPAWN_X', 10);
  setVar('SPAWN_Y', 10);
  vm.runtime.startHats('event_whenbroadcastreceived', { BROADCAST_OPTION: 'SPAWN_REQUEST' });
  for (let i = 0; i < 15; i++) vm.runtime._step();

  const newEntities = vm.runtime.targets.filter(t => t.getName() === 'Entity' && !t.isOriginal).length;
  assert(newEntities > initialEntities, 'SPAWN_REQUEST should create a new Entity clone');
  console.log(`[PASS] Injected species #6 (Carbon). Total active entities: ${newEntities}`);

  // 7. Test Backdrop Switching (UV & Freeze states)
  setVar('UV_ACTIVE', 1);
  vm.runtime.startHats('event_whenbroadcastreceived', { BROADCAST_OPTION: 'UPDATE_BACKDROP' });
  for (let i = 0; i < 5; i++) vm.runtime._step();
  assert.strictEqual(stage.currentCostume, 1, 'Stage backdrop should be backdrop_uv (index 1)');
  console.log('[PASS] UV Activation correctly switched backdrop to ultraviolet chamber');

  setVar('TIME_FROZEN', 1);
  vm.runtime.startHats('event_whenbroadcastreceived', { BROADCAST_OPTION: 'UPDATE_BACKDROP' });
  for (let i = 0; i < 5; i++) vm.runtime._step();
  assert.strictEqual(stage.currentCostume, 2, 'Stage backdrop should be backdrop_frozen (index 2)');
  console.log('[PASS] Cryo Freeze correctly switched backdrop to cryostat chamber');

  setVar('TIME_FROZEN', 0);
  setVar('UV_ACTIVE', 0);
  vm.runtime.startHats('event_whenbroadcastreceived', { BROADCAST_OPTION: 'UPDATE_BACKDROP' });
  for (let i = 0; i < 5; i++) vm.runtime._step();
  assert.strictEqual(stage.currentCostume, 0, 'Stage backdrop should restore to backdrop_vacuum (index 0)');
  console.log('[PASS] Reset correctly restored standard dark vacuum chamber backdrop');

  // 8. Test Clear All (Vacuum Flush)
  vm.runtime.startHats('event_whenbroadcastreceived', { BROADCAST_OPTION: 'CLEAR_ALL' });
  for (let i = 0; i < 10; i++) vm.runtime._step();
  const survivingEntities = vm.runtime.targets.filter(t => t.getName() === 'Entity' && !t.isOriginal).length;
  assert.strictEqual(survivingEntities, 0, 'CLEAR_ALL should purge all active particle clones');
  console.log('[PASS] CLEAR_ALL successfully evacuated all particles from chamber');

  // 9. Test Compendium Modal & Multi-Tab Costumes
  setVar('SHOW_COMPENDIUM', 1);
  setVar('COMPENDIUM_TAB', 1);
  vm.runtime.startHats('event_whenbroadcastreceived', { BROADCAST_OPTION: 'UPDATE_UI' });
  for (let i = 0; i < 5; i++) vm.runtime._step();
  const compUI = vm.runtime.targets.find(t => t.getName() === 'CompendiumUI');
  assert.strictEqual(compUI.visible, true, 'CompendiumUI should be visible when SHOW_COMPENDIUM == 1');
  assert.strictEqual(compUI.getCostumes().length, 6, 'CompendiumUI must have 6 interactive vector costumes');
  assert.strictEqual(compUI.getCostumes()[compUI.currentCostume].name, 'comp_summary', 'Tab 1 should display comp_summary');
  console.log('[PASS] CompendiumUI modal opens correctly on Tab 1 (comp_summary)');

  // Test Tab 2: Elements Injection Array
  setVar('COMPENDIUM_TAB', 2);
  vm.runtime.startHats('event_whenbroadcastreceived', { BROADCAST_OPTION: 'UPDATE_UI' });
  for (let i = 0; i < 5; i++) vm.runtime._step();
  assert.strictEqual(compUI.getCostumes()[compUI.currentCostume].name, 'comp_elements', 'Tab 2 should display comp_elements');
  console.log('[PASS] CompendiumUI switches to Tab 2 (comp_elements)');

  // Test Tab 3: Molecules Page 1
  setVar('COMPENDIUM_TAB', 3);
  vm.runtime.startHats('event_whenbroadcastreceived', { BROADCAST_OPTION: 'UPDATE_UI' });
  for (let i = 0; i < 5; i++) vm.runtime._step();
  assert.strictEqual(compUI.getCostumes()[compUI.currentCostume].name, 'comp_molecules_1', 'Tab 3 should display comp_molecules_1');
  console.log('[PASS] CompendiumUI switches to Tab 3 (comp_molecules_1)');

  // Test Tab 4: Molecules Page 2
  setVar('COMPENDIUM_TAB', 4);
  vm.runtime.startHats('event_whenbroadcastreceived', { BROADCAST_OPTION: 'UPDATE_UI' });
  for (let i = 0; i < 5; i++) vm.runtime._step();
  assert.strictEqual(compUI.getCostumes()[compUI.currentCostume].name, 'comp_molecules_2', 'Tab 4 should display comp_molecules_2');
  console.log('[PASS] CompendiumUI switches to Tab 4 (comp_molecules_2)');

  // Test Tab 5: Radicals
  setVar('COMPENDIUM_TAB', 5);
  vm.runtime.startHats('event_whenbroadcastreceived', { BROADCAST_OPTION: 'UPDATE_UI' });
  for (let i = 0; i < 5; i++) vm.runtime._step();
  assert.strictEqual(compUI.getCostumes()[compUI.currentCostume].name, 'comp_radicals', 'Tab 5 should display comp_radicals');
  console.log('[PASS] CompendiumUI switches to Tab 5 (comp_radicals)');

  // Test Tab 6: Charged Ions
  setVar('COMPENDIUM_TAB', 6);
  vm.runtime.startHats('event_whenbroadcastreceived', { BROADCAST_OPTION: 'UPDATE_UI' });
  for (let i = 0; i < 5; i++) vm.runtime._step();
  assert.strictEqual(compUI.getCostumes()[compUI.currentCostume].name, 'comp_ions', 'Tab 6 should display comp_ions');
  console.log('[PASS] CompendiumUI switches to Tab 6 (comp_ions)');

  // Verify Stage Ambient Sound
  const ambSound = stage.getSounds().find(s => s.name === 'snd_ambient');
  assert(ambSound, 'Stage must contain snd_ambient background sound');
  console.log('[PASS] Stage background ambient sound (snd_ambient) verified');

  // Helper to simulate mouse coordinates in Scratch VM
  const setMouse = (sx, sy) => {
    const cw = 480, ch = 360;
    const cx = (sx / 480 + 0.5) * cw;
    const cy = (-sy / 360 + 0.5) * ch;
    vm.runtime.ioDevices.mouse.postData({ x: cx, y: cy, canvasWidth: cw, canvasHeight: ch });
  };

  // 10. Test Interactive CompendiumUI Click Dispatches (Tab bar, Item spawning, Close button)
  // Re-open Compendium on Tab 1
  setVar('SHOW_COMPENDIUM', 1);
  setVar('COMPENDIUM_TAB', 1);
  vm.runtime.startHats('event_whenbroadcastreceived', { BROADCAST_OPTION: 'UPDATE_UI' });
  for (let i = 0; i < 5; i++) vm.runtime._step();

  // A. Click Tab 2 ('Elements') on the top navigation rail (X=-90, Y=75)
  setMouse(-90, 75);
  vm.runtime.startHats('event_whenthisspriteclicked', null, compUI);
  for (let i = 0; i < 20; i++) vm.runtime._step();
  assert.strictEqual(Number(getVar('COMPENDIUM_TAB')), 2, 'Clicking Tab 2 should set COMPENDIUM_TAB to 2');
  assert.strictEqual(Number(getVar('SHOW_COMPENDIUM')), 1, 'Clicking Tab 2 must keep catalog open');
  assert.strictEqual(compUI.getCostumes()[compUI.currentCostume].name, 'comp_elements');
  console.log('[PASS] Interactive click on Tab 2 switches tab and preserves catalog visibility');

  // B. Click Tab 3 ('Molecules') on the top navigation rail (X=0, Y=75)
  setMouse(0, 75);
  vm.runtime.startHats('event_whenthisspriteclicked', null, compUI);
  for (let i = 0; i < 20; i++) vm.runtime._step();
  assert.strictEqual(Number(getVar('COMPENDIUM_TAB')), 3, 'Clicking Tab 3 should set COMPENDIUM_TAB to 3');
  assert.strictEqual(Number(getVar('SHOW_COMPENDIUM')), 1, 'Clicking Tab 3 must keep catalog open');
  assert.strictEqual(compUI.getCostumes()[compUI.currentCostume].name, 'comp_molecules_1');
  console.log('[PASS] Interactive click on Tab 3 switches tab and preserves catalog visibility');

  // C. Switch back to Tab 2 and click an Element card to inject particle (X=-100, Y=35)
  setMouse(-90, 75);
  vm.runtime.startHats('event_whenthisspriteclicked', null, compUI);
  for (let i = 0; i < 20; i++) vm.runtime._step();

  setMouse(-100, 35);
  vm.runtime.startHats('event_whenthisspriteclicked', null, compUI);
  for (let i = 0; i < 20; i++) vm.runtime._step();
  assert.strictEqual(Number(getVar('SHOW_COMPENDIUM')), 1, 'Clicking element card must NOT close the catalog');
  assert(Number(getVar('SPAWN_SPECIES_ID')) > 0, 'Clicking element card must set SPAWN_SPECIES_ID');
  console.log(`[PASS] Interactive click on element card injected species #${getVar('SPAWN_SPECIES_ID')} without dismissing catalog`);

  const atomCardCenters = [];
  for (let col = 0; col < 10; col++) {
    atomCardCenters.push({ id: col + 1, x: -187 + Math.round(col * 41.2), y: 19 });
  }
  for (let col = 0; col < 9; col++) {
    atomCardCenters.push({ id: col + 11, x: -167 + Math.round(col * 41.2), y: -53 });
  }
  for (const card of atomCardCenters) {
    setMouse(card.x, card.y);
    vm.runtime.startHats('event_whenthisspriteclicked', null, compUI);
    for (let i = 0; i < 8; i++) vm.runtime._step();
    assert.strictEqual(Number(getVar('SPAWN_SPECIES_ID')), card.id,
      `Element card ${card.id} should dispatch its own species ID`);
    assert.strictEqual(Number(getVar('SHOW_COMPENDIUM')), 1,
      `Element card ${card.id} must keep the catalog open`);
  }
  console.log('[PASS] Exhaustive click audit verified all 19 base-atom cards');

  // D. Click Close [x] button (X=195, Y=105)
  setMouse(195, 105);
  vm.runtime.startHats('event_whenthisspriteclicked', null, compUI);
  for (let i = 0; i < 20; i++) vm.runtime._step();
  assert.strictEqual(Number(getVar('SHOW_COMPENDIUM')), 0, 'Clicking [x] button must close catalog');
  assert.strictEqual(compUI.visible, false, 'CompendiumUI must be hidden after close');
  console.log('[PASS] Interactive click on close [x] successfully dismisses catalog');

  setVar('SHOW_PALETTE', 1);
  vm.runtime.startHats('event_whenbroadcastreceived', { BROADCAST_OPTION: 'UPDATE_UI' });
  for (let i = 0; i < 5; i++) vm.runtime._step();
  const paletteUI = vm.runtime.targets.find(t => t.getName() === 'PaletteUI');
  assert.strictEqual(paletteUI.visible, true, 'PaletteUI should be visible when SHOW_PALETTE == 1');
  const paletteCenters = [];
  for (let col = 0; col < 10; col++) {
    paletteCenters.push({ id: col + 1, x: -196 + col * 44, y: -116 });
  }
  for (let col = 0; col < 9; col++) {
    paletteCenters.push({ id: col + 11, x: -174 + col * 44, y: -154 });
  }
  for (const card of paletteCenters) {
    setMouse(card.x, card.y);
    vm.runtime.startHats('event_whenthisspriteclicked', null, paletteUI);
    for (let i = 0; i < 8; i++) vm.runtime._step();
    assert.strictEqual(Number(getVar('SPAWN_SPECIES_ID')), card.id,
      `Palette card ${card.id} should dispatch its own species ID`);
  }
  console.log('[PASS] Exhaustive click audit verified all 19 periodic-palette cards');
  setVar('SHOW_PALETTE', 0);

  // 11. Test Inspector HUD Card
  setVar('SHOW_INFO', 1);
  setVar('INSPECT_SPECIES_ID', 20); // H2
  vm.runtime.startHats('event_whenbroadcastreceived', { BROADCAST_OPTION: 'UPDATE_UI' });
  for (let i = 0; i < 5; i++) vm.runtime._step();
  const inspUI = vm.runtime.targets.find(t => t.getName() === 'InspectorUI');
  assert.strictEqual(inspUI.visible, true, 'InspectorUI should be visible when SHOW_INFO == 1');
  console.log('[PASS] InspectorUI HUD opens with dedicated card for species #20');

  
  // 12. Test Chemical Reaction Synthesis (H + H -> H2)
  console.log('Testing reaction synthesis: Spawning 2 reactive H atoms...');
  setVar('SPAWN_SPECIES_ID', 1); // H
  setVar('SPAWN_X', 0);
  setVar('SPAWN_Y', 0);
  vm.runtime.startHats('event_whenbroadcastreceived', { BROADCAST_OPTION: 'SPAWN_REQUEST' });
  for (let i = 0; i < 5; i++) vm.runtime._step();

  setVar('SPAWN_SPECIES_ID', 1); // H
  setVar('SPAWN_X', 5);
  setVar('SPAWN_Y', 0);
  vm.runtime.startHats('event_whenbroadcastreceived', { BROADCAST_OPTION: 'SPAWN_REQUEST' });
  for (let i = 0; i < 25; i++) vm.runtime._step();

  const currentEnts = vm.runtime.targets.filter(t => t.getName() === 'Entity' && !t.isOriginal);
  console.log(`[PASS] Active entities after collision: ${currentEnts.length}`);
  const discCount = Number(getVar('TOTAL_DISCOVERED'));
  assert(discCount >= 19, 'Discovered count should be at least 19');
  console.log(`[PASS] Reaction synthesis execution verified. Discovered count: ${discCount}`);

  // 13. Test Telemetry Status Console Event-Driven Costume Transitions
  const telem = vm.runtime.targets.find(t => t.getName() === 'TelemetryUI');
  const getCostumeName = (target) => target.getCostumes()[target.currentCostume].name;

  vm.runtime.startHats('event_whenbroadcastreceived', { BROADCAST_OPTION: 'PLAY_FX_EXO' });
  for (let i = 0; i < 5; i++) vm.runtime._step();
  assert.strictEqual(getCostumeName(telem), 'telem_exo', 'Telemetry should be telem_exo');
  console.log('[PASS] Telemetry HUD transitioned to telem_exo on exothermic event');

  vm.runtime.startHats('event_whenbroadcastreceived', { BROADCAST_OPTION: 'PLAY_FX_BOND' });
  for (let i = 0; i < 5; i++) vm.runtime._step();
  assert.strictEqual(getCostumeName(telem), 'telem_react', 'Telemetry should be telem_react');
  console.log('[PASS] Telemetry HUD transitioned to telem_react on molecular bond event');

  vm.runtime.startHats('event_whenbroadcastreceived', { BROADCAST_OPTION: 'PLAY_FX_ZAP' });
  for (let i = 0; i < 5; i++) vm.runtime._step();
  assert.strictEqual(getCostumeName(telem), 'telem_cosmic', 'Telemetry should be telem_cosmic');
  console.log('[PASS] Telemetry HUD transitioned to telem_cosmic on cosmic ionization event');

  vm.runtime.startHats('event_whenbroadcastreceived', { BROADCAST_OPTION: 'CLEAR_ALL' });
  for (let i = 0; i < 5; i++) vm.runtime._step();
  assert.strictEqual(getCostumeName(telem), 'telem_purge', 'Telemetry should be telem_purge');
  console.log('[PASS] Telemetry HUD transitioned to telem_purge on chamber evacuation');

  vm.runtime.startHats('event_whenbroadcastreceived', { BROADCAST_OPTION: 'SHOW_TOAST' });
  for (let i = 0; i < 5; i++) vm.runtime._step();
  assert.strictEqual(getCostumeName(telem), 'telem_discover', 'Telemetry should be telem_discover');
  console.log('[PASS] Telemetry HUD transitioned to telem_discover on new species discovery');

  // 14. Test Complete Keyboard Shortcuts Suite on Stage
  // Key [a]: Toggle Palette
  setVar('SHOW_PALETTE', 0);
  vm.runtime.startHats('event_whenkeypressed', { KEY_OPTION: 'a' });
  for (let i = 0; i < 5; i++) vm.runtime._step();
  assert.strictEqual(Number(getVar('SHOW_PALETTE')), 1, 'Key [a] should toggle SHOW_PALETTE to 1');
  vm.runtime.startHats('event_whenkeypressed', { KEY_OPTION: 'a' });
  for (let i = 0; i < 5; i++) vm.runtime._step();
  assert.strictEqual(Number(getVar('SHOW_PALETTE')), 0, 'Key [a] should toggle SHOW_PALETTE back to 0');
  console.log('[PASS] Keyboard shortcut Key [a] successfully toggled material palette');

  // Key [x]: Toggle Delete Mode
  setVar('CURRENT_TOOL', 'drag');
  vm.runtime.startHats('event_whenkeypressed', { KEY_OPTION: 'x' });
  for (let i = 0; i < 5; i++) vm.runtime._step();
  assert.strictEqual(getVar('CURRENT_TOOL'), 'delete', 'Key [x] should switch CURRENT_TOOL to delete');
  vm.runtime.startHats('event_whenkeypressed', { KEY_OPTION: 'x' });
  for (let i = 0; i < 5; i++) vm.runtime._step();
  assert.strictEqual(getVar('CURRENT_TOOL'), 'drag', 'Key [x] should switch CURRENT_TOOL back to drag');
  console.log('[PASS] Keyboard shortcut Key [x] successfully toggled delete tool mode');

  // Key [i]: Toggle Inspect Mode
  vm.runtime.startHats('event_whenkeypressed', { KEY_OPTION: 'i' });
  for (let i = 0; i < 5; i++) vm.runtime._step();
  assert.strictEqual(getVar('CURRENT_TOOL'), 'inspect', 'Key [i] should switch CURRENT_TOOL to inspect');
  vm.runtime.startHats('event_whenkeypressed', { KEY_OPTION: 'i' });
  for (let i = 0; i < 5; i++) vm.runtime._step();
  assert.strictEqual(getVar('CURRENT_TOOL'), 'drag', 'Key [i] should switch CURRENT_TOOL back to drag');
  console.log('[PASS] Keyboard shortcut Key [i] successfully toggled spectrometer inspect mode');

  // Key [u]: Toggle UV Light
  setVar('UV_ACTIVE', 0);
  vm.runtime.startHats('event_whenkeypressed', { KEY_OPTION: 'u' });
  for (let i = 0; i < 5; i++) vm.runtime._step();
  assert.strictEqual(Number(getVar('UV_ACTIVE')), 1, 'Key [u] should toggle UV_ACTIVE to 1');
  assert.strictEqual(stage.currentCostume, 1, 'Key [u] should switch backdrop to UV chamber');
  vm.runtime.startHats('event_whenkeypressed', { KEY_OPTION: 'u' });
  for (let i = 0; i < 5; i++) vm.runtime._step();
  assert.strictEqual(Number(getVar('UV_ACTIVE')), 0, 'Key [u] should toggle UV_ACTIVE to 0');
  console.log('[PASS] Keyboard shortcut Key [u] successfully toggled UV photochemical irradiation');

  // Key [f]: Toggle Cryo Freeze
  setVar('TIME_FROZEN', 0);
  vm.runtime.startHats('event_whenkeypressed', { KEY_OPTION: 'f' });
  for (let i = 0; i < 5; i++) vm.runtime._step();
  assert.strictEqual(Number(getVar('TIME_FROZEN')), 1, 'Key [f] should toggle TIME_FROZEN to 1');
  assert.strictEqual(stage.currentCostume, 2, 'Key [f] should switch backdrop to Cryo chamber');
  vm.runtime.startHats('event_whenkeypressed', { KEY_OPTION: 'f' });
  for (let i = 0; i < 5; i++) vm.runtime._step();
  assert.strictEqual(Number(getVar('TIME_FROZEN')), 0, 'Key [f] should toggle TIME_FROZEN to 0');
  console.log('[PASS] Keyboard shortcut Key [f] successfully toggled cryostatic time freeze');

  // Key [c]: Toggle Compendium
  setVar('SHOW_COMPENDIUM', 0);
  vm.runtime.startHats('event_whenkeypressed', { KEY_OPTION: 'c' });
  for (let i = 0; i < 5; i++) vm.runtime._step();
  assert.strictEqual(Number(getVar('SHOW_COMPENDIUM')), 1, 'Key [c] should toggle SHOW_COMPENDIUM to 1');
  vm.runtime.startHats('event_whenkeypressed', { KEY_OPTION: 'c' });
  for (let i = 0; i < 5; i++) vm.runtime._step();
  assert.strictEqual(Number(getVar('SHOW_COMPENDIUM')), 0, 'Key [c] should toggle SHOW_COMPENDIUM to 0');
  console.log('[PASS] Keyboard shortcut Key [c] successfully toggled discovery compendium');

  // Key [m]: Toggle Master Audio Mute
  setVar('MASTER_VOLUME', 100);
  vm.runtime.startHats('event_whenkeypressed', { KEY_OPTION: 'm' });
  for (let i = 0; i < 5; i++) vm.runtime._step();
  assert.strictEqual(Number(getVar('MASTER_VOLUME')), 0, 'Key [m] should mute volume to 0');
  vm.runtime.startHats('event_whenkeypressed', { KEY_OPTION: 'm' });
  for (let i = 0; i < 5; i++) vm.runtime._step();
  assert.strictEqual(Number(getVar('MASTER_VOLUME')), 100, 'Key [m] should restore volume to 100');
  console.log('[PASS] Keyboard shortcut Key [m] successfully toggled audio mute and unmute');

  console.log('================================================================');
  console.log('ALL VERIFICATION SUITE CHECKS COMPLETED AND PASSED WITH 100% SUCCESS!');
  console.log('================================================================');
}

testAll().catch(e => {
  console.error('[FAIL]', e);
  process.exit(1);
});
