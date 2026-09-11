MASTER PROMPT — BUILD A COMPLETE SCRATCH .SB3 CHEMISTRY SIMULATOR

You are going to build ONE complete, polished Scratch project.

This is NOT a request for Scratch code examples.

This is NOT a request for pseudocode.

This is NOT a request for instructions explaining how I can build it.

Your job is to actually CREATE THE PROJECT and produce a REAL, VALID .sb3 FILE.

I am using the Gemini app on iPhone, so assume that I will not manually create dozens of files, assets, scripts, JSON structures, sprites, costumes, sounds, or Scratch blocks for you.

YOU must do the work.

If your environment supports file generation, generate the actual files.

If your environment can create archives/ZIP files, assemble the .sb3 yourself.

If your environment cannot directly produce a binary .sb3, construct every required project component in a reproducible way and clearly state the exact limitation rather than pretending that a text response is an .sb3.

⸻

1. FINAL OBJECTIVE

Create a polished chemistry/atomic simulation sandbox inspired by this concept:

“This is a simulation where you can drag and merge atoms and molecules in a vacuum.”

The user should be able to interact with atoms and molecules, combine them, create chemical species and ions, discover compounds, observe reactions, use UV light, encounter cosmic rays, freeze time, inspect information, save/load progress, and browse discovered molecules and ions.

The finished project should feel like a serious, intentionally designed Scratch simulation.

It must NOT look like an AI-generated prototype.

It must NOT look “vibecoded.”

It must look like a human skilled in Scratch spent substantial time designing, implementing, testing, polishing, and organizing it.

⸻

2. MOST IMPORTANT RULE — ACTUAL .SB3

You MUST understand the Scratch 3 .sb3 format before attempting to generate the project.

An .sb3 is not simply Scratch blocks written as text.

It is a packaged Scratch project containing project data and assets.

Understand and correctly handle:

* .sb3
* ZIP packaging
* project.json
* targets
* Stage
* sprites
* blocks
* block IDs
* opcodes
* inputs
* fields
* variables
* lists
* broadcasts
* custom blocks/procedures
* procedure mutations
* costumes
* sounds
* asset references
* layer order
* monitors where needed

The resulting file must be a genuine Scratch project.

Do NOT give me a fake .sb3.

Do NOT rename a text file to .sb3.

Do NOT produce Scratch pseudocode and call it an .sb3.

Do NOT invent Scratch opcodes.

Do NOT invent JSON structures.

Do NOT assume a block exists without verifying it.

⸻

3. LEARN THE SB3 FORMAT BEFORE BUILDING

Before creating the final project, internally establish a correct understanding of the actual Scratch 3 project format.

Use authoritative knowledge of Scratch and the SB3 format.

If tools or browsing are available, inspect actual Scratch projects and documentation.

If an actual working .sb3 reference is provided later, inspect its structure.

Understand how Scratch stores:

* sprites
* stage
* scripts
* variables
* lists
* broadcasts
* custom blocks
* costumes
* sounds
* clones
* block inputs
* block fields
* mutations

Do not rely purely on general language-model memory.

⸻

4. CREATE EVERYTHING YOURSELF

I do NOT want to manually make assets.

You must generate the assets required for the project yourself.

This includes, where appropriate:

Visual assets

* atom graphics
* molecule graphics
* ion graphics
* particle graphics
* cosmic ray graphics
* photon graphics
* reaction effects
* buttons
* icons
* UI panels
* information cards
* periodic-table interface
* backgrounds
* indicators
* selection effects
* hover/pressed states
* freeze effect
* UV effect
* delete mode visuals
* menu elements

Audio

Generate or create appropriate audio assets if the environment supports it.

Examples:

* button click
* selection sound
* merge/bond sound
* reaction sound
* exothermic reaction sound
* photon sound
* error/invalid reaction sound
* UI feedback
* subtle ambience if appropriate

DO NOT use random assets just to fill space.

Every asset must have a purpose.

If you cannot directly generate binary audio assets, implement the audio system in a way that can use generated assets later and clearly identify the limitation.

⸻

5. VISUAL DESIGN

The project must have a coherent visual identity.

Do NOT use generic AI UI.

Do NOT randomly choose colors.

Do NOT cover everything with gradients.

Do NOT make every button a giant rounded rectangle.

Do NOT use inconsistent icons.

Do NOT use placeholder graphics.

Do NOT leave default Scratch UI everywhere.

Design the interface deliberately.

The simulation should visually communicate:

* vacuum
* particles
* atoms
* molecules
* ions
* energy
* reactions
* radiation
* UV
* discovery
* scientific experimentation

The visual style should be clean, readable, polished, and cohesive.

Use consistent:

* typography
* spacing
* icon style
* button proportions
* visual hierarchy
* particle rendering
* effects
* panel design

