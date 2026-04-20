import board
import busio
import digitalio
import storage
import adafruit_sdcard
import audiobusio
import audiomp3
import touchio
import time
import os

# 1. Setup SPI for MicroSD (Use your pins)
# Wiring: SCK=D37, MOSI=D36, MISO=D35, CS=D34
spi = busio.SPI(board.D37, MOSI=board.D36, MISO=board.D35)
cs = digitalio.DigitalInOut(board.D34)

# Try to mount the SD card
try:
    sdcard = adafruit_sdcard.SDCard(spi, cs)
    vfs = storage.VfsFat(sdcard)
    storage.mount(vfs, "/sd")
    print("SD Card Mounted!")
except Exception as e:
    print("SD Card not found or wiring issue:", e)

# 2. Setup Audio (Your specific pins)
audio = audiobusio.I2SOut(bit_clock=board.D12, word_select=board.D10, data=board.D11)

# 3. Plant Monitor (A1)
plant = touchio.TouchIn(board.A1)

def play_song(filename):
    try:
        with open("/sd/" + filename, "rb") as f:
            decoder = audiomp3.MP3Decoder(f)
            audio.play(decoder)
            while audio.playing:
                # Distortion/Skipping logic based on moisture
                if plant.value: # Placeholder for moisture logic
                    time.sleep(0.05) 
    except Exception as e:
        print("Play error:", e)

print("System Ready.")
while True:
    # Look for files on the SD card
    if "sd" in os.listdir("/"):
        songs = [f for f in os.listdir("/sd") if f.endswith(".mp3")]
        for song in songs:
            play_song(song)
    time.sleep(1)
