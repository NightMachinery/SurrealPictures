#!/usr/bin/env python3
##
#: * @usage
#: ** `redo2 20 python preprompter.py`
##
from __future__ import annotations

import argparse
import math
import os
import random
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

# ============================================================
# 1) DATA MODEL
# ============================================================


@dataclass(frozen=True)
class CategoryDefinition:
    key: str
    label: str
    short: str
    weight_field: str
    tree: Any
    template: str
    # If list is not empty, only buckets matching these substrings are allowed.
    forced_filter: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class CategoryCatalog:
    key: str
    label: str
    short: str
    all_items: List[str]  # coded items across all leaf buckets
    buckets: Dict[str, List[str]]  # bucket_path -> coded items in that bucket


@dataclass(frozen=True)
class MatrixConfig:
    prompts_per_batch: int = 10
    seed: Optional[int] = None
    output_dir: str = "preprompts"
    include_code_p: bool = False

    # Core Weights
    archetypes: float = 1.75
    concepts: float = 1.0
    surreal_logic: float = 1.2
    textures: float = 0.0
    scatter: float = 0.0
    emotions: float = 1.1
    symbols: float = 2.5
    settings: float = 0.8

    # Promoted Camera Weights
    cm_angles: float = 0.3
    cm_framing: float = 0.1

    # Promoted Graphic Style Weights
    gr_temporal: float = 0.1
    gr_collage: float = 0.1
    gr_staging: float = 0.1

    # Easter Eggs
    easter_eggs: float = 0.0
    include_ee_narratives: bool = False
    include_ee_motifs: bool = True

    # Constraints (minimum totals across the whole batch, clamped to capacity)
    min_light_emotions: int = 4
    min_celebration_symbols: int = 2


# ============================================================
# 2) MASTER TEMPLATE
# ============================================================

MASTER_TEMPLATE = (
    """
# Role & Objective: The Surrealist Auteur (Adult Dixit Edition)

You are an avant-garde Art Director and a master of surrealist visual storytelling. Your task is to write a single, masterful, high-density prompt for a text-to-image AI. This prompt will be used by multimodal native Transformer model to generate a professional, gallery-quality illustration for a private Dixit card collection. This model is very advanced and you should treat them as a human artist when writing the prompt. You should NOT mention anything about the artistic style, as that will be prepended to your prompt by another artist. You should only describe the semantics and the composition.

You are creating a single illustration for a collectible Dixit card designed for adults — a surrealist artwork that functions as a visual Rorschach test. The image must be polysemic: five different people should look at it and project five completely different stories, emotions, and memories onto it. It should never illustrate a single readable narrative. Instead, it should feel like a half-remembered dream that the viewer is convinced they have had before but cannot quite place.

The emotional register is adult in every dimension. The image should be capable of evoking longing, shame, ecstasy, grief, quiet dread, or tenderness depending on who is looking and what they bring to it. The human body is your most powerful instrument of ambiguity — treat it the way Klimt, Schiele, Mucha, and the great classical painters did: as a site of vulnerability, desire, power, and unresolved contradiction, never as mere decoration.

**Target Audience:** Adults (25+).
**Core Requirement:** High Ambiguity, High Detail, Paradox, Emotionally Intelligent.
**Failure Condition:** Empty space and straightforward interpretations are critical failures. The image must be a **crowded** visual puzzle.
**Aspect Ratio:** 2:3

# Visual Philosophy: "The Frozen Dream"
You are not painting a landscape; you are constructing an emotionally-charged **paradox**.
1.  **The Time:** The scene is a "Frozen Dream"—a single, critical frame paused in the middle of an impossible event. Action is implied, but motion is static.
2.  **The Body:** Sensual and artistic nudity is acceptable if it deepens the vulnerability or surrealism of the piece. Treat the human form (or the inhuman form) as a classical canvas.

# The Dynamic Matrix Blueprint
Synthesize the following specific blocks into your scene.

{dynamic_matrix_block}

# Execution Mandates
1.  **Synthesize, Don't List:** Do not write "There is an archetype..." Instead, describe the scene directly.
2.  **Crowd the Frame:** Fill the foreground, midground, and background. What is happening in the corners? What debris is floating in the air?
3.  **Maintain Ambiguity:** The final image should pose a question, not answer it.
""".strip()
    + "\n"
)


# ============================================================
# 3) CATEGORY DEFINITIONS
# ============================================================