The UI should feel like an actual interactive scientific simulation.

⸻

6. HUMAN-MADE QUALITY REQUIREMENT

Before completion, inspect the project specifically for signs of AI/vibe coding.

Reject your own implementation if you find:

* placeholder UI
* fake functionality
* buttons that do nothing
* meaningless variable names
* random colors
* repetitive layouts
* duplicated logic
* unnecessary scripts
* enormous monolithic scripts
* arbitrary broadcasts
* unused variables
* dead code
* unfinished systems
* inconsistent visuals
* excessive effects
* generic generated-looking graphics
* features that only appear visually but don’t actually work
* systems implemented independently when they should share architecture

The project should look intentional.

Another experienced Scratch developer should be able to inspect the project and understand why the architecture exists.

⸻

7. BUILD A REAL SIMULATION ENGINE

Do not implement every atom as an isolated collection of random scripts.

Create an actual underlying simulation architecture.

Represent entities with appropriate data such as:

* element
* atomic number where useful
* charge
* position
* velocity where useful
* molecule identity
* composition
* bonds
* state
* selected state
* interaction state

Use a consistent entity architecture.

Do not create unnecessary complexity if Scratch performance would suffer.

The simulation must remain responsive.

⸻

8. ATOMS

Implement the atoms/elements required by the chemistry system.

At minimum, support the elements needed to produce ALL requested species in this prompt.

This includes:

H
He
Li
Be
C
N
O
F
Ne if useful
Na
Si
P
S
Cl
Ar
K
Ca
Br
I

And any additional element required by the listed species.

Do not merely display an element’s name.

Atoms must be actual simulation entities.

They must be able to participate in the appropriate interactions.

⸻

9. MOLECULE SYSTEM

The project must support molecules as actual structured entities.

A molecule should not merely be a sprite whose costume says “H2O.”

The underlying state should know that it represents H2O and what atoms/composition it contains.

Where practical, molecules should have:

* formula
* constituent atoms
* charge
* bonds
* molecular identity
* position
* movement
* interaction state

The visual representation can simplify molecular structure for performance, but the underlying simulation state must remain coherent.

⸻

10. CHEMICAL SPECIES

Attempt to support ALL of these:

H2
H2O
O2
Li2
Be2
N2
F2
CN
NH•
NO•
HCl
Cl2
NaCl
BeCl2
ClO2
HOCl
Cl2O
KCl
CaCl2
CO
CO2
CH•
CH2•
CH3•
CH4
C2H6
NH2•
NH3
HCN
Na2CO3
H2CO
HCO•
C2H4
C2H2
CH3CHO
CH3COOH
HS•
H2S
SO2
SO3
H2SO4
NaHSO4
KHSO4
S2
S3
S4
N4
S4N4
S2Cl2
NH4Cl
SiO
SiO2
Na2SiO3
SiH•
SiH2•
SiH3•
SiH4
Si2H6
K2SiO3
P2
P4
PH•
PH2•
PH3
P4O10
H3PO4
PN
Na3PO4
KH2PO4
O3
H2O2
Br2
I2
HF
HBr
HI
NaF
KF
NaBr
KBr
NaI
KI
HArF
CaO
Ca(OH)2
CaCO3
NaOH
OF2

Attempt to support every species.

Do NOT fake support.

If a particular species requires special handling, implement it deliberately and document the simulation rule.

⸻

11. IONS

Support:

H-
H+
H3+
OH-
H2+
NH+
N+
CN-
HeH+
Cl-
Na+
CO3-2
HCO3-
S-2
HSO4-
H3O+
SO4-2
K+
SiO3-2
H2PO4-
HPO4-2
PO4-3

Charges must be represented correctly.

The underlying simulation must know the charge.

Do not merely append “+” or “-” to a visual label while leaving the simulation state unchanged.

⸻

12. DRAGGING

The user must be able to drag atoms and molecules.

Dragging should feel responsive.

The selected entity should visibly respond to being selected.

On release:

* detect nearby entities
* determine whether interaction is possible
* evaluate the reaction rules
* perform the correct transformation
* produce appropriate visual/audio feedback

Do not trigger the same reaction repeatedly every frame.

Prevent accidental duplicate reactions.

⸻

13. ADD BUTTON

Create a clear “+” interface.

It must allow users to add atoms/materials.

The system should be organized rather than presenting a completely chaotic list.

Make the selection interface easy to understand.

⸻

14. DELETE BUTTON

Create a “-” delete mode.

When active:

* clearly indicate delete mode
* allow the user to remove atoms/molecules
* provide appropriate feedback
* prevent accidental permanent actions where practical

⸻

15. REACTION ENGINE

Create a centralized reaction system.

Do NOT create hundreds of completely unrelated scripts if the reactions can be represented as structured rules.

