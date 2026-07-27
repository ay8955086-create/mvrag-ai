from pathlib import Path

from src.processors.caption.caption_generator import CaptionGenerator

generator = CaptionGenerator()

caption = generator.generate_caption(
    Path("data/frames/sample/frame_00000.jpg")
)

print()
print("Caption")
print("----------------")
print(caption)