CATEGORIES: Dict[str, CategoryDefinition] = {
    "ar": CategoryDefinition(
        key="ar",
        label="Archetypes",
        short="AR",
        weight_field="archetypes",
        template="""
### {n}. The Anchor (Subject)
**Archetype:** {content}
*Instruction: This is the protagonist of your visual paradox. Do not depict them generically. Treat them as a mythic, timeless presence. Describe their posture, their attire, and the weight of their existence.*
""".strip(),
        tree={
            "Craft": {
                "Makers": [
                    "The Weaver",
                    "The Architect",
                    "The Gardener",
                    "The Alchemist",
                    "The Cartographer",
                    "The Clockmaker",
                    "The Scientist",
                    "The Inventor",
                    "The Artisan",
                    "The Chef",
                ],
            },
            "Authority": {
                "Court": [
                    "The Monarch",
                    "The Guardian",
                    "The Vizier",
                    "The Shah",
                    "The Mentor",
                ],
                "Wisdom": [
                    "The Oracle",
                    "The Ferryman",
                    "The Librarian",
                    "The Therapist",
                    "The Elder",
                ],
            },
            "Journey": {
                "Wanderers": [
                    "The Traveler",
                    "The Dancer",
                    "The Fool",
                    "The Trickster",
                    "The Explorer",
                ],
                "Performers": [
                    "The Dreamer",
                    "The Musician",
                    "The Athlete",
                    "The Ninja",
                    "The Storyteller",
                ],
            },
            "Relations": {
                "Bonds": [
                    "The Lovers",
                    "The Parent",
                    "The Child",
                    "The Friend",
                    "The Host",
                ],
                "Devotion": [
                    "The Celebrant",
                    "The Beloved",
                    "The Twins",
                    "The Healer",
                    "The Matchmaker",
                ],
            },
            "Liminal": {
                "Shadowed": [
                    "The Hermit",
                    "The Shadow",
                    "The Prisoner",
                    "The Widow",
                    "The Vessel",
                ]
            },
            "Mythic": {
                "Icons": [
                    "The Phoenix",
                    "The Avatar",
                    "The Idol",
                    "The Giant",
                    "The Swarm",
                ],
                "Beings": [
                    "The Beast",
                    "The Mirror",
                    "The Rationalist",
                    "The Romantist",
                    "The Virgin",
                ],
            },
        },
    ),
    "cn": CategoryDefinition(
        key="cn",
        label="Concepts",
        short="CN",
        weight_field="concepts",
        template="""
### {n}. The Core Concept
**Theme:** {content}
*Instruction: This is the intellectual soul of the card. The image must not just be "cool"; it must evoke this specific abstract concept through visual metaphor. How does the environment react to this concept?*
""".strip(),
        tree={
            "Uplift": {
                "Growth & Connection": [
                    "Bloom / Growth",
                    "Transformation / Metamorphosis",
                    "Origin / Genesis",
                    "Resilience / Strength",
                    "Healing / Recovery",
                    "Discovery / Eureka",
                    "Flight / Liberation",
                    "Fusion / Union",
                    "Friendship / Bond",
                    "Belonging / Community",
                ],
                "Joy & Warmth": [
                    "Tenderness / Care",
                    "Sensuality / Passion",
                    "Intimacy / Closeness",
                    "Generosity / Gift",
                    "Celebration / Festivity",
                    "Play / Joy",
                    "Humor / Laughter",
                    "Triumph / Victory",
                    "Abundance / Harvest",
                    "Gratitude / Thanksgiving",
                ],
            },
            "Structure": {
                "Mind & Form": [
                    "Wonder / Curiosity",
                    "Anchor / Safety",
                    "Shelter / Home",
                    "Balance / Symmetry",
                    "Comfort / Warmth",
                    "Clarity / Epiphany",
                    "Resonance / Echo",
                    "Gravity / Weight",
                    "Velocity / Motion",
                    "Ritual / Cycle",
                ]
            },
            "Shadow": {
                "Void & Taboo": [
                    "Entropy",
                    "Silence / Pause",
                    "Hunger / Desire",
                    "Threshold / Doorway",
                    "Labyrinth / Complexity",
                    "Illusion / Mask",
                    "Mystery / Void",
                    "Sacrifice / Exchange",
                    "Forbidden / Taboo",
                    "Abandonment / Desolation",
                ],
                "Aftertaste": [
                    "Grotesque / Uncanny",
                    "Memory / Nostalgia",
                    "Inheritance / Legacy",
                    "Innocence / Purity",
                    "Forgiveness / Grace",
                ],
            },
        },
    ),
    "sl": CategoryDefinition(
        key="sl",
        label="Surreal Logic",
        short="SL",
        weight_field="surreal_logic",
        template="""
### {n}. The Surreal Twist (Crucial)
**Logic Broken:** {content}
*Instruction: This is the "Frozen Dream" element. You are explicitly breaking physics here. Do not make it subtle. Make it the defining impossible feature of the image.*
""".strip(),
        tree={
            "Physics": {
                "Scale & Material": [
                    "Scale Inversion",
                    "Material Transmutation",
                    "Gravity Reversal",
                    "Object Personification",
                    "Literal Metaphor",
                ],
                "Displacement": [
                    "Portal Displacement",
                    "Anatomical Impossibility",
                    "Flora/Fauna Fusion",
                    "Architecture/Nature Fusion",
                    "Celestial Descent",
                ],
                "Matter Flow": [
                    "Fluid Solidity",
                    "Solid Liquidity",
                    "Infinite Recursion",
                    "Time Collapse",
                    "Invisible Presence",
                ],
            },
            "Presence": {
                "Agency": [
                    "Displacement",
                    "Gigantism",
                    "Containment",
                    "Sensory Synesthesia",
                    "Shadow Autonomy",
                ],
                "Geometry": [
                    "Sky Replacement",
                    "Fragmentation",
                    "Levitation",
                    "Mechanical Nature",
                    "Soft Sculpture",
                ],
                "Identity": [
                    "Inside-Out",
                    "Duplication",
                    "Facelessness",
                    "Dream Logic",
                    "Weather Containment",
                ],
                "Materialized Abstraction": [
                    "Edible Architecture",
                    "Musical Materialization",
                    "Emotional Weather",
                    "Memory Projection",
                    "Toy Transmutation",
                ],
            },
        },
    ),
    "tx": CategoryDefinition(
        key="tx",
        label="Textures",
        short="TX",
        weight_field="textures",
        template="""
### {n}. The Texture (The Gankutsuou Effect)
**Pattern:** {content}
*CRITICAL INSTRUCTION: Apply these textures as a static, 2D screen-tone pattern overlaying the 3D forms. The pattern does NOT bend with folds or depth. It remains flat while the character/object moves beneath it. This creates the signature "collage" look.*
""".strip(),
        tree={
            "Luminous": {
                "Painterly": [
                    "Stained Glass & Magma",
                    "Velvet & Ash",
                    "Gold Leaf & Circuitry",
                    "Floral Chintz & Bone",
                    "Watercolors & Ink",
                    "Porcelain & Cracks",
                    "Neon & Concrete",
                    "Silk & Smoke",
                ],
            },
            "Material": {
                "Stone & Metal": [
                    "Constellations & Void",
                    "Marble & Moss",
                    "Origami & Paper",
                    "Feathers & Tar",
                    "Gemstones & Rust",
                    "Lace & Steel",
                    "Fire & Ice",
                    "Woodgrain & Chrome",
                ],
                "Atmospheric": [
                    "Clouds & Maps",
                    "Sand & Mirrors",
                    "Coral & Pearl",
                    "Oil Paint & Pixels",
                    "Leather & Amber",
                    "Obsidian & Lightning",
                    "Tapestry & Thorns",
                    "Mercury & Moonlight",
                ],
                "Heritage": [
                    "Patina & Copper",
                    "Persian Tilework & Lapis Lazuli",
                    "Calligraphy & Saffron",
                    "Honey & Sunlight",
                    "Wildflower Linen & Denim",
                    "Carnival Glass & Confetti",
                    "Beeswax & Parchment",
                    "Terracotta & Olive Wood",
                ],
            },
        },
    ),
    "sc": CategoryDefinition(
        key="sc",
        label="Scatter",
        short="SC",
        weight_field="scatter",
        template="""
### {n}. Environmental Debris (Maximalism)
**Scatter:** {content}
*Instruction: Use one or more of these elements judiciously to fill the void. There should be no empty space. These items should be quietly resting, floating, falling, or swirling around the main action, adding depth and chaos.*
""".strip(),
        tree={
            "Classic": {
                "Atmospheric": [
                    "Floating Keys & Locks",
                    "Unraveling Ribbons",
                    "Broken Clock Gears",
                    "Falling Playing Cards",
                    "Shattered Glass Shards",
                    "Ancient Books / Pages",
                    "Ladders to Nowhere",
                    "Empty Frames",
                    "Chess Pieces",
                    "Strings / Marionette Lines",
                    "Eyes / Watching Orbs",
                    "Scattered Coins / Tokens",
                    "Dripping Candle Wax",
                    "Tiny Origami Birds",
                    "Drifting Lanterns",
                    "Floating Islands / Rocks",
                    "Tangled Vines / Roots",
                    "Bubbles / Orbs",
                    "Falling Leaves / Petals",
                    "Tiny Stars / Moons",
                ],
                "Theatrical": [
                    "Migrating Butterflies",
                    "Floating Feathers",
                    "Spiraling Staircases",
                    "Scattered Pomegranate Seeds",
                    "Drifting Rose Petals & Nightingales",
                    "Musical Notes",
                    "Confetti & Streamers",
                    "Fireflies & Glowworms",
                    "Iridescent Soap Bubbles",
                    "Scattered Wildflowers",
                    "Floating Balloons",
                    "Paper Airplanes",
                    "Ripe Fruit & Berries",
                    "Dancing Silhouettes",
                    "Sparklers & Firework Trails",
                    "Songbirds in Flight",
                    "Scattered Love Letters / Postcards",
                    "Spilled Wine / Overflowing Goblets",
                ],
            },
            "Ornamental": [
                "Loose Pearls & Broken Necklaces",
                "Perfume Bottles & Atomized Mist",
                "Feather Quills & Ink Pots",
                "Wax Seals / Stamps / Signet Rings",
                "Porcelain Shards & Hairline Cracks",
                "Sewing Needles & Thread Spools",
                "Tiny Bells / Chimes / Anklets",
                "Marbles / Glass Beads / Prism Drops",
                "Birdcages (Open, Empty, Drifting)",
                "Masks on Hooks / Mask Fragments",
                "Mirrors with Missing Reflections",
                "Chalk Diagrams & Summoning Circles",
                "Domino Tiles / Dice / Game Tokens",
                "Theater Tickets / Torn Programs",
                "Stray Earrings / Hairpins / Combs",
                "Lace Gloves / Silk Stockings (Abandoned)",
                "Ribbon-Wrapped Gifts / Unopened Boxes",
                "Vials / Elixirs / Tiny Flasks",
                "Seashells / Conch Horns",
                "Compass Needles / Sextants / Astrolabes",
            ],
            "Environmental": [
                "Pressed Flowers in Pages",
                "Candle Snuffers / Matchsticks / Sparks",
                "Origami Boats / Paper Ships",
                "Broken Violin Strings / Instrument Parts",
                "Floating Umbrellas / Parasols",
                "Fallen Crowns / Tiara Pieces",
                "Salt Crystals / Sugar Dust",
                "Handprints / Palm Lines (Appearing on Surfaces)",
                "Tiny Doorways in Tilework",
                "Ripped Fabric Swatches / Patchwork Scraps",
                # "Moss-Lit Mushrooms / Bioluminescent Fungi",
                "Errant Map Pins / Red Thread Routes",
                "Tiny Skeleton Keys (Like Jewelry)",
                "Floating Teacups & Saucers",
                "Spilled Honey / Syrup Trails",
                "Butterfly Pins / Brooches",
                "Bath Beads / Soap Foam / Steam Pearls",
                "Paper Crowns / Party Hats",
                "Snowglobes / Mini Dioramas",
                "Falling Calendars / Loose Date Pages",
            ],
        },
    ),
    "em": CategoryDefinition(
        key="em",
        label="Emotions",
        short="EM",
        weight_field="emotions",
        template="""
### {n}. The Atmosphere
**Emotion:** {content}
*Instruction: Color grade and lighting should reflect this emotion. The mood must be palpable (not vague).*
""".strip(),
        tree={
            "Light": {
                "Joyful": [
                    "Euphoria (Blinding Joy)",
                    "Serenity (Deep Calm)",
                    "Vitality (Explosive Life)",
                    "Whimsy (Playful Absurdity)",
                    "Relief (Weight Lifted)",
                    "Wonder (Childlike Discovery)",
                    "Triumph (Victorious Elation)",
                    "Tenderness (Gentle Love)",
                    "Mischief (Gleeful Trouble)",
                    "Contentment (Perfect Stillness)",
                    "Gratitude (Overflowing Thanks)",
                    "Ecstasy (Transcendent Bliss)",
                ],
            },
            "Shadow": {
                "Complex": [
                    "Melancholy (Beautiful Grief)",
                    "Dread (Creeping Unease)",
                    "Longing (Aching Distance)",
                    "Nostalgia (Warm Sadness)",
                    "Awe (Cosmic Scale)",
                    "Intimacy (Quiet Closeness)",
                    "Determination (Stoic Strength)",
                    "Reverence (Sacred Silence)",
                    "Defiance (Rebellious Fire)",
                    "Courage (Fearless Advance)",
                    "Pride (Earned Glory)",
                    "Compassion (Healing Warmth)",
                ],
            },
        },
    ),
    "sy": CategoryDefinition(
        key="sy",
        label="Symbols",
        short="SY",
        weight_field="symbols",
        template="""
### {n}. The Symbols (Totems)
**Motifs:** {content}
*Instruction: These objects must be physically present in the scene, woven into the architecture or held by the subject. They are the keys to the puzzle.*
""".strip(),
        tree={
            "Celebration": {
                "Fellowship": [
                    "The Wedding Canopy",
                    "The Feast Table",
                    "The Lantern Festival",
                    "The Maypole",
                    "The Rainbow Bridge / Bifrost",
                    "The Hearth Fire",
                    "The Love Letter",
                    "The Cradle",
                    "The Victory Wreath",
                    "The Wishing Well",
                    "The Flying Kite",
                    "The Music Box",
                    "The Friendship Bracelet",
                    "The First Blossom",
                    "The Lighthouse",
                    "The Shared Cup",
                    "The Open Hand",
                    "The Sunrise Gate",
                ],
            },
            "Mythic": {
                "Alchemy & Legend": [
                    "The Ouroboros",
                    "The Philosopher's Stone",
                    "The Caduceus",
                    "The Athanor",
                    "The Three Primes",
                    "The Sphinx",
                    "The Minotaur",
                    "The Cerberus",
                    "The Pegasus",
                    "The Hydra",
                    "The Basilisk",
                    "The Chimera",
                    "Pandora's Box",
                    "The Trojan Horse",
                    "Ariadne's Thread",
                    "The Golden Fleece",
                    "The Sword in the Stone",
                    "The Holy Grail",
                    "The Tower of Babel",
                    "The Ship of Theseus",
                    "Icarus's Wings",
                    "Achilles' Heel",
                    "The Glass Slipper",
                    "The Spinning Wheel",
                    "The Magic Mirror",
                    "The Enchanted Rose",
                    "The Red Cloak",
                    "The Poisoned Apple",
                    "The Breadcrumb Trail",
                    "The Beanstalk",
                    "The Pied Piper's Flute",
                    "The Golden Egg",
                ],
            },
            "Memento": {
                "Mortality": [
                    "The Skull",
                    "The Hourglass",
                    "The Half-Burned Candle",
                    "The Wilting Bouquet",
                    "The Death's-Head Moth",
                    "The Broken Crown",
                    "The Stopped Clock",
                ]
            },
            "Sacred": {
                "Iconic": [
                    "The Tree of Life",
                    "The All-Seeing Eye",
                    "The Mandala",
                    "The Lotus",
                    "The Ankh",
                    "The Halo",
                    "Jacob's Ladder",
                    "The Burning Bush",
                    "The Dharma Wheel",
                    "The Broken Column",
                    "The Cornucopia",
                    "The Lyre of Orpheus",
                    "The Masquerade Mask",
                    "The Comedy/Tragedy Masks",
                    "The Scales of Justice",
                    "The Heraldic Lion",
                    "The Compass Rose",
                    "The Eclipse",
                    "The Tidal Wave",
                    "The Aurora Borealis",
                    "The Lightning-Struck Tree",
                ],
            },
            "Heritage": {
                "Persian": [
                    "The Simurgh",
                    "The Faravahar",
                    "The Eternal Flame of Atar",
                    "The Cypress of Kashmar",
                    "Zahhak's Shoulder Serpents",
                    "The Derafsh Kaviani",
                    "The Gate of All Nations",
                ]
            },
        },
    ),
    "se": CategoryDefinition(
        key="se",
        label="Settings",
        short="SE",
        weight_field="settings",
        template="""
### {n}. The Stage
**Setting:** {content}
*Instruction: Treat this location as a character. It should be dense, atmospheric, and crowded. Avoid empty horizons. The setting should feel like it is consuming or birthing the subject.*
""".strip(),
        tree={
            "Interiors": {
                "Ceremonial Halls": [
                    "Collapsed opera house overgrown with phosphorescent ivy",
                    "Sunken throne room with tidal chandeliers",
                    "Perfume bazaar under mirrored domes",
                    "Cathedral kitchen where ovens glow like planets",
                    "Courtroom amphitheater draped in ceremonial tapestries",
                    "Velvet planetarium with mechanical constellations",
                    "Marble nursery of living statues",
                    "Ritual archive lit by whale-oil lanterns",
                    "Hall of ancestral masks and breathing frescoes",
                    "Gilded banquet nave with floating silverware",
                    "Temple of rotating stained-glass altars",
                    "Ink-black chapel of mirrored confessionals",
                ],
                "Domestic & Intimate": [
                    "Lantern-lit townhouse with endless stairwells",
                    "Attic nursery full of wind-up constellations",
                    "Sunroom draped in silk and trapped rainbows",
                    "Bathhouse of rose steam and porcelain murals",
                    "Kitchen courtyard with fruit trees growing through tile",
                    "Library-bedroom stitched with velvet curtains",
                    "Greenhouse parlor with bioluminescent vines",
                    "Grandmother's salon with mechanical songbirds",
                    "Abandoned dollhouse mansion scaled to human size",
                    "Mirror-lined dressing hall with whispered wardrobes",
                ],
                "Institutions & Archives": [
                    "Labyrinthine university archive with chained atlases",
                    "Museum vault where statues trade places nightly",
                    "Astronomy school with gravity-defying classrooms",
                    "Conservatory of bottled weather specimens",
                    "Medical theater turned ceremonial observatory",
                    "Legal archive where documents glow like embers",
                    "Monastic scriptorium with living ink",
                    "Alchemy academy with suspended furnace towers",
                    "Clockwork orphanage full of puzzle doors",
                    "Palace bureaucracy maze of red-thread records",
                ],
            },
            "Urban & Built": {
                "Markets & Streets": [
                    "Flooded market streets navigated by narrow gondolas",
                    "Rooftop festival quarter linked by kite bridges",
                    "Walled old town mapped in luminous tile mosaics",
                    "Night carnival boulevard of mirrored kiosks",
                    "Monsoon harbor packed with lacquered pagoda ships",
                    "Desert caravan avenue beneath woven canopies",
                    "Moonlit flower market on stepped terraces",
                    "Bridge bazaar suspended between bell towers",
                    "Clock square where shadows are auctioned",
                    "Festival district built around a colossal maypole engine",
                ],
                "Infrastructure & Industry": [
                    "Clockwork foundry with silk conveyor belts",
                    "Neon-lit train depot full of abandoned luggage altars",
                    "Iridescent fish market beneath copper aqueducts",
                    "Mossy hydroelectric chapel in mountain caverns",
                    "Ceramics workshop built inside a giant kiln shell",
                    "Ice refinery with stained-glass safety wards",
                    "Distillery of bottled thunder in basalt tunnels",
                    "Textile factory with humming loom-cathedrals",
                    "Mechanical apiary powered by violin resonance",
                    "Subterranean mint where coins are grown, not struck",
                ],
                "Fortresses & Monuments": [
                    "Glacier citadel with lantern tunnels",
                    "Desert necropolis converted into artisan studios",
                    "Salt-flat pilgrimage road lined with shrine towers",
                    "Fossil forest turned into open-air amphitheater",
                    "Cliffside city of wind organs and rope lifts",
                    "Rotating ring-city with shifting gravity lanes",
                    "Mirror maze embassy between rival kingdoms",
                    "Funerary avenue lined with silent balconies",
                    "Ruined zoo converted into communal workshops",
                    "Cathedral fortress of coral and brass",
                ],
            },
            "Natural": {
                "Forests & Wetlands": [
                    "Bioluminescent mangrove cathedral",
                    "Redwood valley with suspended village pods",
                    "Misty terraced rice ruins reclaimed by cranes",
                    "Orchid swamp threaded by bone-white walkways",
                    "Mushroom catacombs lit by ember spores",
                    "Fog forest of bell-bearing branches",
                    "Jungle ravine with vine elevators",
                    "Moon meadow ringed by standing stones",
                    "Cypress marsh with floating shrines",
                    "Petrified grove with porcelain leaves",
                ],
                "Desert & Arctic": [
                    "Dune city sheltered by giant woven canopies",
                    "Monolithic basalt coast under perpetual aurora",
                    "Snowbound monastery inside a frozen waterfall",
                    "Volcanic plateau of obsidian mirrors",
                    "Storm prairie of lightning-struck totems",
                    "Salt desert crossed by skeletal rail lines",
                    "Ice shelf labyrinth under polar halos",
                    "Cinder valley with smoking glass dunes",
                    "Dust-buried observatory with exposed domes",
                    "Saffron canyon of echoing wind harps",
                ],
                "Coastal & Oceanic": [
                    "Coral canyon with pearl staircases",
                    "Underground lake with upside-down stalactite docks",
                    "Tide clock lighthouse with living interior walls",
                    "Submarine cathedral under a bioluminescent trench",
                    "Sunken observatory where whales pass through domes",
                    "Harbor of upside-down ships and lantern nets",
                    "Sea cave court lit by phosphor waves",
                    "Cliff monastery above black tide pools",
                    "Kelp forest boulevard with drifting market stalls",
                    "Pearl reef amphitheater beneath shallow moonlight",
                ],
            },
            "Liminal": {
                "Transit & Thresholds": [
                    "Spiral district built around a bottomless cenote",
                    "Border checkpoint between two incompatible seasons",
                    "Endless staircase district with no ground level",
                    "Bridge of suspended rooms crossing a void",
                    "Train carriage that loops through different centuries",
                    "Cliff elevator station above cloud oceans",
                    "Hall of doors that open into weather systems",
                    "Floating customs office for dream travelers",
                    "Interdimensional ferry terminal of velvet corridors",
                    "Customs cathedral where passports are painted, not stamped",
                ],
                "Cosmic & Celestial": [
                    "Celestial dry dock where comets are repaired",
                    "Sky reef of drifting stone islands",
                    "Lunar tea district carved into crater rims",
                    "Star-map monastery suspended over abyssal light",
                    "Inverted waterfall palace above the clouds",
                    "Aurora amphitheater built into glacier arches",
                    "Meteor glass quarry with singing winds",
                    "Planetary archive orbiting a black sun",
                    "Dream bazaar set on a ring of moons",
                    "Orbiting chapel where eclipse bells mark time",
                ],
                "Performance & Spectacle": [
                    "Grand midnight circus beneath a striped meteor canopy",
                    "Abandoned circus ring flooded with mirror-water and confetti reeds",
                    "Traveling circus caravan city parked on salt flats",
                    "Clockwork circus menagerie under torn velvet tents",
                    "Aerial circus district suspended by cable bridges and balloons",
                    "Funhouse cathedral of warped mirrors and gilded cages",
                    "Carnival-circus necropolis lit by phosphor ticket booths",
                    "Floating circus coliseum orbiting a lantern moon",
                    "Puppet opera avenue where marionettes cast human shadows",
                    "Firework rehearsal yard built into stepped ruins",
                    "Masked masquerade plaza with living chandeliers",
                    "Circus rail depot where tents unfold like flowers",
                ],
            },
        },
    ),
    # --- PROMOTED: Camera subcategories become top-level categories ---
    "cm_angles": CategoryDefinition(
        key="cm_angles",
        label="Camera: Angles",
        short="CMA",
        weight_field="cm_angles",
        template="""
### {n}. The Lens (Camera Angle)
**Angle:** {content}
*Instruction: Lock the viewpoint. This is the viewer’s body position inside the scene.*
""".strip(),
        tree={
            "Viewpoint": [
                "Worm's-eye view with towering foreground ornament",
                "Bird's-eye diorama with tiny narrative clusters",
                "Isometric cutaway revealing interior and exterior simultaneously",
                "Centered one-point perspective with aggressive depth lines",
                "Dutch angle with cascading diagonals",
                "Extreme low-angle portrait against monumental architecture",
                "Wide panoramic vertical stack of spatial layers",
                "Telephoto compression of crowded planes",
                "Ultra-wide lens distortion with curving edges",
                "Three-quarter cinematic angle with deep parallax",
                "Over-the-shoulder viewpoint into a ritual scene",
                "Behind-the-curtain vantage through translucent textiles",
            ],
        },
    ),
    "cm_framing": CategoryDefinition(
        key="cm_framing",
        label="Camera: Framing",
        short="CMF",
        weight_field="cm_framing",
        template="""
### {n}. The Lens (Composition / Framing)
**Framing:** {content}
*Instruction: This is the composition logic. Enforce it: depth layers, occlusion, partitions, imbalance/symmetry—no compromises.*
""".strip(),
        tree={
            "Depth & Occlusion": [
                "Elevated balcony view through hanging foreground objects",
                "Framed through archways within archways",
                "Foreground occlusion using veils, vines, and railings",
                "Triptych-like internal partitioning in one frame",
                "Split-level composition with mirrored upper/lower worlds",
                "Concentric circular framing around the anchor subject",
                "Radial composition exploding outward from symbol core",
                "Dense left-heavy imbalance countered by micro-details",
                "Symmetrical altar-like arrangement with hidden asymmetries",
                "Layer-cake depth: near clutter, mid action, far architecture",
                "Corridor framing with repeated vanishing points",
                "Nested windows showing alternate micro-narratives",
            ],
        },
    ),
    # --- PROMOTED: Graphic Style subcategories become top-level categories ---
    "gr_temporal": CategoryDefinition(
        key="gr_temporal",
        label="Graphic Style: Temporal",
        short="GRT",
        weight_field="gr_temporal",
        template="""
### {n}. The Graphic Style (Time / Motion)
**Temporal Technique:** {content}
*Instruction: Encode time visually (echoes, trails, sequential beats). This should read as illustration—not a photo.*
""".strip(),
        tree={
            "Motion & Sequence": [
                "Freeze-frame of motion blur trails",
                "Multiple exposure effect within one still",
                "Time-lapse collage with repeated figure phases",
                "Circular motion choreography around static symbol",
                "Falling perspective with downward pull lines",
                "Ascending spiral composition climbing the canvas",
                "Shockwave ripple composition from a central impact",
                "Sequential action beats arranged like storyboard panels",
                "Snapshot candid feel inside maximalist clutter",
                "Long-exposure light trails guiding the eye",
                "Tilting horizon with suspended debris flow",
                "Before-and-after echoes layered in one tableau",
            ],
        },
    ),
    "gr_collage": CategoryDefinition(
        key="gr_collage",
        label="Graphic Style: Collage",
        short="GRC",
        weight_field="gr_collage",
        template="""
### {n}. The Graphic Style (Collage / Layout)
**Collage Logic:** {content}
*Instruction: Flatten space with stacked planes, borders, poster logic, diptychs, mosaics. Make it designed, not naturalistic.*
""".strip(),
        tree={
            "Collage & Decorative": [
                "Still-life foreground with dramatic narrative background",
                "Collage-flatness with stacked decorative planes",
                "Graphic poster framing with hard silhouette cutouts",
                "Decorative border motifs invading the scene interior",
                "Ornament-first composition where pattern dominates figures",
                "Negative-space illusion hiding a secondary figure",
                "Mosaic patchwork segmentation across the whole frame",
                "Paper-theater stage framing with visible layers",
                "Mirror-reflection dual composition with mismatched details",
                "Diptych logic fused into one card",
                "Kaleidoscopic quadrant repetition with intentional breaks",
                "Vintage tarot-card framing with crowded margins",
            ],
        },
    ),
    "gr_staging": CategoryDefinition(
        key="gr_staging",
        label="Graphic Style: Staging",
        short="GRS",
        weight_field="gr_staging",
        template="""
### {n}. The Graphic Style (Staging / Portraiture)
**Staging:** {content}
*Instruction: Direct the theatrical arrangement—silhouettes, reveals, mirrored pairs, or counter-narrative backgrounds.*
""".strip(),
        tree={
            "Portraiture": [
                "Hero centered while background tells counter-narrative",
                "Backlit silhouette with dense object halo",
                "Profile portrait split by architectural axis",
                "Close-up face plus miniature world in iris reflections",
                "Hands-in-foreground storytelling with distant figure",
                "Full-body portrait embedded in ornamental labyrinth",
                "Foreground stillness, background kinetic chaos",
                "Two-character mirrored staging with symbolic divide",
                "Anchor subject framed by crowd of watching motifs",
                "Portrait arranged as a theatrical reveal moment",
                "Subject partly hidden behind symbolic apparatus",
                "Statue-like pose in turbulent environmental motion",
            ],
        },
    ),
    "ee": CategoryDefinition(
        key="ee",
        label="Easter Eggs",
        short="EE",
        weight_field="easter_eggs",
        template="""
### {n}. The Hidden Whisper (Easter Egg)
**Homage:** {content}
*Instruction: Integrate this element subtly. It should NOT be the main focus. A pattern on a rug, a shape in the clouds, or a trinket on a shelf—a reward for the keen observer.*
""".strip(),
        tree={
            "Disney": {
                "Snow White": {
                    "Narrative": [
                        "Poisoned-apple omen and mirrored vanity anxiety",
                        "Whistling woodland labor and jewel-mine domesticity",
                        "Glass-coffin stillness in a flowered forest clearing",
                        "7 dwarfs",
                    ],
                    "Motifs": [
                        "A bright red apple with a single bite",
                        "A golden mirror face on a wall",
                        "Seven small pickaxes leaning against a wall",
                        "A blue bird perched on a finger",
                    ],
                },
                "Pinocchio": {
                    "Narrative": [
                        "Puppet-on-strings struggling toward real identity",
                        "Carnival temptation that turns children into beasts",
                        "Nose grows when lies",
                    ],
                    "Motifs": [
                        "A wooden hand with joint pins",
                        "A cricket with a top hat and umbrella",
                        "Donkey ears emerging from a shadow",
                        "Whale ribs forming an archway",
                    ],
                },
                "Cinderella": {
                    "Narrative": [
                        "Midnight deadline tension with vanishing glamour",
                        "Domestic servitude transformed by handmade couture magic",
                        "Single lost slipper as destiny key",
                    ],
                    "Motifs": [
                        "A glass slipper on a velvet pillow",
                        "A pumpkin turning into a carriage wheel",
                        "Sewing mice with needles",
                        "Clock hands striking twelve",
                    ],
                },
                "Alice in Wonderland": {
                    "Narrative": [
                        "Tea ritual trapped in absurd looping etiquette",
                        "Scale shifts triggered by food and potion symbols",
                        "Card-suit court justice with arbitrary punishments",
                    ],
                    "Motifs": [
                        "A top hat with a 10/6 card",
                        "A grinning floating cat smile",
                        "Red and white roses with paint drips",
                        "A pocket watch on a chain",
                    ],
                },
                "Peter Pan": {
                    "Narrative": [
                        "Second-star flight over moonlit rooftops",
                        "Eternal-childhood island with pirate threat",
                        "Shadow-sewing and nursery-window threshold motifs",
                    ],
                    "Motifs": [
                        "A hook replacing a hand",
                        "A silhouette of a boy flying",
                        "A ticking crocodile",
                        "Thimble kiss",
                    ],
                },
                "Little Mermaid": {
                    "Narrative": [
                        "Voice-for-legs contract with hidden cost",
                        "Shipwreck romance across species and kingdoms",
                        "Undersea court rebellion against protective father rule",
                    ],
                    "Motifs": [
                        "A dinglehopper (fork)",
                        "Glowing nautilus shell",
                        "Trident",
                        "Sea witch tentacles",
                    ],
                },
                "Aladdin": {
                    "Narrative": [
                        "Street thief discovering cosmic wish leverage",
                        "Identity performance between commoner and royalty",
                        "Magic-lamp trickster ally changing geopolitical stakes",
                    ],
                    "Motifs": [
                        "A golden oil lamp",
                        "A flying carpet pattern",
                        "A scarab beetle key",
                        "Blue smoke forming a face",
                    ],
                },
                "Lion King": {
                    "Narrative": [
                        "Exiled heir haunted by paternal sky-vision",
                        "Cycle-of-life kingship duty versus avoidance",
                        "Savanna usurpation ending in firelit confrontation",
                    ],
                    "Motifs": [
                        "A mandrill lifting a lion cub",
                        "A dark mane made of storm clouds",
                        "Outline of a lion on a cliff",
                        "Grubs on a leaf",
                    ],
                },
                "Tangled": {
                    "Narrative": [
                        "Impossibly long luminous hair as tool and prison",
                        "Tower confinement broken by charismatic outlaw partner",
                        "Lantern festival as memory-triggering revelation",
                    ],
                    "Motifs": [
                        "Glowing golden hair wrapped around rafters",
                        "A sun-crest flag",
                        "A chameleon blending into fruit",
                        "Floating sky lanterns",
                    ],
                },
                "Frozen": {
                    "Narrative": [
                        "Sister bond strained by isolating power",
                        "Ice architecture erupting from emotional repression",
                        "False-romance betrayal versus sacrificial familial love",
                    ],
                    "Motifs": [
                        "Snowflakes forming a palace layout",
                        "A carrot nose",
                        "Ice glove",
                        "Purple cape",
                    ],
                },
            },
            "Pixar": {
                "Toy Story": {
                    "Narrative": [
                        "Secret toy society activated when humans leave",
                        "Loyalty conflict between old favorite and flashy newcomer",
                        "Existential fear of replacement in childhood ecosystem",
                    ],
                    "Motifs": [
                        "A cowboy hat and badge",
                        "A space ranger helmet",
                        "A claw machine hand",
                        "Building blocks spelling ANDY",
                    ],
                },
                "Monsters Inc": {
                    "Narrative": [
                        "Fear-harvesting industry converted to laughter economy",
                        "Door-network logistics spanning child-bedroom dimensions",
                        "Unlikely child-monster bond exposing corporate corruption",
                    ],
                    "Motifs": [
                        "A single large eyeball",
                        "Blue fur with purple spots",
                        "Yellow scream canisters",
                        "A shredded wooden door",
                    ],
                },
                "Finding Nemo": {
                    "Narrative": [
                        "Anxious parent crossing vast ocean biomes",
                        "Memory-impaired guide reframing control into trust",
                        "Captivity-escape plot inside ornamental aquarium",
                    ],
                    "Motifs": [
                        "An orange clownfish pattern",
                        "Diver's mask with address",
                        "Seagulls on a buoy",
                        "Turtle shell pattern",
                    ],
                },
                "Up": {
                    "Narrative": [
                        "House lifted by balloons as grief pilgrimage vehicle",
                        "Ageing recluse mentoring eager wilderness novice",
                        "Explorer-idol disillusionment in remote lost-world",
                    ],
                    "Motifs": [
                        "A house floating with thousands of balloons",
                        "Grape soda bottle cap badge",
                        "A large colorful tropical bird",
                        "Talking dog collar",
                    ],
                },
                "Coco": {
                    "Narrative": [
                        "Marigold bridge between living and ancestral metropolis",
                        "Music ban as inherited trauma mechanism",
                        "Memory erasure as second death stakes",
                    ],
                    "Motifs": [
                        "Orange marigold petals",
                        "Sugar skull makeup",
                        "White guitar",
                        "Spirit guide dog",
                    ],
                },
                "Inside Out": {
                    "Narrative": [
                        "Personified emotions governing memory architecture",
                        "Core-memory collapse threatening identity coherence",
                        "Growing complexity from mono-emotion to mixed feeling",
                    ],
                    "Motifs": [
                        "Glowing colored memory orbs",
                        "Control console buttons",
                        "Island of personality",
                        "Rainbow unicorn",
                    ],
                },
            },
            "Studio Ghibli": {
                "Totoro": {
                    "Narrative": [
                        "Rural childhood wonder anchored by forest guardian",
                        "Bus-stop rain ritual with spirit visitation",
                    ],
                    "Motifs": [
                        "Giant leaf umbrella",
                        "Spinning top on a large belly",
                        "Catbus grin",
                        "Soot sprites",
                    ],
                },
                "Spirited Away": {
                    "Narrative": [
                        "Bathhouse labor under spirit-world contract",
                        "Name-theft control and identity recovery journey",
                    ],
                    "Motifs": [
                        "Transparent spirit 'No-Face' mask",
                        "Red bathhouse token",
                        "Dragon with a green mane",
                        "Origami paper birds",
                    ],
                },
                "Howl's Moving Castle": {
                    "Narrative": [
                        "Walking fortress powered by unstable fire demon pact",
                        "Curse-aging transformation and anti-war undertones",
                    ],
                    "Motifs": [
                        "A castle with chicken legs",
                        "A fire demon in a hearth",
                        "Star-children falling",
                        "Turnip scarecrow",
                    ],
                },
                "Princess Mononoke": {
                    "Narrative": [
                        "Forest gods versus ironworks modernity conflict",
                        "Cursed wound driving reluctant mediation between worlds",
                    ],
                    "Motifs": [
                        "Red war paint mask",
                        "Kodama (tree spirits)",
                        "Great wolf white fur",
                        "Cursed black worm tendrils",
                    ],
                },
                "Kiki": {
                    "Narrative": [
                        "Young witch independence learned through daily labor",
                        "Flight confidence tied to emotional self-belief",
                    ],
                    "Motifs": [
                        "Red hair bow",
                        "Black cat in a cage",
                        "Broomstick with a radio",
                        "Bakery wreath",
                    ],
                },
            },
            "Other Franchises": {
                "Harry Potter": {
                    "Narrative": [
                        "Moving staircase topology that re-routes social destiny",
                        "Floating-candle banquet hall under enchanted ceiling weather",
                        "Sorting-hat identity assignment under peer scrutiny",
                        "Patronus projection as weaponized memory of care",
                    ],
                    "Motifs": [
                        "Round glasses and lightning scar",
                        "Golden Snitch",
                        "Sorting Hat",
                        "Floating candles",
                        "Wand sparks",
                    ],
                },
                "Star Wars": {
                    "Narrative": [
                        "The Force binding the galaxy together",
                        "Rebellion against a technological terror",
                        "Redemption of the fallen father",
                    ],
                    "Motifs": [
                        "Dual suns on the horizon",
                        "Silhouette of a masked helmet",
                        "Crossed laser swords",
                        "A spherical space station",
                    ],
                },
                "Matrix": {
                    "Narrative": [
                        "Simulated reality crumbling to reveal code",
                        "Choice between painful truth and blissful ignorance",
                    ],
                    "Motifs": [
                        "Falling green digital rain",
                        "Red and Blue pills reflection",
                        "Black sunglasses",
                        "White rabbit tattoo",
                    ],
                },
                "Coraline": {
                    "Narrative": [
                        "Button-eyed duplicate family using affection as trap",
                        "Tiny hidden door opening to seductive parallel home",
                        "Domestic boredom transformed into uncanny survival trial",
                    ],
                    "Motifs": [
                        "Girl with blue hair and yellow raincoat",
                        "Black cat with crooked tail",
                        "Button eyes",
                        "Seeing stone (triangle with hole)",
                    ],
                },
                "Alice (Literary)": {
                    "Narrative": [
                        "Logic games and riddles undermining fixed reality",
                        "Tea-party etiquette spiraling into absurd procedure",
                    ],
                    "Motifs": [
                        "White Rabbit with a waistcoat",
                        "Flamingo croquet mallet",
                        "Cheshire Cat smile",
                        "Drink Me bottle",
                    ],
                },
            },
        },
    ),
}

