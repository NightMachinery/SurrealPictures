# Execution Loop (Manual Prompt Writing) — 400 Surreal Dixit Prompts

This file is the step-by-step procedure to generate **400 unique, high-density, ambiguous, professional Dixit-style** text-to-image prompts, using the **matrix_generator.py** blueprints, but writing the final prompt text **manually (human-touch)**.

## Ground rules (must follow)

- Use **bash** for commands (avoid zsh startup cost).
- Prompts must be **high ambiguity + high detail**; each card is a crowded visual puzzle with a **detailed background**.
- **Scatter:** at least one must be present, but it does **not** need to “fill every inch.”
- **Adult Dixit:** sensual themes and artistic nudity are acceptable.
- **Symbol Integration Rule:** the **SY** symbol must be **architecturally integrated** into the scene (load-bearing structure, doorway, monument, device, etc.), not a mere decoration.
- **Surreal Logic is primary:** the **SL** item must be the core driver of the world’s weird physics.
- **Mandatory style suffix:** append *exactly* this (no extra params):
  - `in the style of Gankutsuou and Gustav Klimt, rich static textile patterns layered over character silhouettes, iridescent gold leaf and jewel tones, texture mapping, ornate Art Nouveau details, collage-like flatness, surreal opulence, sharp distinct lines, psychedelic baroque, maximalist composition, highly detailed background --ar 2:3 --niji 6`

## File layout
- Generator: `matrix_generator.py`
- Output directory: `prompts/`
- Per batch:
  - Matrix blueprint: `prompts/<batch_number>.matrix`
  - Prompt text: `prompts/<batch_number>.md`
- Final concatenation:
  - `prompts/prompt_all.md`

## Matrix format (important)

Each `.matrix` line contains **8** fields separated by ` + `:

`AR + CN + SL + TX + SC-A + SC-B + EM + SY`

## Execution loop

### 0) Prep

1. Ensure the `prompts/` directory exists.
   - Command: `bash -lc 'mkdir -p prompts'`

### 1) For batch_number = 1..40

For each batch:

1. **Run the generator** and save output:
   - `bash -lc 'python3 matrix_generator.py > prompts/<batch_number>.matrix'`

2. **Read** `prompts/<batch_number>.matrix` (10 lines).

3. **Write 10 prompts manually** into `prompts/<batch_number>.md`:

   - Prompts are **cumulatively numbered**:
     - Batch 1 → prompts **1–10**
     - Batch 2 → prompts **11–20**
     - …
     - Batch 40 → prompts **391–400**

   - For each matrix line:
     1) Copy it verbatim as a comment line in the `.md` file:
        - `// <AR + CN + SL + TX + SC-A + SC-B + EM + SY>\nN. `
     2) Under it, write the full prompt text following this structure:
        - **[Anchor Subject]** (from AR + CN; include character/action; sensuality allowed)
        - **[Symbol woven into the scene]** (SY must be structural/architectural)
        - **[Applying the Surreal Logic to the Environment]** (SL is the main “physics”)
        - **[Scatter/Details]** (include one or two of SC-A and SC-B + additional rich background details)
        - **[Textures & Lighting]** (TX + EM clearly influence materials, palette, and light)
        - Append the **mandatory style suffix exactly**.

   - Uniqueness requirement:
     - Ensure **prompt text and narrative feel** are distinct across all 400.
     - Avoid reusing the same sentence patterns repeatedly; vary composition, framing, and micro-details.

### 2) Final concatenation (after batch 40)

1. Use `cat` to concatenate `prompts/1.md` through `prompts/40.md` in numeric order into `prompts/prompt_all.md`. (Keep order and numbering intact (1..400).)

## “Do not do” list

- Do **not** create an automatic prompt-writer script (the prompt writing is manual).
- Do **not** add extra MJ params beyond the exact suffix.

