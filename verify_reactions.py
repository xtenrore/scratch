# Verification of species reachability and reaction mapping
elements = ["H", "He", "Li", "Be", "C", "N", "O", "F", "Ne", "Na", "Si", "P", "S", "Cl", "Ar", "K", "Ca", "Br", "I"]

molecules = [
    "H2", "H2O", "O2", "Li2", "Be2", "N2", "F2", "CN", "NH•", "NO•", "HCl", "Cl2", "NaCl", "BeCl2", "ClO2", "HOCl",
    "Cl2O", "KCl", "CaCl2", "CO", "CO2", "CH•", "CH2•", "CH3•", "CH4", "C2H6", "NH2•", "NH3", "HCN", "Na2CO3",
    "H2CO", "HCO•", "C2H4", "C2H2", "CH3CHO", "CH3COOH", "HS•", "H2S", "SO2", "SO3", "H2SO4", "NaHSO4", "KHSO4",
    "S2", "S3", "S4", "N4", "S4N4", "S2Cl2", "NH4Cl", "SiO", "SiO2", "Na2SiO3", "SiH•", "SiH2•", "SiH3•", "SiH4",
    "Si2H6", "K2SiO3", "P2", "P4", "PH•", "PH2•", "PH3", "P4O10", "H3PO4", "PN", "Na3PO4", "KH2PO4", "O3", "H2O2",
    "Br2", "I2", "HF", "HBr", "HI", "NaF", "KF", "NaBr", "KBr", "NaI", "KI", "HArF", "CaO", "Ca(OH)2", "CaCO3",
    "NaOH", "OF2"
]

ions = [
    "H-", "H+", "H3+", "OH-", "H2+", "NH+", "N+", "CN-", "HeH+", "Cl-", "Na+", "CO3-2", "HCO3-", "S-2", "HSO4-",
    "H3O+", "SO4-2", "K+", "SiO3-2", "H2PO4-", "HPO4-2", "PO4-3"
]

all_species = elements + molecules + ions
species_set = set(all_species)
print(f"Total species: {len(all_species)}, Unique: {len(species_set)}")
assert len(all_species) == len(species_set)

reactions = [
    # Element + Element syntheses
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

    # Ion combinations / Ionic bonds
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

# Cosmic ray ionizations
cosmic_ionizations = {
    "H": "H+",
    "H2": "H2+",
    "He": "HeH+",
    "N": "N+",
    "NH•": "NH+",
    "Na": "Na+",
    "K": "K+",
    "Cl": "Cl-",
    "S": "S-2",
    "HCN": "CN-",
    "H2O": "OH-",
    "Na2CO3": "CO3-2",
    "H2SO4": "SO4-2",
    "Na2SiO3": "SiO3-2",
    "H3PO4": "H2PO4-",
    "H2PO4-": "HPO4-2",
    "HPO4-2": "PO4-3",
    "H-": "H" # Electron loss
}
# Secondary cosmic ray ionization for H-
cosmic_ionizations["H"] = "H+"

# Let's verify reachability graph from base elements
known = set(elements)

# Add all cosmic ionizations reachable initially
changed = True
while changed:
    changed = False
    # Check cosmic rays
    for src, dst in cosmic_ionizations.items():
        if src in known and dst not in known:
            known.add(dst)
            changed = True
    # Special: H- from cosmic ray on H
    if "H" in known and "H-" not in known:
        known.add("H-")
        changed = True

    # Check reactions
    for r1, r2, prod, exo, uv, name in reactions:
        if r1 in known and r2 in known and prod not in known:
            known.add(prod)
            changed = True

unreached = species_set - known
print(f"Total reachable species: {len(known)} / {len(species_set)}")
if unreached:
    print("Unreached species:", sorted(list(unreached)))
else:
    print("SUCCESS! Every single one of the 129 species is reachable!")

# Add natural carbonate and silicate formation
reactions.extend([
    ("CO2", "OH-", "HCO3-", True, False, "Carbon dioxide hydration to bicarbonate"),
    ("CO2", "NaOH", "Na2CO3", True, False, "Carbon dioxide absorption by lye"),
    ("CO2", "O", "CO3-2", False, False, "Carbonate ion synthesis"),
    ("SiO2", "NaOH", "Na2SiO3", True, False, "Silica dissolution by alkali"),
    ("SiO2", "O", "SiO3-2", False, False, "Silicate ion synthesis"),
])

known = set(elements)
changed = True
while changed:
    changed = False
    for src, dst in cosmic_ionizations.items():
        if src in known and dst not in known:
            known.add(dst)
            changed = True
    if "H" in known and "H-" not in known:
        known.add("H-")
        changed = True

    for r1, r2, prod, exo, uv, name in reactions:
        if r1 in known and r2 in known and prod not in known:
            known.add(prod)
            changed = True

unreached = species_set - known
print(f"Total reachable species: {len(known)} / {len(species_set)}")
if unreached:
    print("Unreached species:", sorted(list(unreached)))
else:
    print("SUCCESS! Every single one of the 129 species is 100% reachable!")
