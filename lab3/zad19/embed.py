from PIL import Image
import numpy as np

# Pliki
cover_path = "AlbertEinstein-modified.png"
secret_path = "secret.jpg"
output_path = "stego.png"

# Wczytaj obrazy
cover = Image.open(cover_path).convert("RGB")
secret = Image.open(secret_path).convert("L")

# Dopasuj rozmiar secret
secret = secret.resize(cover.size)

# Zamień secret na 0 i 1
secret = np.array(secret)
binary_secret = (secret > 128).astype(np.uint8)

# Obraz do tablicy numpy
cover_array = np.array(cover)

# Wpisanie secret do LSB wszystkich kanałów
for channel in range(3):
    cover_array[:, :, channel] = (cover_array[:, :, channel] // 2 * 2) + binary_secret


# Zapisz stego-obraz
stego = Image.fromarray(cover_array)
stego.save(output_path)

print("✅ Gotowe! Ukryty obraz zapisany jako stego.png")
