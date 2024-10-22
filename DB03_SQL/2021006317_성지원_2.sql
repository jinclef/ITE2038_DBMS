set search_path to s_2021006317;

select distinct m.m_name
from movie as m,
	genre as g,
	classify as c
where g.gr_name = 'Drama' and c.gr_id=g.gr_id and c.m_id=m.m_id