CATEGORY_ORDER: List[str] = [
    "ar",
    "cn",
    "sl",
    "tx",
    "sc",
    "em",
    "sy",
    "se",
    "cm_angles",
    "cm_framing",
    "gr_temporal",
    "gr_collage",
    "gr_staging",
    "ee",
]


# ============================================================
# 4) CORE LOGIC
# ============================================================


def validate_definitions() -> None:
    missing = [k for k in CATEGORY_ORDER if k not in CATEGORIES]
    if missing:
        raise ValueError(f"CATEGORY_ORDER contains unknown category keys: {missing}")

    short_codes = [CATEGORIES[k].short.upper() for k in CATEGORY_ORDER]
    dup = {s for s in short_codes if short_codes.count(s) > 1}
    if dup:
        raise ValueError(f"Duplicate category short codes found: {sorted(dup)}")

    for k in CATEGORY_ORDER:
        d = CATEGORIES[k]
        if not d.template or "{content}" not in d.template or "{n}" not in d.template:
            raise ValueError(
                f"Category {k!r} template must include '{{n}}' and '{{content}}' placeholders."
            )


def iter_leaf_buckets(
    node: Any, path: Tuple[str, ...] = ()
) -> Iterable[Tuple[str, List[str]]]:
    if isinstance(node, list):
        yield ("/".join(path), list(node))
        return

    if isinstance(node, dict):
        for key, child in node.items():
            yield from iter_leaf_buckets(child, path + (str(key),))
        return

    raise TypeError(
        f"Unsupported tree node type at {'/'.join(path) or '<root>'}: {type(node)!r}"
    )


