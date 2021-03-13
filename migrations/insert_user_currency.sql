insert into "user_currency" (user_id, currency_id)
select "id", 1 from "user" u
where u."id" not in (
	select user_id from "user_currency"
)