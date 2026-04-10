from datetime import date

MONTHS_WITH_31_DAYS = [1,3,5,7,8,10,12]
MONTH_NAMES = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

def is_leap_year(year: int) -> bool:
    """
    If the year is divisible by 4 it's a leap year.
    Except if the year is also divisible by 100, then it's not a leap year.
    Except if the year is also divisible by 400, then it's a leap year again.
    """
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return True
            return False
        return True
    return False

def number_of_days_in_month(month: int, year: int) -> int:
    if month == 2:
        return 29 if is_leap_year(year) else 28
    elif month in MONTHS_WITH_31_DAYS:
        return 31
    return 30

def is_valid_date(day: int, month: int, year: int) -> bool:
    max_day = number_of_days_in_month(month, year)
    valid_day = 1 <= day <= max_day
    valid_month = 1 <= month <= 12
    return valid_month and valid_day

def century_index_from_year(year: int) -> int:
    """
    Returns the century index for a given year (e.g. 1995 → 19, 875 → 8, 2025 → 20)
    """
    return year // 100

def date_to_string(day: int, month: int, year: int) -> str:
    if not is_valid_date(day, month, year):
        return "invalid date"

    month_names = MONTH_NAMES
    if day == 1 or day == 21 or day == 31:
        ordinal_suffix = "st"
    elif day == 2 or day == 22:
        ordinal_suffix = "nd"
    elif day == 3 or day == 23:
        ordinal_suffix = "rd"
    else:
        ordinal_suffix = "th"
    return f"{month_names[month - 1]} {str(day) + ordinal_suffix}, {str(year)}"

def weekday_from_date(day: int, month: int, year: int, is_julian_date: bool = None) -> str:
    """
    #   Step                                                                    Example
    1.  Take the last two digits of the year                                    27.04.1997 → 97
    2.  Divide by 4, discarding any fraction                                    97 // 4 = 24
    3.  Add the day of the month                                                24 + 27 = 51
    4.  Add the month's key value: JFM AMJ JAS OND 144 025 036 146              51 + 0 = 51
    5.  Subtract 1 if the date is in January or February of a leap year         51 - 0 = 51
    6.  For a Gregorian date add gregorian century offset:
            1600s → 6, 1700s → 4, 1800s → 2, 1900s → 0, 2000s → 6 etc.          51 + 0 = 0
    7.  For a Julian date add julian century offset:
            1 for 1700's, and 1 for every additional century you go back.       not applicable
    8.  Add the last two digits of the year                                     51 + 97 = 148
    9.  Divide by 7 and take the remainder                                      148 % 7 = 1
    10. Interpret the remainder:
            0 → Saturday, 1 → Sunday ... 6 → Friday                             1 = Sunday
    """
    if not is_valid_date(day, month, year):
        return "invalid date"

    #Step 1
    last_two_year_digits = year % 100

    #Step 2
    weekday_index = last_two_year_digits // 4

    #Step 3
    weekday_index += day

    #Step 4
    month_key_values = [1,4,4,0,2,5,0,3,6,1,4,6]
    weekday_index += month_key_values[month - 1]

    #Step 5
    if (month == 1 or month == 2) and is_leap_year(year):
        weekday_index -= 1

    #Step 6
    century = century_index_from_year(year)

    if is_julian_date is False or is_julian_date is None:
        century_offset = century % 4
        weekday_index += 6 - century_offset * 2

    #Step 7
    elif is_julian_date is True:
        julian_century = 17
        century_offset = 0
        while julian_century > century:
            century_offset += 1
            julian_century -= 1
        weekday_index += century_offset
    else:
        raise TypeError("is_julian_date must be True, False or None")

    #Step 8
    weekday_index += last_two_year_digits

    #Step 9
    weekday_index = weekday_index % 7

    #Step 10
    weekday_names = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    given_date = date(year, month, day)
    today = date.today()
    if given_date < today:
        verb = "was"
    elif given_date > today:
        verb = "will be"
    else:
        verb = "is"

    return f"{date_to_string(day, month, year)} {verb} a {weekday_names[weekday_index]}"

print(weekday_from_date(31, 12, 2030))