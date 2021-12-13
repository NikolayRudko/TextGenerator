import random

import re

from collections import Counter

from nltk import WhitespaceTokenizer

from nltk.util import trigrams

class TextGenerator:

    def __init__(self, data: str):

        self.data = data

        self.trigrams_dict = self.create_trigrams_dict()

    def create_trigrams_dict(self):

        # find trigrams

        words = WhitespaceTokenizer().tokenize(self.data)

        trigrams_list = list(trigrams(words))

        trigrams_dict = {}

        for head_first, head_second, end in trigrams_list:

            head = ' '.join([head_first, head_second])

            trigrams_dict.setdefault(head, []).append(end)

        trigrams_dict = {k: Counter(v) for k, v in trigrams_dict.items()}

        return trigrams_dict

    def generate_pseudo_sentence(self) -> str:

        result_list = []

        first_word_template = r"^[A-Z]{1}[^\.\!\?]*?$"

        end_sentence_template = r"^.*[\.\!\?]$"

        # find start of words

        while True:

            head = random.choice(list(self.trigrams_dict.keys()))

            first_word = head.split()[0]

            if re.match(first_word_template, first_word):

                break

        result_list.extend(head.split())

        while True:

            ends = self.trigrams_dict[head]

            end = random.choices(list(ends.keys()), weights=ends.values())[0]

            result_list.append(end)

            if len(result_list) >= 5 and re.match(end_sentence_template, end):

                break

            head = " ".join(result_list[-2:])

        return ' '.join(result_list)

    def print_pseudo_text(self, count: int) -> None:

        for i in range(count):

            print(self.generate_pseudo_sentence())

def main() -> None:

    file_name = input()

    # file_name = 'corpus.txt'

    with open(file_name, 'r', encoding="utf-8") as file:

        data = file.read()

    text_generator = TextGenerator(data)

    text_generator.print_pseudo_text(10)

if __name__ == "__main__":

    main()
