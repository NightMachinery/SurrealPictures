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
    archetypes: float = 0.5
    concepts: float = 1.0
    surreal_logic: float = 0.5
    textures: float = 0.3
    scatter: float = 0.3
    emotions: float = 1.1
    symbols: float = 1.5
    settings: float = 0.5

    # Promoted Camera Weights
    cm_angles: float = 0.3
    cm_framing: float = 0.1

    # Promoted Graphic Style Weights
    gr_temporal: float = 0.1
    gr_collage: float = 0.1
    gr_staging: float = 0.1

    # Easter Eggs
    easter_eggs: float = 2.0
    include_ee_narratives: bool = True
    include_ee_motifs: bool = True

    # Constraints (minimum totals across the whole batch, clamped to capacity)
    min_light_emotions: int = 4
    min_celebration_symbols: int = 2


# ============================================================
# 2) MASTER TEMPLATE
# ============================================================

MASTER_TEMPLATE = (
    """
# Role: The Surrealist Auteur (Adult Dixit Edition)

You are an avant-garde Art Director and a master of surrealist visual storytelling. Your task is to write a single, masterful, high-density prompt for a text-to-image AI.

You are creating a single illustration for a collectible Dixit card designed for adults — a surrealist artwork that functions as a visual Rorschach test. The image must be polysemic: five different people should look at it and project five completely different stories, emotions, and memories onto it.

## Objective
Create a visual description for a "Dixit" style card game designed for adults (25+).
Design a highly intentional and **Polysemic** image. This means the image contains specific details that support multiple, contradictory narratives depending on the viewer's mindset.

**The "Multiple Narrative" Rule:**
Infuse the scene with an overwhelming amount of layered meaning.
*   **Conflicting Clues:** Place objects together that tell different stories.
*   **Psychological Depth:** Set a mature, rich, and playful emotional tone. Evoke complex feelings, both positive and negative.
*   **The Test:** Construct the imagery so that three different viewers will see distinct themes.

# Input Data
Synthesize the following elements into your scene description:

{dynamic_matrix_block}

# Writing Instructions
1.  **Synthesize Interactions:** Describe dynamic interactions between elements. Write active phrasing such as: "A giant [Object A] is slowly consuming [Object B]..."
2.  **Crowd the Frame:** Fill this high-detail image completely. Describe the foreground, the background, the items floating in the sky, and the secrets hidden in the shadows.
3.  **Be Concrete:** Use tangible, physical nouns. To represent a concept like time, describe a physical object like "a melting grandfather clock."
4.  **Aspect Ratio:** Frame the composition vertically (2:3).

# CRITICAL CONSTRAINTS
*   **SEMANTICS ONLY:** Restrict your description entirely to the tangible contents, subjects, and actions within the scene. A separate system will apply the artistic medium, so keep your vocabulary strictly focused on what is physically happening in the world of the image, the composition, camera angles, etc.
*   **Output:** Return only the final prompt text.
""".strip()
    + "\n"
)


# ============================================================
# 3) CATEGORY DEFINITIONS
# ============================================================

