### Text-to-Speech App

This project is a Python-based Text-to-Speech (TTS) application built using `tkinter` for the graphical user interface (GUI) and `pygame` for audio playback.
The app allows users to input text, select a voice, adjust speech speed, and generate audio.
It also includes features like automatic sentence splitting using `pysbd`, pause functionality, and the ability to save generated audio files.

#### Setup Instructions:
1. **Clone the Repository or download the files**:
   ```bash
   git clone https://github.com/Taylor-eOS/kokoro-voice-generation
   ```

2. **Install Dependencies**:
   Ensure you have Python 3.x installed, then install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   Execute the main script to launch the app:
   ```bash
   python gui_app.py
   ```

4. **Usage**:
   - Enter or copy your text into the text box.
   - Select a voice and adjust the speed using the slider.
   - Check "Automatic sentence splitting" if you want the app to split text into sentences automatically.
   - Click "Generate" to create the audio.
   - Use the "Play/Stop" button to listen to the generated audio.
   - Save the audio using the "Save" button.
The  text window has keybound `Ctrl`+`A` for selecting all text, but inserting seems to amend to teh existing text. So delete the old text first.
This has not been tested on Windows.s

#### License:
Do as you wish.
