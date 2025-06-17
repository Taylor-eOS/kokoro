from kokoro import KPipeline
import soundfile as sf
import numpy as np

speed = 1.05
test_text = "All the gulls left the fields and spiralled silently away to the south. Cinctures of golden plover glittered round the clear zenith of the ice-blue sky."

speakers_list = [
    #US Male
    'am_adam', 'am_echo', 'am_eric', 'am_fenrir',
    'am_liam', 'am_michael', 'am_onyx', 'am_puck',
    #US Female
    'af_alloy', 'af_aoede', 'af_bella', 'af_heart',
    'af_jessica', 'af_kore', 'af_nicole', 'af_nova',
    'af_river', 'af_sarah', 'af_sky',
    #British
    'bf_alice', 'bf_emma', 'bf_isabella', 'bf_lily',
    'bm_daniel', 'bm_fable', 'bm_george', 'bm_lewis']

def generate_audio(text, speaker_voice='am_michael', voice_speed=speed):
    #Create pipeline using first character of voice ID for language code
    pipeline = KPipeline(lang_code=speaker_voice[0])
    #Process entire text as single segment (no splitting)
    generator = pipeline(text, voice=speaker_voice, speed=voice_speed, split_pattern=None)
    audio_segments = []
    for i, (gs, ps, audio) in enumerate(generator):
        audio_segments.append(audio)
        print(f"Generated segment {i+1} for {speaker_voice}: {gs}")
    return np.concatenate(audio_segments)

def save_audio(audio, filename):
    sf.write(filename, audio, 24000)

def generate_all_speakers(text):
    for speaker in speakers_list:
        try:
            print(f"\nGenerating audio for {speaker}...")
            audio = generate_audio(text, speaker_voice=speaker)
            filename = f"{speaker}.wav"
            save_audio(audio, filename)
            print(f"Saved: {filename}")
        except Exception as e:
            print(f"Error processing {speaker}: {str(e)}")

def process_text_to_audio():
    text = test_text
    if not text:
        raise ValueError("Input text is empty")
    generate_all_speakers(text)

if __name__ == '__main__':
    process_text_to_audio()