The reaction engine should evaluate:

* reactants
* products
* charge
* conditions
* UV state
* relevant simulation state
* proximity
* reaction availability

Use a data-driven design where practical.

The reaction database must be easy to extend.

⸻

16. EXOTHERMIC REACTIONS

Some reactions should be classified as exothermic.

When one occurs:

* create an orange visual effect
* provide appropriate feedback
* potentially spawn a photon

The photon must correspond to the reaction event.

Do not simply play an orange animation randomly.

⸻

17. COSMIC RAYS

Fast colored particles represent cosmic rays.

Implement an actual cosmic-ray system.

Cosmic rays should be able to interact with appropriate atoms/molecules and create ions.

Do not randomly change labels.

Modify the underlying simulation state.

Use visually recognizable fast particles.

⸻

18. UV LIGHT

Create a UV control.

When enabled:

* visibly indicate UV is active
* modify appropriate reaction behavior
* allow UV-dependent reactions
* provide appropriate visual feedback

Do NOT make UV merely a purple overlay.

The simulation state must know whether UV is active.

⸻

19. FREEZE TIME

Create the snowflake button.

When activated:

* freeze simulation movement
* freeze appropriate timers
* prevent reactions from progressing where appropriate
* preserve the current state

The UI must clearly communicate that time is frozen.

When unfrozen, simulation behavior should resume correctly.

⸻

20. SPEAKER / VOLUME

Create a speaker button.

It should control actual project audio.

Provide sensible volume behavior.

Do not create a button that only changes its appearance.

⸻

21. INFORMATION SYSTEM

Create an “i” information button.

When the user selects an atom, molecule, or ion, the information system should show useful information.

For example:

* name
* formula
* charge
* constituent elements
* useful simulation information
* discovery status

Keep information readable.

Do not fill cards with meaningless filler text.

⸻

22. PERIODIC TABLE / DISCOVERY SYSTEM

Create a dedicated interface showing discovered molecules and ions.

The interface should allow users to browse what they have created.

Organize entries logically.

Make formulas readable.

Clearly distinguish:

* neutral molecules
* ions
* atoms

The D key should delete the appropriate collection/discovery state if that is the intended behavior, but implement this carefully to avoid accidental deletion.

⸻

23. SAVE / LOAD

Implement real save/load behavior to the extent possible within normal Scratch.

Do NOT create fake buttons.

Determine what persistence is actually possible.

If normal Scratch limitations prevent arbitrary cloud persistence, explain and implement the strongest compatible alternative.

Never claim something works if it doesn’t.

The system should save appropriate progress such as:

* discovered molecules
* discovered ions
* settings
* appropriate simulation state

⸻

24. CHEMISTRY DATA ARCHITECTURE

Create a structured chemistry database.

Do not hard-code every property in unrelated scripts.

Represent species using structured data where possible.

The database should contain appropriate information such as:

* formula
* charge
* constituent atoms
* bonds/relationships where useful
* reaction participation
* UV behavior
* ionization behavior
* visual identity
* discovery state

This makes the system maintainable.

⸻

25. PERFORMANCE

Scratch has real performance constraints.

Design around them.

Do not blindly create enormous numbers of clones.

Do not run expensive calculations unnecessarily every frame.

Use:

* controlled update loops
* efficient collision checks
* cleanup of dead entities
* appropriate clone counts
* cached calculations
* event-driven behavior where possible

If the project becomes slow:

DO NOT simply ignore the problem.

Profile the expensive systems and redesign them.

⸻

26. ARCHITECTURE

Use modular systems.

A possible architecture is:

Simulation
├── Entity System
├── Atom System
├── Molecule System
├── Ion System
├── Bonding System
├── Reaction Engine
├── Cosmic Ray System
├── UV System
├── Photon System
├── Time System
├── Input System
├── Spawn/Delete System
├── Audio System
├── Discovery System
├── Information System
├── Save/Load System
└── UI System

You are allowed to change this architecture if a better Scratch-compatible design exists.

Do not create modules merely for the sake of having modules.

⸻

27. VARIABLE NAMING

Use clear names.

GOOD:

selectedAtom
selectedEntity
simulationPaused
reactionEnergy
moleculeID
targetEntity
reactionType
currentCharge

BAD:

x1
x2
thing
thing2
temp
temp2
finalThingNew
AIData123

The project should be understandable.

⸻

28. CUSTOM BLOCKS

Use custom blocks where they genuinely improve organization.

Examples may include:

initialize simulation

spawn atom

remove entity

update entity

check reaction

create molecule

create ion

update UI

save progress

load progress

Do not create hundreds of custom blocks unnecessarily.

⸻

29. TESTING

Before saying the project is complete, test:

Basic

* project opens
* green flag works
* UI initializes
* buttons respond

