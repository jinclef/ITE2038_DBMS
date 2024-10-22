set search_path to s_2021006317;

select w1.*
from watch as w1, (select c.c_id
	from customer as c
	join watch as w on w.c_id=c.c_id
	group by c.c_id
	having count(w.c_id) >=2) as TwiceUser
where w1.c_id=TwiceUser.c_id