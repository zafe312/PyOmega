from ufo_parser.parser import load_ufo_model
from utils import display_particle
from cross_section import extract_annihilation_channels, build_scalar_annihilation_cross_section
from thermal_average import thermal_avg_sigma_v
from sympy.utilities.lambdify import lambdify
import sympy as sp
import numpy as np
from relic_density import compute_relic_density

# model_path = "models/SingletScalarDM_UFO"
model_path = "models/SingletDoubletDM_UFO"

model = load_ufo_model(model_path)
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
LS12 = sp.Symbol('LS12')


param_subs = {
    mh: 125.0,         # Higgs mass in GeV
    Gamma_h: 0.004,    # Higgs width in GeV
    LSH: 0.000001,          # Example coupling strength (can be complex if needed)
    v: 246.0,            # Higgs vev in GeV
    LS12: 0.0001
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
m_chi_val = 100#float(dm.mass.value)

sigma_v = thermal_avg_sigma_v(sigma_numeric, m_chi_val, T)
print(f"\n⟨σv⟩ at T = {T} GeV ≈ {sigma_v:.3e} GeV⁻²")


m_chi_val_list = np.logspace(0,5,1000)
omega_h2_list = []

for m_chi_val in m_chi_val_list:
    omega_h2, x_f = compute_relic_density(m_chi_val, sigma_numeric)

    # print(f"Freeze-out x_f ≈ {x_f:.2f}")
    # print(f"Relic density Ωχ h² ≈ {omega_h2:.4f}")
    omega_h2_list.append(omega_h2)

import matplotlib.pyplot as plt
plt.plot(m_chi_val_list,omega_h2_list)
plt.axhline(y=0.12, color='black', linestyle='--', label='Ωh² = 0.12')
plt.xlabel('$m_{DM}$ [GeV]')
plt.ylabel('$\\Omega_{DM} h^2$')
plt.loglog()
plt.legend()
plt.show()