-- employees -> 2nd highest salary


select salary, 
	DDense_Rank() over (order by salary desc) rn
from employees
where rn = 2


