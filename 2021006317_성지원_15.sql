-- 15. 외부 사이트의 평점과 사용자의 코멘트 점수를 합산하여 최종 평점을 재계산하고, 이를 영화의 이름과 함께 출력하시오.
-- `m_id`, 최종 평균 점수 출력
-- 최종 평점 = [(`m_rating` * `m.votes`) + 해당 영화의 코멘트 점수 합] / [`m_votes` + 해당 영화의 코멘트 개수]

-- 58개의 영화에 대해서만 comment_to 가 있음. 나머지 영화는 없음 -> MovieComments 값이 0

set search_path to s_2021006317;

with MovieComments(movie_id, comment_count, comment_sum) as (
	select m.m_id, COALESCE(count(ct.m_id),0), COALESCE(sum(ct.rating),0)
	from movie as m left outer join comment_to as ct on ct.m_id=m.m_id
	group by m.m_id
)

select mv.m_name, (((mv.m_rating * mv.votes) + COALESCE(mct.comment_sum, 0)) / (mv.votes + COALESCE(count(comment_to.m_id), 0))) as "recalculated_avg_rating"
from movie as mv
left outer join MovieComments as mct on mct.movie_id=mv.m_id
left outer join comment_to on comment_to.m_id=mv.m_id
group by mv.m_id, mct.movie_id, mct.comment_sum
having mct.movie_id=mv.m_id