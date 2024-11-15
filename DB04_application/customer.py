import sys
import time
import argparse
from helpers.connection import conn
from helpers.utils import fetch_customer_password, print_rows, verify_password
from helpers.utils import print_rows_to_file
from helpers.utils import is_valid_genre
from helpers.utils import print_command_to_file
from helpers.utils import make_csv

def display_info(search_type, search_value):
    try:
        cur = conn.cursor()
        
        cur.execute("SET search_path to s_2021006317")

        if search_type == 'id' :
            sql = """
            SELECT 
            cu.c_id, 
            cu.c_name, 
            cu.email, 
            cu.gender, 
            cu.phone, 
            STRING_AGG(DISTINCT gr.gr_name, ', ') AS preferred_genres
            FROM customer cu 
            JOIN prefer p ON cu.c_id = p.c_id 
            JOIN genre gr ON p.gr_id = gr.gr_id
            WHERE cu.c_id = %(id)s
            GROUP BY cu.c_id, cu.c_name, cu.email, cu.gender, cu.phone
            ORDER BY cu.c_id ASC;
            """
            cur.execute(sql, {"id": search_value})

        elif search_type == 'name' :
            sql = """
            SELECT
            cu.c_id, 
            cu.c_name, 
            cu.email, 
            cu.gender, 
            cu.phone, 
            STRING_AGG(DISTINCT gr.gr_name, ', ') AS preferred_genres
            FROM customer cu 
            JOIN prefer p ON cu.c_id = p.c_id 
            JOIN genre gr ON p.gr_id = gr.gr_id
            WHERE cu.c_name ILIKE %(name)s
            GROUP BY cu.c_id, cu.c_name, cu.email, cu.gender, cu.phone
            ORDER BY cu.c_id ASC;
            """
            cur.execute(sql, {"name": search_value})

        elif search_type == 'genre' :
            sql = """
            SELECT 
                cu.c_id, 
                cu.c_name, 
                cu.email, 
                cu.gender, 
                cu.phone, 
                STRING_AGG(DISTINCT gr.gr_name, ', ') AS preferred_genres
            FROM customer cu JOIN prefer p ON cu.c_id = p.c_id JOIN genre gr ON p.gr_id = gr.gr_id
            WHERE cu.c_id IN (
                    SELECT cu.c_id
                    FROM customer cu
                    JOIN prefer p ON cu.c_id = p.c_id
                    JOIN genre gr ON p.gr_id = gr.gr_id
                    WHERE gr.gr_name = %(genre)s
                    )
            GROUP BY cu.c_id, cu.c_name, cu.email, cu.gender, cu.phone
            ORDER BY cu.c_id ASC;
            """
            cur.execute(sql, {"genre": search_value})

        elif search_type == 'all' :
            sql = """
            SELECT
            cu.c_id, 
            cu.c_name, 
            cu.email, 
            cu.gender, 
            cu.phone, 
            STRING_AGG(DISTINCT gr.gr_name, ', ') AS preferred_genres
            FROM customer cu 
            JOIN prefer p ON cu.c_id = p.c_id 
            JOIN genre gr ON p.gr_id = gr.gr_id
            GROUP BY cu.c_id, cu.c_name, cu.email, cu.gender, cu.phone
            ORDER BY cu.c_id ASC
            LIMIT %(all)s;
            """
            cur.execute(sql, {"all": search_value})

        else :
            print("can't search by", search_type)
            return False

        rows = cur.fetchall()
        if not rows:
            print("No results found.")
            return False
        else:
            column_names = [desc[0] for desc in cur.description]
            #
            # print_rows_to_file(column_names, rows)
            # make_csv(column_names, rows)
            #
            print_rows(column_names, rows)
            return True

    except Exception as err:
        print("Unexpected Exception Occurred.")
        print(err)
    
    finally:
        cur.close()

def insert_customer(id, name, email, pwd, gender, phone, genres) :
    #. TODO

    cur = conn.cursor()
    cur.execute("SET search_path to s_2021006317")

    sql = """
    INSERT INTO customer (c_id, c_name, email, pwd, gender, phone)
    VALUES (%(id)s, %(name)s, %(email)s, %(pwd)s, %(gender)s, %(phone)s);
    """

    try:
        cur.execute(sql, {"id": id, "name": name, "email": email, "pwd": pwd, "gender": gender, "phone": phone})
        conn.commit()

        for genre in genres:
            sql = """
            INSERT INTO prefer (c_id, gr_id)
            VALUES (%(id)s, (SELECT gr_id FROM genre WHERE gr_name = %(genre)s));
            """
            cur.execute(sql, {"id": id, "genre": genre})
            conn.commit()
        
        display_info('id', id)
        
    except Exception as err:
        conn.rollback()
        print("Unexpected Exception Occurred.")
        print(err)

    finally:
        cur.close()

