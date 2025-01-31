import whisper
import os

def transcribe_audio(audio_path, output_path, model="base"):

    model = whisper.load_model(model)
    result = model.transcribe(audio_path)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w") as f:
        f.write(result["text"])


audio_dir = "/home/vedika-chauhan/Documents/EML/Project/wav_files/"
transcripts_dir = "/home/vedika-chauhan/Documents/EML/Project/transcripts/"
os.makedirs(transcripts_dir, exist_ok=True)

for audio_file in os.listdir(audio_dir):
    if audio_file.endswith(".wav"):
        output_path = os.path.join(transcripts_dir, audio_file.replace(".wav", ".txt"))
        if not os.path.exists(output_path):  # Skip if the transcription already exists
            print(f"Transcribing: {audio_file}")
            transcribe_audio(os.path.join(audio_dir, audio_file), output_path)
