import time
import argparse
from helpers.connection import conn
from helpers.utils import print_rows
from helpers.utils import print_rows_to_file
from helpers.utils import print_command_to_file
from helpers.utils import make_csv


def display_info(search_type, search_value, search_role):
    # TODO
    # search_type: all / one
    # search_value: m_id args.one
    # search_role: role args[1]?
    pass

def main(args):
    # TODO
    pass

if __name__ == "__main__":
    #
    #print_command_to_file()
    #
    start = time.time()
    parser = argparse.ArgumentParser(description = """
    how to use
    1. info [-a(all) / -o(one)] value role
    2. ...
    3. ...
    """, formatter_class=argparse.RawTextHelpFormatter)
    subparsers = parser.add_subparsers(dest='command', 
        help='select one of query types [info, ...]')

    #info
    parser_info = subparsers.add_parser('info', help='Display participant associated to genre info')
    group_info = parser_info.add_mutually_exclusive_group(required=True)
    #. TODO
    group_info.add_argument('-a', dest='all', type=str, help='display rows with top [value]') # role
    group_info.add_argument('-o', dest='one', type=str, help='display single row with m_id [value]') # movie role 띄어쓰기 인식이 되나?

    args = parser.parse_args()
    main(args)
    print("Running Time: ", end="")
    print(time.time() - start)
