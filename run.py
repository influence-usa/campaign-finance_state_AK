#!/usr/bin/python
"""
run.py -p<print>|-d<download>|-t<test>|-r<report>
                & optional_Filter_String'
"""
import os
import sys
import getopt


def main(argv):
    """ Main """
    if len(argv) == 1:
        argv.append("")
    try:
        opts, args = getopt.getopt(argv, "d:p:r:t")
    except getopt.GetoptError:
        print 'run.py -p<print>|-d<download>|-t<test>|-r<report> \
                & optional_Filter_String'
        sys.exit(2)

    if opts[0][0] in ['-p', '-d', '-r']:
        from work import AK_lobby
        state = AK_lobby(opts[0][1])
        if opts[0][0] == '-p':
            state.print_files()
        if opts[0][0] == '-d':
            state.convert_text_file_to_json()
        if opts[0][0] == '-r':
            state.report()

    if opts[0][0] == '-t':
        os.system("python tests/test_suite_1.py")
if __name__ == "__main__":
    main(sys.argv[1:])
 
