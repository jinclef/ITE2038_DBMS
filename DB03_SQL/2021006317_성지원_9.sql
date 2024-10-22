-- ### 9. 'Drama' 장르를 선호하지 않는 사용자의 이름을 출력하시오. `c_name` 출력
-- 모든 사용자는 반드시 3개의 선호 장르를 가지는 중
set search_path to s_2021006317;

select distinct c.c_name
from genre as g,
	customer as c, prefer as p
where p.c_id=c.c_id and p.gr_id=g.gr_id and
	p.c_id not in (
		select pr.c_id
		from genre as gr, prefer as pr
		where gr.gr_name='Drama' and pr.gr_id=gr.gr_id)