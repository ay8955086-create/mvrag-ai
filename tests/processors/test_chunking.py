from src.processors.chunking.chunk_generator import ChunkGenerator

transcript = [
    {
        "start": 0,
        "end": 8,
        "text": "Welcome to the machine learning course."
    },
    {
        "start": 8,
        "end": 15,
        "text": "Today we study neural networks."
    }
]

ocr = [
    {
        "timestamp": 2,
        "text": "Machine Learning"
    },
    {
        "timestamp": 10,
        "text": "Neural Network"
    }
]

captions = [
    {
        "timestamp": 3,
        "caption": "A teacher standing in front of a whiteboard."
    },
    {
        "timestamp": 12,
        "caption": "Diagram of a neural network."
    }
]

generator = ChunkGenerator()

chunks = generator.generate_chunks(
    transcript,
    ocr,
    captions,
)

for chunk in chunks:

    print("=" * 60)

    print(chunk)