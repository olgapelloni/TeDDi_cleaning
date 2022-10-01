# Detect multiple languages in one file

import sqlite3
from polyglot.detect import Detector

connection = sqlite3.connect('../TeDDi/Database/test.sqlite3')


# These two functions are just for exploring the database structure
# Get table schema
def sqlite_table_schema(conn, name):
    """Return a string representing the table's CREATE"""
    cursor = conn.execute("SELECT sql FROM sqlite_master WHERE name=?;", [name])
    sql = cursor.fetchone()[0]
    cursor.close()
    return sql


# Get the tables names
def get_table_names(conn):
    for row in conn.execute('SELECT name FROM sqlite_master WHERE type = "table" ORDER BY name').fetchall():
        return row


# Iterate through languages, corpora, texts and saving texts
def iterate_languages(conn, f_result):

    # Start iterating the rows in the table language

    # One language
    # cursor_language = conn.execute('SELECT id, name FROM language WHERE name LIKE "Mandarin%"')

    # All languages
    cursor_language = conn.execute("SELECT id, name FROM language")

    for row_language in cursor_language:

        print(row_language)

        # Extract language_id
        language_id = row_language[0]

        # One corpus
        cursor_corpus = conn.execute("SELECT id, name, genre_broad FROM corpus WHERE "
                                     "(language_id = " + str(language_id) + ')')

        # All corpora
        # Search for corpora available for the language_id
        # cursor_corpus = conn.execute("SELECT id, name, genre_broad FROM corpus
        # WHERE language_id = " + str(language_id))

        # Start iterating the rows in the table corpus
        for row_corpus in cursor_corpus:

            print(row_corpus)

            # Extract corpus_id
            corpus_id = row_corpus[0]

            # Search for files in the corpus
            cursor_file = conn.execute("SELECT id, filename FROM file WHERE corpus_id = " + str(corpus_id))

            # Start iterating the rows in the table file
            for row_file in cursor_file:

                print(row_file)

                # Extract file_id
                file_id = row_file[0]

                # Search for lines in the file
                cursor_line = conn.execute("SELECT id, text FROM line WHERE file_id = " + str(file_id))

                all_text = ''

                # Start iterating the rows in the table line
                for row_line in cursor_line:

                    # Print a raw text line
                    if row_line[1]:
                        all_text += row_line[1] + '\n'

                try:
                    lang1 = Detector(all_text).languages[0]
                    lang2 = Detector(all_text).languages[1]
                    lang3 = Detector(all_text).languages[2]

                    print(lang1)
                    print(lang2)
                    print(lang3)

                    if lang1.confidence < 99 and lang2.confidence >= 5:
                        f_result.write(row_file[1] + '\n')
                        f_result.write(lang1.__str__() + '\n')
                        f_result.write(lang2.__str__() + '\n')
                        f_result.write(lang3.__str__() + '\n\n')
                        print('WRITTEN')
                except:
                    pass


with open('multiple_languages.txt', 'a') as f_res:
    iterate_languages(connection, f_res)

