import random

# --- THE INFINITE MATRIX v3.0 ---

archetypes = [
    "AR-01 The Weaver", "AR-02 The Architect", "AR-03 The Gardener", "AR-04 The Alchemist", "AR-05 The Cartographer",
    "AR-06 The Clockmaker", "AR-07 The Scientist", "AR-08 The Inventor", "AR-09 The Artisan", "AR-10 The Chef",
    "AR-11 The Monarch", "AR-12 The Guardian", "AR-13 The Vizier", "AR-14 The Shah", "AR-15 The Mentor",
    "AR-16 The Oracle", "AR-17 The Ferryman", "AR-18 The Librarian", "AR-19 The Therapist", "AR-20 The Elder",
    "AR-21 The Traveler", "AR-22 The Dancer", "AR-23 The Fool", "AR-24 The Trickster", "AR-25 The Explorer",
    "AR-26 The Dreamer", "AR-27 The Musician", "AR-28 The Athlete", "AR-29 The Ninja", "AR-30 The Storyteller",
    "AR-31 The Lovers", "AR-32 The Parent", "AR-33 The Child", "AR-34 The Friend", "AR-35 The Host",
    "AR-36 The Celebrant", "AR-37 The Beloved", "AR-38 The Twins", "AR-39 The Healer", "AR-40 The Matchmaker",
    "AR-41 The Hermit", "AR-42 The Shadow", "AR-43 The Prisoner", "AR-44 The Widow", "AR-45 The Vessel",
    "AR-46 The Phoenix", "AR-47 The Avatar", "AR-48 The Idol", "AR-49 The Giant", "AR-50 The Swarm",
    "AR-51 The Beast", "AR-52 The Mirror", "AR-53 The Rationalist", "AR-54 The Romantist", "AR-55 The Virgin"
]

concepts = [
    "CN-01 Bloom / Growth", "CN-02 Transformation / Metamorphosis", "CN-03 Origin / Genesis", "CN-04 Resilience / Strength", "CN-05 Healing / Recovery",
    "CN-06 Discovery / Eureka", "CN-07 Flight / Liberation", "CN-08 Fusion / Union", "CN-09 Friendship / Bond", "CN-10 Belonging / Community",
    "CN-11 Tenderness / Care", "CN-12 Sensuality / Passion", "CN-13 Intimacy / Closeness", "CN-14 Generosity / Gift", "CN-15 Celebration / Festivity",
    "CN-16 Play / Joy", "CN-17 Humor / Laughter", "CN-18 Triumph / Victory", "CN-19 Abundance / Harvest", "CN-20 Gratitude / Thanksgiving",
    "CN-21 Wonder / Curiosity", "CN-22 Anchor / Safety", "CN-23 Shelter / Home", "CN-24 Balance / Symmetry", "CN-25 Comfort / Warmth",
    "CN-26 Clarity / Epiphany", "CN-27 Resonance / Echo", "CN-28 Gravity / Weight", "CN-29 Velocity / Motion", "CN-30 Ritual / Cycle",
    "CN-31 Entropy", "CN-32 Silence / Pause", "CN-33 Hunger / Desire", "CN-34 Threshold / Doorway", "CN-35 Labyrinth / Complexity",
    "CN-36 Illusion / Mask", "CN-37 Mystery / Void", "CN-38 Sacrifice / Exchange", "CN-39 Forbidden / Taboo", "CN-40 Abandonment / Desolation",
    "CN-41 Grotesque / Uncanny", "CN-42 Memory / Nostalgia", "CN-43 Inheritance / Legacy", "CN-44 Innocence / Purity", "CN-45 Forgiveness / Grace"
]

