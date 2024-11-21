from pydub import AudioSegment
import numpy as np

# Load the original audio file
original_audio = AudioSegment.from_file("resources/sounds/violin/violin.wav")

# Define the frequencies for the A major scale spanning two octaves
# A major scale: A, B, C#, D, E, F#, G#, A (one octave above), B, C#, D, E, F#, G#, A (one octave below)
frequencies = {
    'A3': 220.00,
    'B3': 246.94,
    'C#4': 277.18,
    'D4': 293.66,
    'E4': 329.63,
    'F#4': 369.99,
    'G#4': 415.30,
    'A4': 440.00,
    'B4': 493.88,
    'C#5': 554.37,
    'D5': 587.33,
    'E5': 659.25,
    'F#5': 739.99,
    'G#5': 830.61,
    'A5': 880.00,
}

#change the pitch of the audio file semitones up or down
def change_pitch(audio, semitones):
    new_sample_rate = int(audio.frame_rate * (2.0 ** (semitones / 12.0)))
    return audio._spawn(audio.raw_data, overrides={'frame_rate': new_sample_rate}).set_frame_rate(audio.frame_rate)

# Calculate the pitch shift for each note and create new audio files
original_frequency = frequencies['A4']
for note, freq in frequencies.items():
    semitones = 12 * np.log2(freq / original_frequency)
    new_audio = change_pitch(original_audio, semitones)
    new_audio.export(f"resources/sounds/violin/{note}.wav", format="wav")
    print(f"Created {note}.wav")

