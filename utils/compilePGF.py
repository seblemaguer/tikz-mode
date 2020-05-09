#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AUTHOR

     Sébastien Le Maguer <lemagues@tcd.ie>

DESCRIPTION

    Utility scripts to compile a PGF/TikZ file in a standalone

LICENSE
    This script is in the public domain, free from copyrights or restrictions.
    Created: 08 May 2020
"""

import sys
import os
import string
from subprocess import call

# Temporary
import tempfile
import shutil

# Arguments
import argparse

# Debug/Logging
import traceback
import time
import logging

LEVEL = [logging.WARNING, logging.INFO, logging.DEBUG]

###############################################################################
# Main function
###############################################################################
def main():
    """Main entry function
    """
    global args

    # Get output directory
    pgf_filename = os.path.abspath(args.pgf_filename)
    parent_directory = os.path.abspath(os.path.join(pgf_filename, os.pardir))
    output_directory = os.path.dirname(pgf_filename)
    if args.output_directory is not None:
        output_directory = args.output_directory

    # Generate the content
    header = "\\documentclass[crop,tikz,convert={outext=.svg,command=\\unexpanded{pdf2svg \\infile\\space\\outfile}},multi=false]{standalone}[2012/04/13]"
    if args.with_svg:
        header = "\\documentclass[crop,tikz,multi=false]{standalone}[2012/04/13]"

    tex_content = """%s
    \\usepackage[utf8]{inputenc}
    \\usepackage{pgfplots}
    \\DeclareUnicodeCharacter{2212}{−}
    \\usepgfplotslibrary{groupplots,dateplot}
    \\usetikzlibrary{patterns,shapes.arrows}
    \\pgfplotsset{compat=newest}
    \\graphicspath{{%s/}}
    \\begin{document}
    \\input{%s}
    \\end{document};
    """ % (header, parent_directory, pgf_filename)

    # Create temporary part
    temp_dir = tempfile.mkdtemp()

    # Copy png file (FIXME: tikzplotlib necessity)
    import glob, shutil

    files = glob.iglob(os.path.join(parent_directory, "*.png"))
    for file in files:
        if os.path.isfile(file):
            shutil.copy2(file, temp_dir)

    # Tmp filename
    basename = os.path.basename(pgf_filename)
    basename = os.path.splitext(basename)[0]
    tmp_fn = "%s/%s.tex" % (temp_dir, basename)

    # Generate the temp tex
    with open(tmp_fn, "w") as tex_fh:
        tex_fh.write(tex_content)

    # Compile
    call(["pdflatex", "-shell-escape", "%s.tex" % basename], cwd=temp_dir)

    # Copy
    shutil.copyfile("%s/%s.pdf" % (temp_dir, basename), "%s/%s.pdf" % (output_directory, basename))
    if args.with_svg:
        shutil.copyfile("%s/%s.svg" % (temp_dir, basename), "%s/%s.svg" % (output_directory, basename))

    # Delete temps files
    shutil.rmtree(temp_dir)

###############################################################################
#  Envelopping
###############################################################################
if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description="")

        # Add options
        parser.add_argument("-v", "--verbosity", action="count", default=0,
                            help="increase output verbosity")
        parser.add_argument("-p", "--with-svg", action="store_true",
                            help="Produce the SVG as well")
        parser.add_argument("-o", "--output_directory", default=None,
                            help="output directory")

        # Add arguments
        parser.add_argument("pgf_filename", help="filename of the tikz/pgf file (extension should not be .tex!)")

        # Parsing arguments
        args = parser.parse_args()

        # Verbose level => logging level
        log_level = args.verbosity
        if (args.verbosity > len(LEVEL)):
            logging.warning("verbosity level is too high, I'm gonna assume you're taking the highes ")
            log_level = len(LEVEL) - 1
        logging.basicConfig(level=LEVEL[log_level])

        # Debug time
        start_time = time.time()
        logging.info("start time = " + time.asctime())

        # Running main function <=> run application
        main()

        # Debug time
        logging.info("end time = " + time.asctime())
        logging.info('TOTAL TIME IN MINUTES: %02.2f' %
                     ((time.time() - start_time) / 60.0))

        # Exit program
        sys.exit(0)
    except KeyboardInterrupt as e:  # Ctrl-C
        raise e
    except SystemExit as e:  # sys.exit()
        pass
    except Exception as e:
        logging.error('ERROR, UNEXPECTED EXCEPTION')
        logging.error(str(e))
        traceback.print_exc(file=sys.stderr)
        sys.exit(-1)

# compilePGF.py ends here
