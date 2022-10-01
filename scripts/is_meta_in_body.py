# Find files which have Gutenberg meta (license) inside a text body

import os

for root, dirs, files in os.walk('../TeDDi/Corpus'):
    for file in files:
        if 'fic' in file:
            path_file = os.path.join(root, file)
            with open(path_file, 'r') as f:
                for line in f:
                    if 'GUTENBERG' in line:
                        print('\item ' + file.replace('_', '\_'))