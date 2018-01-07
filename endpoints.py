import os
import sys
import sample


def main(dst_file_path):
    with open(dst_file_path, "r") as fp:
        seq = fp.read()
        sys.stdout.write(seq)
        sys.stdout.write(seq)

        words = seq.split(" ")
        main_word = ' '
        if len(words) == 0:
            sys.stderr.write("Incorrect words input\n")
        else:
            main_word = words[0]

        result_articles = sample.proc_main(main_word=main_word)

        return {main_word: result_articles}
