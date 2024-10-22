select count(c) as "hotmail_user_count"
from s_2021006317.customer as c
where c.email like '%@hotmail.com'