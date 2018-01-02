# zefania2fortune

The goal of this project is to convert a Bible in Zefania XML format 
to a format for use in fortune such that each invocation of fortune will
output a single Bible verse.

## Requirements

- Python 3
- A Bible in Zefania XML format (https://sourceforge.net/projects/zefania-sharp/files/Bibles/)

## Usage
```
usage: zefania2fortune [-h] [-o OUT_DIR] [-n NAMES_FILE] [-s] [-w LINE_WIDTH]
                       in_file

Convert Zefania XML to Fortune-readable files

positional arguments:
  in_file               The input file to read. Must be in Zefania XML format.

optional arguments:
  -h, --help            show this help message and exit
  -o OUT_DIR, --outdir OUT_DIR
                        The directory to store the output files in.
  -n NAMES_FILE, --names NAMES_FILE
                        The CSV file to read the name corrections from. See
                        the provided example.
  -s, --strfile         Automatically run strfile(1) to create the .db files
                        for Fortune.
  -w LINE_WIDTH, --width LINE_WIDTH
                        The width to wrap the verses to.
```
