#!/usr/bin/env python

import os
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

import argparse

parser = argparse.ArgumentParser(description='Easily convert .fif-files to csv-files')
parser.add_argument('filenames', nargs='+', help='Names of the files to convert')
parser.add_argument('--delimiter', '-d', default=';', help='Delimiter used')
parser.add_argument('--newline', '-n', default='\n', help="Character used for new lines")
parser.add_argument('--output_type', '-ot', default='csv')
parser.add_argument('--format' '--fmt', default='%.18e', dest='format',
                    help="Format used in numpy's savetxt(fmt=...). Has to be a valid format string!")
parser.add_argument('--replace_type', '-nap', default=False, action='store_true',
                    help="Replace original file extension with [output_type]")
parser.add_argument('--no_times', '-nt', default=False, action='store_true',
                    help='If used as an argument, no header with the times in seconds is prepended')

args = parser.parse_args()
logger.info(f"Parsed arguments: {args}")

# Do the slow imports only after the parsing was successful
import mne
import numpy as np

for filename in args.filenames:
    logger.info(f"Reading data for {filename}")
    raw = mne.io.read_raw_fif(filename)

    data = raw.get_data()

    if not args.no_times:
        data = np.insert(data, 0, raw.times, axis=0)

    if args.replace_type:
        out_filename = f"{os.path.splitext(filename)[0]}.{args.output_type}"
    else:
        out_filename = f"{filename}.{args.output_type}"

    np.savetxt(out_filename, data, delimiter=args.delimiter, fmt=args.format, newline=args.newline)
    logger.info(f"Saved data into {out_filename}")