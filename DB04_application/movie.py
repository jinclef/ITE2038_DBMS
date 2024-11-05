import time
import argparse
from helpers.connection import conn
from helpers.utils import print_rows
from helpers.utils import print_rows_to_file
from helpers.utils import is_valid_genre
from helpers.utils import print_command_to_file
from helpers.utils import make_csv

def display_info(search_type, search_value):
    #. TODO
    try:
        cur = conn.cursor()
        
        cur.execute("SET search_path to s_2021006317")

        if search_type == 'id' :
            sql = """
            SELECT 
            m_id, 
            m_name, 
            m_genre, 
            m_start_year, 
            m_end_year, 
            is_adult, 
            m_rating
            FROM movie
            WHERE m_id = %(id)s
            ORDER BY m_id ASC;
            """
            cur.execute(sql, {"id": search_value})

        elif search_type == 'name' :
            sql = """
            SELECT
            m_id, 
            m_name, 
            m_genre, 
            m_start_year, 
            m_end_year, 
            is_adult, 
            m_rating
            FROM movie
            WHERE m_name ILIKE %(name)s
            ORDER BY m_id ASC;
            """
            cur.execute(sql, {"name": search_value})

        elif search_type == 'genre' :
            sql = """
            SELECT 
                m_id, 
                m_name, 
                m_genre, 
                m_start_year, 
                m_end_year, 
                is_adult, 
                m_rating
            FROM movie
            WHERE m_genre ILIKE %(genre)s
            ORDER BY m_id ASC;
            """
            cur.execute(sql, {"genre": search_value})

        elif search_type == 'all' :
            sql = """
            SELECT 
                m_id, 
                m_name, 
                m_genre, 
                m_start_year, 
                m_end_year, 
                is_adult, 
                m_rating
            FROM movie
            ORDER BY m_id ASC
            LIMIT %(all)s;
            """
            cur.execute(sql, {"all": search_value})

        elif search_type == 'start_year' :
            sql = """
            SELECT 
                m_id, 
                m_name, 
                m_genre, 
                m_start_year, 
                m_end_year, 
                is_adult, 
                m_rating
            FROM movie
            WHERE m_start_year = %(start_year)s
            ORDER BY m_id ASC;
            """
            cur.execute(sql, {"start_year": search_value})

        elif search_type == 'end_year' :
            sql = """
            SELECT 
                m_id, 
                m_name, 
                m_genre, 
                m_start_year, 
                m_end_year,
                is_adult,
                m_rating
            FROM movie
            WHERE m_end_year = %(end_year)s
            ORDER BY m_id ASC;
            """
            cur.execute(sql, {"end_year": search_value})

        elif search_type == 'is_adult' :
            sql = """
            SELECT 
                m_id, 
                m_name, 
                m_genre, 
                m_start_year, 
                m_end_year,
                is_adult,
                m_rating
            FROM movie
            WHERE is_adult = %(is_adult)s
            ORDER BY m_id ASC;
            """
            cur.execute(sql, {"is_adult": search_value})

        elif search_type == 'rating' :
            sql = """
            SELECT 
                m_id, 
                m_name, 
                m_genre, 
                m_start_year, 
                m_end_year,
                is_adult,
                m_rating
            FROM movie
            WHERE m_rating = %(rating)s
            ORDER BY m_id ASC;
            """
            cur.execute(sql, {"rating": search_value})

        rows = cur.fetchall()
        print_rows(rows)
        print_rows_to_file(rows)
        make_csv(rows, 'movie')
        cur.close()

    except Exception as err:
        print("ERROR: ", err)
        return False
    
    return True

def main(args):
    #. TODO
    if args.command == "info":
        if args.all:
            display_info('all', args.all)
        elif args.id:
            display_info('id', args.id)
        elif args.name:
            display_info('name', args.name)
        elif args.genre:
            display_info('genre', args.genre)
        elif args.start_year:
            display_info('start_year', args.start_year)
        elif args.end_year:
            display_info('end_year', args.end_year)
        elif args.is_adult:
            display_info('is_adult', args.is_adult)
        elif args.rating:
            display_info('rating', args.rating)
        else:
            print("Error: query command error.")

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
