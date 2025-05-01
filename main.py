import numpy as np
from camera import Camera
from ray import Ray
from objects import Sphere
from PIL import Image

# Dimensions of rendered image
aspect_ratio = 2.39  # ultra-wide 
width = 480
height = int(width / aspect_ratio)

image = Image.new("RGB", (width, height))
pixels = image.load()

camera = Camera(
    origin=[0, 0, 0],
    look_at=[0, 0, -1],
    up=[0, 1, 0],
    fov=90,
    image_size=(width, height)
)

sphere = Sphere(center=[0, 0, -3], radius=1)

for j in range(height):
    for i in range(width):
        # Normalize coordinates to range [0, 1]
        x = i / (width - 1)
        y = 1 - (j / (height - 1))  # Flip y-axis for image coordinate
        
        ray = camera.get_ray(x, y)  # Generate ray through pixel
        hit = sphere.intersect(ray)  # Check for intersection

        # Color pixel white if hit, black if not
        if hit is not None:
            pixels[i, j] = (255, 255, 255)  # White pixel = hit
        else:
            pixels[i, j] = (0, 0, 0)  # Black pixel = miss

image.save("render.png")
