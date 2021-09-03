def enter_a_year():
    year = input('> Enter a year: ')
    if year.isdecimal() and int(year) > 1582:
        return year
    else:
        print('Incorrect entry, please try again.')
        return enter_a_year()


def enter_a_month():
    month = input('> Enter a month between 1 and 12: ')
    if month.isdecimal() and int(month) >= 1 and int(month) <= 12:
        return month
    else:
        print('Incorrect entry, please try again.')
        return enter_a_month()


def enter_a_day(year, month):
    int_year = int(year)
    int_month = int(month)

    if int_month == 2:
        if int_year % 4 == 0 and int_year % 100 != 0 or int_year % 400 == 0:
            last_day = 29
        else:
            last_day = 28
    elif int_month in [1, 3, 5, 7, 8, 10, 12]:
        last_day = 31
    else:
        last_day = 30

    day = input(f'> Enter a day between 1 and {last_day}: ')
    if day.isdecimal() and int(day) >= 1 and int(day) <= last_day:
        return day
    else:
        print('Incorrect entry, please try again.')
        return enter_a_day(year, month)