def update_customer(id, target, value) :
    #. TODO
    cur = conn.cursor()
    cur.execute("SET search_path to s_2021006317")

    if target == 'pwd':
        # value[0] : old password
        # value[1] : new password
        real_pwd = fetch_customer_password(id)
        if not verify_password(value[0], real_pwd):
            print("Error: Password is incorrect.")
            return
        
    else:
        display_info('id', id) # before info

    try:
        if (target == 'preferred_genres'):
            
            sql = """
            DELETE FROM prefer WHERE c_id = %(id)s;
            """
            cur.execute(sql, {"id": id})
            conn.commit()

            for genre in value:
                sql = """
                INSERT INTO prefer (c_id, gr_id)
                VALUES (%(id)s, (SELECT gr_id FROM genre WHERE gr_name ILIKE %(genre)s));
                """
                cur.execute(sql, {"id": id, "genre": genre})
                conn.commit()

        else:
            sql = """
            UPDATE customer SET {target} = %(value)s WHERE c_id = %(id)s;
            """.format(target=target)
          
            cur.execute(sql, {"value": value[1], "id": id})
            conn.commit()

        display_info('id', id) # changed info
        
    except Exception as err:
        conn.rollback()
        print("Unexpected Exception Occurred.")
        print(err)

    finally:
        cur.close()

def delete_customer(id) :
    #. TODO
    cur = conn.cursor()
    cur.execute("SET search_path to s_2021006317")

    display_info('id', id) # before info
    
    sql = """
    DELETE FROM prefer WHERE c_id = %(id)s;
    DELETE FROM customer WHERE c_id = %(id)s;
    """
    
    try:
        cur.execute(sql, {"id": id})
        conn.commit()
    
    except Exception as err:
        # rollback
        conn.rollback()
        print("Unexpected Exception Occurred.")
        print(err)

    finally:
        cur.close()

def main(args):
    if args.command == "info":
        if args.id:
            display_info('id',args.id)
        elif args.name:
            display_info('name', args.name)
        elif args.genre:
            if not is_valid_genre(args.genre):
                print(f"Error: '{args.genre}' is not a valid genre.")
                return
            display_info('genre', args.genre)
        elif args.all:
            display_info('all', args.all)

    elif args.command == "insert":
        insert_customer(args.id, args.name, 
            args.email, args.pwd, args.gender, args.phone, args.genre)

    elif args.command == "update":
        #. TODO
        if args.email:
            update_customer(args.id, "email", args.email)
        elif args.password: # list
            update_customer(args.id, "pwd", args.password)
        elif args.phone:
            update_customer(args.id, "phone", args.phone)
        elif args.genres:
            # if count < 3 return
            if len(args.genres) != 3:
                print("Error: You must enter exactly three genres.")
                return
            for genre in args.genres:
                if not is_valid_genre(genre):
                    print(f"Error: '{genre}' is not a valid genre.")
                    return
            update_customer(args.id, "preferred_genres", args.genres)

    elif args.command == "delete":
        #. TODO
        delete_customer(args.id)

    else :
        print("Error: query command error.")


if __name__ == "__main__":
    #
    # print_command_to_file()
    #
    start = time.time()
    
    parser = argparse.ArgumentParser(description = """
    how to use
    1. info [-i(c_id) / -n(c_name) / -g(genre) / -a (all)] [value]
    2. insert c_id, c_name, email, pwd, gender, phone -g (genre1, genre2, genre3)
    3. update -i [c_id] [-m(e-mail) / -p(password) / -ph(phone)] [new_value]
    4. delete -i [c_id]
    """, formatter_class=argparse.RawTextHelpFormatter)
    subparsers = parser.add_subparsers(dest='command', help='select one of query types [info, insert, update, delete]')

    #[1-1]info
    parser_info = subparsers.add_parser('info', help='Display target customers info')
    group_info = parser_info.add_mutually_exclusive_group(required=True)
    group_info.add_argument('-i', dest='id', type=int, help='c_id of customer entity')
    group_info.add_argument('-n', dest='name', type=str, help='c_name of customer entity')
    group_info.add_argument('-g', dest='genre', type=str, help='genre which customer prefer')
    group_info.add_argument('-a', dest='all', type=str, help='display rows with top [value]')

    #[1-2]insert
    parser_insert = subparsers.add_parser('insert', help='Insert new customer data')
    #. TODO
    parser_insert.add_argument('-g', dest='genre', nargs='+', help='genre which customer prefers')
    parser_insert.add_argument('id', type=int, help='c_id of customer entity to be inserted')
    parser_insert.add_argument('name', type=str, help='c_name of customer entity to be inserted')
    parser_insert.add_argument('email', type=str, help='email of customer entity to be inserted')
    parser_insert.add_argument('pwd', type=str, help='pwd of customer entity to be inserted')
    parser_insert.add_argument('gender', type=str, help='gender of customer entity to be inserted')
    parser_insert.add_argument('phone', type=str, nargs='+', help='phone of customer entity to be inserted')

    #[1-3]update
    parser_update = subparsers.add_parser('update', help='Update one of customer data')
    #. TODO
    parser_update.add_argument('-i', dest='id', type=int, help='c_id of customer entity')
    parser_update.add_argument('-m', dest='email', type=str, help='c_email of customer entity')
    parser_update.add_argument('-p', dest='password', type=str, nargs='+', help='c_password of customer entity')
    parser_update.add_argument('-ph', dest='phone', type=str, nargs='+', help='c_phone of customer entity')
    parser_update.add_argument('-gs', dest='genres', type=str, nargs='+', help='three genres which customer prefers')

    #[1-4]delete
    parser_delete = subparsers.add_parser('delete', help='Delete customer data with associated data')
    #. TODO
    customer_delete = parser_delete.add_mutually_exclusive_group(required=True)
    customer_delete.add_argument('-i', dest='id', type=int, help='c_id of customer entity')
    
    args = parser.parse_args()
    if hasattr(args, 'phone') and args.phone:
        args.phone = ' '.join(args.phone)

    main(args)
    print("Running Time: ", end="")
    print(time.time() - start)
