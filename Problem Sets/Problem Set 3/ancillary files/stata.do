clear
import delimited data_csv.csv

drop if hsex == 2

drop if age > 60
drop if age < 25

drop if hannhrs == .
drop if hlabinc == .

drop if hannhrs == 0

drop if hrace == .
drop if hyrsed == .

gen hwage = hlabinc/hannhrs


drop if hwage <=7

gen black = 1 if hrace ==2
replace black = 0 if black == .

gen hispanic = 1 if hrace == 5
replace hispanic =0 if hispanic == .

gen other = 1 if hrace != 1 & hrace != 2 & hrace != 5
replace other = 0 if other == .

gen loghwage = ln(hwage)

reg loghwage hyrsed age black hispanic other if year ==1971
eststo one

reg loghwage hyrsed age black hispanic other if year ==1980
eststo two
reg loghwage hyrsed age black hispanic other if year ==1990
eststo three
reg loghwage hyrsed age black hispanic other if year ==2000
eststo four

estout one two three four , cells(b(star fmt(4)) se) style(tex)
