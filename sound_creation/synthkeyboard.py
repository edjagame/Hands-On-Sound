import pygame
import os

# Initialize pygame mixer
pygame.mixer.init()
pygame.display.init()
pygame.display.set_mode((1, 1))

notes = ["A3", "B3", "C#4", "D4", "E4", "F#4", "G#4", "A4", "B4", "C#5", "D5", "E5", "F#5", "G#5", "A5"]
sounds_folder = "resources/sounds"
def load_sounds(instrument):
    folder = os.path.join(sounds_folder, instrument)
    sounds = {}
    for note in notes:
        path = os.path.join(folder, note + ".wav")
        if os.path.exists(path):
            sounds[note] = pygame.mixer.Sound(path)
        else:
            print(f"File not found: {path}")
    return sounds

sounds = load_sounds("violin")
print("Press the corresponding keys to play violin notes (e.g., A, S, D). Predss ESC to quit.")

key_to_note = {
    pygame.K_a: "A3",
    pygame.K_s: "B3",
    pygame.K_d: "C#4",
    pygame.K_f: "D4",
    pygame.K_g: "E4",
    pygame.K_h: "F#4",
    pygame.K_j: "G#4",
    pygame.K_k: "A4",
    pygame.K_l: "B4",
    pygame.K_z: "C#5",
    pygame.K_x: "D5",
    pygame.K_c: "E5",
    pygame.K_v: "F#5",
    pygame.K_b: "G#5",
    pygame.K_n: "A5"
}

def play_sound(key):
    note = key_to_note.get(key)
    if note in sounds:
        sounds[note].play(loops=-1, fade_ms=500)
        

def stop_sound(key):
    note = key_to_note.get(key)
    if note in sounds:
        sounds[note].fadeout(500)

running = True
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            else:
                play_sound(event.key)
        if event.type == pygame.KEYUP:
            stop_sound(event.key)

pygame.quit()