surreal_logic = [
    "SL-01 Scale Inversion", "SL-02 Material Transmutation", "SL-03 Gravity Reversal", "SL-04 Object Personification", "SL-05 Literal Metaphor",
    "SL-06 Portal Displacement", "SL-07 Anatomical Impossibility", "SL-08 Flora/Fauna Fusion", "SL-09 Architecture/Nature Fusion", "SL-10 Celestial Descent",
    "SL-11 Fluid Solidity", "SL-12 Solid Liquidity", "SL-13 Infinite Recursion", "SL-14 Time Collapse", "SL-15 Invisible Presence",
    "SL-16 Displacement", "SL-17 Gigantism", "SL-18 Containment", "SL-19 Sensory Synesthesia", "SL-20 Shadow Autonomy",
    "SL-21 Sky Replacement", "SL-22 Fragmentation", "SL-23 Levitation", "SL-24 Mechanical Nature", "SL-25 Soft Sculpture",
    "SL-26 Inside-Out", "SL-27 Duplication", "SL-28 Facelessness", "SL-29 Dream Logic", "SL-30 Weather Containment",
    "SL-31 Edible Architecture", "SL-32 Musical Materialization", "SL-33 Emotional Weather", "SL-34 Memory Projection", "SL-35 Toy Transmutation"
]

textures = [
    "TX-01 Stained Glass & Magma", "TX-02 Velvet & Ash", "TX-03 Gold Leaf & Circuitry", "TX-04 Floral Chintz & Bone", "TX-05 Watercolors & Ink",
    "TX-06 Porcelain & Cracks", "TX-07 Neon & Concrete", "TX-08 Silk & Smoke", "TX-09 Constellations & Void", "TX-10 Marble & Moss",
    "TX-11 Origami & Paper", "TX-12 Feathers & Tar", "TX-13 Gemstones & Rust", "TX-14 Lace & Steel", "TX-15 Fire & Ice",
    "TX-16 Woodgrain & Chrome", "TX-17 Clouds & Maps", "TX-18 Sand & Mirrors", "TX-19 Coral & Pearl", "TX-20 Oil Paint & Pixels",
    "TX-21 Leather & Amber", "TX-22 Obsidian & Lightning", "TX-23 Tapestry & Thorns", "TX-24 Mercury & Moonlight", "TX-25 Patina & Copper",
    "TX-26 Persian Tilework & Lapis Lazuli", "TX-27 Calligraphy & Saffron", "TX-28 Honey & Sunlight", "TX-29 Wildflower Linen & Denim",
    "TX-30 Carnival Glass & Confetti", "TX-31 Beeswax & Parchment", "TX-32 Terracotta & Olive Wood"
]