def build_catalog(
    defn: CategoryDefinition, exclude_patterns: List[str], include_codes: bool
) -> CategoryCatalog:
    leaf_buckets = list(iter_leaf_buckets(defn.tree))
    raw_entries: List[Tuple[str, str]] = []

    for bucket_path, names in leaf_buckets:
        # Check exclusions
        if exclude_patterns:
            if any(pat in bucket_path for pat in exclude_patterns):
                continue

        for name in names:
            raw_entries.append((bucket_path, name))

    if not raw_entries:
        return CategoryCatalog(
            key=defn.key, label=defn.label, short=defn.short, all_items=[], buckets={}
        )

    width = max(2, len(str(len(raw_entries))))
    coded_all: List[str] = []
    coded_buckets: Dict[str, List[str]] = {}

    short = defn.short.upper()
    for i, (bucket_path, name) in enumerate(raw_entries, start=1):
        if include_codes:
            code = f"{short}-{i:0{width}d}"
            item_text = f"{code} {name}"
        else:
            item_text = name

        coded_all.append(item_text)
        coded_buckets.setdefault(bucket_path, []).append(item_text)

    return CategoryCatalog(
        key=defn.key,
        label=defn.label,
        short=short,
        all_items=coded_all,
        buckets=coded_buckets,
    )


