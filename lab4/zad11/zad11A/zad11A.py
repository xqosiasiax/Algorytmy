import cv2
import numpy as np
import matplotlib.pyplot as plt


img = cv2.imread('YesNo_TestFiltrow.png', cv2.IMREAD_GRAYSCALE)


h_a = np.array([
    [0, 0, 1, 0, 0],
    [0, 2, 2, 2, 0],
    [1, 2, 5, 2, 1],
    [0, 2, 2, 2, 0],
    [0, 0, 1, 0, 0]
], dtype=np.float32)

h_b = np.array([
    [1, -2, 1],
    [-2, 5, -2],
    [1, -2, 1]
], dtype=np.float32)

h_c = np.array([
    [0, 1, 1],
    [-1, 1, 1],
    [-1, -1, 0]
], dtype=np.float32)

h_d = np.array([
    [1, -1, -1],
    [1, -2, -1],
    [1, 1, 1]
], dtype=np.float32)


# 3. Normalizacja filtrów

def normalize_kernel(kernel):
    s = np.sum(kernel)
    if s != 0:
        kernel = kernel / s
    return kernel

h_a = normalize_kernel(h_a)
h_b = normalize_kernel(h_b)
h_c = normalize_kernel(h_c)
h_d = normalize_kernel(h_d)


# 4. Filtrowanie (konwolucja)


result_a = cv2.filter2D(img, -1, h_a)
result_b = cv2.filter2D(img, -1, h_b) 
result_c = cv2.filter2D(img, -1, h_c)
result_d = cv2.filter2D(img, -1, h_d)


# 5. Wyświetlenie wyników

plt.figure(figsize=(12,8))

plt.subplot(2,3,1)
plt.title("Oryginał")
plt.imshow(img, cmap='gray')
plt.axis('off')

plt.subplot(2,3,2)
plt.title("h_a")
plt.imshow(result_a, cmap='gray')
plt.axis('off')

plt.subplot(2,3,3)
plt.title("h_b")
plt.imshow(result_b, cmap='gray')
plt.axis('off')

plt.subplot(2,3,5)
plt.title("h_c")
plt.imshow(result_c, cmap='gray')
plt.axis('off')

plt.subplot(2,3,6)
plt.title("h_d")
plt.imshow(result_d, cmap='gray')
plt.axis('off')

plt.tight_layout()
plt.savefig("wyniki11zad.png", dpi=300)

plt.show()
