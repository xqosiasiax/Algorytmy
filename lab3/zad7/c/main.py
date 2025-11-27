import cv2
import numpy as np
import matplotlib.pyplot as plt

# obraz w skali szarości
img = cv2.imread("RezydencjaDiabla.png", cv2.IMREAD_GRAYSCALE)

alpha = -1/3

# Hiperbolizacja histogramu
g = img.astype(np.float32)
hyper = 255 / (1 - np.exp(-alpha)) * (1 - np.exp(-alpha * g / 255.0))
hyper = np.clip(hyper, 0, 255).astype(np.uint8)

# obraz wynikowy
cv2.imwrite("RezydencjaDiabla_hyper.png", hyper)

# obrazy
plt.figure(figsize=(12,5))
plt.subplot(1,2,1)
plt.imshow(img, cmap='gray')
plt.title('Oryginalny obraz')
plt.axis('off')

plt.subplot(1,2,2)
plt.imshow(hyper, cmap='gray')
plt.title('Po hiperbolizacji (α = -1/3)')
plt.axis('off')
plt.show()

# Histogram hiperbolicznego obrazu
plt.figure()
plt.hist(hyper.ravel(), bins=256, range=(0,255), color='black')
plt.title('Histogram po hiperbolizacji')
plt.xlabel('Wartości szarości')
plt.ylabel('Liczba pikseli')
plt.savefig("hist_hyper.png") 
plt.show()
