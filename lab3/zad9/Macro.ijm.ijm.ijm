macro "Apply custom LUT" {
    n = 256;
    reds   = newArray(n);
    greens = newArray(n);
    blues  = newArray(n);

    for (x = 0; x < n; x++) {

        // --- kanał BLUE (niebieski) ---
        if (x <= 64)
            b = x/64*64;                     // 0 -> 64
        else if (x <= 128)
            b = (128-x)/64*64;               // 64 -> 0
        else
            b = (x-128)/(255-128)*255;       // 0 -> 255

        // --- kanał RED (czerw=ony) ---
        if (x <= 64)
            r = 0;
        else if (x <= 128)
            r = (x-64)/64*128;               // 0 -> 128
        else if (x <= 192)
            r = (192-x)/64*128;              // 128 -> 0
        else
            r = (x-192)/(255-192)*255;       // 0 -> 255

        // --- kanał GREEN (zielony) ---
        if (x <= 128)
            g = 0;
        else if (x <= 192)
            g = (x-128)/64*255;              // 0 -> 255
        else
            g = 255;                         // 255 -> 255 (stały)

        reds[x]   = round(r);
        greens[x] = round(g);
        blues[x]  = round(b);
    }

    // ustaw LUT dla aktualnego obrazu
    Color.setLut(reds, greens, blues);
}
