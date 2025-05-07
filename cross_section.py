import sympy as sp

def extract_annihilation_channels(model, dm_name):
    # Look for vertices with 2 DM + 1 SM particle
    relevant = []
    for v in model.vertices:
        names = [p.name for p in v.particles]
        if names.count(dm_name) == 2 and len(names) == 3:
            sm_particle = [p for p in v.particles if p.name != dm_name][0]
            relevant.append((v, sm_particle))
    return relevant

def build_scalar_annihilation_cross_section(vertex, dm_mass_val, param_subs={}):
    # Only for scalar DM via Higgs-like mediator
    s = sp.Symbol('s', positive=True)
    m_dm = sp.Symbol('m_dm', positive=True)
    mh, Gamma_h = sp.symbols('mh Gamma_h', positive=True)

    # Coupling: symbolic from UFO
    coupling_str = vertex.couplings[(0,0)].value

    # Convert to symbolic expression
    # clean = coupling_str.replace("complex(0,1)", "I").replace("complexconjugate", "sp.conjugate")
    # g = sp.sympify(clean, locals={"I": sp.I})
    clean = coupling_str.replace("complex(0,1)", "I")
    local_dict = {
        "I": sp.I,
        "conjugate": sp.conjugate,
    }
    g = sp.sympify(clean, locals=local_dict)

    # Simplified σ(s) formula:
    num = g**2 * s
    denom = (s - mh**2)**2 + mh**2 * Gamma_h**2
    sigma = num / denom

    # Substitute parameters
    subs = {m_dm: dm_mass_val}
    subs.update(param_subs)

    return sp.simplify(sigma.subs(subs))