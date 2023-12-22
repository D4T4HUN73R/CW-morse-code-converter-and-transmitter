import simpleaudio as sa
import numpy as np
import time

# International (ITU) Morse Code with Numbers
morse_code = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
    'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
    'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
    'Y': '-.--', 'Z': '--..',
    
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....',
    '7': '--...', '8': '---..', '9': '----.'
}

# converts any text input to morse code chars
def convert_to_morse_code(text):
    morse_text = ""
    for char in text.upper():
        if char in morse_code:
            morse_text += morse_code[char] + " "
        elif char == " ":
            morse_text += " / "
    return morse_text.rstrip()

# plays the 800 Hz tone
def play_tone(duration, frequency=800, sampling_rate=44100):
    t = np.linspace(0, duration, int(duration * sampling_rate), False)
    waveform = np.sin(frequency * t * 2 * np.pi)
    audio = waveform * (2**15 - 1) / np.max(np.abs(waveform))
    audio = audio.astype(np.int16)
    play_obj = sa.play_buffer(audio, 1, 2, sampling_rate)
    play_obj.wait_done()

# transmits the morse code with 800 Hz tones as dots (0.1) and dashes (three times a dot tone)
def transmit(morse_text):
    dot_tone = 0.1
    dash_tone = dot_tone * 3
    for char in morse_text:
        if char == ".":
            play_tone(dot_tone, 800)
        elif char == "-":
            play_tone(dash_tone, 800)
        elif char == " ":
            time.sleep(dot_tone * 3) # space between the letters
        elif char == "/":
            time.sleep(dot_tone * 7) # space between the words

if __name__ == '__main__':
    message = input("Input your morse text in normal letters: ")
    morse_text = convert_to_morse_code(message)
    print("Sound on, we'll transmit your morse code now!")
    print(f"Original: {message}")
    print(f"Morse Code: {morse_text}")
    transmit(morse_text)
