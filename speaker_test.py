from kokoro import KPipeline
import soundfile as sf
import numpy as np
import os
import shutil

speed = 1.0

voice_groups = {
    'am': ['am_adam', 'am_echo', 'am_eric', 'am_fenrir', 'am_liam', 'am_michael', 'am_onyx', 'am_puck', 'am_santa'],
    'af': ['af_alloy', 'af_aoede', 'af_bella', 'af_heart', 'af_jessica', 'af_kore', 'af_nicole', 'af_nova', 'af_river', 'af_sarah', 'af_sky'],
    'bf': ['bf_alice', 'bf_emma', 'bf_isabella', 'bf_lily'],
    'bm': ['bm_daniel', 'bm_fable', 'bm_george', 'bm_lewis'],
}

group_labels = {
    'am': 'American Male',
    'af': 'American Female',
    'bm': 'British Male',
    'bf': 'British Female',
}

SAMPLE_RATE = 24000

def pick_voice_group():
    print("\nAvailable voice groups:")
    for key, label in group_labels.items():
        voices = voice_groups[key]
        print(f"  [{key}] {label} — {len(voices)} voices: {', '.join(voices)}")
    print()
    while True:
        choice = input("Pick a voice group (am / af / bm / bf): ").strip().lower()
        if choice in voice_groups:
            return choice
        print(f"Invalid choice '{choice}'. Please enter one of: am, af, bm, bf")

def generate_audio(text, speaker_voice='am_michael', voice_speed=speed):
    pipeline = KPipeline(lang_code=speaker_voice[0])
    generator = pipeline(text, voice=speaker_voice, speed=voice_speed, split_pattern=None)
    audio_segments = []
    for i, (gs, ps, audio) in enumerate(generator):
        audio_segments.append(audio)
        print(f"Generated segment {i+1} for {speaker_voice}: {gs}")
    silence = np.zeros(SAMPLE_RATE, dtype=np.float32)
    audio_segments.append(silence)
    return np.concatenate(audio_segments)

def save_audio(audio, filename):
    sf.write(filename, audio, SAMPLE_RATE)

def prepare_output_folder(group):
    folder = f"voices_{group}"
    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.makedirs(folder)
    return folder

def generate_group_speakers(text, group):
    folder = prepare_output_folder(group)
    for speaker in voice_groups[group]:
        try:
            print(f"\nGenerating audio for {speaker}...")
            audio = generate_audio(text, speaker_voice=speaker)
            filename = os.path.join(folder, f"{speaker}.wav")
            save_audio(audio, filename)
            print(f"Saved: {filename}")
        except Exception as e:
            print(f"Error processing {speaker}: {str(e)}")

def process_text_to_audio():
    group = pick_voice_group()
    text = input("Enter sample sentence (default): ") or "Human nature is not defined outside of transactions involving other humans."
    if not text:
        raise ValueError("Input text is empty")
    generate_group_speakers(text, group)

if __name__ == '__main__':
    process_text_to_audio()
