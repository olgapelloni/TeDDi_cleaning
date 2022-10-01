# Rename files after removing; make new running numbers in the whole directory

import os
import re
import shutil

path1 = '../Teddi/Corpus/Thai_tha/non-fiction/written1/'
path2 = '../Teddi/Corpus/Thai_tha/non-fiction/written2/'

i = 1
for root, dirs, files in os.walk(path1):
    for file in files:
        number = re.search('[0-9]+', file)
        if number:
            found_number = number.group(0)
            new_file = file.replace(str(found_number), str(i))
            print(file, new_file)
            shutil.move(path1 + file, path2 + new_file)
            i += 1