CATEGORIES: Dict[str, CategoryDefinition] = {
    "ar": CategoryDefinition(
        key="ar",
        label="Archetypes (Wizarding Fanon)",
        short="AR",
        weight_field="archetypes",
        template="""
### {n}. The Anchor (Subject)
**Archetype{plural_suffix}:** {content}
    *Instruction: {anchor_subject} of your visual paradox. Make {anchor_object} the dominant focal protagonist of the scene. Portray {anchor_object} with specificity and symbolic weight. Treat {anchor_object} as a mythic, timeless presence. Show {anchor_possessive} agency, motivations, and emotional state{interaction_clause} {social_clause} {non_human_clause}*
""".strip(),
        tree={
            "School Life": {
                "Students & Alumni": [
                    "The Eighth-Year Mediator",
                    "The Muggleborn Archivist",
                    "The Reformed Slytherin Prefect",
                    "The Gryffindor Who Chose Diplomacy",
                    "The Ravenclaw Rune Hacker",
                    "The Hufflepuff Quartermaster",
                    "The Durmstrang Transfer Duelist",
                    "The Beauxbatons Exchange Enchanter",
                    "The Unsanctioned Animagus Apprentice",
                    "The Anonymous Howler Ghostwriter",
                ],
                "Faculty & Staff": [
                    "The Potions Master on Probation",
                    "The Groundskeeper of Forbidden Creatures",
                    "The Charms Professor with Split Allegiances",
                    "The Librarian of Restricted Shelves",
                    "The St Mungo's Healer-In-Residence",
                    "The House-Elf Union Organizer",
                    "The Portrait Headmistress Who Never Sleeps",
                    "The Caretaker of Broken Wands",
                ],
            },
            "Politics & War": {
                "Ministry & Law": [
                    "The Unspeakable Archivist",
                    "The Auror Investigator",
                    "The Wizengamot Dissenter",
                    "The Ministry Press Liaison",
                    "The Cursed-Artifact Prosecutor",
                    "The Obliviator with a Guilty Conscience",
                    "The Diplomat to Goblin Houses",
                    "The Magical Transport Regulator",
                ],
                "Resistance & Espionage": [
                    "The Order Safehouse Keeper",
                    "The Double Agent",
                    "The Prophecy Smuggler",
                    "The Patronus Courier",
                    "The Invisibility-Cloak Scout",
                    "The Polyjuice Infiltrator",
                    "The Wandmaker's Informant",
                    "The Former Death Eater Defector",
                ],
            },
            "Arcane Specialists": {
                "Magic Disciplines": [
                    "The Arithmancy Savant",
                    "The Ancient Runes Decipherer",
                    "The Time-Turner Theorist",
                    "The Wand-Lore Scholar",
                    "The Ritual Circle Architect",
                    "The Curse-Breaker",
                    "The Memory Alchemist",
                    "The Astral Cartographer",
                ],
                "Curses & Healing": [
                    "The Curse-Healer",
                    "The Werewolf Advocate",
                    "The Occlumency Instructor",
                    "The Legilimens Interrogator",
                    "The Poison Antidote Brewer",
                    "The Blood-Curse Genealogist",
                    "The Patronus Therapist",
                    "The Postwar Trauma Mediwitch",
                ],
            },
            "Relationships": {
                "Bonds": [
                    "The Found-Family Guardian",
                    "The Rival-House Secret Pen Pal",
                    "The Estranged Siblings Reunited by War",
                    "The Betrothed Heirs in Political Truce",
                    "The Childhood Friends Turned Ideological Opponents",
                    "The Mentor and the Reluctant Successor",
                    "The Lovers Bound by Vow and Suspicion",
                ],
                "Rivalries": [
                    "The Legacy Heir Fighting Their Surname",
                    "The Quidditch Captain Turned Whistleblower",
                    "The Duelist Seeking Public Redemption",
                    "The Prefect Enforcing Unjust Rules",
                    "The Journalist Hunting the Hidden Truth",
                    "The Spell-Patent Tycoon",
                    "The Keeper of Family Secrets",
                ],
            },
            "Non-Human": {
                "Magical Beings": [
                    "The House-Elf Matriarch",
                    "The Goblin Oathkeeper",
                    "The Veela Diplomat",
                    "The Centaur Prophecy Reader",
                    "The Merperson Ambassador",
                    "The Phoenix Companion",
                    "The Thestral Guide",
                    "The Kneazle Familiar",
                ],
                "Constructs & Echoes": [
                    "The Sentient Portrait",
                    "The Knight in Enchanted Armor",
                    "The Living Suitcase",
                    "The Self-Writing Quill",
                    "The Animated Chess Champion",
                    "The Echo of a Pensieve Memory",
                    "The Clockwork Owl Messenger",
                    "The Unfinished Golem Guardian",
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
        label="Symbols (Wizarding Fanon)",
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
                    "Interwoven house scarves tied to one banquet chair",
                    "Floating cocoa mugs charmed to refill themselves",
                    "A reconstructed house cup made from fused shards",
                    "An owl-post ribbon wall of unsent apologies",
                    "Yule-ball masks hung beside patched school robes",
                    "A polyglot songbook shared by rival tables",
                    "Candles braided with friendship bracelets",
                    "Tea tins labeled with initials from all four houses",
                    "Joint detention ledgers stamped PAID IN FULL",
                    "A peace toast with four differently colored goblets",
                    "A first-day acceptance letter wrapped around wildflowers",
                    "A pumpkin feast table marked with empty memorial seats",
                ],
                "Ceremony": [
                    "A sorting stool draped in neutral gray ribbon",
                    "A vow book bound in dragonhide and lace",
                    "A repaired dueling platform ringed with lanterns",
                    "A graduation parchment signed by portraits",
                    "A house banner stitched from old Quidditch uniforms",
                    "A victory wreath made of phoenix feathers and ivy",
                ],
            },
            "Relics": {
                "Hallows & Myths": [
                    "A cracked wand wrapped in elder wood splints",
                    "A stone ring casting ghost-light reflections",
                    "A cloak clasp shaped like a closed eye",
                    "A triangle-circle-line sigil scratched into candle wax",
                    "A fable manuscript about three impossible brothers",
                    "A thestral-hair ribbon sealed in glass",
                    "A resurrection sketchbook filled with erased faces",
                    "A mirror shard that shows the wrong room",
                ],
                "School Artifacts": [
                    "A bewitched map with moving ink footprints",
                    "A rewritable detention quill",
                    "A pensieve vial labeled DO NOT EDIT",
                    "A remembrall glowing two colors at once",
                    "A broken time-turner suspended in copper thread",
                    "A prefect badge melted into a key",
                    "A howler envelope sealed but still smoking",
                    "A broom tail tied with anti-jinx charms",
                ],
            },
            "Memento": {
                "Mortality": [
                    "A memorial wall of charred wand cores",
                    "An unclaimed trunk tag from Platform Nine and Three-Quarters",
                    "A fallen auror badge pinned to black velvet",
                    "A stopped pocket watch from a battle night",
                    "A cracked omniocular replaying the same duel",
                    "A potion flask half-full of phoenix ash",
                    "A wilted white lily pressed into a court transcript",
                    "An old newspaper headline bound in mourning ribbon",
                ]
            },
            "Sacred": {
                "Wards & Oaths": [
                    "A blood ward circle drawn in salt and chalk",
                    "An unbreakable vow cord braided with silver",
                    "Runes carved into a school doorway lintel",
                    "A fidelius key written on disappearing parchment",
                    "A family magic crest lit from within",
                    "A patronus sigil burned into a shield",
                    "A goblin contract etched on metal foil",
                    "A protective charm bracelet threaded with teeth",
                ],
                "Cosmic": [
                    "An enchanted ceiling charting impossible constellations",
                    "A prophecy sphere held in iron thorns",
                    "A moon-phase clock with thirteen nights",
                    "An eclipse medallion worn by two rival heirs",
                    "A star map that redraws after each lie",
                    "Meteor-silver dust scattered over a ritual table",
                ],
            },
            "Heritage": {
                "Lineage": [
                    "A black family tapestry with burned-out names",
                    "A signet ring split then soldered in gold",
                    "A genealogy ledger annotated by different hands",
                    "An heirloom locket sealed by serpent runes",
                    "A dowry chest filled with forbidden textbooks",
                    "A wedding contract scorched along one edge",
                    "An ancestral portrait frame standing empty",
                    "A crest pin swapped between enemy families",
                ],
                "Creatures": [
                    "Phoenix molted feathers stored in medicine jars",
                    "Hippogriff tack decorated with apology knots",
                    "Dragon scale armor sewn into school satchels",
                    "Kneazle whiskers tied around a compass",
                    "Acromantula silk threaded through formal gloves",
                    "A basilisk fang mounted beside a healer oath",
                    "Merperson pearl strings hanging over maps",
                    "A bowtruckle nest built inside a quill stand",
                ],
            },
        },
    ),

    "se": CategoryDefinition(
        key="se",
        label="Settings (Wizarding Fanon)",
        short="SE",
        weight_field="settings",
        template="""
### {n}. The Stage
**Setting:** {content}
*Instruction: Treat this location as a character. It should be dense, atmospheric, and crowded. Avoid empty horizons. The setting should feel like it is consuming or birthing the subject.*
""".strip(),
        tree={
            "Interiors": {
                "Castle Halls": [
                    "Repaired Great Hall with floating candles and scaffold shadows",
                    "Moving-stairwell nexus rerouted by emergency enchantments",
                    "Portrait corridor where frames whisper contradictory testimony",
                    "Abandoned potions classroom glowing with slow-bubbling vials",
                    "Hospital wing extension lined with privacy wards",
                    "Hidden dueling club chamber beneath a tapestry stair",
                    "Astronomy tower observatory with weather trapped under glass",
                    "Viaduct gallery draped in memorial house banners",
                    "Prefect bathroom converted into a reconciliation salon",
                    "Room of Requirement appearing as a triage library",
                ],
                "Dormitories & Common Rooms": [
                    "Inter-house safe room with mismatched furniture and anti-jinx sigils",
                    "Slytherin common room lit by lake-green stormlight",
                    "Gryffindor dormitory rebuilt with patched four-poster curtains",
                    "Ravenclaw attic workspace full of self-folding star charts",
                    "Hufflepuff kitchen annex stacked with shared care packages",
                    "Secret attic of confiscated prank artifacts",
                    "Co-ed postwar dorm with curtains used as peace flags",
                    "Prefect lounge split by a glowing arbitration line",
                    "Trunk room where charms keep letters from burning",
                    "House-elf corridor transformed into a union meeting nook",
                ],
                "Institutions & Archives": [
                    "Ministry atrium under temporary reconstruction scaffolds",
                    "Department of Mysteries file vault of humming prophecy dust",
                    "Wizengamot hearing chamber ringed with memory projectors",
                    "St Mungo's curse ward with floating diagnosis slates",
                    "Gringotts arbitration room behind dragon-forged doors",
                    "Owl post sorting hall with stormproof skylights",
                    "Auror evidence archive sealed by rotating rune locks",
                    "Pensieve library where memories queue like lanterns",
                    "Floo regulation office tangled in soot and paperwork",
                    "Magical law records crypt beneath the Ministry",
                ],
            },
            "Urban & Built": {
                "Markets & Alleys": [
                    "Diagon-style high street during curfew amnesty night",
                    "Knockturn-adjacent lane of shuttered cursed-relic shops",
                    "Apothecary arcade perfumed with volatile potion mist",
                    "Broommaker row lined with wind tunnels and test tracks",
                    "Owl emporium courtyard draped in delivery ribbons",
                    "Wizarding book market under charmed anti-rain domes",
                    "Open-air wand repair bazaar lit by blue sparks",
                    "Postwar memorial square where statues quietly move",
                    "Underground duel pit beneath a tea house",
                    "Galleon exchange bridge between rival family districts",
                ],
                "Infrastructure & Industry": [
                    "Floo hub station of emerald fireplaces and brass turnstiles",
                    "Portkey depot with numbered hooks and countdown clocks",
                    "Knight Bus maintenance yard under neon runes",
                    "Wand core processing workshop beside a moonlit greenhouse",
                    "Spell-ink foundry with self-stirring vats",
                    "Enchanted quill factory threaded with metallic feathers",
                    "Potion bottling line protected by splash wards",
                    "Broom race tunnel carved through black stone",
                    "Magical radio broadcast studio hidden in a chimney stack",
                    "Courier owl roost towers linked by rune rails",
                ],
                "Fortresses & Monuments": [
                    "Storm-lashed sea fortress prison with spectral guard lights",
                    "Ruined battle courtyard where animated statues still patrol",
                    "Family manor converted into a truth-and-reconciliation tribunal",
                    "Old pure-blood estate swallowed by thorn wards",
                    "Mountain keep containing a treaty-signing hall",
                    "Monument avenue of broken wands and names",
                    "Abandoned school annex reclaimed as a refugee sanctuary",
                    "Goblin citadel archive beneath iron bridges",
                    "Dragon sanctuary watchtower on volcanic cliffs",
                    "Forgotten dueling amphitheater under snow",
                ],
            },
            "Natural": {
                "Forests & Wetlands": [
                    "Forbidden-forest edge with warded lantern trails",
                    "Moonlit thestral glade ringed by standing stones",
                    "Centaur observatory meadow with carved sky circles",
                    "Acromantula silk ravine over a black-water stream",
                    "Marshland path where will-o-wisps mimic patronuses",
                    "Unicorn sanctuary hidden in frost-touched pines",
                    "Bog garden of carnivorous potion flora",
                    "Fog valley scattered with abandoned training dummies",
                    "Werewolf refuge camp in a birch thicket",
                    "Hippogriff aerie on a cliff above the treeline",
                ],
                "Highlands & Ruins": [
                    "Scottish highland ridge dotted with ward pylons",
                    "Crumbling druid circle repurposed as a classroom",
                    "Wind-blasted moor crossed by enchanted rail tracks",
                    "Snowbound pass leading to a hidden safehouse",
                    "Abandoned Quidditch practice pitch overgrown with ivy",
                    "Volcanic valley where dragon handlers train at dawn",
                    "Ruined watchtower wrapped in anti-apparition chains",
                    "Basalt canyon of echoing spellfire scars",
                    "Hilltop cairn used for secret vow exchanges",
                    "Ancient battlefield plain blooming with silver grass",
                ],
                "Coastal & Underwater": [
                    "Black lake shoreline beneath ghostly boathouse lamps",
                    "Merperson coral court under a moonlit tide",
                    "Sea cave archive accessed through a breathing door",
                    "Storm harbor for smuggling charmed cargo crates",
                    "Cliffside owlery above crashing winter surf",
                    "Sunken chapel of bioluminescent runes",
                    "Kelp maze patrolled by enchanted chain markers",
                    "Pebble beach where portkeys wash ashore",
                    "Lighthouse ward beacon overlooking dark currents",
                    "Ice-rimmed dock where magical ferries moor",
                ],
            },
            "Liminal": {
                "Transit & Thresholds": [
                    "Platform Nine and Three-Quarters in pre-dawn fog",
                    "Shifting corridor of rotating classroom doors",
                    "Mirror hall that opens onto alternate common rooms",
                    "Triwizard portkey chamber lined with warning runes",
                    "Stairwell loop where footsteps arrive before bodies",
                    "Secret passage checkpoint run by house-elf sentries",
                    "Floo crossroads between London and northern keeps",
                    "Border gate between Ministry jurisdiction and school wards",
                    "Rail carriage frozen between two historical eras",
                    "Vault antechamber where locks respond to true names",
                ],
                "Temporal & Cosmic": [
                    "Time-turner observatory with overlapping sunrises",
                    "Prophecy dome where glass orbs orbit a black dais",
                    "Astral classroom with constellations mapped onto desks",
                    "Memory shoreline where pensieve tides roll in",
                    "Eclipse courtyard lit by silver-blue fire",
                    "Clock tower interior with thirteen synchronized faces",
                    "Archive tunnel where past conversations echo forward",
                    "Liminal station between afterlife and return",
                    "Comet-lit rooftop where patronuses migrate",
                    "Hourglass chamber shedding metal sand",
                ],
                "Ritual & Spectacle": [
                    "Reopened Yule Ball hall with protective ward chandeliers",
                    "Postwar graduation court beneath floating lantern scripts",
                    "Inter-house truce feast in a ruined cloister",
                    "Midnight duel exhibition ringed by oath candles",
                    "Masked winter carnival in Hogsmeade backstreets",
                    "Spellcraft symposium staged in a collapsed greenhouse",
                    "Auror swearing-in ceremony before a memorial wall",
                    "Wizarding wedding reception under anti-hex canopies",
                    "Fundraiser gala for curse victims in a manor atrium",
                    "House cup ceremony with rebuilt moving trophies",
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
        label="Wizarding Fanon Seeds",
        short="EE",
        weight_field="easter_eggs",
        template="""
### {n}. The Hidden Whisper (Wizarding Fanon Seed)
**Fanon Seed:** {content}
*Instruction: Integrate this seed as a subtle but legible detail or subplot. Keep it secondary to the main image beat, like a clue for readers who know fanon lore.*
""".strip(),
        tree={
            "Wizarding World Fanon": {
                "Postwar Hogwarts": {
                    "Narrative": [
                        "Eighth-year reconstruction turning rival dorms into forced peace experiments",
                        "Castle corridors becoming memorial routes where portraits debate survivor guilt",
                        "Student-led reforms replacing punitive house rivalries with uneasy alliances",
                        "Hogwarts kitchens becoming a labor-rights forum shared by elves and students",
                        "A rebuilt Great Hall hosting reconciliation rituals under repaired constellations",
                    ],
                    "Motifs": [
                        "Cracked stained-glass house crests repaired with gold seams",
                        "A scorched tapestry edge embroidered over with new names",
                        "Confiscated prank mirrors stacked beside a healing shrine",
                        "Prefect badges traded like ceasefire tokens",
                        "A timetable parchment that rewrites itself after curfew",
                        "Teacups charmed to project tiny patronus sparks",
                    ],
                },
                "Marauders Echoes": {
                    "Narrative": [
                        "First-war secrets resurfacing through abandoned map routes and hidden passages",
                        "A time-slip where modern students overhear unfinished Marauders arguments",
                        "Animagus loyalty pacts treated as sacred inheritance among friends",
                        "Order safehouse memories colliding with school-day nostalgia",
                        "Regulus-style defection reframed as a myth of quiet resistance",
                    ],
                    "Motifs": [
                        "Ink footprints appearing and vanishing across moonlit floorboards",
                        "A dog tag, stag antler, and wolf medallion tied with one ribbon",
                        "An old map corner burned around a single forbidden corridor",
                        "Graffiti initials hidden under fresh varnish on a classroom desk",
                        "A silver-green locket reflected in a puddle of potion water",
                        "Paper cranes folded from outdated detention records",
                    ],
                },
                "Slytherin Politics": {
                    "Narrative": [
                        "Pure-blood etiquette weaponized as courtroom theater after the war",
                        "Slytherin students building covert mutual-aid networks beneath public neutrality",
                        "Strategic betrothal rumors masking underground resistance logistics",
                        "A redemption arc negotiated through contracts, debts, and careful public optics",
                        "House rivalry replaced by coalition politics in the school corridors",
                    ],
                    "Motifs": [
                        "A serpent signet ring split and soldered back together",
                        "Ledger books with names crossed out in emerald ink",
                        "Black silk gloves dusted with silver potion residue",
                        "An heirloom cane engraved with warding runes",
                        "Green wax seals stamped over older family crests",
                        "A courtroom fan painted with serpents and lilies",
                    ],
                },
                "Ministry & Unspeakables": {
                    "Narrative": [
                        "Unspeakables cataloging forbidden prophecies that alter when observed",
                        "Auror bureaucracy clashing with vigilante justice in cursed-object cases",
                        "Departmental rivalries inside a Ministry trying to rebrand as humane",
                        "Memory evidence becoming politically edited before public trials",
                        "A black-market network selling salvaged relics from sealed battle sites",
                    ],
                    "Motifs": [
                        "Hall of Prophecy shards humming in velvet evidence boxes",
                        "A ministry pass that changes department seal every hour",
                        "Clock-hands harvested from broken time-turners",
                        "Runic filing cabinets chained shut with dragonhide straps",
                        "Teal curse-smoke trapped inside blown-glass phials",
                        "A visitor badge stamped with the word WITNESS",
                    ],
                },
                "Time-Travel Fix-It": {
                    "Narrative": [
                        "A fix-it timeline unraveling as each rescue causes a different loss",
                        "Two versions of the same student silently coordinating across looping days",
                        "A forbidden attempt to prevent a death by editing one memory at a time",
                        "Temporal paradoxes treated as emotional debts rather than math errors",
                        "Future letters delivered to past selves through bewitched archive drawers",
                    ],
                    "Motifs": [
                        "A cracked hourglass necklace bleeding silver sand",
                        "Overlapping shadows of the same figure in one stairwell",
                        "Class notes written in two handwritings on one page",
                        "A pocket watch with twelve and thirteen both marked",
                        "Thread-and-pin timeline map stretched across a dormitory wall",
                        "A time-turner chain knotted like a wedding ring",
                    ],
                },
                "Romance & Found Family": {
                    "Narrative": [
                        "Enemies-to-allies romance unfolding through shared detention and war recovery",
                        "A found-family kitchen scene replacing bloodline obligation with chosen care",
                        "Secret correspondence between rival houses sustaining a fragile truce",
                        "Healer and investigator partnership balancing tenderness with suspicion",
                        "Postwar cohabitation turning old enemies into reluctant guardians",
                    ],
                    "Motifs": [
                        "Tea tins labeled with initials from different houses",
                        "A half-knit scarf striped in clashing house colors",
                        "Pressed herbs tucked inside unsent apology letters",
                        "Two wands resting crossed over a medical chart",
                        "A shared umbrella warded against ash and rain",
                        "Charmed photo frames where people swap places nightly",
                    ],
                },
                "Magical Creatures & Bloodlines": {
                    "Narrative": [
                        "Creature inheritance laws exposing prejudice hidden inside polite society",
                        "A werewolf support circle operating behind a reputable clinic",
                        "Veela, goblin, and human diplomacy negotiated through marriage contracts",
                        "Old blood curses reframed as inherited trauma and ritual care",
                        "Dragon sanctuary workers smuggling eggs away from trophy collectors",
                    ],
                    "Motifs": [
                        "Moon-chart pins arranged around a cracked porcelain cup",
                        "Phoenix ash mixed into healing salve",
                        "Goblin-forged chains repurposed as wedding bracelets",
                        "A feather quill that molts iridescent sparks",
                        "Dragon scale mail stitched into a school satchel",
                        "A family tree chart with species symbols replacing surnames",
                    ],
                },
                "Alternative Schools & AUs": {
                    "Narrative": [
                        "Triwizard diplomacy recast as espionage between student delegations",
                        "Durmstrang transfer students importing harsher dueling etiquette",
                        "Beauxbatons alumni network steering postwar politics through charm",
                        "No-Chosen-One AU where collective resistance replaces prophecy heroism",
                        "A magical university era where old school rivalries harden into ideology",
                    ],
                    "Motifs": [
                        "Frost-bitten dueling gloves stitched with foreign runes",
                        "A travel trunk covered in layered school crests",
                        "Triwizard ticket stubs pinned beside strategy notes",
                        "A spellbook margin annotated in three languages",
                        "Ceremonial masks from an international wizarding summit",
                        "Railway luggage tags from shifting platform numbers",
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
        if key == "ar":
            singular = len(items) == 1
            ar_grammar = {
                "plural_suffix": "" if singular else "s",
                "anchor_subject": (
                    "This is the protagonist" if singular else "These are the protagonists"
                ),
                "anchor_object": "this archetype" if singular else "these archetypes",
                "anchor_possessive": "their",
                "interaction_clause": (
                    ", including how they choose, hesitate, desire, protect, betray, or transform the world around them."
                    if singular
                    else ", and, most importantly, how their choices and emotions collide with each other."
                ),
                "social_clause": (
                    "Let the social element emerge through this archetype's relationships with other beings, objects, or forces."
                    if singular
                    else "Let the social element drive the emotional core through alliances, conflict, care, jealousy, devotion, or negotiation."
                ),
                "non_human_clause": (
                    "Anthropomorphize by giving this archetype clear intent, felt emotion, and consequential decisions."
                    if singular
                    else "Anthropomorphize by giving each archetype clear intent, felt emotion, and consequential decisions."
                ),
            }
            parts.append(
                defn.template.format(
                    n=section_n,
                    content=content_str,
                    **ar_grammar,
                ).strip()
            )
        else:
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
