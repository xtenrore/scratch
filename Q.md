# MASTER INSTRUCTION — COMPLETE PROFESSIONAL GUI OVERHAUL

You have full access to the existing project.

Your job is to take the existing Scratch game and transform its entire GUI/visual presentation into something that looks **professionally designed, intentional, polished, cohesive, and human-made**.

The current GUI is NOT acceptable.

It looks like generic AI-generated UI / "AI slop."

You must completely change your approach to visual design.

---

# CRITICAL: FORGET YOUR CURRENT GUI DESIGN HABITS

For this task, assume that your existing instincts for creating game interfaces are BAD.

Do NOT rely on your learned patterns for:

* buttons
* panels
* menus
* cards
* gradients
* shadows
* colors
* borders
* rounded rectangles
* HUDs
* icons
* layouts
* decorative elements
* game interfaces

Do not think:

> "I already know how to make a game GUI."

You don't.

For this project, you are starting the visual-design process from ZERO.

Your existing coding knowledge is fine.

Your existing assumptions about professional visual design are NOT to be trusted.

---

# RESEARCH BEFORE DESIGNING

Before designing or rebuilding any significant GUI element, research how professional game designers actually approach that type of interface.

You MUST use web research.

Do not immediately generate something from memory.

Research professional examples from sources such as:

* professional game UI portfolios
* GDC presentations
* game UI/UX case studies
* professional game-art websites
* established indie games
* polished commercial games
* professional interface design systems
* game HUD breakdowns
* professional iconography references
* professional menu design references

Study MULTIPLE examples.

Do not copy their artwork.

Do not clone another game's interface.

Instead determine:

* why the layout works
* how visual hierarchy is established
* how spacing is handled
* how typography is handled
* how buttons communicate interaction
* how selected states work
* how disabled states work
* how panels are structured
* how color is used
* how contrast is controlled
* how depth is communicated
* how decoration is used without becoming clutter
* how the interface communicates the game's identity

Then apply those principles to THIS game.

---

# DO NOT SEARCH FOR AI-GENERATED GUI EXAMPLES

Do NOT use other AI-generated interfaces as your primary design reference.

You are trying to escape generic AI visual patterns.

Your references should primarily come from professionally designed games and professional UI/UX work.

---

# NO AI-SLOP

Do NOT automatically use:

* giant rounded rectangles
* excessive rounded corners
* glassmorphism
* random gradients
* purple/blue AI palettes
* neon everywhere
* unnecessary glow
* giant floating cards
* excessive shadows
* random outlines
* decorative circles
* random lines
* fake 3D bevels
* excessive gradients
* excessive blur
* meaningless particles
* generic dashboard layouts
* huge icons
* giant empty spaces
* excessive visual effects
* decorative elements with no purpose

These are NOT forbidden if the game's actual visual language genuinely calls for them.

But never use them simply because they are common AI-generated UI patterns.

Every visual decision must have a reason.

---

# THIS IS A GAME, NOT A DASHBOARD

The interface must feel like it belongs to an actual game.

Do NOT make the project look like:

* a SaaS dashboard
* a website
* a generic mobile app
* an AI-generated landing page
* a template
* a random collection of UI cards

Design it as a cohesive game.

---

# DESIGN THE ENTIRE GUI SYSTEM

Do not fix only one screen.

Inspect the ENTIRE project and identify every GUI component.

This includes, where applicable:

* main menu
* play/start screen
* catalog
* item browser
* item cards
* item details
* navigation
* buttons
* tabs
* filters
* category selectors
* selected states
* hover states
* pressed states
* disabled states
* counters
* currency displays
* HUD
* inventory
* settings
* pause menu
* information panels
* popups
* notifications
* tooltips
* loading screens
* backgrounds
* decorative elements
* icons
* titles
* labels
* other interactive UI

Do not assume something is fine simply because it technically works.

Evaluate both:

1. visual quality
2. functionality

---

# DESIGN ONE GUI AT A TIME

Do NOT attempt to blindly redesign everything simultaneously.

Work systematically.

For each GUI:

### STEP 1 — Inspect

Understand:

* what it does
* what elements exist
* which elements are interactive
* how the player uses it
* what assets currently exist
* what is visually wrong
* what is functionally wrong

