class MatrixConfig:
    prompts_per_batch: int = 10
    seed: Optional[int] = None
    output_dir: str = "preprompts"
    include_code_p: bool = False

    # Core Weights
    archetypes: float = 1.2
    concepts: float = 1.0
    surreal_logic: float = 1.2
    textures: float = 1.2
    scatter: float = 3.0
    emotions: float = 1.1
    symbols: float = 1.2
    settings: float = 0.8

    # Promoted Camera Weights
    cm_angles: float = 0.3
    cm_framing: float = 0.1

    # Promoted Graphic Style Weights
    gr_temporal: float = 0.1
    gr_collage: float = 0.1
    gr_staging: float = 0.1

    # Easter Eggs
    easter_eggs: float = 0.5
    include_ee_narratives: bool = True
    include_ee_motifs: bool = True

    # Constraints (minimum totals across the whole batch, clamped to capacity)
    min_light_emotions: int = 4
    min_celebration_symbols: int = 2
