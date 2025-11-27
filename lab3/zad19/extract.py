from PIL import Image
import numpy as np

# Wczytaj obraz
img = Image.open("stego.png").convert("L")
# Konwertuj na tablicę NumPy
arr = np.array(img)

# który bit chcesz sprawdzić (0 = LSB)
bit = 0

# Wyciągnij bit i rozciągnij do 0/255
bitplane = ((arr >> bit) & 1) * 255

# Zapisz wynik
result = Image.fromarray(bitplane.astype(np.uint8))

# Zapisz obraz
result.save(f"extracted_bit_{bit}.png")

print(f"✅ Zapisano obraz: extracted_bit_{bit}.png")