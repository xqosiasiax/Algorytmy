import cv2
import numpy as np
import os

def global_contrast(img_gray):
    """Oblicza kontrast globalny (odchylenie standardowe jasności)."""
    return np.std(img_gray)

def local_contrast(img_gray):
    """Oblicza średni kontrast lokalny (8 sąsiadów)."""
    kernel = np.array([[1,1,1],
                       [1,0,1],
                       [1,1,1]], dtype=np.float32)
    
    mean_neighbors = cv2.filter2D(img_gray.astype(np.float32), -1, kernel/8)
    local_diff = np.abs(img_gray - mean_neighbors)
    return np.mean(local_diff)

# --- główny program ---
folder = '.'  # jeśli obrazy są w tym samym folderze co skrypt
files = ['tygrysA.png', 'tygrysB.png', 'tygrysC.png']

for f in files:
    path = os.path.join(folder, f)
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f'❌ Nie znaleziono pliku: {f}')
        continue

    cg = global_contrast(img)
    cl = local_contrast(img)

    print(f'📷 {f}:')
    print(f'   Kontrast globalny: {cg:.2f}')
    print(f'   Kontrast lokalny:  {cl:.2f}')
    print()
