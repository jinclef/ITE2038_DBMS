select c.c_name
from s_2021006317.customer as c, s_2021006317.watch as w, s_2021006317.movie as m
where w.c_id=c.c_id and w.m_id = m.m_id and m.m_name = 'Gukyeongi';