from ufo_parser.parser import load_ufo_model
from utils import display_particle
from cross_section import extract_annihilation_channels, build_scalar_annihilation_cross_section


model = load_ufo_model("models/SingletScalarDM_UFO")
dm = model.find_dark_matter_candidate()

if dm:
    print(f"\nDetected Dark Matter Candidate:\n{display_particle(dm)}")
else:
    print("No dark matter candidate found.")

# print("Identified DM candidate:")
# print(f"Name: {dm.name}")
# print(f"PDG code: {dm.pdg_code}")
# print(f"Mass: {dm.mass.name}\n")


dm_name = dm.name
channels = extract_annihilation_channels(model, dm_name)

print(f"\nFound {len(channels)} annihilation channels for {dm_name}:")

for v, target in channels:
    print(f"  {dm_name} {dm_name} → {target.name} via vertex {v.name}")
    sigma_expr = build_scalar_annihilation_cross_section(v, float(dm.mass.value), {
        'mh': 125, 'Gamma_h': 0.00407
    })
    print(f"  σ(s) ≈ {sigma_expr}\n")