Input

* dragging works
* selection works
* delete mode works
* keyboard controls work

Chemistry

* atoms can interact
* molecules can form
* ions can form
* reactions work
* invalid combinations don’t cause corruption

Systems

* UV works
* cosmic rays work
* photons work
* exothermic effects work
* freeze works
* volume works
* information works
* discovery works
* save/load works as implemented

Stability

* no infinite accidental loops
* no broken clones
* no missing variables
* no missing broadcasts
* no invalid references
* no obvious performance collapse

⸻

30. TEST THE ACTUAL .SB3

After generating the project:

1. Validate the ZIP.
2. Validate project.json.
3. Validate all assets.
4. Validate all targets.
5. Validate all blocks.
6. Validate variables.
7. Validate lists.
8. Validate broadcasts.
9. Validate custom blocks.
10. Validate mutations.
11. Validate asset references.
12. Open/test the actual generated project if your environment allows it.
13. Fix discovered errors.
14. Rebuild the .sb3.
15. Test again.

Do NOT stop after the first successful generation.

⸻

31. ITERATION REQUIREMENT

You must use an iterative development process.

For every major system:

PLAN
↓
IMPLEMENT
↓
TEST
↓
FIND FAILURE
↓
FIX
↓
REGRESSION TEST

Never assume your first implementation is correct.

If something fails, investigate the root cause.

Do not cover it up.

⸻

32. VISUAL REVIEW

Perform a dedicated visual review.

Ask:

“Does this look like something a skilled human Scratch developer intentionally designed?”

Check:

* spacing
* typography
* colors
* icons
* buttons
* particle graphics
* molecule graphics
* effects
* panels
* menus
* hierarchy
* consistency

Remove anything that looks generic or automatically generated.

⸻

33. USER EXPERIENCE

The project should be understandable without requiring the user to read a giant manual.

A new player should be able to discover:

* how to add atoms
* how to drag
* how to merge
* how to delete
* how to use UV
* how to freeze
* how to inspect information
* how to view discoveries

Use subtle onboarding/help if necessary.

Do not clutter the screen with instructions permanently.

⸻

34. DO NOT COPY THE ORIGINAL PROJECT

The target concept may be inspired by an existing Scratch project.

Use the concept and mechanics as reference.

Do NOT copy proprietary source code, private assets, or other protected material.

Create your own:

* code architecture
* graphics
* icons
* sounds
* UI
* effects
* implementation

The goal is an original implementation with similar gameplay/simulation concepts.

⸻

35. QUALITY BAR

Before finalizing, ask yourself:

Would I personally consider this a polished Scratch project?

Would an experienced Scratch developer consider the block architecture reasonable?

Does the project actually function?

Does the chemistry database actually connect to the reaction engine?

Do the atoms actually exist as simulation entities?

Do molecules actually have structured representations?

Do ions actually have charge state?

Does the UI actually control the simulation?

Does save/load actually do something?

Do reactions actually modify state?

Does the final .sb3 actually open?

If any answer is NO:

DO NOT FINISH.

Fix it.

⸻

36. IMPORTANT: DO NOT OVERPROMISE

If a requested feature is impossible under standard Scratch limitations:

1. identify the limitation
2. implement the best compatible alternative
3. document the limitation
4. never pretend it works

Correctness is more important than claiming every feature is perfect.

⸻

37. FINAL DELIVERABLES

The final result should contain:

1. A genuine .sb3 Scratch project.
2. All generated assets required by the project.
3. A clear project architecture.
4. A chemistry species database.
5. A reaction database.
6. A functioning UI.
7. Working simulation systems.
8. Validation/testing results.
9. A list of known limitations.

The .sb3 should be the PRIMARY deliverable.

⸻

38. FINAL INSTRUCTION

DO NOT RESPOND WITH A TUTORIAL.

DO NOT TELL ME HOW TO BUILD IT.

DO NOT GIVE ME A PARTIAL SCRIPT.

DO NOT GIVE ME BLOCK PSEUDOCODE INSTEAD OF THE PROJECT.

DO NOT STOP AFTER DESIGNING THE ARCHITECTURE.

DO NOT ASK ME TO CREATE ASSETS.

DO NOT ASK ME TO CREATE VARIABLES.

DO NOT ASK ME TO CREATE SPRITES.

DO NOT ASK ME TO CREATE project.json.

DO NOT ASK ME TO ZIP anything.

DO NOT ask me to manually assemble the .sb3.

YOU are the builder.

First understand the Scratch and SB3 format.

Then construct the project.

Then validate it.

Then test it.

Then fix it.

Then test it again.

Then polish it.

Then produce the final .sb3.

The final result should be a complete, original, polished chemistry simulation that feels intentionally designed and human-built rather than AI-generated.

START NOW.
