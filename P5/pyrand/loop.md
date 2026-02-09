# Execution Loop (Manual Prompt Writing) — 400 Surreal Dixit Prompts

This workflow generates **400 unique, high-detail, ambiguous prompts** using `matrix_generator.py` as blueprint input, while the final prose remains **manually authored** (human touch, no auto prompt-writer script).

---

## 1) Core Creative Rules

- Keep scenes visually rich and puzzle-like with a **detailed background**.
- **Symbol integration is architectural** (load-bearing structure, gate, mechanism, ritual object), never mere decoration.
- **Surreal Logic drives the physics** of the scene.
- Scatter/details should be present, but do **not** need to fill every inch.
- Sensual themes / artistic nudity are allowed (no pornographic framing).
- Always append exactly:
  - `in the style of Gankutsuou and Gustav Klimt, rich static textile patterns layered over character silhouettes, iridescent gold leaf and jewel tones, texture mapping, ornate Art Nouveau details, collage-like flatness, surreal opulence, sharp distinct lines, psychedelic baroque, maximalist composition, highly detailed background --ar 2:3 --niji 6`

---

## 2) Generator Is Now Fully Configurable

`matrix_generator.py` now supports:

- Optional categories (set category knob to `0`)
- Per-category sampling counts (floats allowed)
- Ordered hierarchical dictionaries as the source of truth for all categories
- Auto-generated code numbering from dictionary order (no hand-maintained IDs)
- Hierarchical bucket-aware sampling across **all** categories
- Smart diversity when sampling multiple items in one category
- New categories:
  - `SE` = Setting
  - `CP` = Composition / POV
  - `EE` = Easter Eggs
- Bucket inspection mode:
  - `--list-buckets` prints all hierarchical bucket paths and counts, then exits

### Category knobs (per prompt)

- `--ar` archetypes
- `--cn` concepts
- `--sl` surreal logic
- `--tx` textures
- `--sc` scatter
- `--em` emotions
- `--sy` symbols
- `--se` settings
- `--cp` composition/pov
- `--ee` easter eggs

Useful inspection command:

```bash
bash -lc 'python3 matrix_generator.py --list-buckets'
```

### Fractional behavior

If a knob is a float, it is interpreted probabilistically per prompt:

- `2.0` => exactly 2 items/prompt
- `0.3` => each prompt has ~30% chance of getting 1 item (else 0)
- `1.7` => always 1 item, plus ~70% chance of a second

### Defaults (tasteful baseline)

Current default profile is:

- `ar=1, cn=1, sl=1, tx=1, sc=2, em=1, sy=1, se=1, cp=1, ee=0`

Plus:

- min 4 light emotions per 10 prompts
- min 2 celebration/fellowship symbols per 10 prompts

---

## 3) Easter Egg Safety Rule (Important)

If `EE` appears in a matrix line:

- Treat it as a **vibe/cue only**
- EE buckets in the script may explicitly name franchises (Harry Potter, Disney, Pixar, DreamWorks, etc.) for internal indexing only
- Do **not** explicitly name a copyrighted franchise, character, studio, title, logo, or direct quote in the final prompt
- Manually invent an oblique homage that *reminds* the viewer of that pop-culture lineage without explicit naming

---

## 4) File Layout

- Root: `/Users/evar/Pictures/SurrealPictures/P5/pyrand`
- Generator: `matrix_generator.py`
- Output dir: `prompts/`
- Per batch:
  - `prompts/<batch>.matrix`
  - `prompts/<batch>.md`
- Final:
  - `prompts/prompt_all.md`

---

## 5) Batch Loop (1..40)

### Step A — Create prompts dir

```bash
bash -lc 'mkdir -p prompts'
```

### Step B — For each batch

1. Generate matrix:

```bash
bash -lc 'python3 matrix_generator.py > prompts/<batch>.matrix'
```

2. Read matrix file (10 lines by default unless `--prompts` changed).

3. Manually write 10 prompts to `prompts/<batch>.md` with cumulative numbering:
   - batch 1: 1–10
   - batch 2: 11–20
   - ...
   - batch 40: 391–400

4. For each prompt entry:
   - First line:
     - `N. // <full matrix line exactly>`
   - Next line:
     - full prompt text authored manually using the line components

### Step C — Final concatenation

After batch 40:

```bash
bash -lc 'cat prompts/{1..40}.md > prompts/prompt_all.md'
```

---

## 6) Creative Knob Tuning Policy (Allowed & Encouraged)

You may tune generator knobs per batch for variety, while staying tasteful.

Good policy:

- Most batches near baseline defaults
- Occasional targeted variation:
  - e.g. heavier atmosphere: `--se 2 --cp 2`
  - denser symbolism: `--sy 2.5`
  - lighter conceptual abstraction: `--cn 0.7`
  - sparse occasional easter egg: `--ee 0.2`

Example tuned batch command:

```bash
bash -lc 'python3 matrix_generator.py --se 2 --cp 1.5 --sy 1.4 --ee 0.2 > prompts/<batch>.matrix'
```

Keep variation intentional; avoid chaotic overstuffing every batch.

---

## 7) Matrix Parsing Note

Matrix lines are now dynamic-length. Do **not** assume fixed field count.

Codes are now auto-assigned from ordered dictionaries. If category items are reordered in the script, code numbers may shift.

Use the codes/prefixes directly:

- `AR`, `CN`, `SL`, `TX`, `SC`, `EM`, `SY`, `SE`, `CP`, `EE`

Any category may appear multiple times in one line, or be absent if knob is 0/disabled.

---

## 8) Hard “Do Not”

- Do not auto-generate prompt prose with a script.
- Do not add extra MJ parameters beyond the mandatory suffix.
- Do not write direct copyrighted franchise names when using EE cues.
