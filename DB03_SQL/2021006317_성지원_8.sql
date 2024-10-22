-- 8. 가장 많은 장르를 가지는 영화를 출력하시오. `m_name`과 `gr_count` 출력
with GenreCount(m_name, gr_count) as (
	select m.m_name, count(c.gr_id) as "gr_count"
	from s_2021006317.movie as m
	join s_2021006317.classify as c on m.m_id=c.m_id
	group by (m.m_name)
)

select GenreCount.*
from GenreCount
where GenreCount.gr_count >= ALL (select max(gr_count) from GenreCount)