def build_catalogs(cfg: MatrixConfig) -> Dict[str, CategoryCatalog]:
    catalogs = {}
    for k in CATEGORY_ORDER:
        defn = CATEGORIES[k]
        exclude_patterns = []

        # Specific Logic for Easter Eggs (EE)
        if k == "ee":
            if not cfg.include_ee_narratives:
                exclude_patterns.append("Narrative")
            if not cfg.include_ee_motifs:
                exclude_patterns.append("Motifs")

        catalogs[k] = build_catalog(defn, exclude_patterns, cfg.include_code_p)
    return catalogs


def per_prompt_counts(weight: float, prompts: int, rng: random.Random) -> List[int]:
    if weight <= 0:
        return [0] * prompts
    base = int(math.floor(weight))
    frac = weight - base
    counts = [base] * prompts
    if frac > 0:
        for i in range(prompts):
            if rng.random() < frac:
                counts[i] += 1
    return counts


def allocate_mandatory_buckets(
    counts: List[int],
    mandatory_counts: Dict[str, int],
    rng: random.Random,
) -> Dict[int, List[str]]:
    allocation: Dict[int, List[str]] = {i: [] for i in range(len(counts))}
    slots = [i for i, c in enumerate(counts) for _ in range(c)]
    if not slots:
        return allocation

    rng.shuffle(slots)
    cursor = 0
    for bucket_path, need in mandatory_counts.items():
        for _ in range(max(0, int(need))):
            if cursor >= len(slots):
                return allocation
            allocation[slots[cursor]].append(bucket_path)
            cursor += 1
    return allocation


