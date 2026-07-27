from src.pipeline.video_pipeline import VideoPipeline

pipeline = VideoPipeline()

result = pipeline.process("sample.mp4")

print("\nMetadata")
print(result["metadata"])

print("\nTranscript")
print(result["transcript"]["text"][:300])

print("\nFrames :", len(result["frames"]))

print("\nOCR Example")
print(result["ocr"][0])

print("\nCaption Example")
print(result["captions"][0])