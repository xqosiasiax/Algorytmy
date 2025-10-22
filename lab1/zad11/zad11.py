import cv2
import numpy as np

img = cv2.imread('lwy.png', cv2.IMREAD_GRAYSCALE)
if img is None:
    raise FileNotFoundError("Image 'lwy.png' not found. Make sure 'lwy.png' exists in the working directory or provide the correct path.")

def floyd_steinberg_dithering(image, threshold=128):
    img = image.astype(np.float32).copy()
    height, width = img.shape

    for y in range(height):
        for x in range(width):
            old_pixel = img[y, x]
            new_pixel = 255 if old_pixel > threshold else 0
            img[y, x] = new_pixel
            quant_error = old_pixel - new_pixel

            if x + 1 < width:
                img[y, x + 1] += quant_error * 7 / 16
            if x - 1 >= 0 and y + 1 < height:
                img[y + 1, x - 1] += quant_error * 3 / 16
            if y + 1 < height:
                img[y + 1, x] += quant_error * 5 / 16
            if x + 1 < width and y + 1 < height:
                img[y + 1, x + 1] += quant_error * 1 / 16

    return np.clip(img, 0, 255).astype(np.uint8)

def quantize_from_diagram(value):
    if value < 20:
        return 0
    elif value < 40:
        return 64
    elif value < 60:
        return 128
    elif value < 120:
        return 192
    else:
        return 255

def jjn_dithering(image, threshold=128, mode='1bit'):
    img = image.astype(np.float32).copy()
    h, w = img.shape

    diffusion_matrix = [
        (1, 0, 7), (2, 0, 5),
        (-2, 1, 3), (-1, 1, 5), (0, 1, 7), (1, 1, 5), (2, 1, 3),
        (-2, 2, 1), (-1, 2, 3), (0, 2, 5), (1, 2, 3), (2, 2, 1)
    ]
    divisor = 48

    for y in range(h):
        for x in range(w):
            old_pixel = img[y, x]

            if mode == '1bit':
                new_pixel = 255 if old_pixel > threshold else 0
            elif mode == '5bit':
                new_pixel = quantize_from_diagram(old_pixel)
            else:
                raise ValueError("Mode must be '1bit' or '5bit'.")
            
            error = old_pixel - new_pixel
            img[y, x] = new_pixel

            for dx, dy, weight in diffusion_matrix:
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h:
                    img[ny, nx] += error * (weight / divisor)

    return np.clip(img, 0, 255).astype(np.uint8)

# a) Floyd-Steinberg Dithering
lwy_floyd_128 = floyd_steinberg_dithering(img.copy())
cv2.imwrite('lwy_floyd_128.png', lwy_floyd_128)

lwy_floyd_109 = floyd_steinberg_dithering(img.copy(), threshold=109)
cv2.imwrite('lwy_floyd_109.png', lwy_floyd_109)

# b) Jarvis, Judice, and Ninke Dithering
lwy_jjn_1bit_109 = jjn_dithering(img.copy(), threshold=109, mode='1bit')
cv2.imwrite('lwy_jjn_1bit_109.png', lwy_jjn_1bit_109)

lwy_jjn_5bit = jjn_dithering(img.copy(), mode='5bit')
cv2.imwrite('lwy_jjn_5bit.png', lwy_jjn_5bit)
