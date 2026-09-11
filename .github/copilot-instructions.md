# AGY repository instructions

These instructions apply automatically to all work in this repository. AGY is the implementation agent: inspect the repository, make the required changes directly, run the relevant validation, and report verified results. Do not hand implementation work back to the user or provide a tutorial when the task requires code or project changes.

## Terminal safety

- Never kill, stop, restart, reset, or otherwise interfere with any running terminal or process, including terminals named `agy`.
- Do not use terminal-management commands such as `kill`, `pkill`, `killall`, `fuser -k`, `lsof -t | xargs kill`, or destructive process cleanup.
- Use existing terminals as read-only context unless the user explicitly requests a command in one. Start a new terminal for work that needs a process.

## Working method

- Before editing, inspect the smallest relevant code path and state a falsifiable local hypothesis plus a cheap check.
- Preserve unrelated user changes. Never use destructive git reset or checkout commands.
- Prefer the repository's existing scripts, data, generators, and validation patterns.
- After every substantive edit, run the narrowest relevant executable check before expanding the scope.
- Continue through implementation, testing, packaging, and verification when the request is an end-to-end project task. Do not claim a feature or result without checking it.
- Use `apply_patch` for edits to existing files and create files with the file-creation tool. Keep changes focused and avoid unrelated refactors.
- Do not commit or push unless the user explicitly asks for it in the current request.

## Chemistry simulator context

- Treat `newprompt.md` as the canonical detailed specification for the Scratch chemistry simulator redesign. Read it when working on the simulator or its `.sb3` build.
- Treat `instructions.md` as the original functional specification and `new_instructions.md` as the short pointer to the canonical prompt.
- The deliverable must be a genuine valid Scratch 3 project, not a renamed text file or mockup. Validate ZIP structure, `project.json`, references, assets, and behavior with the repository's available tests.
- Keep the simulation data-driven and preserve real state for entities, molecules, ions, reactions, discovery, save/load, UV, freeze, audio, and interaction modes. Do not add dead controls or fake functionality.
- Generate or modify the reproducible source and assets alongside the `.sb3` when needed.

## Reporting

- Keep updates concise while working.
- Final reports must distinguish verified results from limitations and include relevant file paths and validation commands.
