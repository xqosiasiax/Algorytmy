# zad15B.py
# Ordered dithering (Bayer 4x4) redukujący szarość do 5 poziomów {0,64,128,192,255}
# Wynik zapisuje się jako zad15B.png

from PIL import Image
import numpy as np
import argparse
import math

# macierz Bayera 4x4 (0..15)
BAYER_4x4 = np.array([
    [ 0,  8,  2, 10],
    [12,  4, 14,  6],
    [ 3, 11,  1,  9],
    [15,  7, 13,  5],
], dtype=np.float32)

def ordered_dither_bayer(img_gray: Image.Image, palette):
    """Dithering Bayera 4x4 do zadanej palety szarości."""
    pal = np.array(sorted(set(int(v) for v in palette)), dtype=np.float32)
    L = pal.size
    if L < 2:
        raise ValueError("Paleta musi mieć co najmniej 2 poziomy.")

    I = np.array(img_gray, dtype=np.float32)
    h, w = I.shape

    step = 256.0 / L  # szerokość przedziału

    q = np.floor(I / step).astype(np.int32)
    q = np.clip(q, 0, L-1)

    tile_y = math.ceil(h / 4)
    tile_x = math.ceil(w / 4)
    Tloc = (np.tile(BAYER_4x4, (tile_y, tile_x))[:h, :w] + 0.5) / 16.0 * step

    r = I - q.astype(np.float32) * step
    inc = (r > Tloc) & (q < L-1)
    q = q + inc.astype(np.int32)

    out = pal[q]
    return Image.fromarray(out.astype(np.uint8), mode='L')

def main():
    ap = argparse.ArgumentParser(description="Bayer 4x4 dithering (zadanie 15B)")
    ap.add_argument("input", help="Ścieżka do obrazu wejściowego (np. lwy.png)")
    args = ap.parse_args()

    palette = [0, 64, 128, 192, 255]  # stała paleta dla zadania 15B
    img = Image.open(args.input).convert("L")  # konwersja do szarości
    out = ordered_dither_bayer(img, palette)
    out.save("zad15B.png")
    print("✅ Zapisano wynik jako zad15B.png")

if __name__ == "__main__":
    main()
