set search_path to s_2021006317;

select m1.m_name, count(m1) as "gr_count"
from genre as gr, classify as c, movie as m1
join movie as m2 on m1.m_id=m2.m_id
where c.gr_id=gr.gr_id and c.m_id=m1.m_id
group by m1.m_name