def pick_item(items: Sequence[str], used: set[str], rng: random.Random) -> str:
    if not items:
        raise ValueError("pick_item called with empty items")
    unique_items = [x for x in items if x not in used]
    return rng.choice(unique_items) if unique_items else rng.choice(list(items))


def sample_items_for_prompt(
    buckets: Dict[str, List[str]],
    item_count: int,
    forced_bucket_paths: Sequence[str],
    rng: random.Random,
) -> List[str]:
    if item_count <= 0 or not buckets:
        return []

    selected: List[str] = []
    used_items: set[str] = set()
    used_bucket_paths: set[str] = set()
    used_top_groups: set[str] = set()

    # 1) Forced picks first
    for path in forced_bucket_paths:
        items = buckets.get(path)
        if not items:
            continue
        item = pick_item(items, used_items, rng)
        selected.append(item)
        used_items.add(item)
        used_bucket_paths.add(path)
        used_top_groups.add(path.split("/", 1)[0] if "/" in path else path)
        if len(selected) >= item_count:
            return selected

    # 2) Diversity pass (avoid repeating top-group)
    bucket_paths = list(buckets.keys())
    rng.shuffle(bucket_paths)

    for path in bucket_paths:
        if len(selected) >= item_count:
            break
        top = path.split("/", 1)[0] if "/" in path else path
        if top in used_top_groups:
            continue
        item = pick_item(buckets[path], used_items, rng)
        selected.append(item)
        used_items.add(item)
        used_bucket_paths.add(path)
        used_top_groups.add(top)

    # 3) Fill from remaining buckets
    for path in bucket_paths:
        if len(selected) >= item_count:
            break
        if path in used_bucket_paths:
            continue
        item = pick_item(buckets[path], used_items, rng)
        selected.append(item)
        used_items.add(item)
        used_bucket_paths.add(path)

    # 4) If still short, allow repeats
    while len(selected) < item_count:
        path = rng.choice(bucket_paths)
        item = pick_item(buckets[path], used_items, rng)
        selected.append(item)
        used_items.add(item)

    return selected


