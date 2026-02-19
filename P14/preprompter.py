#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import random
from pathlib import Path
from typing import List, Mapping, Sequence

MASTER_TEMPLATE = (
    """
# Role: Lead Surrealist Art Director (Dixit Project)

**Objective:** Generate one high-fidelity text-to-image prompt for a custom *Dixit* card (vertical 2:3), with strong narrative coherence and surreal ambiguity.

## Hard Anti-Seed Policy (Non-Negotiable)
The seed fragments below are for **subconscious directional priming only**.
- Do **NOT** copy, quote, paraphrase, enumerate, or directly depict seed fragments.
- Do **NOT** reuse seed nouns, entities, symbols, places, or relationships in obvious transformed form.
- If seed content appears explicitly in the output, the output is a failure.
- Invent fresh narrative content that is not textually traceable to the seed list.

## Narrative Coherence Constraints
- Build **one frozen story beat**: one focal subject, one central action, one immediate consequence.
- Something must be happening now (mid-action), not a static catalog.
- Keep ambiguity, but the scene must read as one coherent moment.
- Background details must support the same main beat.

## Compactness Constraints
- Output exactly **one paragraph**.
- Target approximately **130-180 words**.
- Prefer concrete visual nouns and actions; avoid bloated lists and repetitive filler.

## Aesthetic Constraints
- Whimsical painterly surrealism / magical realism, playful but adult, soft yet unsettling.
- Do not mention artistic medium; a separate system prepends medium later.

## Deterministic Random Seed
- Seed fragments: {seed_fragments}

## Output Requirements
- Return only the final prompt text.

### Optional Structure (flexible)
`[Narrative Action/Subject] + [Surreal Twists] + [Emotions] + [Rich Environment] + [Lighting & Atmosphere]`
""".strip()
    + "\n"
)


def load_p12_module():
    p12_path = Path(__file__).resolve().parent / "p12_helper.py"
    spec = importlib.util.spec_from_file_location("p13_p12_helper", p12_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to load P12 preprompter from: {p12_path}")
    module = importlib.util.module_from_spec(spec)
    import sys
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def next_prompt_index(output_dir: Path) -> int:
    existing = list(output_dir.glob("prompt_*.md"))
    if not existing:
        return 1

    max_num = 0
    for f in existing:
        parts = f.stem.split("prompt_")
        if len(parts) >= 2 and parts[-1].isdigit():
            max_num = max(max_num, int(parts[-1]))
    return max_num + 1


def flatten_seed_fragments(
    prompt_data: Mapping[str, List[str]],
    category_order: Sequence[str],
    seed_value: int,
) -> List[str]:
    fragments: List[str] = []
    for key in category_order:
        fragments.extend(prompt_data.get(key, []))

    rng = random.Random(seed_value)
    rng.shuffle(fragments)
    return fragments


def generate_seed_values(prompt_count: int, base_seed: int | None) -> List[int]:
    if base_seed is None:
        rng = random.SystemRandom()
    else:
        rng = random.Random(base_seed)
    return [rng.randint(0, 2**63 - 1) for _ in range(prompt_count)]


def write_preprompts(
    structs: Sequence[Mapping[str, List[str]]],
    output_dir: str,
    category_order: Sequence[str],
    base_seed: int | None,
) -> None:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    start_idx = next_prompt_index(out)
    seed_values = generate_seed_values(len(structs), base_seed)

    for offset, data in enumerate(structs):
        seed_value = seed_values[offset]
        seed_fragments_list = flatten_seed_fragments(data, category_order, seed_value)
        seed_fragments = " | ".join(seed_fragments_list) if seed_fragments_list else "(none)"

        filled = MASTER_TEMPLATE.format(
            seed_value=seed_value,
            seed_fragments=seed_fragments,
        )

        file_index = start_idx + offset
        path = out / f"prompt_{file_index:d}.md"
        path.write_text(filled, encoding="utf-8")

        if offset == 0:
            print(f"File numbering started at: prompt_{file_index:d}.md")

    print(f"Successfully generated {len(structs)} P13 pre-prompts in: {out.resolve()}")


def main() -> None:
    p12 = load_p12_module()
    p12.validate_definitions()
    cfg = p12.parse_args()
    structs = p12.generate_matrix_structs(cfg)

    write_preprompts(
        structs=structs,
        output_dir=cfg.output_dir,
        category_order=p12.CATEGORY_ORDER,
        base_seed=cfg.seed,
    )


if __name__ == "__main__":
    main()
