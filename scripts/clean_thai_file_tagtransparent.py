# Clean Thai files from a tag

with open('../TeDDi/Corpus/Thai_tha/non-fiction/written1/tha_nfi_46.txt', 'r') as f:
    with open('../TeDDi/Corpus/Thai_tha/non-fiction/written1/tha_nfi_46_copy.txt', 'w') as f1:
        for line in f:
            if '/c.bg_transparent' in line and 'c.bg_transparent' in line:
                new_line = line.replace('/c.bg_transparent', '')
                new_line = new_line.replace('c.bg_transparent', '')
            elif '/c.bg_transparent' in line:
                new_line = line.replace('/c.bg_transparent', '')
            elif 'c.bg_transparent' in line:
                new_line = line.replace('c.bg_transparent', '')
            else:
                new_line = line
            f1.write(new_line)
