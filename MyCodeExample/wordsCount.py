#  usage: python.exe wordsCount.py C:\XX\YY\Files C:\XX\YY\words.txt
"""
A program that receives 2 arguments:
  1. Path to words file – contains words that we need to search for, each word in the separate line.
    The same word can appear more than once, but we search for each only once.
	The search is case insensitive

  2. Path to directory – contains "text files" and subdirectories  (ignore them).
  The program will count the number of appearances of each word (from the words file) in each dest. file
  The search will be parallel (up to number of cpus parallel tasks)
  The files can be very big

"""
import multiprocessing as mp
from typing import Optional
from loggerConfig import set_file_logger
import os
import sys
import re


logger = set_file_logger(__name__, "logFile.log")


def count_word_in_file(file_path_words_tuple: tuple[str, set]) -> tuple[str, Optional[dict]]:
    """
    search in single file using dict, as data-structure
    where the words are keys and their appearance-counts are values

    :param file_path_words_tuple: tuple with 2 values:
        dest file path - to search into
        words set with all the words we are interested in searching
    :return: a pair of file path and result dict with all the counts per word
    """
    file, words = file_path_words_tuple
    words_counts = {w: 0 for w in words}

    try:
        with open(file, "r") as fo:
            for line in fo:
                line_words_list = re.split(r"[^a-zA-Z]+", line.lower())
                for line_word in line_words_list:
                    if line_word in words:
                        words_counts[line_word] += 1

        return file, words_counts  # returns tuple
    except Exception as ex:
        print(f"In file: {file}: {ex}")
        logger.error(f"In file: {file}: {ex}")
        return file, None


def check_inputs(argv: list[str]):
    """
    script arguments validations
    :param argv: arguments vector
    :return: a pair of files dir. path and words file path
    """
    if len(argv) != 3:
        raise ValueError("args. count error. Usage: wordsCount.py dir_path, words_file_path")
    dir_path = argv[1]
    if not os.path.isdir(dir_path):
        raise ValueError(f"{dir_path} must be an existing directory")
    words_file_path = argv[2]
    if not os.path.isfile(words_file_path):
        raise ValueError(f"{words_file_path} must be an existing file")
    return dir_path, words_file_path


def main():
    dir_path, words_file_path = check_inputs(sys.argv)
    file_paths = [os.path.join(dir_path, fn) for fn in os.listdir(dir_path)
                  if os.path.isfile(os.path.join(dir_path, fn))]
    print(file_paths)

    with open(words_file_path, "r") as fo:
        words = {w.rstrip().lower() for w in fo.readlines()}
        print(words)

    pool = mp.Pool(processes=mp.cpu_count())

    results = pool.map(count_word_in_file, ((file, words) for file in file_paths))
    for file, d in results:
        if d:
            print(f" ============== {file} ============")
            print(f"{d}\n\n")


if __name__ == '__main__':
    main()
