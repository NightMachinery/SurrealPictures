#!/usr/bin/env python3
from __future__ import annotations

import argparse
import math
import random
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Tuple


# ============================================================
# THE INFINITE MATRIX v5.0
# - Hierarchical ordered dictionaries per category
# - Auto-generated short codes (AR-01, EE-137, ...)
# - Per-category optional enable/disable
# - Per-category float sampling (probabilistic fractional picks)
# - Generic bucket-aware multi-pick diversification
# ============================================================


# NOTE:
# Bucket names may use explicit copyrighted franchise names for INTERNAL CUE INDEXING.
# Final prompts should reference them obliquely, without explicit IP naming.


CATEGORY_DEFINITIONS: Dict[str, Dict[str, Any]] = {
    "ar": {
        "label": "Archetypes",
        "short": "AR",
        "tree": {
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
                ],
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
    },
    "cn": {
        "label": "Concepts",
        "short": "CN",
        "tree": {
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
                ],
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
    },
    "sl": {
        "label": "Surreal Logic",
        "short": "SL",
        "tree": {
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
    },
    "tx": {
        "label": "Textures",
        "short": "TX",
        "tree": {
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
    },
    "sc": {
        "label": "Scatter",
        "short": "SC",
        "tree": {
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
                "Moss-Lit Mushrooms / Bioluminescent Fungi",
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
    },
    "em": {
        "label": "Emotions",
        "short": "EM",
        "tree": {
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
    },
    "sy": {
        "label": "Symbols",
        "short": "SY",
        "tree": {
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
                ],
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
                ],
            },
        },
    },
    "se": {
        "label": "Settings",
        "short": "SE",
        "tree": {
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
    },
    "cp": {
        "label": "Composition / POV",
        "short": "CP",
        "tree": {
            "Camera": {
                "Angles": [
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
            "Framing": {
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
            "Temporal": {
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
            "Graphic": {
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
            "Portraiture": {
                "Staging": [
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
        },
    },
    "ee": {
        "label": "Easter Eggs",
        "short": "EE",
        "tree": {
            "Disney Animation Franchises": {
                "Snow White and the Seven Dwarfs": [
                    "Poisoned-apple omen and mirrored vanity anxiety",
                    "Whistling woodland labor and jewel-mine domesticity",
                    "Glass-coffin stillness in a flowered forest clearing",
                    "7 dwarfs",
                ],
                "Pinocchio": [
                    "Puppet-on-strings struggling toward real identity",
                    # "Conscience guide figure interrupting reckless choices",
                    "Carnival temptation that turns children into beasts",
                    "Nose grows when lies"
                ],
                # "Fantasia": [
                #     "Orchestral magic making household tools rebel",
                #     "Abstract dance of seasons and elemental sprites",
                #     "Night-mountain demonic silhouette over ritual bells",
                # ],
                # "Dumbo": [
                #     "Circus outsider transformed by unexpected flight",
                #     "Mother-child tenderness framed by steel cage bars",
                #     "Dreamlike parade imagery drifting into surreal intoxication",
                # ],
                # "Bambi": [
                #     "Forest coming-of-age shadowed by sudden loss",
                #     "Seasonal transformation from spring innocence to winter trial",
                #     "Regal antlered silhouette against burning woodland horizon",
                # ],
                "Cinderella": [
                    "Midnight deadline tension with vanishing glamour",
                    "Domestic servitude transformed by handmade couture magic",
                    "Single lost slipper as destiny key",
                ],
                "Alice in Wonderland (Disney)": [
                    "Tea ritual trapped in absurd looping etiquette",
                    "Scale shifts triggered by food and potion symbols",
                    "Card-suit court justice with arbitrary punishments",
                ],
                "Peter Pan": [
                    "Second-star flight over moonlit rooftops",
                    "Eternal-childhood island with pirate threat",
                    "Shadow-sewing and nursery-window threshold motifs",
                ],
                "Lady and the Tramp": [
                    "Alley-versus-parlor class contrast in romance",
                    "Shared meal scene turning into emotional pact",
                    # "Dog-catcher menace crossing cozy domestic boundaries",
                ],
                "Sleeping Beauty": [
                    "Spindle curse and century-long suspended time",
                    "Three guardian fairies navigating hidden upbringing",
                    "Thorn-wall fortress sealing a sleeping court",
                ],
                # "101 Dalmatians": [
                #     "Fashion predator antagonism tied to spotted coats",
                #     "Urban rescue route coordinated through barking network",
                #     "Soot-smudged disguise escaping aristocratic threat",
                # ],
                "The Jungle Book": [
                    "Law-of-the-jungle mentorship and belonging conflict",
                    "Hypnotic serpent persuasion and identity drift",
                    "River swing rhythm with carefree friend-energy",
                ],
                # "The Aristocats": [
                #     "High-society heirs displaced into street survival",
                #     "Jazz-cat bohemia inside a chaotic attic session",
                #     "Inheritance plot resolved through chosen family",
                # ],
                "Robin Hood": [
                    "Forest-outlaw redistribution under tyrant taxation",
                    "Archery tournament as disguise-and-heist stage",
                    "Animal-feudal court parody with moral rebellion",
                ],
                "The Rescuers": [
                    "Tiny-agent rescue mission in oversized hostile terrain",
                    "Bottle-message clue trail across swamp ruins",
                    "Orphan courage under eccentric villain pressure",
                ],
                "The Fox and the Hound": [
                    "Childhood bond broken by inherited social roles",
                    # "Hunt-training montage against personal loyalty",
                    # "Wildfire crisis forcing moral reconciliation",
                ],
                # "The Great Mouse Detective": [
                #     "Miniature Victorian detective duel in clocktower mechanics",
                #     "Rat underworld conspiracy with theatrical villain flair",
                #     "Forensic clue trail across toy-scale London",
                # ],
                "The Little Mermaid": [
                    "Voice-for-legs contract with hidden cost",
                    "Shipwreck romance across species and kingdoms",
                    "Undersea court rebellion against protective father rule",
                ],
                "Beauty and the Beast": [
                    "Cursed manor where furniture serves as staff",
                    "Rose-petal countdown measuring redemption window",
                    "Village prejudice versus transformative intimacy",
                ],
                "Aladdin": [
                    "Street thief discovering cosmic wish leverage",
                    "Identity performance between commoner and royalty",
                    "Magic-lamp trickster ally changing geopolitical stakes",
                ],
                "The Lion King": [
                    "Exiled heir haunted by paternal sky-vision",
                    "Cycle-of-life kingship duty versus avoidance",
                    "Savanna usurpation ending in firelit confrontation",
                ],
                "Pocahontas": [
                    "Wind-guided spiritual intuition amid colonial conflict",
                    "Two-world diplomacy through forbidden closeness",
                    "Forest colors shifting with emotional weather",
                ],
                "The Hunchback of Notre Dame": [
                    "Bell-tower isolation versus festival crowd hunger",
                    "Sanctuary law clashing with authoritarian obsession",
                    "Gargoyle counsel balancing fear and courage",
                ],
                "Hercules": [
                    "Mythic labor trials converted into public spectacle",
                    "Fame economy distorting heroic purpose",
                    "Underworld bargain threatening true love",
                ],
                "Mulan": [
                    "Gender-disguise duty in militarized empire",
                    "Ancestral expectations versus self-forged honor",
                    "Avalanche tactic turning small figure into strategic legend",
                ],
                "Tarzan": [
                    "Identity split between jungle kin and human origin",
                    "Vine-swinging locomotion as emotional language",
                    "Colonial expedition disrupting found-family ecosystem",
                ],
                "The Emperor's New Groove": [
                    "Royal arrogance collapsed into animal vulnerability",
                    "Road-journey redemption through odd-couple alliance",
                    "Palace intrigue framed as slapstick survival",
                ],
                "Atlantis: The Lost Empire": [
                    "Scholar-led expedition into submerged ancient power",
                    "Linguistic puzzle solving unlocking dormant machines",
                    "Imperial extraction greed versus cultural protection",
                ],
                "Lilo & Stitch": [
                    "Chaotic alien adoption as grief-healing process",
                    "Found-family oath overriding biological norms",
                    "Surf-coast domesticity interrupted by space bounty threat",
                ],
                "Treasure Planet": [
                    "Age-of-sail map quest translated into cosmic routes",
                    "Rebellious youth mentored by morally gray pirate",
                    "Mechanical planet-core collapse in final reckoning",
                ],
                "Brother Bear": [
                    "Human transformed into hunted creature perspective",
                    "Brotherhood guilt resolved through shared pilgrimage",
                    "Aurora-spirit guidance across wilderness thresholds",
                ],
                "The Princess and the Frog": [
                    "Ambition and love negotiated through enchanted transformation",
                    "Jazz-age city mysticism and shadow bargains",
                    "Bayou ritual route toward self-redefinition",
                ],
                "Tangled": [
                    "Impossibly long luminous hair as tool and prison",
                    "Tower confinement broken by charismatic outlaw partner",
                    "Lantern festival as memory-triggering revelation",
                ],
                "Frozen": [
                    "Sister bond strained by isolating power",
                    "Ice architecture erupting from emotional repression",
                    "False-romance betrayal versus sacrificial familial love",
                ],
                "Big Hero 6": [
                    "Inflatable healer-tech companion offsetting grief",
                    "Student inventors assembling vigilante team in neon city",
                    "Portal experiment tragedy driving revenge arc",
                ],
                "Zootopia": [
                    "Predator-prey bias politics in hyper-diverse metropolis",
                    "Buddy-cop mismatch uncovering systemic conspiracy",
                    "Urban biomes stacked as social satire",
                ],
                # "Moana": [
                #     "Ocean selecting reluctant voyager for restoration quest",
                #     "Ancestral wayfinding returning after cultural suppression",
                #     "Living-island deity conflict resolved through recognition",
                # ],
                "Ralph Breaks the Internet": [
                    "Arcade character identity crisis in algorithmic ecosystem",
                    "Friendship strain under divergent life goals",
                    "Platform-world satire using avatar multiplicity",
                ],
                "Encanto": [
                    "Sentient family house reflecting intergenerational stress",
                    "Gift hierarchy pressure and invisible labor resentment",
                    "Casita fracture repaired through emotional truth",
                ],
                "Raya and the Last Dragon": [
                    "Fractured nations rebuilding trust through shared relic",
                    "Lone warrior partnership with chaotic trickster dragon",
                    "Stone-petrification plague as metaphor for social distrust",
                ],
                # "Wish": [
                #     "Constellation wish-energy confronting authoritarian wish-hoarding",
                #     "Young idealist versus charismatic ruler cult",
                #     "Star companion catalyzing collective civic awakening",
                # ],
            },
            "Pixar Franchises": {
                "Toy Story": [
                    "Secret toy society activated when humans leave",
                    "Loyalty conflict between old favorite and flashy newcomer",
                    "Existential fear of replacement in childhood ecosystem",
                ],
                "A Bug's Life": [
                    "Tiny agrarian underclass resisting seasonal extortion",
                    "Mistaken-identity recruitment of chaotic performers",
                    "Miniature engineering flipping predator-prey power",
                ],
                "Toy Story 2": [
                    "Collector's display immortality versus lived belonging",
                    "Rescue heist through urban toy underworld",
                    "Abandonment memory reframing identity choices",
                ],
                "Monsters, Inc.": [
                    "Fear-harvesting industry converted to laughter economy",
                    "Door-network logistics spanning child-bedroom dimensions",
                    "Unlikely child-monster bond exposing corporate corruption",
                ],
                "Finding Nemo": [
                    "Anxious parent crossing vast ocean biomes",
                    "Memory-impaired guide reframing control into trust",
                    "Captivity-escape plot inside ornamental aquarium",
                ],
                "The Incredibles": [
                    "Superhero family balancing domestic friction and duty",
                    "Mid-century futurist villainy built on resentment",
                    "Secret-identity bureaucracy collapsing under old grudges",
                ],
                "Cars": [
                    "Speed celebrity humbled by forgotten roadside community",
                    "Route nostalgia versus sponsorship modernity",
                    "Self-worth shift from trophies to relationships",
                ],
                "Ratatouille": [
                    "Underdog culinary genius hidden beneath social taboo",
                    "Critic culture transformed by remembered childhood taste",
                    "Kitchen hierarchy destabilized by secret collaboration",
                ],
                "WALL-E": [
                    "Lonely cleanup robot preserving relics of humanity",
                    "Consumer-space cruise numbing collective agency",
                    "Plant-life discovery rebooting civilizational purpose",
                ],
                "Up": [
                    "House lifted by balloons as grief pilgrimage vehicle",
                    "Ageing recluse mentoring eager wilderness novice",
                    "Explorer-idol disillusionment in remote lost-world",
                ],
                "Toy Story 3": [
                    "Daycare regime masking authoritarian toy politics",
                    "Aging-out anxiety and farewell to childhood owner",
                    "Incinerator solidarity as loyalty crucible",
                ],
                "Cars 2": [
                    "Racing tour entangled in espionage conspiracy",
                    "Comic sidekick reframed as accidental agent",
                    "Alternative fuel politics folded into action set pieces",
                ],
                "Brave": [
                    "Fate-defying princess rejecting arranged destiny",
                    "Maternal conflict transformed through animal metamorphosis",
                    "Clan ritual competition as political pressure cooker",
                ],
                "Monsters University": [
                    "Campus rivalry evolving into strategic friendship",
                    "Institutional sorting exposing nontraditional strengths",
                    "Scare-sport training montage with absurd obstacles",
                ],
                "Inside Out": [
                    "Personified emotions governing memory architecture",
                    "Core-memory collapse threatening identity coherence",
                    "Growing complexity from mono-emotion to mixed feeling",
                ],
                # "The Good Dinosaur": [
                #     "Prehistoric role-reversal between human and dinosaur",
                #     "Fear-facing journey through elemental landscapes",
                #     "Family separation repaired through chosen courage",
                # ],
                "Finding Dory": [
                    "Memory-fragment quest toward lost family",
                    "Marine rescue facility as obstacle labyrinth",
                    "Found-support network enabling neurodivergent agency",
                ],
                "Cars 3": [
                    "Veteran champion confronting generational replacement",
                    "Mentor shift from ego performance to legacy transfer",
                    "Rust-belt training arc restoring creative drive",
                ],
                "Coco": [
                    "Marigold bridge between living and ancestral metropolis",
                    "Music ban as inherited trauma mechanism",
                    "Memory erasure as second death stakes",
                ],
                "Incredibles 2": [
                    "Public-trust campaign for outlawed heroes",
                    "Role inversion in domestic and frontline labor",
                    "Screenslaver control motif critiquing media dependency",
                ],
                "Toy Story 4": [
                    "Homemade toy sentience and purpose confusion",
                    "Carnival reunion reopening past attachment choices",
                    "Independence versus lifelong service dilemma",
                ],
                "Onward": [
                    "Suburban fantasy quest for partial-parent reunion",
                    "Modernized magic world drained of wonder",
                    "Sibling bond reframed through sacrificial choice",
                ],
                "Soul": [
                    "Pre-life mentorship bureaucracy and purpose anxiety",
                    "Body-swap introspection between artist and unborn soul",
                    "Flow-state transcendence redefining meaning of life",
                ],
                "Luca": [
                    "Seaside friendship hiding aquatic true selves",
                    "Small-town prejudice challenged by youthful alliance",
                    "Vespa-dream motif as escape from inherited fear",
                ],
                "Turning Red": [
                    "Puberty metaphor through sudden giant-creature form",
                    "Mother-daughter boundary negotiation under cultural expectation",
                    "Concert ritual replacing suppression with integration",
                ],
                "Lightyear": [
                    "Time-dilation mission producing generational consequences",
                    "Space-ranger idealism confronting recursive identity threat",
                    "Team cohesion built from mismatched misfits",
                ],
                "Elemental": [
                    "Inter-element romance crossing social segregation",
                    "Family business duty colliding with self-actualization",
                    "City infrastructure built on material incompatibility",
                ],
                "Inside Out 2": [
                    "New adolescent emotions crowding old control systems",
                    "Anxiety takeover restructuring internal command center",
                    "Identity-formation under competitive social pressure",
                ],
            },
            "DreamWorks & Aardman Franchises": {
                "Shrek": [
                    "Swamp recluse romance within satirical fairy-tale politics",
                    "Quest parody where sidekick sincerity wins",
                    "Outsider identity reclaimed against beauty norms",
                ],
                "How to Train Your Dragon": [
                    "Dragon-rider empathy dismantling inherited war culture",
                    "Aerial bond between inventor-teen and wounded beast",
                    "Village modernization negotiated through trust",
                ],
                "Kung Fu Panda": [
                    "Unlikely chosen hero mastering legacy scroll",
                    "Mentor disappointment transformed into acceptance",
                    "Food, discipline, and destiny braided into combat ritual",
                ],
                "Madagascar": [
                    "Urban zoo identity crisis in wild ecology",
                    "Friend group dynamics strained by instinct and comfort",
                    "Performance culture adapting into survival strategy",
                ],
                "The Prince of Egypt": [
                    "River-origin prophecy splitting adopted brotherhood",
                    "Liberation theology framed through monumental plagues",
                    "Desert pilgrimage toward covenantal law",
                ],
                "Puss in Boots": [
                    "Flamboyant duelist charisma masking mortality fear",
                    "Fairy-tale artifact heist with shifting alliances",
                    "Legend economy and reputation wagering",
                ],
                "Megamind": [
                    "Performer-villain discovering responsibility after victory",
                    "Identity built on opposition collapsing into vacancy",
                    "Public narrative rewriting hero-villain binaries",
                ],
                "Chicken Run": [
                    "Farmyard prison-break engineered by collective cunning",
                    "Improvised aviation dream as liberation symbol",
                    "Factory threat escalating urgency of escape",
                ],
                "Wallace & Gromit": [
                    "Overengineered domestic inventions causing precise chaos",
                    "Silent companion intelligence correcting human optimism",
                    "British village mystery solved through tactile contraptions",
                ],
                "Coraline (2009, Laika)": [
                    "Button-eyed duplicate family using affection as trap",
                    "Button-eyed doubles masking predatory affection",
                    "Needle-and-thread motifs tied to control and identity",
                    "Small courage defeating ornate predatory domesticity",
                    "Tiny hidden door opening to seductive parallel home",
                    "Domestic boredom transformed into uncanny survival trial",
                ],
            },
            "Wizarding World": {
                "Harry Potter": [
                    "Moving staircase topology that re-routes social destiny",
                    "Floating-candle banquet hall under enchanted ceiling weather",
                    "Sorting-hat identity assignment under peer scrutiny",
                    "House-point economy driving school-wide rivalry",
                    "Marauder-map footprints revealing hidden nocturnal traffic",
                    "Portrait corridors functioning as surveillance network",
                    "Time-turner loop where consequence meets causality",
                    "Pensieve memory extraction and selective narrative truth",
                    "Horcrux-style soul-fragment relic hidden in ordinary object",
                    "Room of Requirement adapting architecture to secret need",
                    "Patronus projection as weaponized memory of care",
                    "Forbidden forest trial with predatory sentient shadows",
                    "Triwizard-like arena tasks mixing water, air, and maze",
                    "Quidditch flight choreography under roaring house banners",
                    "Invisibility-cloak privilege versus ethical trespass",
                    "Polyjuice disguise destabilizing trust and intimacy",
                    "Howler-style public shaming delivered by enchanted letter",
                    "Owl-post logistics and wax-sealed correspondence rituals",
                    "Diagon-like market street packed with dangerous curios",
                    "Knockturn-adjacent black-market relic traffic",
                    "Wand-lore compatibility and allegiance reversal",
                    "Ancient blood ward protection tied to family sacrifice",
                    "Mirror of desire exposing hidden longing",
                    "Gauntlet of protective enchantments guarding secret chamber",
                    "Basilisk-catacomb dread beneath elite institution",
                    "Dark-mark sky omen triggering collective panic",
                    "Order-style clandestine resistance in bureaucratic regime",
                    "Prophecy archive where futures are fragile glass",
                    "Occlumency vs mind-intrusion psychological duel",
                    "Half-blood notebook shortcut to dangerous excellence",
                    "Master-of-death myth embedded across three artifacts",
                    "Shattered wand repaired by elder relic intervention",
                    "Battle of school grounds with statues joining combat",
                    "King's Cross liminal station between death and return",
                    "Postwar epilogue platform scene echoing cyclical inheritance",
                ],
            },
            "Studio Ghibli Franchises": {
                "Nausicaa of the Valley of the Wind": [
                    "Toxic jungle ecology and pacifist mediation",
                    "Wind-rider heroine navigating giant insect diplomacy",
                ],
                "Castle in the Sky": [
                    "Floating ruin-city powered by ancient crystal tech",
                    "Sky pirates and militarists racing for lost power",
                ],
                "My Neighbor Totoro": [
                    "Rural childhood wonder anchored by forest guardian",
                    "Bus-stop rain ritual with spirit visitation",
                ],
                "Grave of the Fireflies": [
                    "War aftermath seen through sibling survival lens",
                    "Transient light of fireflies against hunger and loss",
                ],
                "Kiki's Delivery Service": [
                    "Young witch independence learned through daily labor",
                    "Flight confidence tied to emotional self-belief",
                ],
                "Only Yesterday": [
                    "Adult memory collage intercut with childhood scenes",
                    "Rural harvest rhythms reframing urban identity",
                ],
                "Porco Rosso": [
                    "Cynical ace pilot with transformed face and honor code",
                    "Adriatic sky-duel romance under political unrest",
                ],
                "Pom Poko": [
                    "Shape-shifting tanuki resistance to urban expansion",
                    "Folkloric protest staged as surreal performance",
                ],
                "Whisper of the Heart": [
                    "Teen creative awakening through handmade storytelling",
                    "Antique-shop serendipity and crafted aspiration",
                ],
                "Princess Mononoke": [
                    "Forest gods versus ironworks modernity conflict",
                    "Cursed wound driving reluctant mediation between worlds",
                ],
                "My Neighbors the Yamadas": [
                    "Domestic comedy vignettes in stylized watercolor minimalism",
                    "Everyday family chaos elevated to mythic micro-drama",
                ],
                "Spirited Away": [
                    "Bathhouse labor under spirit-world contract",
                    "Name-theft control and identity recovery journey",
                ],
                "The Cat Returns": [
                    "Human girl courted into absurd feline kingdom",
                    "Baron-figure rescue through elegant whimsy",
                ],
                "Howl's Moving Castle": [
                    "Walking fortress powered by unstable fire demon pact",
                    "Curse-aging transformation and anti-war undertones",
                ],
                "Tales from Earthsea": [
                    "Balance-of-life-and-death metaphysical crisis",
                    "Young mage confronting shadow-self fragmentation",
                ],
                "Ponyo": [
                    "Ocean-child metamorphosis driven by innocent devotion",
                    "Flooded coastal town under mythic tidal imbalance",
                ],
                "Arrietty": [
                    "Miniature borrowers surviving beneath human domestic giants",
                    "Secret-scale friendship across impossible size difference",
                ],
                "From Up on Poppy Hill": [
                    "School-club restoration as memory and activism",
                    "Harbor-era nostalgia confronting buried family history",
                ],
                "The Wind Rises": [
                    "Aviation dream colliding with wartime machinery ethics",
                    "Romance shadowed by illness and historical inevitability",
                ],
                "The Tale of the Princess Kaguya": [
                    "Moon-origin child pressured by aristocratic expectations",
                    "Brushstroke impermanence amplifying emotional immediacy",
                ],
                "When Marnie Was There": [
                    "Lonely youth bonding across temporal/psychic ambiguity",
                    "Marsh-house memory mystery resolving inherited grief",
                ],
                "The Red Turtle": [
                    "Wordless island survival transformed by mythic encounter",
                    "Cycle-of-life acceptance through elemental allegory",
                ],
                "Earwig and the Witch": [
                    "Stubborn orphan negotiating household occult hierarchy",
                    "Music and spellcraft entangled in domestic power struggle",
                ],
                "The Boy and the Heron": [
                    "Tower portal into war-grief dreamworld ecology",
                    "Shapeshifting guide bird provoking moral inheritance choices",
                ],
            },
            "Series": {
                "The Office": [
                    "Deadpan workplace ritual with awkward social micro-politics",
                    "Mock-documentary gaze exposing petty power games",
                    "Cringe comedy rhythm puncturing mundane bureaucracy",
                ],
                "Friends": [
                    "Urban found-family comfort in recurring social hub",
                    "Romantic crosscurrents inside long-term friend group",
                    "Apartment-centered life stage transitions and identity drift",
                ],
                "Avatar: The Last Airbender": [
                    "Elemental martial choreography shaping terrain directly",
                    "Chosen-avatar burden versus childlike spontaneity",
                    "Traveling found-family resisting imperial expansion",
                    "Spirit-world thresholds and mask-driven identity conflicts",
                ],
            },
            "Gaming Franchises": {
                "Civilization": [
                    "Turn-based empire growth from village to megacity",
                    "Tech-tree decisions rewriting military and cultural destiny",
                    "Wonders race driving geopolitical tension and prestige",
                ],
                "StarCraft": [
                    "Three-species asymmetry in total-war resource chess",
                    "Hive evolution versus mechanized industry versus psionic empire",
                    "Drop-pod raids and base-defense pressure under fog-of-war",
                ],
                "Slay the Spire": [
                    "Roguelike ascension through branching elite encounters",
                    "Deck-building choices compounding into fragile strategy",
                    "Relic synergies and boss-path risk management tension",
                ],
            },
            "Superhero": {
                "Batman": [
                    "Noir vigilante silhouette over gothic megacity skyline",
                    "Masked detective using fear theatrics against theatrical villains",
                    "Rooftop gargoyle surveillance and trauma-forged discipline",
                    "Bat-signal civic icon toggling hope and dread",
                    "High-tech cave arsenal beneath aristocratic facade",
                ],
            },
            "Classic / Literary Franchises": {
                "Alice in Wonderland (Literary Franchise)": [
                    "Logic games and riddles undermining fixed reality",
                    "Tea-party etiquette spiraling into absurd procedure",
                    "Queenly justice ritual based on arbitrary decree",
                ],
                "Arabian Nights": [
                    "Story-within-story frame delaying death through narration",
                    "Genie bargain dynamics around power and unintended outcomes",
                    "Bazaar labyrinth of thieves, viziers, and hidden chambers",
                    "Sultanate court intrigue threaded through caravan myth",
                    "Flying carpet, brass astrolabe, and moonlit minaret iconography",
                ],
            },
        },
    },
}


CATEGORY_ORDER = ["ar", "cn", "sl", "tx", "sc", "em", "sy", "se", "cp", "ee"]


@dataclass(frozen=True)
class CategoryCatalog:
    key: str
    label: str
    short: str
    all_items: List[str]
    buckets: Dict[str, List[str]]


@dataclass
class MatrixConfig:
    prompts_per_batch: int = 10
    seed: Optional[int] = None
    separator: str = " + "

    archetypes: float = 1.2
    concepts: float = 1.0
    surreal_logic: float = 1.2
    textures: float = 1.0
    scatter: float = 1.3
    emotions: float = 1.0
    symbols: float = 1.0
    settings: float = 0.8
    composition_pov: float = 0.5
    easter_eggs: float = 0.33

    min_light_emotions: int = 4
    min_celebration_symbols: int = 2
    list_buckets: bool = False


CATEGORY_FIELD_MAP: Dict[str, str] = {
    "ar": "archetypes",
    "cn": "concepts",
    "sl": "surreal_logic",
    "tx": "textures",
    "sc": "scatter",
    "em": "emotions",
    "sy": "symbols",
    "se": "settings",
    "cp": "composition_pov",
    "ee": "easter_eggs",
}


def _iter_leaf_buckets(
    node: Any, path: Tuple[str, ...] = ()
) -> Sequence[Tuple[str, List[str]]]:
    if isinstance(node, list):
        return [("/".join(path), list(node))]
    if isinstance(node, dict):
        out: List[Tuple[str, List[str]]] = []
        for key, child in node.items():
            out.extend(_iter_leaf_buckets(child, path + (str(key),)))
        return out
    raise TypeError(
        f"Unsupported tree node type at {'/'.join(path) or '<root>'}: {type(node)!r}"
    )


def _build_catalog_for_category(
    key: str, definition: Dict[str, Any]
) -> CategoryCatalog:
    short = str(definition["short"]).upper()
    label = str(definition["label"])
    tree = definition["tree"]

    leaf_buckets = _iter_leaf_buckets(tree)
    raw_entries: List[Tuple[str, str]] = []
    for bucket_path, names in leaf_buckets:
        for name in names:
            raw_entries.append((bucket_path, name))

    if not raw_entries:
        return CategoryCatalog(
            key=key, label=label, short=short, all_items=[], buckets={}
        )

    width = max(2, len(str(len(raw_entries))))
    coded_all: List[str] = []
    coded_buckets: Dict[str, List[str]] = {}

    for i, (bucket_path, name) in enumerate(raw_entries, start=1):
        code = f"{short}-{i:0{width}d}"
        item_text = f"{code} {name}"
        coded_all.append(item_text)
        coded_buckets.setdefault(bucket_path, []).append(item_text)

    return CategoryCatalog(
        key=key, label=label, short=short, all_items=coded_all, buckets=coded_buckets
    )


def build_catalogs() -> Dict[str, CategoryCatalog]:
    catalogs: Dict[str, CategoryCatalog] = {}
    for key in CATEGORY_ORDER:
        catalogs[key] = _build_catalog_for_category(key, CATEGORY_DEFINITIONS[key])
    return catalogs


def print_buckets() -> None:
    catalogs = build_catalogs()
    for key in CATEGORY_ORDER:
        c = catalogs[key]
        print(f"[{key}] {c.label} ({c.short})")
        for bucket_path in c.buckets:
            print(f"  - {bucket_path} [{len(c.buckets[bucket_path])}]")
            print()


def _per_prompt_counts(value: float, prompts: int, rng: random.Random) -> List[int]:
    if value <= 0:
        return [0] * prompts
    base = int(math.floor(value))
    frac = value - base
    counts = [base] * prompts
    if frac > 0:
        for i in range(prompts):
            if rng.random() < frac:
                counts[i] += 1
    return counts


def _allocate_mandatory_buckets(
    counts: List[int], mandatory_counts: Dict[str, int], rng: random.Random
) -> Dict[int, List[str]]:
    allocation = {i: [] for i in range(len(counts))}
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


def _pick_item(items: Sequence[str], used: set[str], rng: random.Random) -> str:
    unique_items = [x for x in items if x not in used]
    if unique_items:
        return rng.choice(unique_items)
    return rng.choice(list(items))


def _sample_items_for_prompt(
    buckets: Dict[str, List[str]],
    item_count: int,
    forced_bucket_paths: Sequence[str],
    rng: random.Random,
) -> List[str]:
    if item_count <= 0:
        return []
    if not buckets:
        return []

    selected: List[str] = []
    used_items: set[str] = set()
    used_bucket_paths: set[str] = set()
    used_top_groups: set[str] = set()

    # 1) Forced paths first
    for path in forced_bucket_paths:
        items = buckets.get(path)
        if not items:
            continue
        item = _pick_item(items, used_items, rng)
        selected.append(item)
        used_items.add(item)
        used_bucket_paths.add(path)
        used_top_groups.add(path.split("/", 1)[0] if "/" in path else path)
        if len(selected) >= item_count:
            return selected

    bucket_paths = list(buckets.keys())
    rng.shuffle(bucket_paths)

    # 2) Diversify by top-level group
    for path in bucket_paths:
        if len(selected) >= item_count:
            break
        top = path.split("/", 1)[0] if "/" in path else path
        if top in used_top_groups:
            continue
        item = _pick_item(buckets[path], used_items, rng)
        selected.append(item)
        used_items.add(item)
        used_bucket_paths.add(path)
        used_top_groups.add(top)

    # 3) Diversify by distinct bucket paths
    for path in bucket_paths:
        if len(selected) >= item_count:
            break
        if path in used_bucket_paths:
            continue
        item = _pick_item(buckets[path], used_items, rng)
        selected.append(item)
        used_items.add(item)
        used_bucket_paths.add(path)

    # 4) Fill remainder from any path
    while len(selected) < item_count:
        path = rng.choice(bucket_paths)
        item = _pick_item(buckets[path], used_items, rng)
        selected.append(item)
        used_items.add(item)

    return selected


def _mandatory_constraints(cfg: MatrixConfig) -> Dict[str, Dict[str, int]]:
    return {
        "em": {"Light/Joyful": cfg.min_light_emotions},
        "sy": {"Celebration/Fellowship": cfg.min_celebration_symbols},
    }


def generate_matrix_lines(cfg: MatrixConfig) -> List[str]:
    if cfg.prompts_per_batch <= 0:
        raise ValueError("prompts_per_batch must be > 0")

    catalogs = build_catalogs()
    rng = random.Random(cfg.seed)

    per_prompt_counts: Dict[str, List[int]] = {}
    forced_alloc: Dict[str, Dict[int, List[str]]] = {}
    constraints = _mandatory_constraints(cfg)

    for key in CATEGORY_ORDER:
        count_field = CATEGORY_FIELD_MAP[key]
        count_value = float(getattr(cfg, count_field))

        if count_value <= 0:
            per_prompt_counts[key] = [0] * cfg.prompts_per_batch
            forced_alloc[key] = {i: [] for i in range(cfg.prompts_per_batch)}
            continue

        counts = _per_prompt_counts(count_value, cfg.prompts_per_batch, rng)
        per_prompt_counts[key] = counts

        category_constraints = constraints.get(key, {})
        if category_constraints and sum(counts) > 0:
            capacity = sum(counts)
            clamped: Dict[str, int] = {}
            for bucket_path, n_required in category_constraints.items():
                take = min(max(0, int(n_required)), capacity)
                if take > 0:
                    clamped[bucket_path] = take
                    capacity -= take
                    forced_alloc[key] = _allocate_mandatory_buckets(
                        counts, clamped, rng
                    )
        else:
            forced_alloc[key] = {i: [] for i in range(cfg.prompts_per_batch)}

    lines: List[str] = []
    for prompt_i in range(cfg.prompts_per_batch):
        parts: List[str] = []
        for key in CATEGORY_ORDER:
            item_count = per_prompt_counts[key][prompt_i]
            if item_count <= 0:
                continue
            catalog = catalogs[key]
            picks = _sample_items_for_prompt(
                catalog.buckets,
                item_count,
                forced_alloc[key][prompt_i],
                rng,
            )
            parts.extend(picks)

        lines.append(cfg.separator.join(parts))

    return lines


def _add_category_args(parser: argparse.ArgumentParser) -> None:
    defaults = MatrixConfig()
    parser.add_argument(
        "--ar", "--archetypes", dest="archetypes", type=float, default=defaults.archetypes
    )
    parser.add_argument("--cn", "--concepts", dest="concepts", type=float, default=defaults.concepts)
    parser.add_argument(
        "--sl", "--surreal-logic", dest="surreal_logic", type=float, default=defaults.surreal_logic
    )
    parser.add_argument("--tx", "--textures", dest="textures", type=float, default=defaults.textures)
    parser.add_argument("--sc", "--scatter", dest="scatter", type=float, default=defaults.scatter)
    parser.add_argument("--em", "--emotions", dest="emotions", type=float, default=defaults.emotions)
    parser.add_argument("--sy", "--symbols", dest="symbols", type=float, default=defaults.symbols)
    parser.add_argument("--se", "--settings", dest="settings", type=float, default=defaults.settings)
    parser.add_argument(
        "--cp", "--composition-pov", dest="composition_pov", type=float, default=defaults.composition_pov
    )
    parser.add_argument(
        "--ee", "--easter-eggs", dest="easter_eggs", type=float, default=defaults.easter_eggs
    )


def parse_args() -> MatrixConfig:
    defaults = MatrixConfig()
    parser = argparse.ArgumentParser(
        description="Generate configurable surreal matrix blueprints (hierarchical + auto-coded).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--prompts",
        "--prompts-per-batch",
        dest="prompts_per_batch",
        type=int,
        default=defaults.prompts_per_batch,
    )
    parser.add_argument("--seed", type=int, default=defaults.seed)
    parser.add_argument("--separator", type=str, default=defaults.separator)
    parser.add_argument(
        "--min-em-light", dest="min_light_emotions", type=int, default=defaults.min_light_emotions
    )
    parser.add_argument(
        "--min-sy-celebration", dest="min_celebration_symbols", type=int, default=defaults.min_celebration_symbols
    )
    parser.add_argument(
        "--list-buckets",
        dest="list_buckets",
        action="store_true",
        help="List category bucket paths and exit",
    )

    _add_category_args(parser)
    args = parser.parse_args()

    return MatrixConfig(
        prompts_per_batch=args.prompts_per_batch,
        seed=args.seed,
        separator=args.separator,
        archetypes=args.archetypes,
        concepts=args.concepts,
        surreal_logic=args.surreal_logic,
        textures=args.textures,
        scatter=args.scatter,
        emotions=args.emotions,
        symbols=args.symbols,
        settings=args.settings,
        composition_pov=args.composition_pov,
        easter_eggs=args.easter_eggs,
        min_light_emotions=args.min_light_emotions,
        min_celebration_symbols=args.min_celebration_symbols,
        list_buckets=args.list_buckets,
    )


def main() -> None:
    cfg = parse_args()
    if cfg.list_buckets:
        print_buckets()
        return
    lines = generate_matrix_lines(cfg)
    for line in lines:
        print(line)


if __name__ == "__main__":
    main()
