-- table -> playername, date, score
-- print list of players with latest score

with pyaerrankedData as (
    select payerName, Score, 
	    Row_Number(Partition by PlayerName order by Date Desc) rn
    from PlayerTable)


select payerName, Score from pyaerrankedData where rn = 1
