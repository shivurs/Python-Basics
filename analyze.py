import file_utils
from pathlib import Path

nr = file_utils.count_lines(Path('names.txt'))
print('Number of lines = ' + str(nr))

file_utils.filter_longer(Path('names.txt'), Path('long_names.txt'), 6)
flines = file_utils.count_lines(Path('long_names.txt'))
print('Filtered number of lines = ' + str(flines))