select distinct m.m_name
from s_2021006317.movie as m,
	s_2021006317.genre as g,
	s_2021006317.classify as c
where g.gr_name = 'Drama' and c.gr_id=g.gr_id and c.m_id=m.m_id