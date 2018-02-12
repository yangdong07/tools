
import os
import textract

from collections import Counter


def is_english_word(word):
    return word.isalpha()


def extract_words(filename, threshold=20):
    text = textract.process(filename)
    words = filter(is_english_word, text.split())
    counter = Counter(words)

    wc = [(c, w) for w, c in counter.items() if c < threshold]
    wc.sort(reverse=True)
    basename = os.path.basename(filename)
    output_filename = 'words_' + basename.rsplit('.', 1)[0] + '.txt'
    with open(output_filename, 'w') as f:
        for c, w in wc:
            f.write(str(c) + ' ' + w.decode('ascii') + '\n')

if __name__ == '__main__':
    # extract_words('Python4DataAnalysis.pdf')
    extract_words('/Users/yangdong/Study/Documents/book/DeepLearningBook.pdf')