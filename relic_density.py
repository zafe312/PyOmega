import numpy as np
from scipy.special import lambertw
from thermal_average import thermal_avg_sigma_v

Mpl = 1.22e19  # Planck mass in GeV
const_prefactor = 1.07e9  # GeV^-1

def estimate_freezeout(dm_mass, sigma_func, g_eff=90, tol=1e-3, max_iter=100):
    x = 25.0  # initial guess: x_f = m/T
    for _ in range(max_iter):
        T = dm_mass / x
        sigma_v = thermal_avg_sigma_v(sigma_func, dm_mass, T)
        # print(sigma_v)
        rhs = np.log(0.038 * Mpl * dm_mass * sigma_v / np.sqrt(g_eff * x))
        x_new = rhs
        if abs(x - x_new) < tol:
            return x_new
        x = x_new
    return x

def compute_relic_density(dm_mass, sigma_func, g_eff=90):
    x_f = estimate_freezeout(dm_mass, sigma_func, g_eff)
    T_f = dm_mass / x_f
    sigma_v = thermal_avg_sigma_v(sigma_func, dm_mass, T_f)
    
    omega_h2 = const_prefactor / Mpl * x_f / np.sqrt(g_eff) / sigma_v
    return omega_h2, x_f