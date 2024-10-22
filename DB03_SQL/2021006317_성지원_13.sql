set search_path to s_2021006317;

with MaxCommentUser(c_id, ct_count) as (
	select ct.c_id, count(ct.comment) as "ct_count"
	from customer as c, comment_to as ct
	where ct.c_id=c.c_id
	group by (ct.c_id)
)

select ct.c_id, ct.m_id, ct.rating, ct.comment, ct.write_date
from comment_to as ct, MaxCommentUser as mcu
where ct.c_id=mcu.c_id and mcu.ct_count >= ALL (select max(ct_count) from MaxCommentUser)