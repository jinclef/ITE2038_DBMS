-- 11. 코멘트 간의 작성 날짜가 3일 이상 차이나는 것이 하나 이상인 사용자 수를 출력하시오. - 사용자의 수 출력
set search_path to s_2021006317;

select count(c) as "cnt_customer"
from customer as c
where c.c_id in (
	select cm1.c_id
	from comment_to as cm1, comment_to as cm2
	where cm1.c_id=cm2.c_id
	group by cm1.c_id, cm1.write_date, cm2.write_date
	having AGE(cm1.write_date, cm2.write_date) >= '3 days'
)