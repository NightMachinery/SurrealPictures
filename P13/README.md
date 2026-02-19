# P13

P13 keeps **all elements/categories from** `/Users/evar/Pictures/SurrealPictures/p12/preprompter.py` and changes only:

1. the master template (now P2-style, creativity-first), and
2. insertion format (now shuffled deterministic seed fragments instead of rigid labeled sections).

## Reproducibility
- `P13/p12_helper.py` is a **local snapshot copy** of P12's matrix logic.
- `P13/preprompter.py` loads this local helper, so P13 behavior is stable even if `/Users/evar/Pictures/SurrealPictures/p12/preprompter.py` changes later.
- Use `--seed <number>` for deterministic output.

## Behavior
- Category trees, item pools, sampling logic, and constraints come from `P13/p12_helper.py`.
- For each output preprompt, sampled items are flattened, shuffled, and inserted as unlabeled seed fragments.
- The writing model is told the seed is guidance only and can be creatively reinterpreted.

## Usage
From `/Users/evar/Pictures/SurrealPictures/P13`:

```bash
python3 preprompter.py --prompts 10 --seed 13 --output preprompts
```

All original P12 CLI options are supported because P13 reuses P12's parser/config via the local helper snapshot.
