# MASTER DIRECTIVE — STOP AI-SLOP UI GENERATION AND LEARN PROFESSIONAL UI DESIGN FIRST

You have full access to this repository and are responsible for improving its graphical user interface.

Repository:

https://github.com/xtenrore/scratch/tree/main

There is one extremely important problem:

**The current GUI looks AI-generated.**

You have repeatedly produced interfaces that look like generic AI/vibe-coded dashboards instead of something a professional human game/UI designer would actually make.

I do NOT want another minor improvement to the current GUI.

I want you to fundamentally change HOW you approach UI design.

---

# 1. FIRST: STOP CODING

Do NOT immediately modify the project.

Do NOT immediately edit `gen_graphics.py`.

Do NOT immediately generate new SVGs.

Do NOT assume that your existing approach to GUI design is correct.

Do NOT look at the current GUI and simply make it "more polished."

Your first job is to LEARN.

Treat yourself as if you are a programmer who has never professionally designed a GUI before.

Your existing instincts for generating interfaces are NOT trusted.

For this task:

**research first, design second, code third.**

---

# 2. YOU MUST RESEARCH PROFESSIONAL UI DESIGN

Use the internet extensively.

Do not perform one quick Google search and then start coding.

Perform a serious research phase.

Research how professional designers actually create:

* game interfaces
* educational game interfaces
* children's/teen interfaces
* science/chemistry interfaces
* Scratch interfaces
* vector interfaces
* SVG interfaces
* game HUDs
* menus
* cards
* buttons
* tabs
* navigation
* dialogs
* information panels
* inventories
* encyclopedias/compendiums
* interactive learning interfaces

Look at REAL interfaces.

Prefer studying actual shipped products, established design systems, professional portfolios, design documentation, open-source projects, and high-quality games.

Do not use random AI-generated UI galleries as your design reference.

Do not copy a single game's appearance.

Instead, study WHY professional interfaces look professional.

---

# 3. LEARN THE DIFFERENCE BETWEEN "DECORATED" AND "DESIGNED"

This is extremely important.

A professional interface is NOT professional because it has:

* gradients
* glow
* rounded rectangles
* shadows
* neon colors
* borders
* fancy fonts
* tiny technical labels
* icons everywhere
* animations everywhere

Those things are decoration.

Professional design comes from:

* hierarchy
* spacing
* alignment
* consistency
* typography
* proportion
* contrast
* grouping
* visual rhythm
* affordance
* simplicity
* intentionality
* information density
* predictable interaction
* appropriate emphasis

Study this distinction carefully.

If you find yourself adding decoration to make something "look professional", STOP and reconsider the underlying design.

---

# 4. STUDY HUMAN DESIGN DECISIONS

For every professional UI example you research, ask:

1. Why is this element located here?
2. Why is it this size?
3. Why is this text this size?
4. Why does this button look like this?
5. Why are these elements grouped together?
6. Why is this information emphasized?
7. Why is this information visually quiet?
8. What is the player's eye supposed to see first?
9. What is the player's eye supposed to see second?
10. What happens when the player interacts with it?
11. How does the interface communicate state?
12. What visual rules remain consistent throughout the interface?

Do NOT just collect screenshots.

Understand the design decisions behind them.

---

# 5. STUDY SCRATCH SPECIFICALLY

Because this is a Scratch project, research the actual Scratch ecosystem.

Study:

* Scratch's official GUI
* Scratch editor UI
* Scratch project/player UI
* Scratch component design
* Scratch vector assets
* Scratch's typography
* Scratch's buttons
* Scratch's dialogs
* Scratch's navigation
* Scratch's use of spacing
* Scratch's use of color
* Scratch's interaction states

Also inspect high-quality Scratch projects.

Do NOT copy Scratch.

Learn how Scratch designers solve interface problems.

---

# 6. STUDY PROFESSIONAL GAME UI

Research professional game interfaces.

Pay special attention to interfaces that have:

* lots of information
* educational content
* inventories
* encyclopedias
* crafting
* character/item cards
* statistics
* progression
* selection menus
* discovery systems

The game is a chemistry/educational experience.

Therefore, research interfaces from:

* educational software
* science applications
* chemistry software
* museum interactive exhibits
* educational games
* polished game encyclopedias
* polished game inventories

Again:

DO NOT COPY THEM.

Extract their design principles.

---

# 7. IDENTIFY THE CURRENT AI-SLOP PATTERNS

Before changing anything, inspect the existing project.

Find every file involved in graphics/UI generation.

Especially inspect:

* `gen_graphics.py`
* `generate_all_sprites.py`
* `build_full_project.py`
* every graphics-related script
* every SVG-generation function
* every UI asset
* every UI layout
* every generated sprite

Then create a written audit.

Identify exactly what currently makes the interface look AI-generated.

Examples to investigate:

* unnecessary borders
* excessive boxes
* excessive rounded rectangles
* meaningless labels
* fake technical terminology
* tiny text
* poor typography
* inconsistent spacing
* arbitrary colors
* excessive cyan/purple/blue
* excessive glow
* excessive gradients
* excessive symmetry
* generic dashboard layouts
* repetitive cards
* poor hierarchy
* too many controls
* decorative UI elements with no purpose
* inconsistent iconography
* bad proportions
* poor alignment
* elements that exist only because an AI thought they "look cool"

