import argparse
import os

class Options(object):

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Ripper:  A utility for borrowing websites')
        self.parser.add_argument(
            "-u",
            "--url",
            dest="url",
            required=True,
            help="Url of page to be coppied"
        )
        self.parser.add_argument(
            "-d",
            "--destination",
            dest="destination",
            default="",
            help="Path to write the files. Defalt: CWD"
        )
        self.parser.add_argument(
            "-t",
            "--threads",
            type=int,
            dest="threads",
            default=4,
            help="Number of threads (processes) to use."
        )
        self.parser.add_argument(
            "-w",
            "--window",
            action="store_true",
            dest="window",
            default=False,
            help="Operate in Window mode"
        )
        self.parser.add_argument(
            "-s",
            "--site",
            action="store_true",
            dest="top_level_pages",
            default=False,
            help="Rip all top level pages found on the main page (Experimental)"
        )


        parsed = self.parser.parse_args()
        for attr, value in parsed.__dict__.iteritems():
                self.__setattr__(attr, value)
