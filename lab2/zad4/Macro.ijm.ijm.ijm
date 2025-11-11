// Podaj ścieżki:
open("/Users/lukaszkulpaczynski/Desktop/V-semester/algorytmy-przetwarzania-obrazow-cyfrowych/Algorytmy/lab2/zad4/osaRGB_PNG.png"); rename("REF");
open("/Users/lukaszkulpaczynski/Desktop/V-semester/algorytmy-przetwarzania-obrazow-cyfrowych/Algorytmy/lab2/zad4/osaRGB_JPG.jpg"); rename("JPG");
open("/Users/lukaszkulpaczynski/Desktop/V-semester/algorytmy-przetwarzania-obrazow-cyfrowych/Algorytmy/lab2/zad4/osaRGB_GIF.gif"); rename("GIF");

// --- Ustawienia ---
run("Set Measurements...", "mean");
setBatchMode(true);

// ——— Funkcje pomocnicze ———
function ensureRGB(title) {
  selectWindow(title);
  run("RGB Color"); // bezpieczne nawet jeśli już RGB
}

function splitChannels(prefix) {
  // Jeśli już są rozdzielone – wyjdź
  if (isOpen(prefix+"_R") && isOpen(prefix+"_G") && isOpen(prefix+"_B")) return;

  selectWindow(prefix);
  run("Split Channels"); // tworzy: prefix (red|green|blue)

  // Teraz jawnie wybieramy i nazywamy
  selectWindow(prefix + " (red)");   rename(prefix + "_R");
  selectWindow(prefix + " (green)"); rename(prefix + "_G");
  selectWindow(prefix + " (blue)");  rename(prefix + "_B");
}

function mseBetween(a_ch, b_ch) {
  // różnica^2 i średnia = MSE kanału
  run("Image Calculator...", "operation=Subtract image1="+a_ch+" image2="+b_ch+" create");
  run("Square");
  run("Measure");
  v = getResult("Mean", nResults-1);
  close(); // zamknij okno różnicy^2
  return v;
}

function mseRGB(aPrefix, bPrefix) {
  // policz MSE dla R,G,B i uśrednij
  r = mseBetween(aPrefix+"_R", bPrefix+"_R");
  g = mseBetween(aPrefix+"_G", bPrefix+"_G");
  b = mseBetween(aPrefix+"_B", bPrefix+"_B");
  return (r+g+b)/3.0;
}

// ——— Główna logika ———
ensureRGB("REF"); ensureRGB("JPG"); ensureRGB("GIF");
splitChannels("REF");
splitChannels("JPG");
splitChannels("GIF");

mse_jpg = mseRGB("REF","JPG");
mse_gif = mseRGB("REF","GIF");

setBatchMode(false);
print("MSE JPG vs PNG: " + mse_jpg);
print("MSE GIF vs PNG: " + mse_gif);

if (mse_jpg < mse_gif)
  print("Lepsza wg MSE: JPEG");
else if (mse_gif < mse_jpg)
  print("Lepsza wg MSE: GIF");
else
  print("Remis wg MSE.");
