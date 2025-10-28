import numpy as np
from PIL import Image

def bilinear_minmax_resize(img: Image.Image, new_w: int, new_h: int) -> Image.Image:
    """
    Skalowanie 50x65 -> 500x650 (lub dowolne) wariant (d):
    dla każdego piksela wyjściowego pobierz 4 sąsiadów (x0/x1, y0/y1),
    a wartość piksela ustaw na (min + max)/2 liczone per-kanał.
    """
    arr = np.array(img)
    if arr.ndim == 2:      # obraz L (jednokanałowy)
        arr = arr[..., None]

    h_in, w_in, c = arr.shape
    out = np.zeros((new_h, new_w, c), dtype=np.float32)

    # mapowanie rogów na rogi (bez przesunięcia pół-piksela)
    sx = (w_in - 1) / (new_w - 1) if new_w > 1 else 0.0
    sy = (h_in - 1) / (new_h - 1) if new_h > 1 else 0.0

    for y_out in range(new_h):
        y_src = y_out * sy
        y0 = int(np.floor(y_src)); y1 = int(np.ceil(y_src))
        y0 = max(0, min(h_in - 1, y0))
        y1 = max(0, min(h_in - 1, y1))

        for x_out in range(new_w):
            x_src = x_out * sx
            x0 = int(np.floor(x_src)); x1 = int(np.ceil(x_src))
            x0 = max(0, min(w_in - 1, x0))
            x1 = max(0, min(w_in - 1, x1))

            # Cztery sąsiedztwa (klasyczny blok do bilinear)
            v00 = arr[y0, x0, :].astype(np.float32)
            v10 = arr[y0, x1, :].astype(np.float32)
            v01 = arr[y1, x0, :].astype(np.float32)
            v11 = arr[y1, x1, :].astype(np.float32)

            block = np.stack([v00, v10, v01, v11], axis=0)  # (4, C)
            vmin = block.min(axis=0)
            vmax = block.max(axis=0)
            out[y_out, x_out, :] = 0.5 * (vmin + vmax)

    out = np.clip(out + 0.5, 0, 255).astype(np.uint8)
    if c == 1:
        return Image.fromarray(out[..., 0], "L")
    return Image.fromarray(out, "RGB")


if __name__ == "__main__":
    # Wejście 50×65 (u Ciebie: potworek_pixelart.png)
    img = Image.open("potworek_pixelart.png").convert("RGB")

    # Docelowo 500×650 (jak w zadaniu)
    result = bilinear_minmax_resize(img, 500, 650)

    # Zapis wariantu (d)
    result.save("potworek_d_bilinear_minmax.png")
    print("Zapisano: potworek_d_bilinear_minmax.png")
