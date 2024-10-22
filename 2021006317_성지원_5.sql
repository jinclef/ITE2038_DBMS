select w1.*
from s_2021006317.watch as w1, (select c.c_id
	from s_2021006317.customer as c
	join s_2021006317.watch as w on w.c_id=c.c_id
	group by c.c_id
	having count(w.c_id) >=2) as TwiceUser
where w1.c_id=TwiceUser.c_id