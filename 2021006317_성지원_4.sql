select c.c_name
from s_2021006317.customer as c
join s_2021006317.watch as w on w.c_id=c.c_id
group by c.c_name
having count(w.c_id) >=2