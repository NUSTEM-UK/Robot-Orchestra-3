## Wemos Light Controller

Updates neopixels synced to the note playback system, so they flash in time to the music. Or at least, they update on each note played. Almost all of the code is pulled from the earlier Wemos-based servo players. Many defunct functions have been dropped, and the servo-handling code ripped out in favour of NeoPixel access. Roughly half the development time for this component was spent in trying to debug a neopixel string which turned out to be mis-wired.

Two versions:

### player-lights

Sets entire light string to random brightness of red, green, white, or just plain random colours. The random colours look nice, but overall it's not very festive.

### player-lights2

Sets each pixel to a random brightness and a random choice of red, green or white. Which overall looks prettier, we think.