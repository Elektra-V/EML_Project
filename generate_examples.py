import os
import spacy
import re


MAX_SENTENCES = 100
TRANSCRIPT_DIR = "transcripts"
OUTPUT_DIR = "popper_main"

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# Define contractions to expand
CONTRACTIONS = {
    "I'm": "I am", "I've": "I have", "don't": "do not", "can't": "cannot",
    "won't": "will not", "didn't": "did not", "it's": "it is",
    "he's": "he is", "she's": "she is", "we're": "we are", "they're": "they are",
    "you'll": "you will", "he'll": "he will", "she'll": "she will"
}

def clean_text(text):
    """Clean text to ensure Prolog compatibility."""
    text = text.strip().lower()
    
    # Expand contractions
    words = text.split()
    words = [CONTRACTIONS[word] if word in CONTRACTIONS else word for word in words]
    text = " ".join(words)

    # Remove special characters except underscores
    text = re.sub(r"[^a-zA-Z0-9_]", "", text)

    return text

def is_valid_sentence(sent):
    """Check if a sentence is valid for processing."""
    words = [token.text for token in sent]
    return (len(sent) >= 3 and
            any(token.pos_ == "VERB" for token in sent) and
            any(token.dep_ == "nsubj" for token in sent))

def generate_sentences():
    """Generate a file containing valid sentences with their sentence IDs."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    sentences_path = os.path.join(OUTPUT_DIR, "sentences.txt")

    with open(sentences_path, "w") as sentences_file:
        sentence_id = 1
        processed = 0

        for filename in os.listdir(TRANSCRIPT_DIR):
            if not filename.endswith(".txt"):
                continue

            print(f"\nProcessing file: {filename}")

            with open(os.path.join(TRANSCRIPT_DIR, filename), "r") as file:
                content = file.read()
                doc = nlp(content)

                for sent in list(doc.sents):
                    if processed >= MAX_SENTENCES:
                        break

                    if not is_valid_sentence(sent):
                        continue

                    sent_id = f"s{sentence_id}"
                    sentences_file.write(f"{sent_id}: {sent.text.strip()}\n")
                    
                    sentence_id += 1
                    processed += 1

                print(f"Processed {processed} valid sentences from {filename}.")

            if processed >= MAX_SENTENCES:
                break

    print(f"\n✅ File generated in {OUTPUT_DIR}/sentences.txt")
    print("\n⚡ Review `sentences.txt`, and we'll manually split it into `bk.pl` and `exs.pl`.")

if __name__ == "__main__":
    print("Generating valid sentences...")
    generate_sentences()
    print("\nDone.")
