# Detect non-linguistic noise

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
def iterate_languages(conn):

    with open('nonling_noise.txt', 'w') as f_res:

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
                    symbols = {}

                    # Start iterating the rows in the table line
                    for row_line in cursor_line:

                        # Print a raw text line
                        if row_line[1]:
                            all_text += row_line[1] + '\n'

                            # Count frequency of symbols
                            for symbol in row_line[1]:
                                if symbol not in symbols:
                                    symbols[symbol] = 1
                                else:
                                    symbols[symbol] += 1

                    low_freq = {}
                    for key in symbols:
                        if symbols[key] < 20:
                            low_freq[key] = symbols[key]

                    # Find sequences of 5 symbols with freq < 20
                    for i in range(len(all_text)):
                        if all_text[i] in low_freq:
                            if i == 0:
                                if (all_text[i+1] in low_freq) and (all_text[i+2] in low_freq) and\
                                        (all_text[i+3] in low_freq) and (all_text[i+4] in low_freq):
                                    low_freq_line = ''.join([all_text[i], all_text[i+1], all_text[i+2],
                                                             all_text[i+3], all_text[i+4]])
                                    print(low_freq_line)
                                    f_res.write(row_file[1] + ', ' + low_freq_line + '\n')
                            elif i == 1:
                                if (all_text[i+1] in low_freq) and (all_text[i+2] in low_freq) and\
                                        (all_text[i+3] in low_freq) and (all_text[i-1] in low_freq):
                                    low_freq_line = ''.join([all_text[i-1], all_text[i], all_text[i+1],
                                                             all_text[i+2], all_text[i+3]])
                                    print(low_freq_line)
                                    f_res.write(row_file[1] + ', ' + low_freq_line + '\n')
                            elif i > 1 and (i < len(all_text) - 1):
                                if (all_text[i+1] in low_freq) and (all_text[i+2] in low_freq) and\
                                        (all_text[i-2] in low_freq) and (all_text[i-1] in low_freq):
                                    low_freq_line = ''.join([all_text[i-2], all_text[i-1], all_text[i],
                                                             all_text[i+1], all_text[i+2]])
                                    print(low_freq_line)
                                    f_res.write(row_file[1] + ', ' + low_freq_line + '\n')
                            elif i == len(all_text) - 2:
                                if (all_text[i-1] in low_freq) and (all_text[i-3] in low_freq) and\
                                        (all_text[i-4] in low_freq) and (all_text[i-5] in low_freq):
                                    low_freq_line = ''.join([all_text[i-5], all_text[i-4],
                                                             all_text[i-3], all_text[i], all_text[i-1]])
                                    print(low_freq_line)
                                    f_res.write(row_file[1] + ', ' + low_freq_line + '\n')
                            elif i == len(all_text) - 1:
                                if (all_text[i-1] in low_freq) and (all_text[i-2] in low_freq) and\
                                        (all_text[i-3] in low_freq) and (all_text[i-4] in low_freq):
                                    low_freq_line = ''.join([all_text[i-4], all_text[i-3],
                                                             all_text[i-2], all_text[i-1], all_text[i]])
                                    print(low_freq_line)
                                    f_res.write(row_file[1] + ', ' + low_freq_line + '\n')


iterate_languages(connection)
