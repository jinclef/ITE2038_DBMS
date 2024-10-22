set search_path to s_2021006317;

with ComedyMovie (comedy_movie) as (
select cl.m_id
from movie as m, genre as gr, classify as cl
where gr.gr_name='Comedy' and cl.gr_id=gr.gr_id and cl.m_id=m.m_id
)

select m.m_id, m.m_name
from movie as m, genre as gr, classify as cl, ComedyMovie
where gr.gr_name='Action' and cl.gr_id=gr.gr_id and cl.m_id=m.m_id and m.m_id=ComedyMovie.comedy_movie