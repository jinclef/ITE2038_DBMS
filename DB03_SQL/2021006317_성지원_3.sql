set search_path to s_2021006317;

select count(c) as "hotmail_user_count"
from customer as c
where c.email like '%@hotmail.com'