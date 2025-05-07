import importlib.util
import sys
import os

class UFOModel:
    def __init__(self, model_path):
        self.model_path = os.path.abspath(model_path)
        self.particles = []
        self.vertices = []
        self.load_model()

    def load_model(self):
        sys.path.insert(0, self.model_path)

        # Dynamically import UFO modules
        particles = self._import_module("particles")
        vertices = self._import_module("vertices")

        self.particles = getattr(particles, "all_particles", [])
        self.vertices = getattr(vertices, "all_vertices", [])

    def _import_module(self, module_name):
        spec = importlib.util.find_spec(module_name)
        if spec is None:
            raise ImportError(f"Module {module_name} not found in {self.model_path}")
        return importlib.import_module(module_name)

    # def find_dark_matter_candidate(self):
    #     """
    #     Naively assumes that the DM candidate is:
    #     - electrically neutral
    #     - colorless
    #     - stable (not in any decay vertices)
    #     """
    #     candidates = []
    #     decaying_particles = set()

    #     # Track particles that appear in decays
    #     for v in self.vertices:
    #         if len(v.particles) >= 2:
    #             decaying_particles.add(v.particles[0].name)

    #     for p in self.particles:
    #         # Skip if Z2 parity not defined
    #         parity = getattr(p, "Z2", None)
    #         if parity != -1:
    #             continue

    #         if p.charge != 0:
    #             continue
    #         if p.color != 1:
    #             continue
    #         if p.name in decaying_particles:
    #             continue

    #         candidates.append(p)

    #     if not candidates:
    #         raise ValueError("No Z2-odd DM candidate found.")
    #     elif len(candidates) > 1:
    #         print("[WARNING] Multiple Z2-odd DM candidates found, returning the lightest.")

    #         # Optional: Return the lightest candidate if multiple
    #         candidates = sorted(candidates, key=lambda x: x.mass.name)

    #     return candidates[0]

    def find_dark_matter_candidate(self):
        """
        Naively assumes that the DM candidate is:
        - electrically neutral
        - colorless
        - stable (not in any decay vertices)
        """
        candidates = []
        decaying_particles = set()
        
        for v in self.vertices:
            if len(v.particles) >= 2:
                decaying_particles.add(v.particles[0].name)

        for p in self.particles:
            if p.charge != 0: continue
            if p.color != 1: continue
            if p.name in decaying_particles: continue
            if p.name in ['nu1','nu2','nu3','A','Z','gA','gAc','gZ','gZc']: continue
            candidates.append(p)

        if not candidates:
            raise ValueError("No DM candidate found.")
        elif len(candidates) > 1:
            print("[WARNING] Multiple DM candidates found, returning first.")

        return candidates[0]


def load_ufo_model(model_path):
    print(model_path)
    return UFOModel(model_path)