Be brutally honest.

Do not defend the current design.

---

# 8. IMPORTANT: PRESERVE FUNCTIONALITY, NOT VISUAL DESIGN

The existing GUI is NOT sacred.

You are allowed to redesign it.

Preserve:

* game mechanics
* Scratch functionality
* interactions
* data
* important asset references
* project behavior

You do NOT have to preserve:

* current colors
* current layout
* current buttons
* current panels
* current typography
* current visual hierarchy
* current SVG compositions
* current UI architecture

If the existing graphics-generation system is responsible for the poor design, redesign the system.

---

# 9. CREATE A REAL DESIGN SYSTEM BEFORE BUILDING THE GUI

Before generating the new graphics, create a design specification.

Define:

## Typography

Determine:

* primary typeface
* secondary typeface if necessary
* heading sizes
* body sizes
* labels
* button text
* numerical text
* line spacing
* letter spacing
* text hierarchy

Avoid tiny text.

Every piece of text must have a reason to exist.

---

## Color

Create a restrained palette.

Define:

* background
* surface
* elevated surface
* primary text
* secondary text
* disabled text
* primary action
* secondary action
* success
* warning
* error
* selection
* hover
* pressed

Do not randomly choose colors for individual components.

Every color must belong to the system.

---

## Spacing

Create a spacing scale.

For example:

4
8
12
16
24
32
48

Do not use random spacing values everywhere.

Everything should align to a consistent system unless there is a deliberate reason not to.

---

## Shapes

Define:

* corner radius
* border thickness
* icon size
* button height
* card proportions
* panel proportions
* spacing between controls

Do not make every component a rounded rectangle.

Different shapes should have different purposes.

---

## Shadows and depth

Define whether shadows exist.

If they do:

* how strong?
* how large?
* where are they used?

Do not add shadows randomly.

---

## Icons

Define an icon style.

Icons must look like they belong to the same family.

Do not mix:

* random emoji
* random SVG icons
* random clip-art
* random AI-generated icons
* inconsistent line weights

---

# 10. DESIGN THE INFORMATION HIERARCHY

This is more important than decoration.

For every screen, determine:

### Primary information

What should the player notice first?

### Secondary information

What should they notice after that?

### Tertiary information

What can remain visually quiet?

### Actions

What should the player be able to do?

### Feedback

How does the interface show that something happened?

If everything is emphasized, nothing is emphasized.

---

# 11. REDESIGN ONE SCREEN FIRST

Do NOT redesign the entire game at once.

Choose the most important screen.

Completely redesign that screen using the new design system.

Build it carefully.

Inspect it.

Then ask yourself:

> "If I saw this screenshot without knowing an AI created it, would I reasonably believe a human designer made it?"

If the answer is no:

DO NOT CONTINUE.

Redesign it.

---

# 12. DO NOT USE "AI DASHBOARD" DESIGN

This is a hard requirement.

Avoid the common AI-generated aesthetic:

```text
dark background
+
glowing cyan border
+
purple accent
+
many rounded cards
+
tiny uppercase labels
+
random statistics
+
gradient buttons
+
technical-looking text
+
decorative lines
+
random icons
```

That aesthetic is specifically what we are trying to eliminate.

Do not automatically choose dark mode.

Do not automatically choose neon colors.

Do not automatically use glassmorphism.

Do not automatically use gradients.

Do not automatically use rounded cards.

Choose these things ONLY when the research and design require them.

---

# 13. DO NOT OVERDESIGN

A professional designer knows when to stop.

If removing an element makes the interface clearer, remove it.

If a label is unnecessary, remove it.

If a border does not communicate anything, remove it.

If a decorative shape does not improve comprehension, remove it.

If a color does not communicate meaning, remove it.

If an animation exists only because it looks cool, remove it.

The goal is:

**clarity + personality + polish**

not:

**maximum visual effects.**

---

# 14. MANUALLY CONSTRUCT THE VECTOR GRAPHICS

The graphics should be deliberately constructed.

Do not ask an AI image generator to invent the UI.

Do not create generic raster images and call them UI.

Use carefully authored SVG/vector graphics where appropriate.

Construct:

* shapes
* icons
* panels
* buttons
* cards
* indicators
* illustrations
* chemistry-related visual elements

from intentional geometry.

Every path, shape, stroke, and text element should have a purpose.

---

# 15. BUILD REUSABLE COMPONENTS

Create a proper component vocabulary.

For example:

* Button
* IconButton
* Tab
* Panel
* Card
* Modal
* Tooltip
* Badge
* ProgressBar
* Toggle
* Dropdown
* NavigationItem
* ElementCard
* MoleculeCard
* ResultCard
* Notification

Each component should have defined states:

* default
* hover
* pressed
* selected
* disabled
* focused
* active

Do not manually invent a slightly different button every time.

---

# 16. THE CHEMISTRY UI NEEDS PERSONALITY

This is a chemistry game.

The interface should feel appropriate for chemistry.

