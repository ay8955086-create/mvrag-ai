from src.processors.frames.frame_extractor import FrameExtractor

extractor = FrameExtractor(interval_seconds=2)

frames = extractor.extract("sample.mp4")

print()

print("Frames extracted:")

for frame in frames:
    print(frame)