scatter = [
    "SC-01 Floating Keys & Locks", "SC-02 Unraveling Ribbons", "SC-03 Broken Clock Gears", "SC-04 Falling Playing Cards", "SC-05 Shattered Glass Shards",
    "SC-06 Ancient Books / Pages", "SC-07 Ladders to Nowhere", "SC-08 Empty Frames", "SC-09 Chess Pieces", "SC-10 Strings / Marionette Lines",
    "SC-11 Eyes / Watching Orbs", "SC-12 Scattered Coins / Tokens", "SC-13 Dripping Candle Wax", "SC-14 Tiny Origami Birds", "SC-15 Drifting Lanterns",
    "SC-16 Floating Islands / Rocks", "SC-17 Tangled Vines / Roots", "SC-18 Bubbles / Orbs", "SC-19 Falling Leaves / Petals", "SC-20 Tiny Stars / Moons",
    "SC-21 Migrating Butterflies", "SC-22 Floating Feathers", "SC-23 Spiraling Staircases", "SC-24 Scattered Pomegranate Seeds", "SC-25 Drifting Rose Petals & Nightingales",
    "SC-26 Musical Notes", "SC-27 Confetti & Streamers", "SC-28 Fireflies & Glowworms", "SC-29 Iridescent Soap Bubbles", "SC-30 Scattered Wildflowers",
    "SC-31 Floating Balloons", "SC-32 Paper Airplanes", "SC-33 Ripe Fruit & Berries", "SC-34 Dancing Silhouettes", "SC-35 Sparklers & Firework Trails",
    "SC-36 Songbirds in Flight", "SC-37 Scattered Love Letters / Postcards", "SC-38 Spilled Wine / Overflowing Goblets",
    # Expanded Scatter Pool (SC-39+): extra motifs for richer backgrounds and more variety
    "SC-39 Loose Pearls & Broken Necklaces", "SC-40 Perfume Bottles & Atomized Mist", "SC-41 Feather Quills & Ink Pots",
    "SC-42 Wax Seals / Stamps / Signet Rings", "SC-43 Porcelain Shards & Hairline Cracks", "SC-44 Sewing Needles & Thread Spools",
    "SC-45 Tiny Bells / Chimes / Anklets", "SC-46 Marbles / Glass Beads / Prism Drops", "SC-47 Birdcages (Open, Empty, Drifting)",
    "SC-48 Masks on Hooks / Mask Fragments", "SC-49 Mirrors with Missing Reflections", "SC-50 Chalk Diagrams & Summoning Circles",
    "SC-51 Domino Tiles / Dice / Game Tokens", "SC-52 Theater Tickets / Torn Programs", "SC-53 Stray Earrings / Hairpins / Combs",
    "SC-54 Lace Gloves / Silk Stockings (Abandoned)", "SC-55 Ribbon-Wrapped Gifts / Unopened Boxes", "SC-56 Vials / Elixirs / Tiny Flasks",
    "SC-57 Seashells / Conch Horns", "SC-58 Compass Needles / Sextants / Astrolabes", "SC-59 Pressed Flowers in Pages",
    "SC-60 Candle Snuffers / Matchsticks / Sparks", "SC-61 Origami Boats / Paper Ships", "SC-62 Broken Violin Strings / Instrument Parts",
    "SC-63 Floating Umbrellas / Parasols", "SC-64 Fallen Crowns / Tiara Pieces", "SC-65 Salt Crystals / Sugar Dust",
    "SC-66 Handprints / Palm Lines (Appearing on Surfaces)", "SC-67 Tiny Doorways in Tilework", "SC-68 Ripped Fabric Swatches / Patchwork Scraps",
    "SC-69 Moss-Lit Mushrooms / Bioluminescent Fungi", "SC-70 Errant Map Pins / Red Thread Routes", "SC-71 Tiny Skeleton Keys (Like Jewelry)",
    "SC-72 Floating Teacups & Saucers", "SC-73 Spilled Honey / Syrup Trails", "SC-74 Butterfly Pins / Brooches",
    "SC-75 Bath Beads / Soap Foam / Steam Pearls", "SC-76 Paper Crowns / Party Hats", "SC-77 Snowglobes / Mini Dioramas",
    "SC-78 Falling Calendars / Loose Date Pages"
]

emotions_light = [
    "EM-01 Euphoria (Blinding Joy)", "EM-02 Serenity (Deep Calm)", "EM-03 Vitality (Explosive Life)", "EM-04 Whimsy (Playful Absurdity)",
    "EM-05 Relief (Weight Lifted)", "EM-06 Wonder (Childlike Discovery)", "EM-07 Triumph (Victorious Elation)", "EM-08 Tenderness (Gentle Love)",
    "EM-09 Mischief (Gleeful Trouble)", "EM-10 Contentment (Perfect Stillness)", "EM-11 Gratitude (Overflowing Thanks)", "EM-12 Ecstasy (Transcendent Bliss)"
]

emotions_other = [
    "EM-13 Melancholy (Beautiful Grief)", "EM-14 Dread (Creeping Unease)", "EM-15 Longing (Aching Distance)", "EM-16 Nostalgia (Warm Sadness)",
    "EM-17 Awe (Cosmic Scale)", "EM-18 Intimacy (Quiet Closeness)", "EM-19 Determination (Stoic Strength)", "EM-20 Reverence (Sacred Silence)",
    "EM-21 Defiance (Rebellious Fire)", "EM-22 Courage (Fearless Advance)", "EM-23 Pride (Earned Glory)", "EM-24 Compassion (Healing Warmth)"
]

symbols_celebration = [
    "SY-68 The Wedding Canopy", "SY-69 The Feast Table", "SY-70 The Lantern Festival", "SY-71 The Maypole", "SY-72 The Rainbow Bridge / Bifrost",
    "SY-73 The Hearth Fire", "SY-74 The Love Letter", "SY-75 The Cradle", "SY-76 The Victory Wreath", "SY-77 The Wishing Well",
    "SY-78 The Flying Kite", "SY-79 The Music Box", "SY-80 The Friendship Bracelet", "SY-81 The First Blossom", "SY-82 The Lighthouse",
    "SY-83 The Shared Cup", "SY-84 The Open Hand", "SY-85 The Sunrise Gate"
]

