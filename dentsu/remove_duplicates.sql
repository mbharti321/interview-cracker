-- # remove duplicates
with ranked_employee as (
    select employee_id, 
        rank(partition over email order by createddate desc) as rn
    from employees
)

delete from employees where employee_id in (
    select employee_id from ranked_employee where rn > 1
)