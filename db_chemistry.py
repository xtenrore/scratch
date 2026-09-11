# Complete Chemistry Database for Chemistry Simulator Scratch 3.0
# Total: 129 Species (19 Elements, 88 Molecules/Radicals, 22 Ions)

SPECIES = [
    # --- 19 Base Elements (IDs 1-19) ---
    {
        "id": 1, "symbol": "H", "name": "Hydrogen", "formula": "H", "charge": 0,
        "type": "Element", "color": "#E2E8F0", "border": "#94A3B8", "z": 1,
        "atoms": "H: 1", "desc": "Lightest and most abundant element in the universe."
    },
    {
        "id": 2, "symbol": "He", "name": "Helium", "formula": "He", "charge": 0,
        "type": "Noble Gas", "color": "#67E8F9", "border": "#0891B2", "z": 2,
        "atoms": "He: 1", "desc": "Inert noble gas created by cosmic nuclear fusion."
    },
    {
        "id": 3, "symbol": "Li", "name": "Lithium", "formula": "Li", "charge": 0,
        "type": "Alkali Metal", "color": "#FB7185", "border": "#E11D48", "z": 3,
        "atoms": "Li: 1", "desc": "Lightest alkali metal, highly reactive solid."
    },
    {
        "id": 4, "symbol": "Be", "name": "Beryllium", "formula": "Be", "charge": 0,
        "type": "Alkaline Earth", "color": "#34D399", "border": "#059669", "z": 4,
        "atoms": "Be: 1", "desc": "Lightweight, rigid alkaline earth metal."
    },
    {
        "id": 5, "symbol": "C", "name": "Carbon", "formula": "C", "charge": 0,
        "type": "Nonmetal", "color": "#475569", "border": "#0F172A", "z": 6,
        "atoms": "C: 1", "desc": "The chemical foundation for all organic life."
    },
    {
        "id": 6, "symbol": "N", "name": "Nitrogen", "formula": "N", "charge": 0,
        "type": "Nonmetal", "color": "#38BDF8", "border": "#0284C7", "z": 7,
        "atoms": "N: 1", "desc": "Diatomic component forming 78% of Earth atmosphere."
    },
    {
        "id": 7, "symbol": "O", "name": "Oxygen", "formula": "O", "charge": 0,
        "type": "Reactive Nonmetal", "color": "#EF4444", "border": "#B91C1C", "z": 8,
        "atoms": "O: 1", "desc": "Vital oxidant participating in aerobic combustion."
    },
    {
        "id": 8, "symbol": "F", "name": "Fluorine", "formula": "F", "charge": 0,
        "type": "Halogen", "color": "#A3E635", "border": "#65A30D", "z": 9,
        "atoms": "F: 1", "desc": "Most electronegative and reactive halogen."
    },
    {
        "id": 9, "symbol": "Ne", "name": "Neon", "formula": "Ne", "charge": 0,
        "type": "Noble Gas", "color": "#FB923C", "border": "#C2410C", "z": 10,
        "atoms": "Ne: 1", "desc": "Colorless noble gas that glows reddish-orange in high voltage."
    },
    {
        "id": 10, "symbol": "Na", "name": "Sodium", "formula": "Na", "charge": 0,
        "type": "Alkali Metal", "color": "#A855F7", "border": "#7E22CE", "z": 11,
        "atoms": "Na: 1", "desc": "Soft alkali metal that reacts vigorously with water."
    },
    {
        "id": 11, "symbol": "Si", "name": "Silicon", "formula": "Si", "charge": 0,
        "type": "Metalloid", "color": "#F59E0B", "border": "#B45309", "z": 14,
        "atoms": "Si: 1", "desc": "Tetravalent semiconductor forming quartz and silicones."
    },
    {
        "id": 12, "symbol": "P", "name": "Phosphorus", "formula": "P", "charge": 0,
        "type": "Reactive Nonmetal", "color": "#F97316", "border": "#C2410C", "z": 15,
        "atoms": "P: 1", "desc": "Essential component of cellular DNA and ATP."
    },
    {
        "id": 13, "symbol": "S", "name": "Sulfur", "formula": "S", "charge": 0,
        "type": "Reactive Nonmetal", "color": "#FACC15", "border": "#CA8A04", "z": 16,
        "atoms": "S: 1", "desc": "Bright yellow multivalent nonmetal with brimstone aroma."
    },
    {
        "id": 14, "symbol": "Cl", "name": "Chlorine", "formula": "Cl", "charge": 0,
        "type": "Halogen", "color": "#22C55E", "border": "#15803D", "z": 17,
        "atoms": "Cl: 1", "desc": "Pale yellow-green halogen gas with strong oxidizing power."
    },
    {
        "id": 15, "symbol": "Ar", "name": "Argon", "formula": "Ar", "charge": 0,
        "type": "Noble Gas", "color": "#2DD4BF", "border": "#0F766E", "z": 18,
        "atoms": "Ar: 1", "desc": "Abundant noble gas widely used for inert vacuum shielding."
    },
    {
        "id": 16, "symbol": "K", "name": "Potassium", "formula": "K", "charge": 0,
        "type": "Alkali Metal", "color": "#C084FC", "border": "#9333EA", "z": 19,
        "atoms": "K: 1", "desc": "Silvery alkali metal crucial for biological ion gradients."
    },
    {
        "id": 17, "symbol": "Ca", "name": "Calcium", "formula": "Ca", "charge": 0,
        "type": "Alkaline Earth", "color": "#14B8A6", "border": "#0F766E", "z": 20,
        "atoms": "Ca: 1", "desc": "Reactive alkaline earth metal forming bone and limestone."
    },
    {
        "id": 18, "symbol": "Br", "name": "Bromine", "formula": "Br", "charge": 0,
        "type": "Halogen", "color": "#D97706", "border": "#92400E", "z": 35,
        "atoms": "Br: 1", "desc": "Reddish-brown fuming halogen liquid at room temperature."
    },
    {
        "id": 19, "symbol": "I", "name": "Iodine", "formula": "I", "charge": 0,
        "type": "Halogen", "color": "#8B5CF6", "border": "#5B21B6", "z": 53,
        "atoms": "I: 1", "desc": "Lustrous purple-black halogen solid that sublimes into violet vapor."
    },

    # --- 88 Molecules & Radicals (IDs 20-107) ---
    {"id": 20, "symbol": "H2", "name": "Molecular Hydrogen", "formula": "H2", "charge": 0, "type": "Diatomic Molecule", "color": "#E2E8F0", "border": "#94A3B8", "atoms": "H: 2", "desc": "Diatomic fuel gas forming primordial stars."},
    {"id": 21, "symbol": "H2O", "name": "Water", "formula": "H2O", "charge": 0, "type": "Molecular Compound", "color": "#38BDF8", "border": "#0284C7", "atoms": "H: 2, O: 1", "desc": "Polar universal solvent essential to all known biology."},
    {"id": 22, "symbol": "O2", "name": "Diatomic Oxygen", "formula": "O2", "charge": 0, "type": "Diatomic Molecule", "color": "#EF4444", "border": "#B91C1C", "atoms": "O: 2", "desc": "Essential gas powering cellular respiration."},
    {"id": 23, "symbol": "Li2", "name": "Dilithium", "formula": "Li2", "charge": 0, "type": "Diatomic Molecule", "color": "#FB7185", "border": "#E11D48", "atoms": "Li: 2", "desc": "Gas-phase homonuclear diatomic lithium molecule."},
    {"id": 24, "symbol": "Be2", "name": "Diberine", "formula": "Be2", "charge": 0, "type": "Diatomic Molecule", "color": "#34D399", "border": "#059669", "atoms": "Be: 2", "desc": "Weakly bound transient beryllium dimer."},
    {"id": 25, "symbol": "N2", "name": "Diatomic Nitrogen", "formula": "N2", "charge": 0, "type": "Diatomic Molecule", "color": "#38BDF8", "border": "#0284C7", "atoms": "N: 2", "desc": "Extremely inert gas bound by a strong triple bond."},
    {"id": 26, "symbol": "F2", "name": "Fluorine Gas", "formula": "F2", "charge": 0, "type": "Halogen Gas", "color": "#A3E635", "border": "#65A30D", "atoms": "F: 2", "desc": "Extremely toxic, highly reactive pale yellow gas."},
    {"id": 27, "symbol": "CN", "name": "Cyano Radical", "formula": "CN", "charge": 0, "type": "Radical", "color": "#64748B", "border": "#334155", "atoms": "C: 1, N: 1", "desc": "Interstellar radical with an unpaired electron."},
    {"id": 28, "symbol": "NH•", "name": "Imidogen Radical", "formula": "NH•", "charge": 0, "type": "Radical", "color": "#38BDF8", "border": "#0284C7", "atoms": "N: 1, H: 1", "desc": "Short-lived radical observed in stellar atmospheres."},
    {"id": 29, "symbol": "NO•", "name": "Nitric Oxide", "formula": "NO•", "charge": 0, "type": "Radical", "color": "#0284C7", "border": "#0369A1", "atoms": "N: 1, O: 1", "desc": "Free-radical signaling molecule in biology."},
    {"id": 30, "symbol": "HCl", "name": "Hydrogen Chloride", "formula": "HCl", "charge": 0, "type": "Strong Acid Gas", "color": "#22C55E", "border": "#15803D", "atoms": "H: 1, Cl: 1", "desc": "Corrosive gas that dissociates completely in water."},
    {"id": 31, "symbol": "Cl2", "name": "Chlorine Gas", "formula": "Cl2", "charge": 0, "type": "Halogen Gas", "color": "#22C55E", "border": "#15803D", "atoms": "Cl: 2", "desc": "Greenish-yellow disinfectant and strong oxidizer."},
    {"id": 32, "symbol": "NaCl", "name": "Sodium Chloride", "formula": "NaCl", "charge": 0, "type": "Ionic Salt", "color": "#A855F7", "border": "#7E22CE", "atoms": "Na: 1, Cl: 1", "desc": "Common table salt forming cubic ionic crystals."},
    {"id": 33, "symbol": "BeCl2", "name": "Beryllium Chloride", "formula": "BeCl2", "charge": 0, "type": "Inorganic Salt", "color": "#34D399", "border": "#059669", "atoms": "Be: 1, Cl: 2", "desc": "Linear electron-deficient beryllium halide."},
    {"id": 34, "symbol": "ClO2", "name": "Chlorine Dioxide", "formula": "ClO2", "charge": 0, "type": "Radical Oxide", "color": "#EAB308", "border": "#CA8A04", "atoms": "Cl: 1, O: 2", "desc": "Yellow-red paramagnetic gas used in water treatment."},
    {"id": 35, "symbol": "HOCl", "name": "Hypochlorous Acid", "formula": "HOCl", "charge": 0, "type": "Weak Acid", "color": "#86EFAC", "border": "#22C55E", "atoms": "H: 1, O: 1, Cl: 1", "desc": "Potent antimicrobial agent produced by neutrophils."},
    {"id": 36, "symbol": "Cl2O", "name": "Dichlorine Monoxide", "formula": "Cl2O", "charge": 0, "type": "Halogen Oxide", "color": "#84CC16", "border": "#4D7C0F", "atoms": "Cl: 2, O: 1", "desc": "Brownish-yellow explosive gas and strong oxidizer."},
    {"id": 37, "symbol": "KCl", "name": "Potassium Chloride", "formula": "KCl", "charge": 0, "type": "Ionic Salt", "color": "#C084FC", "border": "#9333EA", "atoms": "K: 1, Cl: 1", "desc": "Major mineral salt replenishing electrolyte balance."},
    {"id": 38, "symbol": "CaCl2", "name": "Calcium Chloride", "formula": "CaCl2", "charge": 0, "type": "Ionic Salt", "color": "#14B8A6", "border": "#0F766E", "atoms": "Ca: 1, Cl: 2", "desc": "Hygroscopic salt widely used for deicing roads."},
    {"id": 39, "symbol": "CO", "name": "Carbon Monoxide", "formula": "CO", "charge": 0, "type": "Toxic Gas", "color": "#64748B", "border": "#334155", "atoms": "C: 1, O: 1", "desc": "Colorless, odorless poisonous gas binding hemoglobin."},
    {"id": 40, "symbol": "CO2", "name": "Carbon Dioxide", "formula": "CO2", "charge": 0, "type": "Greenhouse Gas", "color": "#64748B", "border": "#1E293B", "atoms": "C: 1, O: 2", "desc": "Greenhouse gas consumed by plants during photosynthesis."},
    {"id": 41, "symbol": "CH•", "name": "Methylidyne Radical", "formula": "CH•", "charge": 0, "type": "Radical", "color": "#475569", "border": "#0F172A", "atoms": "C: 1, H: 1", "desc": "Interstellar hydrocarbon radical found in molecular clouds."},
    {"id": 42, "symbol": "CH2•", "name": "Methylene Radical", "formula": "CH2•", "charge": 0, "type": "Carbene Radical", "color": "#475569", "border": "#0F172A", "atoms": "C: 1, H: 2", "desc": "Highly reactive carbene intermediate."},
    {"id": 43, "symbol": "CH3•", "name": "Methyl Radical", "formula": "CH3•", "charge": 0, "type": "Organic Radical", "color": "#475569", "border": "#0F172A", "atoms": "C: 1, H: 3", "desc": "Planar organic radical driving radical chain reactions."},
    {"id": 44, "symbol": "CH4", "name": "Methane", "formula": "CH4", "charge": 0, "type": "Alkane Gas", "color": "#38BDF8", "border": "#0284C7", "atoms": "C: 1, H: 4", "desc": "Primary component of natural gas, tetrahedral alkane."},
    {"id": 45, "symbol": "C2H6", "name": "Ethane", "formula": "C2H6", "charge": 0, "type": "Alkane Gas", "color": "#38BDF8", "border": "#0284C7", "atoms": "C: 2, H: 6", "desc": "Two-carbon alkane gas isolated from petrochemicals."},
    {"id": 46, "symbol": "NH2•", "name": "Amino Radical", "formula": "NH2•", "charge": 0, "type": "Radical", "color": "#38BDF8", "border": "#0284C7", "atoms": "N: 1, H: 2", "desc": "Neutral form of amide ion, active in combustion flames."},
    {"id": 47, "symbol": "NH3", "name": "Ammonia", "formula": "NH3", "charge": 0, "type": "Alkaline Gas", "color": "#38BDF8", "border": "#0284C7", "atoms": "N: 1, H: 3", "desc": "Pungent trigonal pyramidal alkaline gas for fertilizers."},
    {"id": 48, "symbol": "HCN", "name": "Hydrogen Cyanide", "formula": "HCN", "charge": 0, "type": "Toxic Gas", "color": "#64748B", "border": "#334155", "atoms": "H: 1, C: 1, N: 1", "desc": "Volatile liquid smelling of bitter almonds, metabolic poison."},
    {"id": 49, "symbol": "Na2CO3", "name": "Sodium Carbonate", "formula": "Na2CO3", "charge": 0, "type": "Inorganic Salt", "color": "#A855F7", "border": "#7E22CE", "atoms": "Na: 2, C: 1, O: 3", "desc": "Washing soda used in glassmaking and water softening."},
    {"id": 50, "symbol": "H2CO", "name": "Formaldehyde", "formula": "H2CO", "charge": 0, "type": "Aldehyde Gas", "color": "#64748B", "border": "#334155", "atoms": "H: 2, C: 1, O: 1", "desc": "Simplest aldehyde, pungent preservative and chemical precursor."},
    {"id": 51, "symbol": "HCO•", "name": "Formyl Radical", "formula": "HCO•", "charge": 0, "type": "Radical", "color": "#64748B", "border": "#334155", "atoms": "H: 1, C: 1, O: 1", "desc": "Transient combustion radical created by photolysis of formaldehyde."},
    {"id": 52, "symbol": "C2H4", "name": "Ethylene", "formula": "C2H4", "charge": 0, "type": "Alkene Gas", "color": "#38BDF8", "border": "#0284C7", "atoms": "C: 2, H: 4", "desc": "Double-bonded alkene gas functioning as a plant ripening hormone."},
    {"id": 53, "symbol": "C2H2", "name": "Acetylene", "formula": "C2H2", "charge": 0, "type": "Alkyne Gas", "color": "#38BDF8", "border": "#0284C7", "atoms": "C: 2, H: 2", "desc": "Triple-bonded alkyne fuel burning at extreme flame temperatures."},
    {"id": 54, "symbol": "CH3CHO", "name": "Acetaldehyde", "formula": "CH3CHO", "charge": 0, "type": "Aldehyde", "color": "#38BDF8", "border": "#0284C7", "atoms": "C: 2, H: 4, O: 1", "desc": "Pungent fruity aldehyde formed during alcohol metabolism."},
    {"id": 55, "symbol": "CH3COOH", "name": "Acetic Acid", "formula": "CH3COOH", "charge": 0, "type": "Carboxylic Acid", "color": "#38BDF8", "border": "#0284C7", "atoms": "C: 2, H: 4, O: 2", "desc": "Key component of vinegar giving it characteristic sour taste."},
    {"id": 56, "symbol": "HS•", "name": "Thiohydroxy Radical", "formula": "HS•", "charge": 0, "type": "Radical", "color": "#FACC15", "border": "#CA8A04", "atoms": "S: 1, H: 1", "desc": "Sulfur analogue of hydroxyl radical in astrochemistry."},
    {"id": 57, "symbol": "H2S", "name": "Hydrogen Sulfide", "formula": "H2S", "charge": 0, "type": "Toxic Gas", "color": "#FACC15", "border": "#CA8A04", "atoms": "H: 2, S: 1", "desc": "Colorless chalcogenide gas smelling strongly of rotten eggs."},
    {"id": 58, "symbol": "SO2", "name": "Sulfur Dioxide", "formula": "SO2", "charge": 0, "type": "Sulfur Oxide", "color": "#FACC15", "border": "#CA8A04", "atoms": "S: 1, O: 2", "desc": "Pungent volcanic gas contributing to acid rain."},
    {"id": 59, "symbol": "SO3", "name": "Sulfur Trioxide", "formula": "SO3", "charge": 0, "type": "Sulfur Oxide", "color": "#FACC15", "border": "#CA8A04", "atoms": "S: 1, O: 3", "desc": "Precursor to sulfuric acid, fuming corrosive trioxide."},
    {"id": 60, "symbol": "H2SO4", "name": "Sulfuric Acid", "formula": "H2SO4", "charge": 0, "type": "Strong Acid", "color": "#FACC15", "border": "#CA8A04", "atoms": "H: 2, S: 1, O: 4", "desc": "Extremely strong industrial diprotic mineral acid."},
    {"id": 61, "symbol": "NaHSO4", "name": "Sodium Bisulfate", "formula": "NaHSO4", "charge": 0, "type": "Acid Salt", "color": "#A855F7", "border": "#7E22CE", "atoms": "Na: 1, H: 1, S: 1, O: 4", "desc": "Dry acid salt used to lower pH in water systems."},
    {"id": 62, "symbol": "KHSO4", "name": "Potassium Bisulfate", "formula": "KHSO4", "charge": 0, "type": "Acid Salt", "color": "#C084FC", "border": "#9333EA", "atoms": "K: 1, H: 1, S: 1, O: 4", "desc": "Potassium acid salt used in analytical chemistry fluxes."},
    {"id": 63, "symbol": "S2", "name": "Disulfur", "formula": "S2", "charge": 0, "type": "Diatomic Molecule", "color": "#FACC15", "border": "#CA8A04", "atoms": "S: 2", "desc": "Violet gas analogue of dioxygen existing at high temperatures."},
    {"id": 64, "symbol": "S3", "name": "Trisulfur", "formula": "S3", "charge": 0, "type": "Polyatomic Molecule", "color": "#FACC15", "border": "#CA8A04", "atoms": "S: 3", "desc": "Cherry-red allotrope of sulfur found in sulfur vapors."},
    {"id": 65, "symbol": "S4", "name": "Tetrasulfur", "formula": "S4", "charge": 0, "type": "Polyatomic Molecule", "color": "#FACC15", "border": "#CA8A04", "atoms": "S: 4", "desc": "Red allotrope of sulfur with open-chain configuration."},
    {"id": 66, "symbol": "N4", "name": "Tetranitrogen", "formula": "N4", "charge": 0, "type": "Polyatomic Molecule", "color": "#38BDF8", "border": "#0284C7", "atoms": "N: 4", "desc": "Polynitrogen allotrope synthesized under photochemical UV."},
    {"id": 67, "symbol": "S4N4", "name": "Tetrasulfur Tetranitride", "formula": "S4N4", "charge": 0, "type": "Inorganic Ring", "color": "#FACC15", "border": "#CA8A04", "atoms": "S: 4, N: 4", "desc": "Bright orange cage compound sensitive to shock."},
    {"id": 68, "symbol": "S2Cl2", "name": "Disulfur Dichloride", "formula": "S2Cl2", "charge": 0, "type": "Sulfur Halide", "color": "#EAB308", "border": "#CA8A04", "atoms": "S: 2, Cl: 2", "desc": "Golden-yellow liquid used for vulcanizing synthetic rubber."},
    {"id": 69, "symbol": "NH4Cl", "name": "Ammonium Chloride", "formula": "NH4Cl", "charge": 0, "type": "Ammonium Salt", "color": "#38BDF8", "border": "#0284C7", "atoms": "N: 1, H: 4, Cl: 1", "desc": "White crystalline salt subliming into ammonia and HCl vapors."},
    {"id": 70, "symbol": "SiO", "name": "Silicon Monoxide", "formula": "SiO", "charge": 0, "type": "Silicon Oxide", "color": "#F59E0B", "border": "#B45309", "atoms": "Si: 1, O: 1", "desc": "Brownish glass-like coating vaporized in stellar envelopes."},
    {"id": 71, "symbol": "SiO2", "name": "Silicon Dioxide", "formula": "SiO2", "charge": 0, "type": "Network Solid", "color": "#F59E0B", "border": "#B45309", "atoms": "Si: 1, O: 2", "desc": "Quartz crystals and major constituent of beach sand."},
    {"id": 72, "symbol": "Na2SiO3", "name": "Sodium Silicate", "formula": "Na2SiO3", "charge": 0, "type": "Silicate Salt", "color": "#A855F7", "border": "#7E22CE", "atoms": "Na: 2, Si: 1, O: 3", "desc": "Water glass adhesive and fireproofing inorganic polymer."},
    {"id": 73, "symbol": "SiH•", "name": "Silylidyne Radical", "formula": "SiH•", "charge": 0, "type": "Radical", "color": "#F59E0B", "border": "#B45309", "atoms": "Si: 1, H: 1", "desc": "Reactive silicon hydride radical detected in interstellar space."},
    {"id": 74, "symbol": "SiH2•", "name": "Silylene Radical", "formula": "SiH2•", "charge": 0, "type": "Radical", "color": "#F59E0B", "border": "#B45309", "atoms": "Si: 1, H: 2", "desc": "Divalent silicon intermediate analogous to methylene."},
    {"id": 75, "symbol": "SiH3•", "name": "Silyl Radical", "formula": "SiH3•", "charge": 0, "type": "Radical", "color": "#F59E0B", "border": "#B45309", "atoms": "Si: 1, H: 3", "desc": "Pyramidal radical precursor in semiconductor deposition."},
    {"id": 76, "symbol": "SiH4", "name": "Silane", "formula": "SiH4", "charge": 0, "type": "Pyrophoric Gas", "color": "#F59E0B", "border": "#B45309", "atoms": "Si: 1, H: 4", "desc": "Pyrophoric silicon gas spontaneously combusting in air."},
    {"id": 77, "symbol": "Si2H6", "name": "Disilane", "formula": "Si2H6", "charge": 0, "type": "Pyrophoric Gas", "color": "#F59E0B", "border": "#B45309", "atoms": "Si: 2, H: 6", "desc": "Silicon analogue of ethane used in precision microchip fabrication."},
    {"id": 78, "symbol": "K2SiO3", "name": "Potassium Silicate", "formula": "K2SiO3", "charge": 0, "type": "Silicate Salt", "color": "#C084FC", "border": "#9333EA", "atoms": "K: 2, Si: 1, O: 3", "desc": "Soluble mineral silicate delivering plant strengthening silica."},
    {"id": 79, "symbol": "P2", "name": "Diphosphorus", "formula": "P2", "charge": 0, "type": "Diatomic Molecule", "color": "#F97316", "border": "#C2410C", "atoms": "P: 2", "desc": "Triple-bonded gaseous phosphorus allotrope at high temperature."},
    {"id": 80, "symbol": "P4", "name": "White Phosphorus", "formula": "P4", "charge": 0, "type": "Polyatomic Molecule", "color": "#F97316", "border": "#C2410C", "atoms": "P: 4", "desc": "Tetrahedral white allotrope glowing with green chemiluminescence."},
    {"id": 81, "symbol": "PH•", "name": "Phosphinidyne Radical", "formula": "PH•", "charge": 0, "type": "Radical", "color": "#F97316", "border": "#C2410C", "atoms": "P: 1, H: 1", "desc": "Phosphorus hydride radical identified in cosmic circumstellar gas."},
    {"id": 82, "symbol": "PH2•", "name": "Phosphino Radical", "formula": "PH2•", "charge": 0, "type": "Radical", "color": "#F97316", "border": "#C2410C", "atoms": "P: 1, H: 2", "desc": "Free radical formed by photolysis of phosphine."},
    {"id": 83, "symbol": "PH3", "name": "Phosphine", "formula": "PH3", "charge": 0, "type": "Toxic Gas", "color": "#F97316", "border": "#C2410C", "atoms": "P: 1, H: 3", "desc": "Flammable fishy-smelling gas considered an atmospheric biosignature."},
    {"id": 84, "symbol": "P4O10", "name": "Phosphorus Pentoxide", "formula": "P4O10", "charge": 0, "type": "Acid Anhydride", "color": "#F97316", "border": "#C2410C", "atoms": "P: 4, O: 10", "desc": "Extraordinary dehydrating agent violently extracting water."},
    {"id": 85, "symbol": "H3PO4", "name": "Phosphoric Acid", "formula": "H3PO4", "charge": 0, "type": "Mineral Acid", "color": "#F97316", "border": "#C2410C", "atoms": "H: 3, P: 1, O: 4", "desc": "Triprotic acid used in rust removal and carbonated cola drinks."},
    {"id": 86, "symbol": "PN", "name": "Phosphorus Mononitride", "formula": "PN", "charge": 0, "type": "Diatomic Molecule", "color": "#F97316", "border": "#C2410C", "atoms": "P: 1, N: 1", "desc": "High-temperature inorganic diatomic observed in interstellar clouds."},
    {"id": 87, "symbol": "Na3PO4", "name": "Trisodium Phosphate", "formula": "Na3PO4", "charge": 0, "type": "Inorganic Salt", "color": "#A855F7", "border": "#7E22CE", "atoms": "Na: 3, P: 1, O: 4", "desc": "Heavy-duty cleaning and degreasing alkaline salt."},
    {"id": 88, "symbol": "KH2PO4", "name": "Monopotassium Phosphate", "formula": "KH2PO4", "charge": 0, "type": "Acid Salt", "color": "#C084FC", "border": "#9333EA", "atoms": "K: 1, H: 2, P: 1, O: 4", "desc": "Soluble fertilizer salt displaying piezoelectric properties."},
    {"id": 89, "symbol": "O3", "name": "Ozone", "formula": "O3", "charge": 0, "type": "Allotrope Gas", "color": "#67E8F9", "border": "#0284C7", "atoms": "O: 3", "desc": "Triatomic pale blue gas absorbing harmful ultraviolet radiation."},
    {"id": 90, "symbol": "H2O2", "name": "Hydrogen Peroxide", "formula": "H2O2", "charge": 0, "type": "Peroxide", "color": "#38BDF8", "border": "#0284C7", "atoms": "H: 2, O: 2", "desc": "Pale blue oxidizing liquid containing a single oxygen-oxygen bond."},
    {"id": 91, "symbol": "Br2", "name": "Molecular Bromine", "formula": "Br2", "charge": 0, "type": "Halogen Liquid", "color": "#D97706", "border": "#92400E", "atoms": "Br: 2", "desc": "Dense reddish-brown volatile fuming halogen liquid."},
    {"id": 92, "symbol": "I2", "name": "Molecular Iodine", "formula": "I2", "charge": 0, "type": "Halogen Solid", "color": "#8B5CF6", "border": "#5B21B6", "atoms": "I: 2", "desc": "Deep purple lustrous solid subliming into brilliant violet vapor."},
    {"id": 93, "symbol": "HF", "name": "Hydrogen Fluoride", "formula": "HF", "charge": 0, "type": "Acid Gas", "color": "#A3E635", "border": "#65A30D", "atoms": "H: 1, F: 1", "desc": "Extremely corrosive contact poison capable of etching glass."},
    {"id": 94, "symbol": "HBr", "name": "Hydrogen Bromide", "formula": "HBr", "charge": 0, "type": "Strong Acid Gas", "color": "#D97706", "border": "#92400E", "atoms": "H: 1, Br: 1", "desc": "Colorless fuming gas forming strong hydrobromic acid in water."},
    {"id": 95, "symbol": "HI", "name": "Hydrogen Iodide", "formula": "HI", "charge": 0, "type": "Strong Acid Gas", "color": "#8B5CF6", "border": "#5B21B6", "atoms": "H: 1, I: 1", "desc": "Colorless reducing gas dissociating into one of the strongest acids."},
    {"id": 96, "symbol": "NaF", "name": "Sodium Fluoride", "formula": "NaF", "charge": 0, "type": "Ionic Salt", "color": "#A855F7", "border": "#7E22CE", "atoms": "Na: 1, F: 1", "desc": "Inorganic salt incorporated into toothpaste to strengthen enamel."},
    {"id": 97, "symbol": "KF", "name": "Potassium Fluoride", "formula": "KF", "charge": 0, "type": "Ionic Salt", "color": "#C084FC", "border": "#9333EA", "atoms": "K: 1, F: 1", "desc": "Deliquescent salt supplying fluoride ions in organic synthesis."},
    {"id": 98, "symbol": "NaBr", "name": "Sodium Bromide", "formula": "NaBr", "charge": 0, "type": "Ionic Salt", "color": "#A855F7", "border": "#7E22CE", "atoms": "Na: 1, Br: 1", "desc": "White crystalline salt historically used as an anticonvulsant."},
    {"id": 99, "symbol": "KBr", "name": "Potassium Bromide", "formula": "KBr", "charge": 0, "type": "Ionic Salt", "color": "#C084FC", "border": "#9333EA", "atoms": "K: 1, Br: 1", "desc": "Halide salt widely used in infrared spectroscopy optical windows."},
    {"id": 100, "symbol": "NaI", "name": "Sodium Iodide", "formula": "NaI", "charge": 0, "type": "Ionic Salt", "color": "#A855F7", "border": "#7E22CE", "atoms": "Na: 1, I: 1", "desc": "Deliquescent iodide salt serving as a gamma-ray scintillator."},
    {"id": 101, "symbol": "KI", "name": "Potassium Iodide", "formula": "KI", "charge": 0, "type": "Ionic Salt", "color": "#C084FC", "border": "#9333EA", "atoms": "K: 1, I: 1", "desc": "Essential nutritional salt and thyroid blocking agent in radiation medicine."},
    {"id": 102, "symbol": "HArF", "name": "Argon Fluorohydride", "formula": "HArF", "charge": 0, "type": "Noble Gas Compound", "color": "#2DD4BF", "border": "#0F766E", "atoms": "H: 1, Ar: 1, F: 1", "desc": "First true chemical compound discovered containing neutral argon."},
    {"id": 103, "symbol": "CaO", "name": "Calcium Oxide", "formula": "CaO", "charge": 0, "type": "Basic Anhydride", "color": "#14B8A6", "border": "#0F766E", "atoms": "Ca: 1, O: 1", "desc": "Quicklime producing extreme exothermic heat when slaked with water."},
    {"id": 104, "symbol": "Ca(OH)2", "name": "Calcium Hydroxide", "formula": "Ca(OH)2", "charge": 0, "type": "Strong Base", "color": "#14B8A6", "border": "#0F766E", "atoms": "Ca: 1, O: 2, H: 2", "desc": "Slaked lime suspension forming traditional limewash mortar."},
    {"id": 105, "symbol": "CaCO3", "name": "Calcium Carbonate", "formula": "CaCO3", "charge": 0, "type": "Mineral Carbonate", "color": "#14B8A6", "border": "#0F766E", "atoms": "Ca: 1, C: 1, O: 3", "desc": "Main component of chalk, limestone, marble, and marine seashells."},
    {"id": 106, "symbol": "NaOH", "name": "Sodium Hydroxide", "formula": "NaOH", "charge": 0, "type": "Caustic Alkali", "color": "#A855F7", "border": "#7E22CE", "atoms": "Na: 1, O: 1, H: 1", "desc": "Caustic lye base dissolving grease and saponifying fats into soap."},
    {"id": 107, "symbol": "OF2", "name": "Oxygen Difluoride", "formula": "OF2", "charge": 0, "type": "Fluoride Compound", "color": "#A3E635", "border": "#65A30D", "atoms": "O: 1, F: 2", "desc": "Rare compound where oxygen exhibits a positive oxidation state (+2)."},

    # --- 22 Ions (IDs 108-129) ---
    {"id": 108, "symbol": "H-", "name": "Hydride Ion", "formula": "H⁻", "charge": -1, "type": "Anion", "color": "#38BDF8", "border": "#0284C7", "atoms": "H: 1", "desc": "Hydrogen atom with an extra paired electron, strong reducing base."},
    {"id": 109, "symbol": "H+", "name": "Proton / Hydron", "formula": "H⁺", "charge": 1, "type": "Cation", "color": "#F43F5E", "border": "#BE123C", "atoms": "H: 1", "desc": "Bare atomic hydrogen nucleus mediating all Arrhenius acidity."},
    {"id": 110, "symbol": "H3+", "name": "Trihydrogen Cation", "formula": "H3⁺", "charge": 1, "type": "Molecular Cation", "color": "#38BDF8", "border": "#0284C7", "atoms": "H: 3", "desc": "Crucial initiator of all gas-phase astrochemistry in interstellar space."},
    {"id": 111, "symbol": "OH-", "name": "Hydroxide Ion", "formula": "OH⁻", "charge": -1, "type": "Anion", "color": "#38BDF8", "border": "#0284C7", "atoms": "O: 1, H: 1", "desc": "Diatomic anion defining alkaline pH in aqueous solution."},
    {"id": 112, "symbol": "H2+", "name": "Dihydrogen Cation", "formula": "H2⁺", "charge": 1, "type": "Molecular Cation", "color": "#38BDF8", "border": "#0284C7", "atoms": "H: 2", "desc": "Simplest molecular ion bound by a single one-electron bond."},
    {"id": 113, "symbol": "NH+", "name": "Imidogen Cation", "formula": "NH⁺", "charge": 1, "type": "Molecular Cation", "color": "#38BDF8", "border": "#0284C7", "atoms": "N: 1, H: 1", "desc": "Ionized nitrogen hydride radical produced in cosmic ionizing fields."},
    {"id": 114, "symbol": "N+", "name": "Nitrogen Cation", "formula": "N⁺", "charge": 1, "type": "Atomic Cation", "color": "#38BDF8", "border": "#0284C7", "atoms": "N: 1", "desc": "Singly ionized nitrogen atom common in planetary auroras."},
    {"id": 115, "symbol": "CN-", "name": "Cyanide Ion", "formula": "CN⁻", "charge": -1, "type": "Polyatomic Anion", "color": "#64748B", "border": "#334155", "atoms": "C: 1, N: 1", "desc": "Lethal inhibitor of mitochondrial cytochrome c oxidase."},
    {"id": 116, "symbol": "HeH+", "name": "Hydrohelium Cation", "formula": "HeH⁺", "charge": 1, "type": "Molecular Cation", "color": "#67E8F9", "border": "#0891B2", "atoms": "He: 1, H: 1", "desc": "Strongest known acid and first molecular bond formed in the early universe."},
    {"id": 117, "symbol": "Cl-", "name": "Chloride Ion", "formula": "Cl⁻", "charge": -1, "type": "Halide Anion", "color": "#22C55E", "border": "#15803D", "atoms": "Cl: 1", "desc": "Major extracellular anion maintaining cellular osmotic pressure."},
    {"id": 118, "symbol": "Na+", "name": "Sodium Cation", "formula": "Na⁺", "charge": 1, "type": "Alkali Cation", "color": "#A855F7", "border": "#7E22CE", "atoms": "Na: 1", "desc": "Primary extracellular electrolyte transmitting neural action potentials."},
    {"id": 119, "symbol": "CO3-2", "name": "Carbonate Ion", "formula": "CO3²⁻", "charge": -2, "type": "Oxyanion", "color": "#64748B", "border": "#1E293B", "atoms": "C: 1, O: 3", "desc": "Trigonal planar buffer anion regulating ocean pH and coral growth."},
    {"id": 120, "symbol": "HCO3-", "name": "Bicarbonate Ion", "formula": "HCO3⁻", "charge": -1, "type": "Oxyanion", "color": "#64748B", "border": "#1E293B", "atoms": "H: 1, C: 1, O: 3", "desc": "Vital physiological buffer stabilizing blood pH at 7.4."},
    {"id": 121, "symbol": "S-2", "name": "Sulfide Ion", "formula": "S²⁻", "charge": -2, "type": "Chalcogenide Anion", "color": "#FACC15", "border": "#CA8A04", "atoms": "S: 1", "desc": "Chalcogenide anion precipitating heavy metals in mineral veins."},
    {"id": 122, "symbol": "HSO4-", "name": "Bisulfate Ion", "formula": "HSO4⁻", "charge": -1, "type": "Acid Anion", "color": "#FACC15", "border": "#CA8A04", "atoms": "H: 1, S: 1, O: 4", "desc": "Conjugate base of sulfuric acid acting as a moderately strong acid."},
    {"id": 123, "symbol": "H3O+", "name": "Hydronium Ion", "formula": "H3O⁺", "charge": 1, "type": "Molecular Cation", "color": "#38BDF8", "border": "#0284C7", "atoms": "H: 3, O: 1", "desc": "Protonated water molecule delivering acid character in water."},
    {"id": 124, "symbol": "SO4-2", "name": "Sulfate Ion", "formula": "SO4²⁻", "charge": -2, "type": "Tetrahedral Oxyanion", "color": "#FACC15", "border": "#CA8A04", "atoms": "S: 1, O: 4", "desc": "Tetrahedral divalent oxyanion forming insoluble gypsum and barite."},
    {"id": 125, "symbol": "K+", "name": "Potassium Cation", "formula": "K⁺", "charge": 1, "type": "Alkali Cation", "color": "#C084FC", "border": "#9333EA", "atoms": "K: 1", "desc": "Primary intracellular cation firing muscular contraction and heart rhythm."},
    {"id": 126, "symbol": "SiO3-2", "name": "Silicate Ion", "formula": "SiO3²⁻", "charge": -2, "type": "Silicate Anion", "color": "#F59E0B", "border": "#B45309", "atoms": "Si: 1, O: 3", "desc": "Fundamental chain unit of geological pyroxene and amphibole minerals."},
    {"id": 127, "symbol": "H2PO4-", "name": "Dihydrogen Phosphate", "formula": "H2PO4⁻", "charge": -1, "type": "Phosphate Anion", "color": "#F97316", "border": "#C2410C", "atoms": "H: 2, P: 1, O: 4", "desc": "Primary intracellular acid buffer maintaining cytoplasmic pH."},
    {"id": 128, "symbol": "HPO4-2", "name": "Hydrogen Phosphate", "formula": "HPO4²⁻", "charge": -2, "type": "Phosphate Anion", "color": "#F97316", "border": "#C2410C", "atoms": "H: 1, P: 1, O: 4", "desc": "Conjugate basic partner in the physiological phosphate buffer system."},
    {"id": 129, "symbol": "PO4-3", "name": "Phosphate Ion", "formula": "PO4³⁻", "charge": -3, "type": "Tetrahedral Oxyanion", "color": "#F97316", "border": "#C2410C", "atoms": "P: 1, O: 4", "desc": "Triply negative structural backbone of DNA and calcium hydroxyapatite."}
]