### STEP 2 — Research

Research professional examples of that specific type of interface.

### STEP 3 — Analyze

Determine the appropriate:

* hierarchy
* layout
* spacing
* proportions
* typography
* colors
* iconography
* interaction states
* visual language

### STEP 4 — Design

Create the new design based on your research.

### STEP 5 — Implement

Actually implement the design in the existing project.

Do not merely describe what should be done.

### STEP 6 — Test

Actually test it.

### STEP 7 — Critique

Look at your result critically.

Ask:

> "Does this actually look professionally designed, or does it still look like something an AI would generate?"

If it still looks AI-generated:

DO NOT ACCEPT IT.

Research more.

Redesign it.

Improve it.

### STEP 8 — Move to the next GUI

Only after the current GUI is properly finished.

---

# DO NOT USE PYTHON

Do NOT create Python scripts to generate the GUI.

Do NOT create Python-based image-generation pipelines.

Do NOT create temporary Python programs.

Do NOT solve this by writing some giant automated script that generates the interface.

Work directly with the project's existing technologies and assets.

Use the tools and workflow already available to you.

---

# DO NOT TAKE SHORTCUTS

Do not say:

> "This is good enough."

Do not stop after making the GUI technically functional.

The goal is:

**professional + functional + polished.**

Not merely:

**working.**

---

# CATALOG IS CURRENTLY BROKEN — FIX IT COMPLETELY

There is a known critical bug in the Catalog menu.

The Catalog currently has a large number of things that appear to be clickable, but ONLY FOUR of them actually respond.

When the user clicks many of the other catalog items, NOTHING happens.

This is a hard bug.

You MUST investigate and fix it.

Do NOT simply hide the broken items.

Do NOT reduce the catalog to four clickable things.

Every intended interactive catalog element must actually work.

---

# CATALOG REQUIREMENTS

Inspect the Catalog implementation carefully.

Determine:

* how catalog items are represented
* how click detection works
* how coordinates are calculated
* whether hitboxes are correct
* whether scrolling changes coordinates
* whether items overlap
* whether invisible elements intercept clicks
* whether only four items have event handlers
* whether the remaining items are missing handlers
* whether item IDs are incorrect
* whether cloned sprites have broken state
* whether lists/arrays are incomplete
* whether pagination is broken
* whether category filtering is broken
* whether the visible UI and logical click regions disagree

Find the ACTUAL ROOT CAUSE.

Do not patch symptoms.

---

# CATALOG TESTING

After fixing the Catalog, test EVERY interactive item.

Do not test only four.

Systematically click every intended clickable catalog element.

Verify that:

* clicking the item works
* the correct item is selected
* the correct item information appears
* buttons associated with the item work
* navigation works
* selection state updates correctly
* scrolling does not break hitboxes
* filtering does not break hitboxes
* returning to the catalog does not break it
* repeatedly opening/closing the catalog does not break it
* different item positions work
* edge items work
* items near screen boundaries work
* items after scrolling work
* items after changing categories work

If there are 20 items, test all 20.

If there are 50 items, test all 50.

Do not assume that because four work, the rest work.

---

# TEST THE GUI LIKE A REAL PLAYER

After implementing each GUI, actually interact with it.

Test:

* mouse movement
* clicking
* navigation
* opening
* closing
* returning
* selecting
* deselecting
* scrolling
* changing tabs
* changing categories
* pressing buttons repeatedly
* rapidly clicking
* moving between menus
* reopening screens
* different item selections

Look for:

* broken hitboxes
* visual overlap
* elements that don't respond
* incorrect states
* incorrect positions
* elements appearing behind other elements
* elements disappearing
* inconsistent spacing
* incorrect scaling
* text overflow
* broken navigation
* stale UI state
* assets that don't load
* inconsistent styling

Fix every issue you discover.

---

# DO NOT JUST MAKE IT PRETTY

A professional interface is BOTH:

**visually good**
AND
**functionally reliable.**

A beautiful menu with broken interactions is a failed result.

A functional menu that looks generic is also a failed result.

Both requirements matter equally.

---

# CREATE A CONSISTENT VISUAL LANGUAGE

After researching the project, establish a coherent design system.

