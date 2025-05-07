from ufo_parser.parser import load_ufo_model

model = load_ufo_model("models/SingletScalarDM_UFO")
dm = model.find_dark_matter_candidate()

print("Identified DM candidate:")
print(f"Name: {dm.name}")
print(f"PDG code: {dm.pdg_code}")
print(f"Mass: {dm.mass.name}")