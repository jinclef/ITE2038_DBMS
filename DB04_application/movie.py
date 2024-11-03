import time
import argparse
from helpers.connection import conn
from helpers.utils import print_rows
from helpers.utils import print_rows_to_file
from helpers.utils import is_valid_genre
from helpers.utils import print_command_to_file
from helpers.utils import make_csv

def display_info(search_type, search_value):
    # TODO

def main(args):
    # TODO


if __name__ == "__main__":
    #
    #print_command_to_file()
    #
    start = time.time()
    parser = argparse.ArgumentParser(description = """
    how to use
    1-1. info [-a(all) / -i(m_id) / -n(m_name) / -g(genre)] [value]
    1-2. info [-sy(start_year) / -ey(end_year) / -ad(is_adult) / -r(rating)] [value]
    2. ...
    3. ...
    """, formatter_class=argparse.RawTextHelpFormatter)
    subparsers = parser.add_subparsers(dest='command', 
        help='select one of query types [info, ...]')

    #info
    parser_info = subparsers.add_parser('info', help='Display target movie info')
    group_info = parser_info.add_mutually_exclusive_group(required=True)
    #. TODO
    group_info.add_argument('-a', dest='all', type=str, help='display rows with top [value]')
    group_info.add_argument('-i', dest='id', type=int, help='m_id of movie entity')
    group_info.add_argument('-n', dest='name', type=str, help='m_name of movie entity')
    group_info.add_argument('-g', dest='genre', type=str, help='genre which movie classified')

    group_info.add_argument('-sy', dest='start_year', type=str, help='start_year of movie entity')
    group_info.add_argument('-ey', dest='end_year', type=str, help='end_year of movie entity')
    group_info.add_argument('-ad', dest='is_adult', type=bool, help='is_adult of movie entity')
    group_info.add_argument('-r', dest='rating', type=int, help='m_rating of movie entity')
    
    args = parser.parse_args()
    main(args)
    print("Running Time: ", end="")
    print(time.time() - start)
