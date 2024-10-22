select distinct c_name
from s_2021006317.customer as c, s_2021006317.watch as w
where w.c_id=c.c_id and (
	c.c_id in (
		select distinct w.c_id
		from s_2021006317.customer as c, s_2021006317.classify as cl, s_2021006317.genre as gr, s_2021006317.watch as w
		where gr.gr_name='Drama' and cl.gr_id=gr.gr_id and w.m_id=cl.m_id
	) and
 	c.c_id in (
		select distinct w.c_id
		from s_2021006317.customer as c, s_2021006317.classify as cl, s_2021006317.genre as gr, s_2021006317.watch as w
		where gr.gr_name='Crime' and cl.gr_id=gr.gr_id and w.m_id=cl.m_id
	) and
	c.c_id in (
		select distinct w.c_id
	from s_2021006317.customer as c, s_2021006317.classify as cl, s_2021006317.genre as gr, s_2021006317.watch as w
	where gr.gr_name='Mystery' and cl.gr_id=gr.gr_id and w.m_id=cl.m_id
	)
)