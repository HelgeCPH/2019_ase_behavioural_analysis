import sys
import string
from tqdm import tqdm
from pprint import pprint
from textblob import TextBlob
from collections import Counter
from nltk.corpus import stopwords


def prepare_data_nlp(path):
    all_words = []
    with open(path, encoding="utf-8") as fp:
        lines = fp.readlines()

    non_lemmatizable_tags = (
        "TO",
        "DT",
        "IN",
        "CC",
        "CD",
        "POS",
        "FW",
        "WRB",
        "PRP",
        "PRP$",
        "WDT",
        "MD",
        "RP",
        "EX",
        "WP",
        "PDT",
        "UH",
        "SYM",
        "WP$",
        "LS",
    )
    lemmatizable_tags = set([])

    for line in tqdm(lines):
        commit_msg = TextBlob(line)
        for word, tag in commit_msg.tags:
            if tag not in non_lemmatizable_tags:
                new_word = word.lemmatize(tag)
                all_words.append(new_word)
                lemmatizable_tags.add(tag)
            else:
                all_words.append(word)
    return all_words


def prepare_data_simple(path):
    """Remove punctuation characters from words and split into words."""
    with open(path, encoding="utf-8") as fp:
        data = fp.read()

    trans_table = str.maketrans({key: None for key in string.punctuation})
    new_data = data.translate(trans_table)
    words = new_data.split()
    return words


def prepare_data(path, kind="simple"):
    if kind == "simple":
        return prepare_data_simple(path)
    elif kind == "nlp":
        return prepare_data_nlp(path)
    else:
        raise NotImplementedError("Use either kind `simple` or `nlp`.")


def all_to_lower(words):
    return [w.lower() for w in tqdm(words)]


def remove_stopwords(words):
    english_stopwords = stopwords.words("english")
    filtered_freqs = {
        w: f for w, f in tqdm(words.items()) if w not in english_stopwords
    }
    return filtered_freqs


def main(path_to_file, kind="simple", all_lower=True, no_stopwords=True):
    print("Reading data...")
    words = prepare_data(path_to_file, kind)
    if all_lower:
        print("Lowering cases...")
        words = all_to_lower(words)
    print("Counting frequencies...")
    word_freqs = Counter(words)
    if no_stopwords:
        print("Removing stopwords...")
        word_freqs = remove_stopwords(word_freqs)
    return word_freqs


if __name__ == "__main__":
    if len(sys.argv) > 2:
        kind = sys.argv[2]
    else:
        kind = "simple"

    freqs = main(sys.argv[1], kind=kind)
    freqs_sorted = sorted(freqs.items(), key=lambda el: el[1])
    for word, freq in list(reversed(freqs_sorted))[:50]:
        print(freq, word)
