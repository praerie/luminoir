import numpy as np
from ray import Ray  

class Camera:
    def __init__(self, origin, look_at, up, fov, image_size):
        self.origin = np.array(origin)  # Store camera's position (origin) as NumPy array.
        self.fov = np.radians(fov)  # Convert fov from degrees to radians, required for trigonometric calcs in viewport creation.
        self.image_size = image_size  # Store image resolution (width and height).
        self.aspect_ratio = image_size[0] / image_size[1]  # Calculate aspect ratio of image (width / height) to avoid viewport distortion.

        # Compute basis vectors for camera's local coordinate system (right, up, and forward)
        w = self.normalize(self.origin - np.array(look_at))  # 'w' = normalized vector pointing backwards from camera towards "look_at" point
        u = self.normalize(np.cross(np.array(up), w))  # 'u' = normalized right vector, cross product of 'v' (up) vector and 'w'
        v = np.cross(w, u)  # 'v' = normalized up vector, orthogonal to both 'u' and 'w'

        self.u = u
        self.v = v
        self.w = w

        # Calculate viewport's dimensions using fov and aspect ratio
        viewport_height = 2 * np.tan(self.fov / 2)  # based on fov and tangent function, derived from vertical angle of view
        viewport_width = viewport_height * self.aspect_ratio  # adjusted by aspect ratio (width = height * aspect_ratio)

        self.horizontal = viewport_width * u  # width of viewport along 'u' axis
        self.vertical = viewport_height * v  # height of viewport along 'v' axis
        
        # 'lower_left_corner' defines corner of viewport in 3D space (i.e., starting point of pixel grid)
        self.lower_left_corner = (self.origin
                                  - self.horizontal / 2  # half the width of viewport (left side)
                                  - self.vertical / 2    # half the height of viewport (bottom side)
                                  - w)                   # 'w' vector points backward to give depth

    def get_ray(self, x, y):
        """Generate a ray from pixel (x, y) in normalized coordinates [0,1]."""
        
        # Direction of ray is computed by adjusting 'lower_left_corner' by the pixel's position.
        # Direction vector moves from lower-left corner towards current pixel (x, y) in the normalized space.
        direction = (self.lower_left_corner
                     + x * self.horizontal  # horizontal displacement for the pixel
                     + y * self.vertical    # vertical displacement for the pixel
                     - self.origin)         # subtract the camera's origin to get direction from the camera

        return Ray(self.origin, direction)  # return new Ray obj using camera's origin and calculated direction

    def normalize(self, v):
        """Return unit vector of v, computed by dividing it by its magnitude (Euclidean L2 norm)."""
        return v / np.linalg.norm(v) 
