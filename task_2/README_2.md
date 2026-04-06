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

Решение №1:  
```sql
select distinct on (r.id_patients) r.id_patients, r.id_doctors
from receptions r 
order by r.id_patients, r.startdatetime desc
```
Решение №2:  
```sql
with receptions_with_nums as (select r.id_patients, r.id_doctors, r.startdatetime,
					row_number() over (
			            partition by id_patients
			            order by startdatetime desc
			        ) as rn
		    	from receptions r
		    	)
select id_patients, id_doctors
from receptions_with_nums 
where rn = 1
```
Решение №3:  
```sql
select r1.id_patients, r1.id_doctors
from receptions r1
where r1.startdateTime = (
    select max(r2.startdateTime)
    from receptions r2
    where r2.id_patients = r1.id_patients
)
```
Решение 1, 2 - всегда одна строка, когда в 3 варианте может вернутся несколько, если дат несколько
Решение 2 лучше на больших объёмах данных
Индекс везде ускоряет нахождение нужного результата