def mandatory_constraints(cfg: MatrixConfig) -> Dict[str, Dict[str, int]]:
    # bucket paths must match iter_leaf_buckets output for those category trees
    return {
        "em": {"Light/Joyful": cfg.min_light_emotions},
        "sy": {"Celebration/Fellowship": cfg.min_celebration_symbols},
    }


def generate_matrix_structs(cfg: MatrixConfig) -> List[Dict[str, List[str]]]:
    if cfg.prompts_per_batch <= 0:
        raise ValueError("prompts_per_batch must be > 0")

    catalogs = build_catalogs(cfg)
    rng = random.Random(cfg.seed)

    per_counts: Dict[str, List[int]] = {}
    forced_alloc: Dict[str, Dict[int, List[str]]] = {}
    constraints = mandatory_constraints(cfg)

    # Precompute per-category counts and forced allocations (batch-level)
    warnings: List[str] = []
    for key in CATEGORY_ORDER:
        defn = CATEGORIES[key]
        weight = float(getattr(cfg, defn.weight_field))

        counts = per_prompt_counts(weight, cfg.prompts_per_batch, rng)
        per_counts[key] = counts

        cat_constraints = constraints.get(key, {})
        if cat_constraints and sum(counts) > 0:
            capacity = sum(counts)
            clamped: Dict[str, int] = {}
            for bucket_path, need in cat_constraints.items():
                take = min(max(0, int(need)), capacity)
                if take > 0:
                    clamped[bucket_path] = take
                    capacity -= take

            if clamped:
                forced_alloc[key] = allocate_mandatory_buckets(counts, clamped, rng)
                for bucket_path, need in cat_constraints.items():
                    if clamped.get(bucket_path, 0) < int(need):
                        warnings.append(
                            f"[constraint] {key}:{bucket_path} requested {need} but capacity only allowed {clamped.get(bucket_path, 0)}"
                        )
            else:
                forced_alloc[key] = {i: [] for i in range(cfg.prompts_per_batch)}
                for bucket_path, need in cat_constraints.items():
                    warnings.append(
                        f"[constraint] {key}:{bucket_path} requested {need} but capacity was 0"
                    )
        else:
            forced_alloc[key] = {i: [] for i in range(cfg.prompts_per_batch)}

    if warnings:
        print("\n".join(warnings), file=sys.stderr)

    # Build per-prompt picks
    prompt_structs: List[Dict[str, List[str]]] = []
    for prompt_i in range(cfg.prompts_per_batch):
        prompt_data: Dict[str, List[str]] = {}
        for key in CATEGORY_ORDER:
            item_count = per_counts[key][prompt_i]
            if item_count <= 0:
                prompt_data[key] = []
                continue

            catalog = catalogs[key]
            # Handle case where exclusion resulted in empty catalog
            if not catalog.buckets:
                prompt_data[key] = []
                continue

            prompt_data[key] = sample_items_for_prompt(
                buckets=catalog.buckets,
                item_count=item_count,
                forced_bucket_paths=forced_alloc[key][prompt_i],
                rng=rng,
            )
        prompt_structs.append(prompt_data)

    return prompt_structs


