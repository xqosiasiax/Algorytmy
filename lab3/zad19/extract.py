from PIL import Image
import numpy as np


img = Image.open("stego.png").convert("L")
arr = np.array(img)


bit = 0

# Wyciągnij bit i rozciągnij do 0/255
#rzesuwasz bity w prawo i biore ostatni bit Czyli oglądasz wizualizację warstwy bitowej
bitplane = ((arr >> bit) & 1) * 255


result = Image.fromarray(bitplane.astype(np.uint8))
result.save(f"extracted_bit_{bit}.png")

print("✅ Zapisano obraz: extracted_bit_0.png")
# Wygenerowano obrazy dla bitów od 0 do 7, zmieniając wartość zmiennej 'bit' powyżej.