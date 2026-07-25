from src.processors.audio.audio_extractor import AudioExtractor
from src.processors.whisper.transcriber import WhisperTranscriber

audio = AudioExtractor.extract("sample.mp4")

transcriber = WhisperTranscriber()

result = transcriber.transcribe(audio)

print(result["text"])