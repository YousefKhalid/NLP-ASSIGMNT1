## Yousef Khalid Alturki
## 440013537
## 171

import re
import nltk
import os
from collections import Counter
import string

# Read in the corpus of plain text in Arabic
with open('aa1.txt', 'r', encoding='utf-8') as f:
    text = f.read()
# Preprocess the text to remove any unwanted characters or punctuation
text = re.sub(r'[^\w\s]','',text)

def generate_sentence():
    n = int(input("Enter n-gram value (2-6): ")) # User input for n-gram value
    max_words = int(input("Enter maximum number of words in sentence: ")) # Maximum number of words in generated sentence
    start_word = input("Enter starting word: ") # Starting word for generated sentence
    # Tokenize corpus into words
    tokens = nltk.word_tokenize(text)
    # Generate n-grams
    ngrams = list(nltk.ngrams(tokens, n))
    # Calculate frequency distribution of n-grams and sort them in descending order
    freq_dist = nltk.FreqDist(ngrams)
    sorted_ngrams = sorted(freq_dist.items(), key=lambda x: x[1], reverse=True)
    # Generate sentence
    sentence = start_word
    current_words = sentence.split()
    while len(current_words) < n and len(current_words) > 0:
        # If the starting word contains fewer words than n, append words until length n is reached
        # Choose next word with highest frequency
        next_words = []
        for ngram, freq in sorted_ngrams:
            if ngram[:len(current_words)] == tuple(current_words):
                next_words.append(ngram[len(current_words)])
        if not next_words:
            break
        # Select next word with the highest frequency
        next_word = max(next_words, key=lambda w: next_words.count(w))
        sentence += " " + next_word
        current_words.append(next_word)
    if len(current_words) == n:
        for i in range(max_words - n):
            # Get list of possible next words based on current words
            next_words = []
            for ngram, freq in sorted_ngrams:
                if ngram[:-1] == tuple(current_words[-(n-1):]):
                    next_words.append(ngram[-1])
            # If no next words found, try with shorter prefix
            while not next_words and len(current_words) > n:
                current_words = current_words[1:]
                for ngram, freq in sorted_ngrams:
                    if ngram[:-1] == tuple(current_words[-(n-1):]):
                        next_words.append(ngram[-1])
            # If still no next words found, break out of loop
            if not next_words:
                break
            # Select next word with the highest frequency
            next_word = max(next_words, key=lambda w: next_words.count(w))
            sentence += " " + next_word
            current_words.append(next_word)
    print(sentence)
#################################
def generate_sentence2():
    # Define sentences to use for n-gram model
    sentences = nltk.sent_tokenize(text)
    # Ask user for value of n (between 2-6)
    n = int(input("Enter the value of n for the N-gram model (2-6): "))
    if n < 2 or n > 6:
        print("Value of n must be between 2-6")
        return
    # Ask user for number of words in desired sentence
    num_words = int(input("Enter number of words in desired sentence: "))
    # Create empty dictionary to store ngrams and their frequency
    ngram_dict = {}
    # Loop through sentences in corpus
    for sentence in sentences:
        # Tokenize sentence into words
        words = nltk.word_tokenize(sentence)
        # Use ngrams() function to generate ngrams from words
        for gram in nltk.ngrams(words, n):
            # Convert ngram tuple to string and add to dictionary
            ngram = " ".join(gram[:-1])
            if ngram in ngram_dict:
                ngram_dict[ngram].append(gram[-1])
            else:
                ngram_dict[ngram] = [gram[-1]]
    # Ask user for previous words
    prev_words = input(f"Enter {n-1} previous words separated by spaces: ").strip().split()
    if len(prev_words) != n-1:
        print(f"Expected {n-1} words, but received {len(prev_words)}")
        return
    # Function to predict next word based on previous words
    def predict_next_word(prev_words):
        # Convert previous words to string and look up in ngram model
        ngram = " ".join(prev_words)
        if ngram in ngram_dict:
            # Get all possible choices
            choices = ngram_dict[ngram]
            # Filter choices to only include words longer or equal to n
            candidate_words = [word for word in choices if len(word) >= n]
            # If there are no candidate words, use all choices
            if not candidate_words:
                candidate_words = choices
            # Count frequency of each candidate word
            freq_dict = {}
            for word in candidate_words:
                freq_dict[word] = choices.count(word)
            # Choose candidate word with highest frequency
            next_word = max(freq_dict, key=freq_dict.get)
        else:
            print("\nNo prediction available")
            return None
        return next_word
    # Generate sentence using predicted next words
    sentence = " ".join(prev_words)
    for i in range(num_words-n+1):
        next_word = predict_next_word(prev_words)
        if next_word is None:
            print("Unable to generate sentence! ")
            return
        sentence += f" {next_word}"
        prev_words.pop(0)
        prev_words.append(next_word)
    # Print generated sentence
    print("Generated sentence:", sentence)
def process_text_files():
    # Step 1: Traverse directory tree and merge all text files into one
    merged_text = ""
    folder_path = "/Users/usef/Desktop/NLP ASSIGMNET/Yousef Khalid Alturki-440013537/Corpus"
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    merged_text += f.read()
    # Step 2: Preprocess text by removing punctuation, numbers, and symbols
    translator = str.maketrans("", "", string.punctuation + string.digits + "‘’“”")
    merged_text = merged_text.translate(translator)
    # Step 3: Tokenize text into trigrams
    tokens = nltk.word_tokenize(merged_text)
    trigrams = list(nltk.trigrams(tokens))
    # Step 4: Count frequency of each trigram
    trigram_counts = Counter(trigrams)
    # Step 5: Sort trigrams by frequency
    sorted_trigrams = sorted(trigram_counts.items(), key=lambda x: x[1], reverse=True)
    # Step 6: Select top 10 most frequent trigrams
    top_10_trigrams = sorted_trigrams[:10]
    # Write results to file
    with open("top_10trigrams.txt", "w") as f:
        for trigram, count in top_10_trigrams:
            f.write(f"{trigram}: {count}\n")

if __name__ == "__main__":
    user_input = input("\n1)Enter 1 for generate text from one word or more\n2)Enter 2 for generate next word based on previous words\n3)Enter 3 to print most 10 trigram frequncy in a text file \nEnter Number: ")
    if user_input == "1":
        generate_sentence()
    elif user_input == "2":
        generate_sentence2()
    elif user_input == "3":
        process_text_files()
    else:
        print("Invalid input. Please enter 1, 2 or 3.")