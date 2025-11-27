import numpy as np
import matplotlib.pyplot as plt

alpha = -1/3

# Funkcja hiperbolicznego wzmocnienia kontrastu
def H_hyper(g, alpha=alpha):
    """
    Funkcja hiperboliczna:
    H(g) = 255 / (1 - e^{-α}) * (1 - e^{-α g / 255})
    """
    g = np.array(g, dtype=np.float64)
    return 255 / (1 - np.exp(-alpha)) * (1 - np.exp(-alpha * g / 255))


# ===============================================
# 1. Obliczenia dla g = 40, 45, 50
# ===============================================

values = [40, 45, 50]
results = {g: H_hyper(g) for g in values}
# ==============================================
# 2. Wyświetlanie wyników
# ==============================================
print("Wyniki hiperbolizacji H_hyper(g) dla α = -1/3:\n")
for g, val in results.items():
    print(f"g = {g:3d} → H_hyper(g) = {val:.4f}")