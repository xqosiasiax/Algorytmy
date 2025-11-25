import cv2
import numpy as np
from skimage.filters import threshold_otsu


img = cv2.imread("kwiatki.png", 0)   

# a) Globalne progowanie Otsu

T = threshold_otsu(img) #obliczenie progu
global_bin = np.where(img > T, 255, 0).astype(np.uint8)  #T>0 przyjmuja 255(biały) a T<=0 0 (czarny)

cv2.imwrite("a_otsu_global.png", global_bin)

print(f"(a) Próg Otsu = {T}")


# b) Poprawione iteracyjne trójklasowe progowanie (Otsu)


T = threshold_otsu(img) #Na początku wyznaczam globalny próg Otsu dla całego obrazu Dzieli on obraz wstępnie na dwa zbiory pikseli:

delta = 999
while delta >= 2: #Delta mówi o ile zmienił się próg między iteracjami jest to warunek dzialania algorytmu 

    g0 = img[img <= T]  #g0 – piksele o jasności mniejszej lub równej T
    g1 = img[img > T]   #g1 – piksele o jasności większej od T

    if len(g0) == 0 or len(g1) == 0:
        break

    T0 = threshold_otsu(g0) #tutaj ich progi
    T1 = threshold_otsu(g1)

    T_new = (T0 + T1) / 2 
    delta = abs(T_new - T)
    T = T_new


three_class = np.zeros_like(img, dtype=np.uint8)


three_class[img <= T0] = 0 #ciemne mniejsze od T0
three_class[(img > T0) & (img <= T1)] = 127 #średnie 
three_class[img > T1] = 255 #jasne

cv2.imwrite("b_otsu_three_class.png", three_class)

print(f"(b) T0 = {T0:.2f}, T1 = {T1:.2f}, Δ = {delta:.2f}")


# c) Lokalny Otsu (okno 11x11 + odbicie symetryczne)


h, w = img.shape #zastosowano padding zeby uzyskac 11x11 okno
pad = 5  # (11x11) => 2*5+1

padded = np.pad(img, pad, mode='reflect')
local_bin = np.zeros_like(img)

for y in range(h):
    for x in range(w):
        window = padded[y:y+11, x:x+11] #dla kazdego piksela jest pobierane jego lokalne okno 
        t_local = threshold_otsu(window) # i obliczany lokalny prog dla kazdego osobny LOKALNIE a nie GLOBLNIE JAK W A
        local_bin[y, x] = 255 if img[y, x] > t_local else 0 #jesli jasnosc > progu to 255 (biały) a else 0

cv2.imwrite("c_otsu_local_11x11.png", local_bin)

print("(c) Zapisano lokalne progowanie 11x11 (symetryczne odbicie)")
