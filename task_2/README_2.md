**Задача 2.1**

Решение №1:  
```sql
with calendar as (
    select generate_series(
    '2015-01-01'::date,  
    '2016-01-01'::date,
    '1 day') as date    
)    
select 
    c.date::date,    
    count(r.ID) as receptions_count    
from calendar c    
left join receptions r on r.startdatetime::date = c.date    
group by c.date    
order by c.date    
```
Решение №2:
***
**Задача 2.2** 

***
***