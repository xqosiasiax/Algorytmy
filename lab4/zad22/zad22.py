import cv2
import numpy as np
import matplotlib.pyplot as plt

# 1. Wczytanie obrazu
img = cv2.imread("nosorozec.png", cv2.IMREAD_GRAYSCALE)

# 2. Rozmycie Gaussa (filtr dolnoprzepustowy)
blur = cv2.GaussianBlur(img, (11, 11), 0)

# 3. Unsharp mask (maska nieostra)
unsharp_mask = cv2.subtract(img, blur)


# 4. High-boost filtering
k = 2.0
highboost = img + (k * unsharp_mask)
highboost = np.clip(highboost, 0, 255).astype(np.uint8)

# 5. Zapis wyników do plików
cv2.imwrite("nosorozec_blur.png", blur)
cv2.imwrite("nosorozec_unsharp_mask.png", unsharp_mask)
cv2.imwrite("nosorozec_highboost.png", highboost)

# 6. Wyświetlenie
plt.figure(figsize=(10, 6))

plt.subplot(2,2,1)
plt.title("Oryginał")
plt.imshow(img, cmap='gray')
plt.axis('off')

plt.subplot(2,2,2)
plt.title("Gaussian Blur")
plt.imshow(blur, cmap='gray')
plt.axis('off')

plt.subplot(2,2,3)
plt.title("Unsharp Mask")
plt.imshow(unsharp_mask, cmap='gray')
plt.axis('off')

plt.subplot(2,2,4)
plt.title("High-Boost Filtering")
plt.imshow(highboost, cmap='gray')
plt.axis('off')

plt.tight_layout()
plt.savefig("nosorozec_wyniki.png", dpi=300)
plt.show()