# Map symbol to id
SYMBOL_TO_ID = {s["symbol"]: s["id"] for s in SPECIES}
assert len(SPECIES) == 129

REACTIONS_RAW = [
    # Element syntheses
    ("H", "H", "H2", True, False, "Hydrogen combination"),
    ("O", "O", "O2", True, False, "Oxygen combination"),
    ("N", "N", "N2", True, False, "Nitrogen combination"),
    ("F", "F", "F2", True, False, "Fluorine combination"),
    ("Cl", "Cl", "Cl2", True, False, "Chlorine combination"),
    ("Br", "Br", "Br2", True, False, "Bromine combination"),
    ("I", "I", "I2", True, False, "Iodine combination"),
    ("Li", "Li", "Li2", False, False, "Lithium dimerization"),
    ("Be", "Be", "Be2", False, False, "Beryllium dimerization"),
    ("C", "N", "CN", False, False, "Cyano radical formation"),
    ("N", "H", "NH•", False, False, "Imidogen radical synthesis"),
    ("N", "O", "NO•", False, False, "Nitric oxide synthesis"),
    ("H", "Cl", "HCl", True, False, "Hydrogen chloride synthesis"),
    ("Na", "Cl", "NaCl", True, False, "Sodium chloride synthesis"),
    ("K", "Cl", "KCl", True, False, "Potassium chloride synthesis"),
    ("Ca", "Cl2", "CaCl2", True, False, "Calcium chloride synthesis"),
    ("Be", "Cl2", "BeCl2", True, False, "Beryllium chloride synthesis"),
    ("C", "O", "CO", True, False, "Carbon monoxide synthesis"),
    ("CO", "O", "CO2", True, False, "Carbon dioxide oxidation"),
    ("C", "H", "CH•", False, False, "Methylidyne radical synthesis"),
    ("CH•", "H", "CH2•", False, False, "Methylene radical synthesis"),
    ("CH2•", "H", "CH3•", False, False, "Methyl radical synthesis"),
    ("CH3•", "H", "CH4", True, False, "Methane synthesis"),
    ("CH3•", "CH3•", "C2H6", True, False, "Ethane synthesis"),
    ("CH2•", "CH2•", "C2H4", True, False, "Ethylene synthesis"),
    ("CH•", "CH•", "C2H2", True, False, "Acetylene synthesis"),
    ("NH•", "H", "NH2•", False, False, "Amino radical synthesis"),
    ("NH2•", "H", "NH3", True, False, "Ammonia synthesis"),
    ("H", "CN", "HCN", False, False, "Hydrogen cyanide synthesis"),
    ("H2", "O", "H2O", True, False, "Water synthesis"),
    ("H2O", "O", "H2O2", False, False, "Hydrogen peroxide synthesis"),
    ("O2", "O", "O3", False, True, "Ozone photochemical synthesis"),
    ("H", "F", "HF", True, False, "Hydrogen fluoride synthesis"),
    ("H", "Br", "HBr", True, False, "Hydrogen bromide synthesis"),
    ("H", "I", "HI", True, False, "Hydrogen iodide synthesis"),
    ("Na", "F", "NaF", True, False, "Sodium fluoride synthesis"),
    ("K", "F", "KF", True, False, "Potassium fluoride synthesis"),
    ("Na", "Br", "NaBr", True, False, "Sodium bromide synthesis"),
    ("K", "Br", "KBr", True, False, "Potassium bromide synthesis"),
    ("Na", "I", "NaI", True, False, "Sodium iodide synthesis"),
    ("K", "I", "KI", True, False, "Potassium iodide synthesis"),
    ("Ca", "O", "CaO", True, False, "Quicklime synthesis"),
    ("CaO", "H2O", "Ca(OH)2", True, False, "Slaked lime hydration"),
    ("Ca(OH)2", "CO2", "CaCO3", True, False, "Calcium carbonate precipitation"),
    ("Na", "H2O", "NaOH", True, False, "Sodium hydroxide synthesis"),
    ("O", "F2", "OF2", False, False, "Oxygen difluoride synthesis"),
    ("CO", "H2", "H2CO", False, False, "Formaldehyde synthesis"),
    ("H2CO", "H", "HCO•", False, True, "Formyl radical photolysis"),
    ("H2CO", "CH2•", "CH3CHO", False, False, "Acetaldehyde synthesis"),
    ("CH3CHO", "O", "CH3COOH", True, False, "Acetic acid oxidation"),
    ("S", "H", "HS•", False, False, "Thiohydroxy radical synthesis"),
    ("HS•", "H", "H2S", True, False, "Hydrogen sulfide synthesis"),
    ("S", "O2", "SO2", True, False, "Sulfur dioxide combustion"),
    ("SO2", "O", "SO3", True, False, "Sulfur trioxide oxidation"),
    ("SO3", "H2O", "H2SO4", True, False, "Sulfuric acid hydration"),
    ("H2SO4", "Na", "NaHSO4", True, False, "Sodium bisulfate synthesis"),
    ("H2SO4", "K", "KHSO4", True, False, "Potassium bisulfate synthesis"),
    ("S", "S", "S2", False, False, "Disulfur synthesis"),
    ("S2", "S", "S3", False, False, "Trisulfur synthesis"),
    ("S2", "S2", "S4", False, False, "Tetrasulfur synthesis"),
    ("N2", "N2", "N4", False, True, "Tetranitrogen synthesis"),
    ("S4", "N4", "S4N4", True, False, "Tetrasulfur tetranitride synthesis"),
    ("S2", "Cl2", "S2Cl2", False, False, "Disulfur dichloride synthesis"),
    ("NH3", "HCl", "NH4Cl", True, False, "Ammonium chloride synthesis"),
    ("Si", "O", "SiO", False, False, "Silicon monoxide synthesis"),
    ("SiO", "O", "SiO2", True, False, "Silicon dioxide synthesis"),
    ("SiO2", "Na2CO3", "Na2SiO3", False, False, "Sodium silicate synthesis"),
    ("Si", "H", "SiH•", False, False, "Silylidyne radical synthesis"),
    ("SiH•", "H", "SiH2•", False, False, "Silylene radical synthesis"),
    ("SiH2•", "H", "SiH3•", False, False, "Silyl radical synthesis"),
    ("SiH3•", "H", "SiH4", True, False, "Silane synthesis"),
    ("SiH3•", "SiH3•", "Si2H6", True, False, "Disilane synthesis"),
    ("SiO2", "K", "K2SiO3", False, False, "Potassium silicate synthesis"),
    ("P", "P", "P2", False, False, "Diphosphorus synthesis"),
    ("P2", "P2", "P4", False, False, "White phosphorus synthesis"),
    ("P", "H", "PH•", False, False, "Phosphinidyne radical synthesis"),
    ("PH•", "H", "PH2•", False, False, "Phosphino radical synthesis"),
    ("PH2•", "H", "PH3", True, False, "Phosphine synthesis"),
    ("P4", "O2", "P4O10", True, False, "Phosphorus pentoxide synthesis"),
    ("P4O10", "H2O", "H3PO4", True, False, "Phosphoric acid hydration"),
    ("P", "N", "PN", False, False, "Phosphorus mononitride synthesis"),
    ("H3PO4", "Na", "Na3PO4", True, False, "Trisodium phosphate synthesis"),
    ("H3PO4", "K", "KH2PO4", True, False, "Monopotassium phosphate synthesis"),
    ("HF", "Ar", "HArF", False, True, "Argon fluorohydride synthesis"),
    ("Cl", "O2", "ClO2", False, False, "Chlorine dioxide synthesis"),
    ("Cl", "OH-", "HOCl", False, False, "Hypochlorous acid synthesis"),
    ("Cl2", "O", "Cl2O", False, False, "Dichlorine monoxide synthesis"),
    ("Na", "HCO3-", "Na2CO3", True, False, "Sodium carbonate neutralization"),
    ("CO2", "OH-", "HCO3-", True, False, "Carbon dioxide hydration to bicarbonate"),
    ("CO2", "NaOH", "Na2CO3", True, False, "Carbon dioxide absorption by lye"),
    ("CO2", "O", "CO3-2", False, False, "Carbonate ion synthesis"),
    ("SiO2", "NaOH", "Na2SiO3", True, False, "Silica dissolution by alkali"),
    ("SiO2", "O", "SiO3-2", False, False, "Silicate ion synthesis"),

    # Ion combinations
    ("H+", "OH-", "H2O", True, False, "Neutralization reaction"),
    ("H3O+", "OH-", "H2O", True, False, "Acid-base neutralization"),
    ("H+", "H2", "H3+", False, False, "Trihydrogen cation formation"),
    ("H+", "H2O", "H3O+", True, False, "Hydronium formation"),
    ("H+", "CN-", "HCN", False, False, "Cyanide protonation"),
    ("He", "H+", "HeH+", False, False, "Hydrohelium formation"),
    ("Na+", "Cl-", "NaCl", True, False, "Ionic lattice bond"),
    ("K+", "Cl-", "KCl", True, False, "Ionic lattice bond"),
    ("CO3-2", "H+", "HCO3-", False, False, "Carbonate protonation"),
    ("SO4-2", "H+", "HSO4-", False, False, "Sulfate protonation"),
    ("Na+", "OH-", "NaOH", True, False, "Sodium hydroxide ionic bond"),
    ("H+", "Cl-", "HCl", True, False, "Hydrogen chloride ionic combination"),
    ("Na", "CO3-2", "Na2CO3", True, False, "Sodium carbonate formation"),
    ("Na", "SiO3-2", "Na2SiO3", True, False, "Sodium silicate formation"),
    ("K", "SiO3-2", "K2SiO3", True, False, "Potassium silicate formation"),
    ("Na", "PO4-3", "Na3PO4", True, False, "Trisodium phosphate formation"),
    ("K", "H2PO4-", "KH2PO4", True, False, "Monopotassium phosphate formation"),
    ("Na", "HSO4-", "NaHSO4", True, False, "Sodium bisulfate formation"),
    ("K", "HSO4-", "KHSO4", True, False, "Potassium bisulfate formation")
]

