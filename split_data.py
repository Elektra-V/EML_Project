import os
import spacy
import random

# Load spaCy model for better POS tagging and dependency parsing
nlp = spacy.load("en_core_web_sm")

# Paths
INPUT_FILE = "/home/vedika-chauhan/Documents/EML/Project/popper_main/sentences.txt"
OUTPUT_DIR = "."
BK_FILE = os.path.join(OUTPUT_DIR, "bk.pl")

def get_pos_tag(token):
    """Convert spaCy POS tags to simplified tags."""
    pos_map = {
        'NOUN': 'noun',
        'PROPN': 'propn',
        'VERB': 'verb',
        'ADJ': 'adj',
        'ADV': 'adv',
        'PRON': 'pronoun',
        'DET': 'det',
        'ADP': 'prep',
        'PUNCT': 'punct',
        'NUM': 'num'
    }
    return pos_map.get(token.pos_, token.pos_.lower())

def clean_word(word):
    """Clean a word for Prolog compatibility."""
    return word.lower().replace("'", "").replace('"', "").strip('.,!?')

def analyze_sentence(doc, sent_id):
    """
    Analyze sentence structure using spaCy.
    Returns subject, verb, object, modifiers, and POS tags.
    """
    structure = {
        'subjects': set(),    
        'verbs': set(),      
        'objects': set(),   
        'modifiers': set(), 
        'pos_tags': set() 
    }
    
    for token in doc:
        clean = clean_word(token.text)
        if not clean:
            continue
            
        # Add POS tag
        structure['pos_tags'].add((clean, get_pos_tag(token)))
        
        # Find subject
        if token.dep_ in ('nsubj', 'nsubjpass'):
            structure['subjects'].add(clean)
            
        # Find verbs
        elif token.pos_ == 'VERB':
            structure['verbs'].add(clean)
            
        # Find objects
        elif token.dep_ in ('dobj', 'pobj', 'obj'):
            structure['objects'].add(clean)
            
        # Find modifiers
        if token.dep_ in ('amod', 'advmod') and token.head.text:
            structure['modifiers'].add((clean_word(token.head.text), clean))
            
    return structure

def write_background_knowledge(sentences):
    """Write the background knowledge file with enhanced grammatical structure."""
    with open(BK_FILE, "w") as bk:
        # Write headers
        bk.write("""% Enable discontiguous predicates
:- discontiguous sentence/1.
:- discontiguous word_pos/2.
:- discontiguous has_subject/2.
:- discontiguous has_verb/2.
:- discontiguous has_object/2.
:- discontiguous has_modifier/2.

""")

        # Track all unique words and their POS tags
        all_pos_tags = set()
        
        # First pass: Analyze all sentences
        sentence_structures = {}
        for sent_id, sentence in sentences:
            doc = nlp(sentence)
            sentence_structures[sent_id] = analyze_sentence(doc, sent_id)
            all_pos_tags.update(sentence_structures[sent_id]['pos_tags'])

        # Write sentence declarations
        bk.write("% Sentence declarations\n")
        for sent_id, _ in sentences:
            bk.write(f"sentence({sent_id}).\n")
        bk.write("\n")

        # Write subject relationships
        bk.write("% Subject relationships\n")
        for sent_id, struct in sentence_structures.items():
            for subj in sorted(struct['subjects']):  # Sort for consistent output
                bk.write(f"has_subject({sent_id}, '{subj}').\n")
        bk.write("\n")

        # Write verb relationships
        bk.write("% Verb relationships\n")
        for sent_id, struct in sentence_structures.items():
            for verb in sorted(struct['verbs']):  # Sort for consistent output
                bk.write(f"has_verb({sent_id}, '{verb}').\n")
        bk.write("\n")

        # Write object relationships
        bk.write("% Object relationships\n")
        for sent_id, struct in sentence_structures.items():
            for obj in sorted(struct['objects']):  # Sort for consistent output
                bk.write(f"has_object({sent_id}, '{obj}').\n")
        bk.write("\n")

        # Write modifier relationships
        bk.write("% Modifier relationships\n")
        for sent_id, struct in sentence_structures.items():
            for head, modifier in sorted(struct['modifiers']):  # Sort for consistent output
                bk.write(f"has_modifier('{head}', '{modifier}').\n")
        bk.write("\n")

        # Write POS tags
        bk.write("% Word POS tags\n")
        for word, pos in sorted(all_pos_tags):  # Sort for consistent output
            bk.write(f"word_pos('{word}', {pos}).\n")
        bk.write("\n")

        # Write full sentence word positions (keep these as they should show position)
        bk.write("% Full sentences in word_pos format\n")
        seen_word_pos = set()  # Track unique word_pos combinations
        for sent_id, sentence in sentences:
            words = [w for w in sentence.split() if clean_word(w)]
            for word in words:
                clean = clean_word(word)
                if clean:
                    word_pos_key = (sent_id, clean)
                    if word_pos_key not in seen_word_pos:
                        bk.write(f"word_pos({sent_id}, '{clean}').\n")
                        seen_word_pos.add(word_pos_key)
            bk.write("\n")

def read_sentences(file_path):
    """Read sentences from file and return a list of (id, sentence)."""
    sentences = []
    with open(file_path, "r") as f:
        for line in f:
            parts = line.strip().split(": ", 1)
            if len(parts) == 2:
                sent_id, sentence = parts
                sentences.append((sent_id.strip(), sentence.strip()))
    return sentences

if __name__ == "__main__":
    sentences = read_sentences(INPUT_FILE)
    if not sentences:
        print("No valid sentences found in sentences.txt!")
    else:
        print(f"Found {len(sentences)} sentences, generating background knowledge...")
        write_background_knowledge(sentences)
        print("\n Generated background knowledge file: bk.pl")
        print("\n Now you can manually create exs.pl with positive and negative examples")