symbols_other = [
    "SY-01 The Ouroboros", "SY-02 The Philosopher's Stone", "SY-03 The Caduceus", "SY-04 The Athanor", "SY-05 The Three Primes",
    "SY-06 The Sphinx", "SY-07 The Minotaur", "SY-08 The Cerberus", "SY-09 The Pegasus", "SY-10 The Hydra",
    "SY-11 The Basilisk", "SY-12 The Chimera", "SY-13 Pandora's Box", "SY-14 The Trojan Horse", "SY-15 Ariadne's Thread",
    "SY-16 The Golden Fleece", "SY-17 The Sword in the Stone", "SY-18 The Holy Grail", "SY-19 The Tower of Babel", "SY-20 The Ship of Theseus",
    "SY-21 Icarus's Wings", "SY-22 Achilles' Heel", "SY-23 The Glass Slipper", "SY-24 The Spinning Wheel", "SY-25 The Magic Mirror",
    "SY-26 The Enchanted Rose", "SY-27 The Red Cloak", "SY-28 The Poisoned Apple", "SY-29 The Breadcrumb Trail", "SY-30 The Beanstalk",
    "SY-31 The Pied Piper's Flute", "SY-32 The Golden Egg", "SY-33 The Skull", "SY-34 The Hourglass", "SY-35 The Half-Burned Candle",
    "SY-36 The Wilting Bouquet", "SY-37 The Death's-Head Moth", "SY-38 The Broken Crown", "SY-39 The Stopped Clock", "SY-40 The Tree of Life",
    "SY-41 The All-Seeing Eye", "SY-42 The Mandala", "SY-43 The Lotus", "SY-44 The Ankh", "SY-45 The Halo",
    "SY-46 Jacob's Ladder", "SY-47 The Burning Bush", "SY-48 The Dharma Wheel", "SY-49 The Broken Column", "SY-50 The Cornucopia",
    "SY-51 The Lyre of Orpheus", "SY-52 The Masquerade Mask", "SY-53 The Comedy/Tragedy Masks", "SY-54 The Scales of Justice", "SY-55 The Heraldic Lion",
    "SY-56 The Compass Rose", "SY-57 The Eclipse", "SY-58 The Tidal Wave", "SY-59 The Aurora Borealis", "SY-60 The Lightning-Struck Tree",
    "SY-61 The Simurgh", "SY-62 The Faravahar", "SY-63 The Eternal Flame of Atar", "SY-64 The Cypress of Kashmar", "SY-65 Zahhak's Shoulder Serpents",
    "SY-66 The Derafsh Kaviani", "SY-67 The Gate of All Nations"
]

# --- SELECTION LOGIC ---

# 1. Standard Categories: Pick 10 unique
ar_pick = random.sample(archetypes, 10)
cn_pick = random.sample(concepts, 10)
sl_pick = random.sample(surreal_logic, 10)
tx_pick = random.sample(textures, 10)
# Scatter: Pick 20 unique so each prompt gets TWO scatter motifs (SC-A + SC-B)
sc_pick = random.sample(scatter, 20)

# 2. Emotions: Enforce AT LEAST 4 Joyful/Light
em_joyful = random.sample(emotions_light, 4)
# Combine remainder of Light + All Others for the remaining 6 slots
em_pool_remaining = [e for e in emotions_light if e not in em_joyful] + emotions_other
em_rest = random.sample(em_pool_remaining, 6)
em_pick = em_joyful + em_rest
random.shuffle(em_pick)

# 3. Symbols: Enforce AT LEAST 2 Celebration/Fellowship
sy_celeb = random.sample(symbols_celebration, 2)
# Combine remainder of Celebration + All Others for the remaining 8 slots
sy_pool_remaining = [s for s in symbols_celebration if s not in sy_celeb] + symbols_other
sy_rest = random.sample(sy_pool_remaining, 8)
sy_pick = sy_celeb + sy_rest
random.shuffle(sy_pick)

# OUTPUT
for i in range(10):
    sc_a = sc_pick[i * 2]
    sc_b = sc_pick[i * 2 + 1]
    print(f"{ar_pick[i]} + {cn_pick[i]} + {sl_pick[i]} + {tx_pick[i]} + {sc_a} + {sc_b} + {em_pick[i]} + {sy_pick[i]}")
