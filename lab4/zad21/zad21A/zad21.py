import cv2
import numpy as np
from scipy.signal import convolve2d
import matplotlib.pyplot as plt

# --- 1. Wczytanie obrazu ---
img = cv2.imread("Escher.png", cv2.IMREAD_GRAYSCALE)
img = img.astype(np.float32)

# --- 2. Definicja 8 masek Kirscha ---
k1 = np.array([[-3, 5, 5],
               [-3, 0, 5],
               [-3, -3, -3]])

kernels = [k1]
# pozostałe rotacje (45°, 90°, ..., 315°)
for i in range(1, 8):
    kernels.append(np.rot90(k1, k=i))

# --- 3. Konwolucje ---
responses = []
for k in kernels:
    conv = convolve2d(img, k, mode='same', boundary='symm')
    responses.append(conv)

# --- 4. Maksimum z odpowiedzi we wszystkich kierunkach ---
edges = np.max(responses, axis=0)

# --- 5. Normalizacja do 0–255 ---
edges_norm = edges - edges.min()
edges_norm = edges_norm / edges_norm.max() * 255
edges_norm = edges_norm.astype(np.uint8)

# --- 6. Zapis i wyświetlenie ---
cv2.imwrite("kirsch_edges.png", edges_norm)

plt.figure(figsize=(12,5))
plt.subplot(1,2,1)
plt.title("Oryginał")
plt.imshow(img, cmap='gray')

plt.subplot(1,2,2)
plt.title("Kirsch edges")
plt.imshow(edges_norm, cmap='gray')
plt.show()
