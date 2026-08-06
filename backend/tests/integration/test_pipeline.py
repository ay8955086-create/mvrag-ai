from src.pipeline.video_pipeline import VideoPipeline


pipeline = VideoPipeline()

result = pipeline.process("sample.mp4")


print("=" * 70)
print("METADATA")
print("=" * 70)
print(result["metadata"])


print("\n" + "=" * 70)
print("TRANSCRIPT")
print("=" * 70)
print(result["transcript"]["text"][:300])


print("\n" + "=" * 70)
print("FRAMES")
print("=" * 70)
print("Total Frames :", len(result["frames"]))


print("\n" + "=" * 70)
print("OCR SAMPLE")
print("=" * 70)
print(result["ocr"][0])


print("\n" + "=" * 70)
print("CAPTION SAMPLE")
print("=" * 70)
print(result["captions"][0])


print("\n" + "=" * 70)
print("CHUNK SUMMARY")
print("=" * 70)
print("Total Chunks :", len(result["chunks"]))


if result["chunks"]:

    chunk = result["chunks"][0]

    print("\nChunk Index :", chunk.chunk_index)

    print("\nStart :", chunk.start_time)

    print("\nEnd :", chunk.end_time)

    print("\nTranscript\n")
    print(chunk.transcript)

    print("\nOCR\n")
    print(chunk.ocr_text)

    print("\nCaption\n")
    print(chunk.caption)

    print("\nCombined Text\n")
    print(chunk.combined_text)