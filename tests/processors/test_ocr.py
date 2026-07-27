from pathlib import Path

from src.processors.ocr.ocr_processor import OCRProcessor

ocr = OCRProcessor(["en"])

image = Path("data/frames/sample/frame_00000.jpg")

result = ocr.extract_text(image)

print()

print("Detected Text")

print("----------------")

print(result["text"])

print()

print("Confidence:", result["confidence"])