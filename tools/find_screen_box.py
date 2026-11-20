from PIL import Image

im = Image.open("preview_red/slide1_t6.0.png")
w, h = im.size

# Let's inspect horizontal line at y = 540 (middle height)
# and vertical line at x = 960 (middle width)
# The monitor screen has a black bezel.
# Let's find the inner active screen area.

# From left edge towards center:
row = [im.getpixel((x, 540)) for x in range(w)]
# Find where the active screen starts (red pixel)
# background: (142, 121, 97)
# bezel: very dark (e.g. < 40, 40, 40)
# active screen: deep red (e.g. R > 80, G < 30, B < 30)

x_start = None
x_end = None
for x in range(w):
    r, g, b = row[x][:3]
    if r > 60 and g < 30 and b < 30:
        if x_start is None:
            x_start = x
        x_end = x

col = [im.getpixel((960, y)) for y in range(h)]
y_start = None
y_end = None
for y in range(h):
    r, g, b = col[y][:3]
    if r > 60 and g < 30 and b < 30:
        if y_start is None:
            y_start = y
        y_end = y

print(f"Active slide screen area: x=[{x_start}, {x_end}], y=[{y_start}, {y_end}]")
print(f"Screen width: {x_end - x_start + 1}, height: {y_end - y_start + 1}")
print(f"Aspect ratio: {(x_end - x_start + 1) / (y_end - y_start + 1):.4f} (target 16/9 = 1.7778)")
