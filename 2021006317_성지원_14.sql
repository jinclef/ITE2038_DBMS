-- ### 14. 2개 이상 영화를 본 사용자가 남긴 코멘트 점수 평균을 출력하시오. - `c_id`, 코멘트 평균 점수 출력

select c.c_id, avg(ct.rating) as "avg_rating"
from s_2021006317.customer as c, s_2021006317.comment_to as ct
where c.c_id=ct.c_id and c.c_id in (
	select u.c_id
	from s_2021006317.customer as u, s_2021006317.watch as w
	where w.c_id=u.c_id
	group by u.c_id
		having count(w.m_id)>=2
)
group by c.c_id