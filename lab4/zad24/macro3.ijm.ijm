// =====================
// VAN–CITTERT DECONVOLUTION (SAFE VERSION)
// =====================

// --- LOWPASS KERNEL (5×5 BINOMIAL) ---
kernel = "1 4 6 4 1 "
       + "4 16 24 16 4 "
       + "6 24 36 24 6 "
       + "4 16 24 16 4 "
       + "1 4 6 4 1";

// --- LOAD INPUT ---
selectImage("wiewiorka_filtered.png");
rename("input");

// --- SAFE VAN–CITTERT ITERATION ---
function VC_step(curName, origName, iter) {

    // 1. Blur current estimate
    selectImage(curName);
    run("Duplicate...", "title=blur_" + iter);
    selectImage("blur_" + iter);
    run("Convolve...", "text=[" + kernel + "] normalize");

    // 2. Error = original - blurred
    imageCalculator("Subtract create", origName, "blur_" + iter);
    rename("err_" + iter);

    // 3. New = current + error
    imageCalculator("Add create", curName, "err_" + iter);
    rename("new_" + iter);

    return "new_" + iter;
}

// --- ITERATIONS ---
iterArr = newArray(2, 5, 15);

// --- MAIN LOOP ---
for (ii = 0; ii < iterArr.length; ii++) {

    // Start from input for each run
    selectImage("input");
    run("Duplicate...", "title=est_0");
    current = "est_0";

    // Perform Van-Cittert iterations safely
    for (k = 1; k <= iterArr[ii]; k++) {
        current = VC_step(current, "input", k);
    }

    // Rename final result
    finalName = "VC_k" + iterArr[ii];
    selectImage(current);
    rename(finalName);

    // Create symmetric difference
    imageCalculator("Subtract create", finalName, "input");
    run("Abs");
    rename("diff_k" + iterArr[ii]);
}

print("DONE – generated VC_k2, VC_k5, VC_k15, diff_k2, diff_k5, diff_k15");
