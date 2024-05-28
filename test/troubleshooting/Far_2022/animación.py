#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 27 12:55:36 2024

@author: daniel
"""

from PIL import Image

# List to hold the filenames
image_paths = []

# Construct filenames in the desired order
for i in range(1, 30):  # Assuming there are 60 images
    for j in range(2):  # Assuming each i has two images (0 and 12)
        filename = f'{i}_{j*12}.png'
        image_paths.append(filename)

# Open images and store them in a list
images = [Image.open(image) for image in image_paths]

# Save as a GIF
images[0].save('output.gif', save_all=True, append_images=images[1:], duration=500, loop=0)