# Standardize reaction dictionary keyed by sorted reactant IDs
REACTIONS = []
seen_pairs = set()
for r1_sym, r2_sym, prod_sym, is_exo, req_uv, desc in REACTIONS_RAW:
    id1 = SYMBOL_TO_ID[r1_sym]
    id2 = SYMBOL_TO_ID[r2_sym]
    prod_id = SYMBOL_TO_ID[prod_sym]
    # canonical key: "min_max"
    key = f"{min(id1, id2)}_{max(id1, id2)}"
    if key in seen_pairs:
        continue
    seen_pairs.add(key)
    REACTIONS.append({
        "key": key,
        "reactant1_id": min(id1, id2),
        "reactant2_id": max(id1, id2),
        "product_id": prod_id,
        "is_exo": 1 if is_exo else 0,
        "req_uv": 1 if req_uv else 0,
        "desc": desc
    })

COSMIC_IONIZATIONS = [
    ("H", "H+"),
    ("H2", "H2+"),
    ("He", "HeH+"),
    ("N", "N+"),
    ("NH•", "NH+"),
    ("Na", "Na+"),
    ("K", "K+"),
    ("Cl", "Cl-"),
    ("S", "S-2"),
    ("HCN", "CN-"),
    ("H2O", "OH-"),
    ("Na2CO3", "CO3-2"),
    ("H2SO4", "SO4-2"),
    ("Na2SiO3", "SiO3-2"),
    ("H3PO4", "H2PO4-"),
    ("H2PO4-", "HPO4-2"),
    ("HPO4-2", "PO4-3"),
    ("H-", "H")
]

IONIZE_RULES = []
for src_sym, dst_sym in COSMIC_IONIZATIONS:
    IONIZE_RULES.append({
        "src_id": SYMBOL_TO_ID[src_sym],
        "dst_id": SYMBOL_TO_ID[dst_sym]
    })

print(f"Total Unique Reactions: {len(REACTIONS)}")
print(f"Total Ionization Rules: {len(IONIZE_RULES)}")
