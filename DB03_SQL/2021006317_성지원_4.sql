set search_path to s_2021006317;

select c.c_name
from customer as c
join watch as w on w.c_id=c.c_id
group by c.c_name
having count(w.c_id) >=2