import random
import textwrap

samples = [
    "Shipment BOL-8832 is delayed at Port of LA due to customs strike. Expected release is Friday. Temp dropped to 4C.",
    "The cargo with BOL-1245 encountered a storm causing a 3‑day delay. No critical impact.",
    "BOL-3321 arrived at warehouse early, no delay.",
    "Due to a mechanical failure, BOL-4567 will be delayed by 5 days. Critical for downstream production.",
    "Customs cleared BOL-7890, expected arrival tomorrow.",
]

def generate_documents(num: int = 20):
    docs = []
    for _ in range(num):
        docs.append(random.choice(samples))
    return docs

def main():
    docs = generate_documents()
    for i, doc in enumerate(docs, 1):
        print(f"--- Document {i} ---")
        print(doc)
        print()

if __name__ == "__main__":
    main()