But do NOT accomplish that by putting random:

* atom icons
* molecule icons
* equations
* scientific labels
* "LAB SYSTEM ONLINE"
* "ATOMIC DATABASE"
* "SPECIMEN"
* fake technical terminology

everywhere.

Instead, create a visual identity inspired by chemistry.

Use things like:

* meaningful molecular geometry
* periodic-table-inspired structure where appropriate
* scientific diagram language
* carefully chosen scientific notation
* restrained laboratory-inspired visual motifs
* elegant molecular illustrations

The interface should feel like a chemistry game naturally.

It should not scream:

"LOOK, THIS IS A SCIENCE UI."

---

# 17. TYPOGRAPHY IS CRITICAL

Stop using tiny text to make interfaces look sophisticated.

Tiny text does NOT automatically look professional.

Use a clear hierarchy.

For example:

Large:
screen title

Medium:
section title

Normal:
important information

Small:
secondary information

Very small:
only genuinely necessary metadata

If a player needs to squint to understand the interface, the typography is wrong.

---

# 18. USE REAL VISUAL QA

After implementing a screen:

1. Run/build the project.
2. Open the resulting project.
3. Capture screenshots.
4. Inspect the screenshot.
5. Compare it against professional references.
6. Identify weaknesses.
7. Fix them.
8. Repeat.

Do not assume that because the SVG code looks clean, the resulting GUI looks good.

The final rendered result is what matters.

---

# 19. CRITIQUE YOUR OWN WORK

After every major UI implementation, perform a harsh critique.

Use this checklist:

### Does it look AI-generated?

Yes / No

### Is there unnecessary decoration?

Yes / No

### Is the typography professional?

Yes / No

### Is the spacing consistent?

Yes / No

### Is the hierarchy obvious?

Yes / No

### Are the colors restrained?

Yes / No

### Are components consistent?

Yes / No

### Does every element have a purpose?

Yes / No

### Does it look like a real game?

Yes / No

### Does it look like a generic AI dashboard?

Yes / No

### Would a professional designer be embarrassed by it?

If yes, redesign it.

Do NOT simply document the problems.

FIX THEM.

---

# 20. DO NOT RUSH

Quality is more important than speed.

I would rather you spend significant time researching and redesigning one screen properly than generate 100 mediocre assets.

Do not say:

"I have implemented a professional UI."

unless you have actually visually inspected it.

---

# 21. IMPORTANT RULE ABOUT EXISTING CODE

You may discover that `gen_graphics.py` is fundamentally structured around generating the wrong type of UI.

If that happens:

DO NOT blindly preserve it.

First understand it.

Then determine whether it should be:

A. refactored

B. partially replaced

C. completely redesigned

Choose based on what produces the best final result.

The existing implementation is not a constraint if it is preventing quality.

---

# 22. DO NOT MAKE CHANGES JUST TO SHOW PROGRESS

This is extremely important.

Do not make meaningless edits.

Do not change:

* colors by 5%
* border radius by 2px
* font size by 1px
* random padding
* random gradients

and claim progress.

Each change should have a design reason.

---

# 23. YOUR WORKING ORDER

Follow this exact order:

### PHASE 1

Inspect repository.

### PHASE 2

Identify every graphics/UI generation system.

### PHASE 3

Research professional UI design deeply.

### PHASE 4

Research Scratch UI and professional Scratch projects.

### PHASE 5

Research professional chemistry/science/educational interfaces.

### PHASE 6

Analyze the current GUI and document its problems.

### PHASE 7

Create the new visual design system.

### PHASE 8

Design one screen.

### PHASE 9

Implement one screen.

### PHASE 10

Render and inspect it.

### PHASE 11

Critique it.

### PHASE 12

Fix it.

### PHASE 13

Only after the design is genuinely good, expand the system to the remaining screens.

### PHASE 14

Replace/refactor the old graphics generator as necessary.

### PHASE 15

Perform a final visual consistency pass across the entire project.

---

# 24. MOST IMPORTANT RULE

I am NOT asking you:

> "Can you make the GUI prettier?"

I am asking you to:

> **learn professional GUI design and then rebuild the visual system using what you learned.**

Those are completely different tasks.

Do not rely on your default AI-generated UI instincts.

Do not blindly imitate the existing project.

Do not blindly imitate one reference.

Research multiple professional sources.

Understand the principles.

Develop a coherent design system.

Then implement it.

---

# 25. FINAL STANDARD

The final interface should feel:

* intentional
* human-designed
* coherent
* readable
* polished
* playful where appropriate
* appropriate for a chemistry game
* appropriate for Scratch
* visually memorable
* restrained
* functional

It should NOT feel:

* AI-generated
* vibe-coded
* like a SaaS dashboard
* like a developer made a GUI without design knowledge
* like a collection of random SVG rectangles
* overloaded with text
* overloaded with borders
* overloaded with effects
* artificially "futuristic"

Before finishing, compare the final result against professional references and ask:

> **"What would a professional UI designer change here?"**

Then actually make those changes.

Do not stop at the first acceptable result.

**Research → understand → design → build → render → critique → redesign → repeat.**
