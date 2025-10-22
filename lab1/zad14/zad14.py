from PIL import Image
import numpy as np

# wczytaj obraz
im = Image.open("lwy.png").convert("L")  # konwertuj do 8-bit gray
arr = np.array(im)

M = np.array([[7,1,5],
              [3,0,2],
              [4,8,6]])

h, w = arr.shape
out = np.zeros_like(arr, dtype=np.uint8)

for y in range(h):
    for x in range(w):
        m = M[y % 3, x % 3]
        T = 255.0 * (m + 0.5) / 9.0
        out[y,x] = 255 if arr[y,x] > T else 0

res = Image.fromarray(out)
res.save("lew_dithered.png")
res.show()
