from sound_player import SoundPlayer

# Define the C major notes frequencies
c_major_notes = {
    'C': 261.63,
    'D': 293.66,
    'E': 329.63,
    'F': 349.23,
    'G': 392.00,
    'A': 440.00,
    'B': 493.88,
    'C_high': 523.25
}

# Initialize the sound player
player = SoundPlayer()

# Play each note in the C major scale
for note, frequency in c_major_notes.items():
    print(f"Playing {note} at {frequency} Hz")
    player.play_tone(frequency, duration=1.0)  # Play each note for 1 second