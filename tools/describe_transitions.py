# -*- coding: utf-8 -*-
from PIL import Image
import numpy as np

# Let's write a small script to describe what happens in each frame of transition_1_2
# Let's inspect the exact positions of elements in transition 1->2
print("Transition 1->2 analysis:")
print("Frames t12_008 to t12_018:")
# In t12_008 (slide 1 steady):
# Left: White text "Triết học Mác - Lênin", red text "Quan điểm...", presenter tag.
# Right: Lenin cutout in front of a red flag banner with Russian text.
# Bottom: Red bar with logo.

# In t12_009:
# "Triết học Mác - Lênin" text block is moving left (-X).
# Red flag with worker + Marx-Engels-Lenin starts rising from bottom-left.

# In t12_012:
# Worker+Flag is now large on bottom left.
# Star + hammer/sickle appears on top left.
# Title "Nội Dung Trình Bày" is entering on top right!
# Lenin from slide 1 has moved right and dimmed.