Use consistent rules for:

* colors
* typography
* spacing
* sizing
* borders
* corner treatment
* shadows
* icon style
* button states
* selection states
* disabled states
* panels
* backgrounds
* decorative elements

The entire project should feel like it was designed by ONE professional designer.

Do not make every screen look unrelated.

---

# PRESERVE WHAT IS ALREADY GOOD

Do not destroy good existing work just for the sake of changing it.

If something is already professionally designed:

KEEP IT.

Improve only what needs improvement.

However, if something is clearly inconsistent with the new visual system, redesign it so everything feels cohesive.

---

# DO NOT COPY OTHER GAMES

Research is for understanding professional design principles.

Do not copy:

* exact layouts
* exact artwork
* copyrighted characters
* logos
* proprietary assets
* exact visual identities

The final result must be original.

---

# SCRATCH CONSTRAINTS

Everything must work properly inside the actual Scratch project.

Prioritize:

* readability
* clear silhouettes
* strong hierarchy
* appropriate scaling
* reasonable asset sizes
* clean transparent assets where appropriate
* reliable positioning
* reliable click detection
* reliable interaction states

Do not create beautiful assets that become unreadable when actually used in the Scratch game.

---

# TEXT

Do not unnecessarily bake text into images.

Whenever practical:

ICON + REAL SCRATCH TEXT

is preferable to:

IMAGE CONTAINING TEXT

This makes the interface easier to maintain and prevents generated-text errors.

---

# INSPECT THE ACTUAL PROJECT

Do not guess about how the project works.

Inspect the existing implementation.

Understand the existing architecture before modifying it.

Determine how:

* screens are switched
* sprites are positioned
* clicks are detected
* catalog items are stored
* assets are loaded
* states are tracked
* menus are opened
* menus are closed

Then make targeted improvements.

---

# TEST AFTER EVERY MAJOR CHANGE

After making substantial changes:

1. Run the project.
2. Interact with it.
3. Verify the changed GUI.
4. Verify the surrounding GUIs.
5. Verify that existing functionality wasn't broken.
6. Fix regressions immediately.

Do not make 100 changes and only test at the end.

---

# FINAL FULL-PROJECT TEST

When all GUI work is finished, perform a complete end-to-end test.

Go through the game as a normal player.

Test every major screen.

Test every important interaction.

Especially test the Catalog thoroughly.

Do not finish until:

* all intended catalog items are clickable
* all catalog interactions work
* navigation works
* GUI states work
* menus open correctly
* menus close correctly
* no obvious visual bugs remain
* no obvious interaction bugs remain
* the visual system is consistent
* the interface is readable
* the interface does not look generic or AI-generated
* existing gameplay functionality still works

---

# FINAL PROFESSIONAL DESIGN TEST

At the very end, stop thinking like an AI coding agent.

Evaluate the project as a professional game/UI designer.

Ask:

1. Does this look intentionally designed?
2. Does every visual element have a purpose?
3. Is the hierarchy obvious?
4. Is the spacing deliberate?
5. Are interactions obvious?
6. Are states communicated clearly?
7. Is the visual language consistent?
8. Does it look like a real game?
9. Does anything look like generic AI-generated UI?
10. Would a professional indie game designer be embarrassed to ship any of these screens?

If the answer to #9 or #10 is yes:

KEEP WORKING.

Do not declare the project finished.

---

# IMPORTANT: YOU ARE RESPONSIBLE FOR THE RESULT

Do not give me instructions telling me how to fix things myself.

Do not tell me:

> "You should change..."

Actually change it.

Do not tell me:

> "You can test this..."

Actually test it.

Do not tell me:

> "The remaining catalog items probably need..."

Actually investigate them.

Do the work yourself.

---

# COMPLETION STANDARD

The task is NOT complete when:

* the code compiles
* the project opens
* four catalog items work
* the GUI looks slightly better
* assets were generated
* the first design looks acceptable

The task is complete ONLY when the entire GUI system has been professionally redesigned, implemented, tested, and polished, AND the Catalog's interaction system has been fully repaired and verified.

Work carefully.

Research professionally.

Design deliberately.

Implement directly.

Test aggressively.

Iterate until polished.

DO NOT STOP EARLY.
