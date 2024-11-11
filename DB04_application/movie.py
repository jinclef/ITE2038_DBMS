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

        # Base query with common SELECT statement and JOINs
        base_sql = """
        WITH MovieComments(movie_id, comment_count, comment_sum) AS (
            SELECT m.m_id, 
                COALESCE(COUNT(ct.m_id), 0) AS comment_count, 
                COALESCE(SUM(ct.rating), 0) AS comment_sum
            FROM movie AS m 
            LEFT OUTER JOIN comment_to AS ct ON ct.m_id = m.m_id
            GROUP BY m.m_id
        )
        SELECT 
            m.m_id, 
            m.m_name, 
            m.m_type, 
            m.start_year, 
            m.end_year,
            m.is_adult,
            m.runtimes,
            m.m_rating AS imdb_rating,
            ((m.m_rating * m.votes + COALESCE(mct.comment_sum, 0)) / 
            (m.votes + COALESCE(mct.comment_count, 0))) AS final_rating,
            STRING_AGG(DISTINCT gr.gr_name, ', ') AS genres
        FROM movie AS m
        LEFT OUTER JOIN MovieComments AS mct ON mct.movie_id = m.m_id
        JOIN classify AS cl ON m.m_id = cl.m_id
        JOIN genre AS gr ON cl.gr_id = gr.gr_id
        """

        # Add conditions based on search_type
        condition_sql = ""
        params = {}
        if search_type == 'id':
            condition_sql = "WHERE m.m_id = %(id)s"
            params = {"id": search_value}

        elif search_type == 'name':
            condition_sql = "WHERE m.m_name ILIKE %(name)s"
            params = {"name": search_value}

        elif search_type == 'type':
            condition_sql = "WHERE m.m_type ILIKE %(type)s"
            params = {"type": search_value}
        
        elif search_type == 'genre':
            condition_sql = """
            WHERE m.m_id IN (
                SELECT m.m_id
                FROM movie m
                JOIN classify cl ON m.m_id = cl.m_id
                JOIN genre gr ON cl.gr_id = gr.gr_id
                WHERE gr.gr_name ILIKE %(genre)s
            )
            """
            params = {"genre": search_value}
        
        elif search_type == 'all':
            condition_sql = ""
            limit_sql = "LIMIT %(all)s"
            params = {"all": search_value}
        
        elif search_type == 'start_year':
            condition_sql = "WHERE EXTRACT(YEAR FROM m.start_year) >= %(start_year)s"
            params = {"start_year": search_value}

        elif search_type == 'end_year':
            condition_sql = "WHERE EXTRACT(YEAR FROM m.end_year) >= %(end_year)s"
            params = {"end_year": search_value}

        
        elif search_type == 'is_adult':
            condition_sql = "WHERE m.is_adult = %(is_adult)s"
            params = {"is_adult": search_value}
        
        elif search_type == 'rating':
            condition_sql = "WHERE m.m_rating >= %(rating)s"
            params = {"rating": search_value}
        
        else:
            print("can't search by", search_type)
            return False

        # Final SQL with GROUP BY and ORDER BY clauses
        final_sql = f"""
        {base_sql}
        {condition_sql}
        GROUP BY m.m_id, m.m_name, m.m_type, m.start_year, m.end_year, 
                 m.is_adult, m.runtimes, m.m_rating, m.votes, mct.comment_sum, mct.comment_count
        ORDER BY m.m_id ASC
        """
        
        if search_type == 'all':
            final_sql += f" {limit_sql}"
        
        final_sql += ";"

        # Execute the final SQL
        cur.execute(final_sql, params)

        # Fetch results and display or save them
        rows = cur.fetchall()
        if not rows:
            print("No results found.")
            return False
        else:
            column_names = [desc[0] for desc in cur.description]
            print_rows_to_file(column_names, rows)
            make_csv(column_names, rows)
            print_rows(column_names, rows)
            return True

    except Exception as err:
        print("ERROR: ", err)
        return False
    
    finally:
        cur.close()

def main(args):
    #. TODO
    if args.command == "info":
        if args.all:
            display_info('all', args.all)
        elif args.id:
            display_info('id', args.id)
        elif args.name:
            display_info('name', args.name)
        elif args.type:
            display_info('type', args.type)
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
    print_command_to_file()
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
    group_info.add_argument('-t', dest='type', type=str, help='m_type of movie entity')
    group_info.add_argument('-g', dest='genre', type=str, help='genre which movie classified')
    group_info.add_argument('-sy', dest='start_year', type=int, help='start_year of movie entity')
    group_info.add_argument('-ey', dest='end_year', type=int, help='end_year of movie entity')
    group_info.add_argument('-ad', dest='is_adult', type=bool, help='is_adult of movie entity')
    group_info.add_argument('-r', dest='rating', type=float, help='m_rating of movie entity')
    
    args = parser.parse_args()
    main(args)
    print("Running Time: ", end="")
    print(time.time() - start)
