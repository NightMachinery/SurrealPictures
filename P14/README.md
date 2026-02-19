# P14

P14 is a direct clone of `/Users/evar/Pictures/SurrealPictures/P13` with one intentional change:

- **Only the master prompt text in** `/Users/evar/Pictures/SurrealPictures/P14/preprompter.py` was rewritten.

## Why P14 exists

P13 often encouraged overly literal seed usage and crowded, list-like prompt outputs. This could reduce coherence and cause text-to-image models to ignore many details.

P14 addresses this by enforcing a **hard anti-seed-use policy** in the master prompt while keeping the same underlying generation pipeline.

## Hard anti-seed-use strategy

P14 still passes seed fragments into each preprompt for latent directional priming, but the master prompt now explicitly instructs the writing model to:

- treat seed fragments as subconscious-only guidance,
- never copy, paraphrase, enumerate, or directly depict them,
- fail if seed content appears explicitly,
- invent a fresh coherent narrative moment instead.

## Additional output constraints in P14 master prompt

- one frozen story beat (one focal subject, one central action, one immediate consequence),
- one coherent scene (no disconnected micro-scenes),
- one paragraph,
- target approximately 130-180 words,
- concrete visual language with minimal bloat.

## Reproducibility and compatibility

- `P14/p12_helper.py` is a local snapshot copy (from P13's helper snapshot).
- CLI behavior is **drop-in compatible** with P13/P12 because P14 still uses the helper's parser and matrix generation.
- No new CLI flags were added.

## Usage

From `/Users/evar/Pictures/SurrealPictures/P14`:

```bash
python3 preprompter.py --prompts 10 --seed 13 --output preprompts
```

All original P12/P13 CLI options remain available.
