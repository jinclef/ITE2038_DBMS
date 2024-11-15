import time
import argparse
from helpers.connection import conn
from helpers.utils import print_rows
from helpers.utils import print_rows_to_file
from helpers.utils import is_valid_genre
from helpers.utils import print_command_to_file
from helpers.utils import make_csv
from helpers.utils import is_valid_pro

'''
 p_id, p_name, major_work, ocu_name(profession) 모두 출력
• 단, ocu_name(profession) 은 모두 “,” 로 연결해서출력할것
• 예시참조
• p_id기준오름차순정렬

table occupation: ocu_id, ocu_name
table participant: p_id, p_name, major_work
table profession: p_id, ocu_id
'''

def display_info(search_type, search_value):
    try:
        cur = conn.cursor()
        
        cur.execute("SET search_path to s_2021006317")

        base_sql = """
        SELECT pa.p_id, pa.p_name, pa.major_work, string_agg(ocu_name, ', ') as profession
        FROM participant pa
        JOIN profession pr ON pa.p_id = pr.p_id
        JOIN occupation ocu ON pr.ocu_id = ocu.ocu_id
        """
        
        # Add conditions based on search_type
        condition_sql = ""
        params = {}

        if search_type == 'id' :
            condition_sql = "WHERE pr.p_id = %(id)s"
            params = {"id": search_value}

        elif search_type == 'name' :
            condition_sql = "WHERE pa.p_name ILIKE %(name)s"
            params = {"name": search_value}
        
        elif search_type == 'profession' :
            condition_sql = "WHERE ocu.ocu_name ILIKE %(profession)s"
            params = {"profession": search_value}

        elif search_type == 'all' :
            condition_sql = ""
            limit_sql = "LIMIT %(all)s"
            params = {"all": search_value}

        else :
            print("can't search by", search_type)
            return False

        # Final SQL with GROUP BY and ORDER BY clauses
        final_sql = f"""
        {base_sql}
        {condition_sql}
        GROUP BY pa.p_id, pa.p_name, pa.major_work
        ORDER BY pa.p_id ASC
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
    if args.command == "info":
        if args.all:
            display_info('all', args.all)
        elif args.id:
            display_info('id',args.id)
        elif args.name:
            display_info('name', args.name)
        elif args.profession:
            if not is_valid_pro(args.profession) :
                print(f"Error: {args.profession} is not valid profession.")
                return
            display_info('profession', args.profession)
    
    else :
        print("Error: query command error.")


if __name__ == "__main__":
    #
    print_command_to_file()
    #
    start = time.time()
    parser = argparse.ArgumentParser(description = """
    how to use
    1. info [-a(all) / -i(p_id) / -n(p_name) / -pr(profession name)] [value]
    2. ...
    3. ...
    """, formatter_class=argparse.RawTextHelpFormatter)
    subparsers = parser.add_subparsers(dest='command', 
        help='select one of query types [info, ...]')

    #info
    parser_info = subparsers.add_parser('info', help='Display target participant info')
    group_info = parser_info.add_mutually_exclusive_group(required=True)
    #. TODO
    group_info.add_argument('-a', dest='all', type=str, help='display rows with top [value]')
    group_info.add_argument('-i', dest='id', type=int, help='p_id of participant entity')
    group_info.add_argument('-n', dest='name', type=str, help='p_name of participant entity')
    group_info.add_argument('-pr', dest='profession', type=str, help='ocu_name of participant entity')

    args = parser.parse_args()
    main(args)
    print("Running Time: ", end="")
    print(time.time() - start)