def format_dynamic_block(prompt_data: Mapping[str, List[str]]) -> str:
    parts: List[str] = []
    section_n = 0

    for key in CATEGORY_ORDER:
        items = prompt_data.get(key, [])
        if not items:
            continue

        section_n += 1
        defn = CATEGORIES[key]
        content_str = " & ".join(items)
        parts.append(defn.template.format(n=section_n, content=content_str).strip())

    return "\n\n".join(parts)


def write_prompts_to_files(
    structs: Sequence[Mapping[str, List[str]]], output_dir: str
) -> None:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    # Detect existing numbered files to continue sequence
    start_index = 1
    existing_files = list(out.glob("prompt_*.md"))
    if existing_files:
        max_num = 0
        for f in existing_files:
            # Expected format: prompt_001.md
            # Split to get the number part
            parts = f.stem.split("prompt_")
            # Check if the last part is a number (e.g., prompt_005 -> 005)
            if len(parts) >= 2 and parts[-1].isdigit():
                num = int(parts[-1])
                if num > max_num:
                    max_num = num
        start_index = max_num + 1

    for i, data in enumerate(structs, start=start_index):
        dynamic_block = format_dynamic_block(data)
        filled_text = MASTER_TEMPLATE.format(dynamic_matrix_block=dynamic_block)

        name = f"prompt_{i:d}.md"
        if i == start_index:
            print(f"File numbering started at: {name}")

        filepath = out / name
        filepath.write_text(filled_text, encoding="utf-8")

    print(
        f"Successfully generated {len(structs)} 'Frozen Dream' pre-prompts in: {out.resolve()}"
    )


# ============================================================
# 5) CLI
# ============================================================


def parse_args() -> MatrixConfig:
    defaults = MatrixConfig()
    p = argparse.ArgumentParser(
        description="Generate 'Frozen Dream' Dixit pre-prompts (Matrix v9.x, Granular POV).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    p.add_argument(
        "--prompts",
        dest="prompts_per_batch",
        type=int,
        default=defaults.prompts_per_batch,
    )
    p.add_argument("--seed", type=int, default=defaults.seed)
    p.add_argument("--output", dest="output_dir", type=str, default=defaults.output_dir)

    p.add_argument(
        "--include-codes",
        dest="include_code_p",
        action="store_true",
        help="Include alphanumeric codes (e.g. AR-01) in output",
    )

    # Core categories
    p.add_argument("--ar", dest="archetypes", type=float, default=defaults.archetypes)
    p.add_argument("--cn", dest="concepts", type=float, default=defaults.concepts)
    p.add_argument(
        "--sl", dest="surreal_logic", type=float, default=defaults.surreal_logic
    )
    p.add_argument("--tx", dest="textures", type=float, default=defaults.textures)
    p.add_argument("--sc", dest="scatter", type=float, default=defaults.scatter)
    p.add_argument("--em", dest="emotions", type=float, default=defaults.emotions)
    p.add_argument("--sy", dest="symbols", type=float, default=defaults.symbols)
    p.add_argument("--se", dest="settings", type=float, default=defaults.settings)

    # Promoted Camera Weights
    p.add_argument(
        "--cm-angles", dest="cm_angles", type=float, default=defaults.cm_angles
    )
    p.add_argument(
        "--cm-framing", dest="cm_framing", type=float, default=defaults.cm_framing
    )

    # Promoted Graphic Style Weights
    p.add_argument(
        "--gr-temporal", dest="gr_temporal", type=float, default=defaults.gr_temporal
    )
    p.add_argument(
        "--gr-collage", dest="gr_collage", type=float, default=defaults.gr_collage
    )
    p.add_argument(
        "--gr-staging", dest="gr_staging", type=float, default=defaults.gr_staging
    )

    p.add_argument("--ee", dest="easter_eggs", type=float, default=defaults.easter_eggs)

    # Easter Egg Filters
    p.add_argument(
        "--no-ee-motifs",
        dest="include_ee_motifs",
        action="store_false",
        default=True,
        help="Disable Visual Motifs in Easter Eggs",
    )
    p.add_argument(
        "--no-ee-narratives",
        dest="include_ee_narratives",
        action="store_false",
        default=True,
        help="Disable Narrative Themes in Easter Eggs",
    )

    # Constraints
    p.add_argument(
        "--min-em-light",
        dest="min_light_emotions",
        type=int,
        default=defaults.min_light_emotions,
    )
    p.add_argument(
        "--min-sy-celebration",
        dest="min_celebration_symbols",
        type=int,
        default=defaults.min_celebration_symbols,
    )

    a = p.parse_args()
    return MatrixConfig(
        prompts_per_batch=a.prompts_per_batch,
        seed=a.seed,
        output_dir=a.output_dir,
        include_code_p=a.include_code_p,
        archetypes=a.archetypes,
        concepts=a.concepts,
        surreal_logic=a.surreal_logic,
        textures=a.textures,
        scatter=a.scatter,
        emotions=a.emotions,
        symbols=a.symbols,
        settings=a.settings,
        cm_angles=a.cm_angles,
        cm_framing=a.cm_framing,
        gr_temporal=a.gr_temporal,
        gr_collage=a.gr_collage,
        gr_staging=a.gr_staging,
        easter_eggs=a.easter_eggs,
        include_ee_motifs=a.include_ee_motifs,
        include_ee_narratives=a.include_ee_narratives,
        min_light_emotions=a.min_light_emotions,
        min_celebration_symbols=a.min_celebration_symbols,
    )


def main() -> None:
    validate_definitions()
    cfg = parse_args()
    structs = generate_matrix_structs(cfg)

    write_prompts_to_files(structs, cfg.output_dir)


if __name__ == "__main__":
    main()
