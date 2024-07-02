##############################################################################
##################### Get vocabulary memory wise #############################
##############################################################################

import os
import pandas as pd
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Load data from CSV files
data = pd.read_csv("../data/queries_dev_train.csv", sep=",", header=None, names=["query_idx", "text"])

# Initialize a set to store the vocabulary
vocabulary = set()

# Process each text using spaCy
for doc in nlp.pipe(data['text'], batch_size=3000, n_process=5):
    for token in doc:
        # Only include ____ tokens 
        if token.pos_ not in ("SYM", "PUNCT", "X", "NUM"):
            vocabulary.add(token.text.lower())

# Convert the set to a sorted list
vocabulary = sorted(vocabulary)

# Convert the list to a DataFrame
vocabulary_df = pd.DataFrame(vocabulary, columns=["word"])

# Save the vocabulary to a CSV file
output_dir = "../data/"
output_file = os.path.join(output_dir, "vocabulary_queries_dev_train.csv")
vocabulary_df.to_csv(output_file, index=False)

print(f"Vocabulary saved to {output_file}")
