import numpy as np

class Sphere:
    def __init__(self, center, radius):
        self.center = np.array(center)
        self.radius = radius

    def intersect(self, ray):
        """
        Return distance t where the ray hits the sphere, or None if there's no intersection.
        """
        # oc = vector from the sphere center to the ray origin
        oc = ray.origin - self.center  

        # a = dot product of ray direction with itself (magnitude squared)
        # Represents how fast the ray moves along its direction vector (used to scale the equation)
        a = np.dot(ray.direction, ray.direction)  
        
        # b = 2 * dot product of oc and ray direction
        # Measures how much the ray is pointing toward the sphere
        b = 2.0 * np.dot(oc, ray.direction) 

        # c = squared distance from ray origin to sphere center minus the radius squared
        # Represents how far the ray starts from the sphere's surface, relative to its size
        c = np.dot(oc, oc) - self.radius ** 2

        # Discriminant tells us if there's a real solution (intersection)
        discriminant = b ** 2 - 4 * a * c

        # If discriminant is negative, there are no real roots (ray misses the sphere)
        if discriminant < 0:
            return None
        
        # Compute the two possible intersection distances along the ray
        t1 = (-b - np.sqrt(discriminant)) / (2.0 * a)  # Closer hit (entry point)
        t2 = (-b + np.sqrt(discriminant)) / (2.0 * a)  # Farther hit (exit point)

        # Return the nearest intersection point in front of the camera
        if t1 > 0:
            return t1  # Ray hits the front of the sphere
        elif t2 > 0:
            return t2  # Ray started inside the sphere and exits out the back
        else:
            return None  # Both intersections are behind the camera
