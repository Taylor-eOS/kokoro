from kokoro import KPipeline
import soundfile as sf
import numpy as np

# Global settings
LANG_CODE = 'a' #'a'merican or 'b'ritish
VOICE = 'am_eric'
#us male: am_adam, am_echo, am_eric, am_fenrir, am_liam, am_michael, am_onyx, am_puck
#us female: af_alloy, af_aoede, af_bella, af_heart, af_jessica, af_kore, af_nicole, af_nova, af_river, af_sarah, af_sky 	
#british: bf_alice, bf_emma, bf_isabella, bf_lily, bm_daniel, bm_fable, bm_george, bm_lewis
SPEED = 1.0
SPLIT_PATTERN = r'\n+'
SAMPLE_RATE = 24000

def generate_audio(text):
    pipeline = KPipeline(lang_code=LANG_CODE)
    generator = pipeline(text, voice=VOICE, speed=SPEED, split_pattern=SPLIT_PATTERN)
    audio_segments = []
    for i, (gs, ps, audio) in enumerate(generator):
        print(f"Processing segment {i}: {gs}")
        audio_segments.append(audio)
    return np.concatenate(audio_segments)

def save_audio(audio, filename):
    sf.write(filename, audio, SAMPLE_RATE)

def process_text_to_audio(input_file='input.txt', output_file='output.wav'):
    with open(input_file, 'r') as file:
        text = file.read()
    combined_audio = generate_audio(text)
    save_audio(combined_audio, output_file)

process_text_to_audio()
