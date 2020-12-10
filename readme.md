# fif2csv
This is a simple python script to save .fif-files as .csv-files.
It takes several command line arguments to customize the formatting and delimiters.
The first row contains the time points as given by the raw.times (on by default)

Due to the less efficient encoding, the output files can be up to ~8 times larger than the input files.

## Requirements
- [numpy](https://numpy.org/)
- [mne-python](https://mne.tools/stable/index.html#)

## Usage
### Linux
```
fif2csv.py [-h] [--delimiter DELIMITER] [--newline NEWLINE]
                  [--output_type OUTPUT_TYPE] [--format--fmt FORMAT]
                  [--replace_type] [--no_times]
                  filenames [filenames ...]

Easily convert .fif-files to csv-files

positional arguments:
  filenames             Names of the files to convert

optional arguments:
  -h, --help            show this help message and exit
  --delimiter DELIMITER, -d DELIMITER
                        Delimiter used
  --newline NEWLINE, -n NEWLINE
                        Character used for new lines
  --output_type OUTPUT_TYPE, -ot OUTPUT_TYPE
  --format--fmt FORMAT  Format used in numpy's savetxt(fmt=...). Has to be a
                        valid format string!
  --replace_type, -nap  Replace original file extension with [output_type]
  --no_times, -nt       If used as an argument, no header with the times in
                        seconds is prepended
```

### Windows
See Linux, but on Windows you might need to explicitly state which interpreter should be used:
```shell
python.exe fif2csv.py [-h] ... filenames [filenames ...]
```

#### Example usage
```shell
python.exe fif2csv.py recording.fif
```