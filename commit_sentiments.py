import csv
import sys
from textblob import TextBlob


def main(commit_msg_file):
    writer = csv.writer(sys.stdout, quoting=csv.QUOTE_ALL)
    writer.writerow(("msg", "polarity", "subjectivity"))
    with open(commit_msg_file) as fp:
        reader = csv.reader(fp)
        # Each commit message is on a line
        for idx, commit in enumerate(reader):
            try:
                commit_hash, commit_msg = commit
            except:
                print(idx)
            commit_msg = commit_msg.rstrip()
            blob = TextBlob(commit_msg)
            # https://textblob.readthedocs.io/en/dev/api_reference.html#textblob.blob.TextBlob.sentiment
            # polarity is a float within the range [-1.0, 1.0]
            # subjectivity is a float within the range [0.0, 1.0]
            # where 0.0 is very objective and 1.0 is very subjective.
            row = (
                commit_hash,
                commit_msg,
                blob.sentiment.polarity,
                blob.sentiment.subjectivity,
            )
            writer.writerow(row)


if __name__ == "__main__":
    main(sys.argv[1])
