"""Run me with pythonw
$ pythonw wordcloud_gen.py FreeBSD11_1_0_commit_msgs.txt nlp
"""
import os
import sys
import word_freq
import matplotlib.pyplot as plt
from wordcloud import WordCloud


def get_random_color(
    word=None,
    font_size=None,
    position=None,
    orientation=None,
    font_path=None,
    random_state=None,
):
    h = int(360.0 * 45.0 / 255.0)
    s = int(100.0 * 255.0 / 255.0)
    l = int(100.0 * float(random_state.randint(60, 120)) / 255.0)

    return f"hsl({h}, {s}%, {l}%)"


def generate_plot(word_freqs, amount_of_words="all", width=1200, height=1000):
    if amount_of_words != "all":
        amount_of_words = int(amount_of_words)
        wordcloud = WordCloud(
            width=width,
            height=height,
            max_words=amount_of_words,
            color_func=get_random_color,
        )
    else:
        wordcloud = WordCloud(
            width=width, height=height, color_func=get_random_color
        )

    wordcloud_img = wordcloud.generate_from_frequencies(word_freqs)
    return wordcloud_img


def save_plot(outfname, wordcloud_img, show=False):
    plt.axis("off")
    plt.imshow(wordcloud_img)
    plt.savefig(outfname, dpi=300)
    if show:
        plt.show()


def count_words(path_to_file, kind="simple"):
    word_freqs = word_freq.main(path_to_file, kind=kind)
    return word_freqs


def main(path_to_file, kind="simple", amount_of_words="all"):
    word_freqs = count_words(path_to_file, kind=kind)
    img = generate_plot(
        word_freqs, amount_of_words=amount_of_words, width=1200, height=1000
    )
    fname = os.path.basename(path_to_file)
    out_path = os.path.join("out", fname.replace(".txt", ".png"))
    save_plot(out_path, img)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        kind = sys.argv[2]
    else:
        kind = "simple"
    main(sys.argv[1], kind=kind)
