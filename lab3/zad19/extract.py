from PIL import Image
import numpy as np

# Wczytaj obraz
img = Image.open("stego.png").convert("L")

# Konwertuj na tablicę NumPy
arr = np.array(img)

bit = 0

# Wyciągnij bit i rozciągnij do 0/255
# rzesuwasz bity w prawo i bierzesz ostatni bit, czyli oglądasz wizualizację warstwy bitowej
bitplane = ((arr >> bit) & 1) * 255

result = Image.fromarray(bitplane.astype(np.uint8))

# Zapisz obraz
result.save(f"extracted_bit_{bit}.png")

print(f"✅ Zapisano obraz: extracted_bit_{bit}.png")
# Wygenerowano obrazy dla bitów od 0 do 7, zmieniając wartość zmiennej 'bit' powyżej.
