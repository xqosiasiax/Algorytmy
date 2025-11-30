import cv2
import numpy as np

# ===================================================
# Load image (RGB)
# ===================================================
img = cv2.imread("spadochronNASA.png")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# ===================================================
# (a) Linear filters
# ===================================================

# Mean filter 5x5
mean_5x5 = cv2.blur(img, (5, 5))

# Gaussian σ=2 (kernel size automatically chosen; 5x5 approx)
gauss_sigma2 = cv2.GaussianBlur(img, (5, 5), sigmaX=2, sigmaY=2)

# Save results
cv2.imwrite("spadochron_mean_5x5.png",
            cv2.cvtColor(mean_5x5, cv2.COLOR_RGB2BGR))
cv2.imwrite("spadochron_gauss_sigma2.png",
            cv2.cvtColor(gauss_sigma2, cv2.COLOR_RGB2BGR))

# ===================================================
# (b) k-trimmed mean 5x5, k = 3
# ===================================================

def k_trimmed_mean(channel, k=3, size=5):
    pad = size // 2
    h, w = channel.shape
    out = np.zeros_like(channel)

    # padding (reflect gives ImageJ-like behavior)
    padded = cv2.copyMakeBorder(channel, pad, pad, pad, pad,
                                cv2.BORDER_REFLECT_101)

    for y in range(h):
        for x in range(w):
            window = padded[y:y+size, x:x+size].ravel().astype(np.float32)
            window.sort()

            trimmed = window[k: size*size - k]  # remove k lowest & highest
            out[y, x] = np.mean(trimmed)

    return out.astype(np.uint8)

# Split channels
r = img[:, :, 0]
g = img[:, :, 1]
b = img[:, :, 2]

# Apply k-trimmed-mean to each channel
r_f = k_trimmed_mean(r, k=3, size=5)
g_f = k_trimmed_mean(g, k=3, size=5)
b_f = k_trimmed_mean(b, k=3, size=5)

# Merge back into RGB
ktrimmed = np.dstack([r_f, g_f, b_f])

# Save
cv2.imwrite("spadochron_ktrimmed_5x5_k3.png",
            cv2.cvtColor(ktrimmed, cv2.COLOR_RGB2BGR))

print("Wszystko gotowe!")
print("Zapisane pliki:")
print(" - spadochron_mean_5x5.png")
print(" - spadochron_gauss_sigma2.png")
print(" - spadochron_ktrimmed_5x5_k3.png")
