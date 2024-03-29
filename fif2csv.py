#!/usr/bin/env python

"""
Take .fif-file(s) from the parsed arguments and save the channel data as csv (see also --help)
"""

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
parser.add_argument('--format' '--fmt', default='%.6e', dest='format',
                    help="Format used in numpy's savetxt(fmt=...). Has to be a valid format string!")
parser.add_argument('--replace_type', '-nap', default=False, action='store_true',
                    help="Replace original file extension with [output_type]")
parser.add_argument('--no_times', '-nt', default=False, action='store_true',
                    help='If used as an argument, no header with the times in seconds is prepended')
parser.add_argument('--transpose', '-t', default=False, action='store_true',
                    help="Transpose the data such that time is in columns. Puts the time into rows by default")
parser.add_argument('--no_header', '-nh', default=False, action='store_true',
                    help="Store a header for each column (Time, Sensor name(s)). Only if transpose is not set")

args = parser.parse_args()
logger.info(f"Parsed arguments: {args}")

# Do the slow imports only after the parsing was successful
import mne
import numpy as np

# Iterate over all files listed by the user
for filename in args.filenames:
    logger.info(f"Reading data for {filename}")
    raw = mne.io.read_raw_fif(filename)

    data = raw.get_data()

    header = None
    # If the user wants the time points to be in the first row of the csv
    if not args.no_times:
        data = np.insert(data, 0, raw.times, axis=0)

    if not args.transpose:
        data = data.T

    if args.no_header or args.transpose:
        header = ''
    else:
        # Append the list of channel names to the header
        header = []
        if not args.no_times:
            header += ["T [s]"]
        header += raw.info.ch_names
        header = args.delimiter.join(header)


    # Replace the original file extension in for the output filename
    if args.replace_type:
        out_filename = f"{os.path.splitext(filename)[0]}.{args.output_type}"
    else:
        out_filename = f"{filename}.{args.output_type}"

    np.savetxt(out_filename, data, delimiter=args.delimiter, fmt=args.format, newline=args.newline, header=header)
    logger.info(f"Saved data into {out_filename}")