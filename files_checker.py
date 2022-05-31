# Check whether the SFX files are valid: only one sound can play at a time

import os

for filename in os.listdir("./data/sfx-info"):
    with open(f'./data/sfx-info/{filename}') as file:
        lines = file.readlines()
        # lines = [l.strip() for l in lines if l.strip() != str()]

        sound_start = False
        for i, line in enumerate(lines):
            if line.startswith("[SOUND_START]"):
                if sound_start:
                    print(f"{filename}, line", i+1)
                    exit()
                sound_start = True

            if line.startswith("[SOUND_STOP]"):
                sound_start = False
