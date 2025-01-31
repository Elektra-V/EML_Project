# Learning Semantic Grammar Rules From ASR

A system that learns grammar rules from Automatic Speech Recognition (ASR) transcripts using Inductive Logic Programming (ILP).

## Overview
This project combines Whisper ASR with ILP to extract and validate grammatical rules from speech transcriptions. The system converts speech to text, processes it through NLP pipelines, and learns first-order logic rules using the Popper ILP system.

## Requirements
- Python 3.8+
- SpaCy (en_core_web_sm)
- Whisper AI
- Popper ILP system
- LibriSpeech dataset

## Pipeline Components
1. Data Processing
   - LibriSpeech Clean Dataset → Whisper ASR
   - Text cleaning and formatting
   - Grammar structure extraction

2. ILP System
   - Background knowledge generation (bk.pl)
   - Example creation (exs.pl)
   - Bias constraints (bias.pl)

## Usage
```bash
# Add Popper
git submodule add git@github.com:logic-and-learning-lab/Popper.git Project/Popper
# Process audio files
python trascribe.py

# Generate background knowledge
python split_data.py

# Run Popper
python3 Popper/popper.py popper_main --debug
```

## Results
- Precision: 1.00
- Recall: 0.60
- Accuracy: 80%

## Limitations
- Computational complexity with large datasets
- Speech vs written grammar differences
- Trade-off between formalization and authenticity
