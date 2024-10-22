-- 10. 배역(casting)을 한 번도 가진 적이 없는 참여자 이름을 출력하시오. - `p_name` 출력
-- participant

select p.p_name
from s_2021006317.participant as p
where p.p_id not in (
select pt.p_id
from s_2021006317.participant as pt, s_2021006317.participate as pe
where pt.p_id=pe.p_id and pe.casting is not null
	)