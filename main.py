from ufo_parser.parser import load_ufo_model
from utils import display_particle
from cross_section import extract_annihilation_channels, build_scalar_annihilation_cross_section
from thermal_average import thermal_avg_sigma_v
from sympy.utilities.lambdify import lambdify
import sympy as sp
import numpy as np


model = load_ufo_model("models/SingletScalarDM_UFO")
dm = model.find_dark_matter_candidate()

if dm:
    print(f"\nDetected Dark Matter Candidate:\n{display_particle(dm)}")
else:
    print("No dark matter candidate found.")


dm_name = dm.name
channels = extract_annihilation_channels(model, dm_name)

print(f"\nFound {len(channels)} annihilation channels for {dm_name}:")


s = sp.Symbol('s', positive=True)
m_dm = sp.Symbol('m_dm', positive=True)
mh = sp.Symbol('mh', positive=True)
Gamma_h = sp.Symbol('Gamma_h', positive=True)
LSH = sp.Symbol('LSH')
v = sp.Symbol('v')

param_subs = {
    mh: 125.0,         # Higgs mass in GeV
    Gamma_h: 0.004,    # Higgs width in GeV
    LSH: 0.01,          # Example coupling strength (can be complex if needed)
    v: 246.0            # Higgs vev in GeV
}
for v, target in channels:
    print(f"  {dm_name} {dm_name} → {target.name} via vertex {v.name}")
    sigma_expr = build_scalar_annihilation_cross_section(v, float(dm.mass.value), param_subs=param_subs)
    print(f"  σ(s) ≈ {sigma_expr}\n")

s = sp.Symbol('s')
lambdify_namespace = {
    "complexconjugate": np.conj,   # This handles complexconjugate(...)
    "conjugate": np.conj,
    "Abs": np.abs,
    "sqrt": np.sqrt
}
# Replace all complexconjugate(...) and conjugate(...) with identity
sigma_expr_clean = sigma_expr.replace(sp.conjugate, lambda x: x)
sigma_numeric = sp.lambdify(s, sigma_expr_clean, modules=[lambdify_namespace, "numpy"])

T = 5.0  # Example temperature in GeV
m_chi_val = float(dm.mass.value)

sigma_v = thermal_avg_sigma_v(sigma_numeric, m_chi_val, T)
print(f"\n⟨σv⟩ at T = {T} GeV ≈ {sigma_v:.3e} GeV⁻²")