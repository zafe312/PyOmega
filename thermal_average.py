import numpy as np
import scipy.integrate as integrate
import scipy.special as sp

def thermal_avg_sigma_v(sigma_func, m_chi, T):
    """
    sigma_func(s): function returning σ(s)
    m_chi: dark matter mass
    T: temperature (in same units as m_chi)
    """
    def integrand(s):
        if s < 4 * m_chi**2:
            return 0.0
        K1 = sp.k1(np.sqrt(s) / T)
        # print(sigma_func(s))
        return sigma_func(s) * (s - 4 * m_chi**2) * np.sqrt(s) * K1

    s_min = 4 * m_chi**2
    result, _ = integrate.quad(integrand, s_min, s_min * 100, limit=500)
    K2 = sp.kn(2, m_chi / T)
    
    prefactor = 1 / (8 * m_chi**4 * T * K2**2)
    return abs(prefactor * result)