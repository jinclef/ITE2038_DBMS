set search_path to s_2021006317;

select distinct c_name
from customer as c, watch as w
where w.c_id=c.c_id and (
	c.c_id in (
		select distinct w.c_id
		from customer as c, classify as cl, genre as gr, watch as w
		where gr.gr_name='Drama' and cl.gr_id=gr.gr_id and w.m_id=cl.m_id
	) and
 	c.c_id in (
		select distinct w.c_id
		from customer as c, classify as cl, genre as gr, watch as w
		where gr.gr_name='Crime' and cl.gr_id=gr.gr_id and w.m_id=cl.m_id
	) and
	c.c_id in (
		select distinct w.c_id
	from customer as c, classify as cl, genre as gr, watch as w
	where gr.gr_name='Mystery' and cl.gr_id=gr.gr_id and w.m_id=cl.m_id
	)
)