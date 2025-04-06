import os
import pygame

class SoundPlayer:
    scales = ("C", "D", "E", "G", "A", "B", "F#", "C#", "Ab", "Eb", "Bb", "F")
    modes = ("Major", "Minor")
    def __init__(self, sounds_folder = "resources/sounds", scale = "C", mode = "Major"):
        pygame.mixer.init()

        self.scale = scale
        self.mode = mode

        self.sounds_folder = sounds_folder
        self.channels = {0: pygame.mixer.Channel(0), 1: pygame.mixer.Channel(1)}
        self.sounds = {
            "violin": self.load_sounds("violin", scale, mode),
            "flute": self.load_sounds("flute", scale, mode),
            "snareDrum": self.load_sounds("snareDrum", scale, mode),
            "trumpet": self.load_sounds("trumpet", scale, mode),
            "generic": self.load_sounds("generic", scale, mode),
            "none": []
        }
        
        self.current_sounds = [self.sounds["none"], self.sounds["none"]]
        self.current_notes = [None, None]

    def load_sounds(self, instrument, scale = "C", mode = "Major"):
        # if instrument == "snareDrum":
        #     folder = os.path.join(self.sounds_folder, instrument)
        #     sounds = []
        #     for i in range(6):
        #         path = os.path.join(folder, str(i) + ".wav")
        #         if os.path.exists(path):
        #             sounds.append(([str(i)], pygame.mixer.Sound(path)))
        #         else:
        #             print("File not found: " + path)
        #     return sounds
        
        notes = self.get_notes(scale, mode)
        folder = os.path.join(self.sounds_folder, instrument)
        sounds = []
        for i in range(10):
            for note in notes:
                path = os.path.join(folder, note + str(i) + ".wav")
                if os.path.exists(path):
                    sounds.append(([note + str(i)], pygame.mixer.Sound(path)))
        return sounds
    
    def play_sound(self, note, channel):
        channel.play(note, loops=-1, fade_ms=200)

    def stop_sound(self, channel):
            channel.fadeout(1000)

    def get_note(self, center_x, width, sounds):
        if sounds:
            note_index = int(center_x / (width / len(sounds)))
            return sounds[min(note_index, len(sounds) - 1)][1]
        return None

    def set_volume(self, channel, center_y, height):
        channel.set_volume(1 - center_y / height)
    
    def set_scale(self, scale, mode):

        self.scale = scale
        self.mode = mode

        self.sounds["violin"] = self.load_sounds("violin", scale, mode)
        self.sounds["flute"] = self.load_sounds("flute", scale, mode)
        self.sounds["snareDrum"] = self.load_sounds("snareDrum", scale, mode)
        self.sounds["trumpet"] = self.load_sounds("trumpet", scale, mode)
        self.sounds["generic"] = self.load_sounds("generic", scale, mode)
    
    # get_notes returns the notes of a scale in a given mode
    def get_notes(self, scale, mode) -> list:
        major = {
            "C": ["C", "D", "E", "F", "G", "A", "B"],
            "D": ["D", "E", "F#", "G", "A", "B", "C#"],
            "E": ["E", "F#", "G#", "A", "B", "C#", "D#"],
            "G": ["G", "A", "B", "C", "D", "E", "F#"],
            "A": ["A", "B", "C#", "D", "E", "F#", "G#"],
            "B": ["B", "C#", "D#", "E", "F#", "G#", "A#"],
            "F#": ["F#", "G#", "A#", "B", "C#", "D#", "F"],
            "C#": ["C#", "D#", "F", "F#", "G#", "A#", "C"],
            "Ab": ["G#", "A#", "C", "C#", "D#", "F", "G"],
            "Eb": ["D#", "F", "G", "G#", "A#", "C", "D"],
            "Bb": ["A#", "C", "D", "D#", "F", "G", "A"],
            "F": ["F", "G", "A", "A#", "C", "D", "E"]
        }

        minor = {
            "C": ["C", "D", "D#", "F", "G", "G#", "A#"],
            "D": ["D", "E", "F", "G", "A", "A#", "C"],
            "E": ["E", "F#", "G", "A", "B", "C", "D"],
            "G": ["G", "A", "A#", "C", "D", "D#", "F"],
            "A": ["A", "B", "C", "D", "E", "F", "G"],
            "B": ["B", "C#", "D", "E", "F#", "G", "A"],
            "F#": ["F#", "G#", "A", "B", "C#", "C", "D#"],
            "C#": ["C#", "D#", "E", "F#", "G#", "A", "B"],
            "Ab": ["G#", "A#", "B", "C#", "D#", "E", "F#"],
            "Eb": ["D#", "F", "F#", "G#", "A#", "B", "C#"],
            "Bb": ["A#", "C", "C#", "D#", "F", "F#", "G#"],
            "F": ["F", "G", "G#", "A#", "C", "C#", "D#"]
        }

        if scale not in major:
            print("Error getting scale")
            return []

        scale_notes = major[scale]
        if mode == "Minor":
            scale_notes = minor[scale]

        #Make C or C charp first in the list
        if "C" in scale_notes:
            while scale_notes[0] != "C":
                scale_notes.append(scale_notes.pop(0))
        elif "C#" in scale_notes:
            while scale_notes[0] != "C#":
                scale_notes.append(scale_notes.pop(0))

        return scale_notes
    
    def get_note_names(self, scale, mode) -> list:
        major = {
            "C": ["C", "D", "E", "F", "G", "A", "B"],
            "D": ["D", "E", "F#", "G", "A", "B", "C#"],
            "E": ["E", "F#", "G#", "A", "B", "C#", "D#"],
            "G": ["G", "A", "B", "C", "D", "E", "F#"],
            "A": ["A", "B", "C#", "D", "E", "F#", "G#"],
            "B": ["B", "C#", "D#", "E", "F#", "G#", "A#"],
            "F#": ["F#", "G#", "A#", "B", "C#", "D#", "E#"],
            "C#": ["C#", "D#", "E#", "F#", "G#", "A#", "B#"],
            "Ab": ["Ab", "Bb", "C", "Db", "Eb", "F", "G"],
            "Eb": ["Eb", "F", "G", "Ab", "Bb", "C", "D"],
            "Bb": ["Bb", "C", "D", "Eb", "F", "G", "A"],
            "F": ["F", "G", "A", "Bb", "C", "D", "E"]
        }

        minor = {
            "C": ["C", "D", "Eb", "F", "G", "Ab", "Bb"],
            "D": ["D", "E", "F", "G", "A", "Bb", "C"],
            "E": ["E", "F#", "G", "A", "B", "C", "D"],
            "G": ["G", "A", "Bb", "C", "D", "Eb", "F"],
            "A": ["A", "B", "C", "D", "E", "F", "G"],
            "B": ["B", "C#", "D", "E", "F#", "G", "A"],
            "F#": ["F#", "G#", "A", "B", "C#", "D", "E"],
            "C#": ["C#", "D#", "E", "F#", "G#", "A", "B"],
            "Ab": ["Ab", "Bb", "C", "Db", "Eb", "F", "G"],
            "Eb": ["Eb", "F", "G", "Ab", "Bb", "C", "Db"],
            "Bb": ["Bb", "C", "Db", "Eb", "F", "G", "Ab"],
            "F": ["F", "G", "Ab", "Bb", "C", "Db", "Eb"]
        }

        if scale not in major:
            print("Error getting scale")
            return []

        scale_notes = major[scale]
        if mode == "Minor":
            scale_notes = minor[scale]

        #Make C or C charp first in the list
        if "C" in scale_notes:
            while scale_notes[0] != "C":
                scale_notes.append(scale_notes.pop(0))
        elif "C#" in scale_notes:
            while scale_notes[0] != "C#":
                scale_notes.append(scale_notes.pop(0))

        return scale_notes

    # similar to get_notes but returns the note names with proper sharps and flats (e.g. Ab instead of G# if the scale is Ab)

    