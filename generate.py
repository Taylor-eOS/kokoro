from kokoro import KPipeline
import soundfile as sf
import numpy as np

# 'a' => American English,  'b' => British English
pipeline = KPipeline(lang_code='a')

text = '''
At least he built the roads.
'''

generator = pipeline(
    text, voice='af_heart',
    speed=1, split_pattern=r'\n+'
)

audio_segments = []
for i, (gs, ps, audio) in enumerate(generator):
    print(f"Processing segment {i}")
    print(f'\"{gs}\"')
    audio_segments.append(audio)

# Combine all segments into one audio array
combined_audio = np.concatenate(audio_segments)
sf.write('output.wav', combined_audio, 24000)
print("Combined audio saved")

