import numpy as np
from PIL import Image

def two_nearest_average_resize(img: Image.Image, new_w: int, new_h: int) -> Image.Image:
    # na wejściu RGB lub L; na wyjściu RGB/L
    arr = np.array(img)
    if arr.ndim == 2:  # L
        arr = arr[..., None]  # (H,W,1)

    h_in, w_in, c = arr.shape
    out = np.zeros((new_h, new_w, c), dtype=np.float32)

    # skala tak, aby rogi mapowały się na rogi (unikanie przesunięcia pół-piksela)
    sx = (w_in - 1) / (new_w - 1) if new_w > 1 else 0.0
    sy = (h_in - 1) / (new_h - 1) if new_h > 1 else 0.0

    for y_out in range(new_h):
        y_src = y_out * sy
        y0 = int(np.floor(y_src))
        y1 = int(np.ceil(y_src))
        y0 = max(0, min(h_in - 1, y0))
        y1 = max(0, min(h_in - 1, y1))

        for x_out in range(new_w):
            x_src = x_out * sx
            x0 = int(np.floor(x_src))
            x1 = int(np.ceil(x_src))
            x0 = max(0, min(w_in - 1, x0))
            x1 = max(0, min(w_in - 1, x1))

            # cztery kandydaty (x0/y0; x1/y0; x0/y1; x1/y1)
            candidates = [
                (x0, y0),
                (x1, y0),
                (x0, y1),
                (x1, y1),
            ]
            # odległości euklidesowe w przestrzeni współrzędnych źródłowych
            dists = []
            for (xx, yy) in candidates:
                dx = x_src - xx
                dy = y_src - yy
                dists.append(np.hypot(dx, dy))

            # indeksy dwóch najbliższych pikseli
            two_idx = np.argsort(dists)[:2]
            (x_a, y_a) = candidates[two_idx[0]]
            (x_b, y_b) = candidates[two_idx[1]]

            # średnia dwóch najbliższych (per-channel)
            out[y_out, x_out, :] = 0.5 * (arr[y_a, x_a, :].astype(np.float32) +
                                          arr[y_b, x_b, :].astype(np.float32))

    out = np.clip(out + 0.5, 0, 255).astype(np.uint8)  # zaokrąglenie i zakres
    if c == 1:
        out = out[..., 0]
        mode = "L"
    else:
        mode = "RGB"
    return Image.fromarray(out, mode)

if __name__ == "__main__":
    # 1) wczytaj obraz
    img = Image.open("potworek_pixelart.png").convert("RGB")  # 50×65

    # 2) przeskaluj wg wariantu (b)
    result = two_nearest_average_resize(img, 500, 650)

    # 3) zapisz wynik
    result.save("potworek_b_two_nearest.png")
    print("Zapisano: potworek_b_two_nearest.png")
