const fs = require('fs');
const assert = require('assert');
const VirtualMachine = require('scratch-vm');

async function testExhaustiveCatalog() {
  console.log('=== STARTING EXHAUSTIVE CATALOG VERIFICATION SUITE ===');

  const vm = new VirtualMachine();
  const buf = fs.readFileSync('sb3/ChemistrySimulator.sb3');
  await vm.loadProject(buf);
  console.log('[PASS] Scratch VM loadProject completed cleanly');

  vm.runtime.currentStepTime = 33;
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

  const compUI = vm.runtime.targets.find(t => t.getName() === 'CompendiumUI');
  assert(compUI, 'CompendiumUI sprite must exist');

  const setMouse = (sx, sy) => {
    const cw = 480, ch = 360;
    const cx = (sx / 480 + 0.5) * cw;
    const cy = (-sy / 360 + 0.5) * ch;
    vm.runtime.ioDevices.mouse.postData({ x: cx, y: cy, canvasWidth: cw, canvasHeight: ch });
  };

  const clickComp = (sx, sy) => {
    setMouse(sx, sy);
    vm.runtime.startHats('event_whenthisspriteclicked', null, compUI);
    for (let i = 0; i < 8; i++) vm.runtime._step();
  };

  // 1. Open Compendium on Tab 1
  setVar('SHOW_COMPENDIUM', 1);
  setVar('COMPENDIUM_TAB', 1);
  vm.runtime.startHats('event_whenbroadcastreceived', { BROADCAST_OPTION: 'UPDATE_UI' });
  for (let i = 0; i < 5; i++) vm.runtime._step();
  assert.strictEqual(compUI.visible, true);
  console.log('[PASS] Compendium opened on Tab 1');

  // Test 4 Category Jump Cards on Tab 1
  // Card 1: Atoms (x: -160, y: 0)
  clickComp(-160, 0);
  assert.strictEqual(Number(getVar('COMPENDIUM_TAB')), 2, 'Card 1 must switch to Tab 2 (Elements)');
  console.log('[PASS] Category Card 1 (Atoms) switched to Tab 2');

  setVar('COMPENDIUM_TAB', 1);
  vm.runtime.startHats('event_whenbroadcastreceived', { BROADCAST_OPTION: 'UPDATE_UI' });
  for (let i = 0; i < 5; i++) vm.runtime._step();

  // Card 2: Molecules (x: -50, y: 0)
  clickComp(-50, 0);
  assert.strictEqual(Number(getVar('COMPENDIUM_TAB')), 3, 'Card 2 must switch to Tab 3 (Molecules)');
  console.log('[PASS] Category Card 2 (Molecules) switched to Tab 3');

  setVar('COMPENDIUM_TAB', 1);
  vm.runtime.startHats('event_whenbroadcastreceived', { BROADCAST_OPTION: 'UPDATE_UI' });
  for (let i = 0; i < 5; i++) vm.runtime._step();

  // Card 3: Radicals (x: 50, y: 0)
  clickComp(50, 0);
  assert.strictEqual(Number(getVar('COMPENDIUM_TAB')), 5, 'Card 3 must switch to Tab 5 (Radicals)');
  console.log('[PASS] Category Card 3 (Radicals) switched to Tab 5');

  setVar('COMPENDIUM_TAB', 1);
  vm.runtime.startHats('event_whenbroadcastreceived', { BROADCAST_OPTION: 'UPDATE_UI' });
  for (let i = 0; i < 5; i++) vm.runtime._step();

  // Card 4: Ions (x: 160, y: 0)
  clickComp(160, 0);
  assert.strictEqual(Number(getVar('COMPENDIUM_TAB')), 6, 'Card 4 must switch to Tab 6 (Ions)');
  console.log('[PASS] Category Card 4 (Ions) switched to Tab 6');

  // 2. Test Tab Bar navigation
  clickComp(-165, 80);
  assert.strictEqual(Number(getVar('COMPENDIUM_TAB')), 1, 'Tab 1 button must switch to Tab 1');
  console.log('[PASS] Tab bar switched to Tab 1 (Summary)');

  clickComp(-85, 80);
  assert.strictEqual(Number(getVar('COMPENDIUM_TAB')), 2, 'Tab 2 button must switch to Tab 2');
  console.log('[PASS] Tab bar switched to Tab 2 (Elements)');

  clickComp(0, 80);
  assert.strictEqual(Number(getVar('COMPENDIUM_TAB')), 3, 'Tab 3 button must switch to Tab 3');
  console.log('[PASS] Tab bar switched to Tab 3 (Molecules)');

  clickComp(88, 80);
  assert.strictEqual(Number(getVar('COMPENDIUM_TAB')), 5, 'Tab 5 button must switch to Tab 5');
  console.log('[PASS] Tab bar switched to Tab 5 (Radicals)');

  clickComp(170, 80);
  assert.strictEqual(Number(getVar('COMPENDIUM_TAB')), 6, 'Tab 6 button must switch to Tab 6');
  console.log('[PASS] Tab bar switched to Tab 6 (Ions)');

  // 3. Test Pagination between Tab 3 and Tab 4
  setVar('COMPENDIUM_TAB', 3);
  vm.runtime.startHats('event_whenbroadcastreceived', { BROADCAST_OPTION: 'UPDATE_UI' });
  for (let i = 0; i < 5; i++) vm.runtime._step();

  clickComp(160, 64);
  assert.strictEqual(Number(getVar('COMPENDIUM_TAB')), 4, 'Clicking Next Page on Tab 3 must switch to Tab 4');
  console.log('[PASS] Pagination: Next Page switched from Tab 3 to Tab 4');

  clickComp(85, 64);
  assert.strictEqual(Number(getVar('COMPENDIUM_TAB')), 3, 'Clicking Prev Page on Tab 4 must switch to Tab 3');
  console.log('[PASS] Pagination: Prev Page switched from Tab 4 to Tab 3');

  // 4. Test Tab 2: All 19 Element Cards
  setVar('COMPENDIUM_TAB', 2);
  vm.runtime.startHats('event_whenbroadcastreceived', { BROADCAST_OPTION: 'UPDATE_UI' });
  for (let i = 0; i < 5; i++) vm.runtime._step();

  const atomCardCenters = [];
  for (let col = 0; col < 10; col++) {
    atomCardCenters.push({ id: col + 1, x: -187 + Math.round(col * 41.2), y: 19 });
  }
  for (let col = 0; col < 9; col++) {
    atomCardCenters.push({ id: col + 11, x: -167 + Math.round(col * 41.2), y: -53 });
  }
  for (const card of atomCardCenters) {
    clickComp(card.x, card.y);
    assert.strictEqual(Number(getVar('SPAWN_SPECIES_ID')), card.id, `Element card ${card.id} dispatch`);
    assert.strictEqual(Number(getVar('SHOW_COMPENDIUM')), 1, 'Must keep catalog open');
  }
  console.log(`[PASS] Verified all 19 Base Element cards on Tab 2`);

  // Helper for 8-card grid verification
  const cardCols = [-157, -53, 51, 155];
  const rowY = [17, -55];

  function test8Grid(tabNum, tabName, expectedIds) {
    setVar('COMPENDIUM_TAB', tabNum);
    vm.runtime.startHats('event_whenbroadcastreceived', { BROADCAST_OPTION: 'UPDATE_UI' });
    for (let i = 0; i < 5; i++) vm.runtime._step();

    for (let row = 0; row < 2; row++) {
      for (let col = 0; col < 4; col++) {
        const idx = row * 4 + col;
        const expectedId = expectedIds[idx];
        const x = cardCols[col];
        const y = rowY[row];
        clickComp(x, y);
        assert.strictEqual(Number(getVar('SPAWN_SPECIES_ID')), expectedId,
          `${tabName} card [${row}, ${col}] must dispatch species #${expectedId}`);
        assert.strictEqual(Number(getVar('SHOW_COMPENDIUM')), 1, 'Must keep catalog open');
      }
    }
    console.log(`[PASS] Verified all 8 cards on ${tabName} (Tab ${tabNum})`);
  }

  // 5. Test Tab 3: Molecules Page 1
  test8Grid(3, 'Molecules (Page 1)', [20, 21, 22, 25, 39, 40, 44, 47]);

  // 6. Test Tab 4: Molecules Page 2
  test8Grid(4, 'Molecules (Page 2)', [30, 32, 57, 58, 60, 71, 85, 106]);

  // 7. Test Tab 5: Radicals
  test8Grid(5, 'Free Radicals', [41, 42, 43, 28, 46, 29, 27, 56]);

  // 8. Test Tab 6: Ions
  test8Grid(6, 'Charged Ions', [109, 111, 118, 117, 123, 124, 119, 129]);

  // 9. Test Close buttons
  // Top-right close [x]
  clickComp(195, 105);
  assert.strictEqual(Number(getVar('SHOW_COMPENDIUM')), 0, 'Top-right [x] must close catalog');
  assert.strictEqual(compUI.visible, false);
  console.log('[PASS] Top-right close button dismissed catalog');

  // Bottom-right close [CLOSE CATALOG]
  setVar('SHOW_COMPENDIUM', 1);
  vm.runtime.startHats('event_whenbroadcastreceived', { BROADCAST_OPTION: 'UPDATE_UI' });
  for (let i = 0; i < 5; i++) vm.runtime._step();

  clickComp(150, -110);
  assert.strictEqual(Number(getVar('SHOW_COMPENDIUM')), 0, 'Bottom-right close button must close catalog');
  assert.strictEqual(compUI.visible, false);
  console.log('[PASS] Bottom-right close button dismissed catalog');

  // 10. Test Reset Archive button
  setVar('SHOW_COMPENDIUM', 1);
  vm.runtime.startHats('event_whenbroadcastreceived', { BROADCAST_OPTION: 'UPDATE_UI' });
  for (let i = 0; i < 5; i++) vm.runtime._step();

  clickComp(-150, -110);
  const survivingEntities = vm.runtime.targets.filter(t => t.getName() === 'Entity' && !t.isOriginal).length;
  assert.strictEqual(survivingEntities, 0, 'Reset Archive button must clear chamber entities');
  console.log('[PASS] Reset Archive button successfully cleared chamber');

  console.log('================================================================');
  console.log('EXHAUSTIVE CATALOG VERIFICATION: ALL 57 INTERACTIVE ELEMENTS PASSED!');
  console.log('================================================================');
}

testExhaustiveCatalog().catch(e => {
  console.error('[FAIL]', e);
  process.exit(1);
});
