def prompt_date_year():
	year = input('> Enter a year: ')
	if len(year)==0:
		return None
	elif year.isdecimal() and int(year)>1582:
		return year
	else:
		print('Incorrect entry, please try again.')
		return prompt_date_year()

def prompt_date_month():
	month = input('> Enter a month between 1 and 12: ')
	if len(month)==0:
		return None
	elif month.isdecimal() and int(month)>=1 and int(month)<=12:
		return month
	else:
		print('Incorrect entry, please try again.')
		return prompt_date_month()

def prompt_date_day(year, month):
	iyear = int(year)
	imonth = int(month)

	if imonth==2:
		if iyear%4==0 and iyear%100!=0 or iyear%400==0:
			last_day = 29
		else:
			last_day = 28
	elif imonth in [1, 3, 5, 7, 8, 10, 12]:
		last_day = 31
	else:
		last_day = 30

	day = input(f'> Enter a day between 1 and {last_day}: ')
	if day.isdecimal() and int(day)>=1 and int(day)<=last_day:
		return day
	else:
		print('Incorrect entry, please try again.')
		return prompt_date_day(year, month)