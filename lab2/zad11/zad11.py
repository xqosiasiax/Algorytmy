import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# === 1. Wczytanie obrazu ===
img = Image.open("stripe.png").convert("L")  # grayscale
img = np.array(img, dtype=np.float32) / 255.0
N = img.shape[0]
print(f"Obraz: {img.shape}, zakres: {img.min()}–{img.max()}")

# === 2. FFT ===
F = np.fft.fft2(img)
Fshift = np.fft.fftshift(F)  # zero w centrum

# === 3. Funkcja do ograniczania widma (maski kołowe) ===
def reconstruct_with_radius(r):
    cy, cx = N // 2, N // 2
    Y, X = np.ogrid[:N, :N]
    mask = (X - cx) ** 2 + (Y - cy) ** 2 <= r ** 2  # koło o promieniu r
    Ftrunc = np.zeros_like(Fshift)
    Ftrunc[mask] = Fshift[mask]
    rec = np.fft.ifft2(np.fft.ifftshift(Ftrunc)).real
    rec = (rec - rec.min()) / (rec.max() - rec.min() + 1e-9)
    return rec

# === 4. Dwie rekonstrukcje (dwie długości szeregu) ===
radii = [10, 50]  # mało i dużo harmonicznych
recs = [reconstruct_with_radius(r) for r in radii]

# === 5. Zapisz obrazy rekonstrukcji ===
for r, rec in zip(radii, recs):
    Image.fromarray((rec * 255).astype(np.uint8)).save(f"rekonstrukcja_r{r}.png")

# === 6. Profil poziomy (przez środek) ===
y = N // 2
x = np.arange(N)
ref_profile = img[y, :]
profiles = [rec[y, :] for rec in recs]

# === 7. Wykresy profili ===
plt.figure(figsize=(8,5))
plt.plot(x, ref_profile, 'k-', label='oryginał')
plt.plot(x, profiles[0], 'r--', label=f'rekonstrukcja r={radii[0]}')
plt.plot(x, profiles[1], 'b-', label=f'rekonstrukcja r={radii[1]}')
plt.title('Profile liniowe – efekt Gibbsa')
plt.xlabel('pozycja [piksele]')
plt.ylabel('jasność')
plt.legend()
plt.tight_layout()
plt.savefig('profile_gibbs.png', dpi=150)
plt.show()

print("✅ Zapisano: rekonstrukcja_r10.png, rekonstrukcja_r50.png, profile_gibbs.png")
