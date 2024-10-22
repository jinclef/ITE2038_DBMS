set search_path to s_2021006317;

select c.c_name
from customer as c, watch as w, movie as m
where w.c_id=c.c_id and w.m_id = m.m_id and m.m_name = 'Gukyeongi';