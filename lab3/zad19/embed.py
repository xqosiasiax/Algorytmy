from PIL import Image
import numpy as np


cover_path = "AlbertEinstein-modified.png"
secret_path = "secret.jpg"
output_path = "stego.png"

cover = Image.open(cover_path).convert("RGB")
secret = Image.open(secret_path).convert("L")

# Dopasuj rozmiar secret
secret = secret.resize(cover.size)

# Zamień secret na 0 i 1
secret = np.array(secret)
binary_secret = (secret > 128).astype(np.uint8)

# Obraz do tablicy numpy
cover_array = np.array(cover)

for channel in range(3): #usuwa ostatni bit i wstawia ostani bit jak w ukrytym
    cover_array[:, :, channel] = (cover_array[:, :, channel] // 2 * 2) + binary_secret



stego = Image.fromarray(cover_array)
stego.save(output_path)

print("✅ Gotowe! Ukryty obraz zapisany jako stego.png")
