import math

def compute_gamma(mean_filtered, mean_target=105.546):
    # normalizacja do zakresu 0-1
    x = mean_filtered / 255.0
    y = mean_target / 255.0
    
    gamma = math.log(y) / math.log(x)
    return gamma

mean_filtered = 62.035     # wartosc z histogramu b
gamma = compute_gamma(mean_filtered)
print("Gamma =", gamma)
# Gamma = 0.6240369498992909