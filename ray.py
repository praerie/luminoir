import numpy as np

class Ray:
    def __init__(self, origin, direction):
        self.origin = np.array(origin, dtype=np.float32)
        self.direction = self.normalize(direction)

    def at(self, t):
        """Return point at distance t along the ray."""
        return self.origin + t * self.direction
    
    def normalize(self, v):
        return v / np.linalg.norm(v)