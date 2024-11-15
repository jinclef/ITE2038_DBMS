import time
import argparse
from helpers.connection import conn
from helpers.utils import print_rows
from helpers.utils import print_rows_to_file
from helpers.utils import print_command_to_file
from helpers.utils import make_csv

'''
table participate: m_id, p_id, role, casting, ordering
table participant: p_id, p_name
table movie: m_id, m_name
'''

def display_info(search_type, search_value, role):
    try:
        cur = conn.cursor()
        cur.execute("SET search_path TO s_2021006317")

        if search_type == 'all':
            sql = """
            SELECT p.p_id, p.p_name, r.role, m.m_name, STRING_AGG(r.casting, ', ') AS casting
            FROM participant p
            JOIN participate r ON p.p_id = r.p_id
            JOIN movie m ON r.m_id = m.m_id
            WHERE r.role ILIKE %(role)s
            GROUP BY p.p_id, p.p_name, r.role, m.m_name
            ORDER BY p.p_id
            LIMIT %(limit)s;
            """
            params = {'role': role, 'limit': search_value}

        elif search_type == 'one':
            # Query for retrieving data based on a specific participant ID and role
            sql = """
            SELECT p.p_id, p.p_name, r.role, STRING_AGG(r.casting, ', ') AS casting
            FROM participant p
            JOIN participate r ON p.p_id = r.p_id
            JOIN movie m ON r.m_id = m.m_id
            WHERE m.m_id = %(id)s AND r.role ILIKE %(role)s
            GROUP BY p.p_id, p.p_name, r.role
            ORDER BY p.p_id;
            """
            params = {'id': search_value, 'role': role}

        else:
            print("Invalid search type provided.")
            return False

        # Execute the final SQL
        cur.execute(sql, params)

        # Fetch results and display or save the
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
        print("ERROR:", err)
        return False

    finally:
        cur.close()


def main(args):
    if args.command == "info":
        if args.all: # -a
            display_info('all', args.all, args.role)
        elif args.one: # -i
            display_info('one', args.one, args.role)
    else :
        print("Error: query command error.")

if __name__ == "__main__":
    #
    print_command_to_file()
    #
    start = time.time()
    parser = argparse.ArgumentParser(description = """
    how to use
    1. info [-a(all) / -i(one)] value role
    2. ...
    3. ...
    """, formatter_class=argparse.RawTextHelpFormatter)
    subparsers = parser.add_subparsers(dest='command', 
        help='select one of query types [info, ...]')

    #info
    parser_info = subparsers.add_parser('info', help='Display participant associated to genre info')
    #. TODO
    parser_info.add_argument('-a', dest='all', type=str, help='display rows with top [value]')
    parser_info.add_argument('-i', dest='one', type=str, help='display single row with m_id [value]')
    parser_info.add_argument('role', type=str, help='role of participant entity')
    
    args = parser.parse_args()
    main(args)
    print("Running Time: ", end="")
    print(time.time() - start)
