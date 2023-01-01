import re

start_with = "^"
end_with = "$"
ten_plus_chars = ".{10,}"
one_char = ".{1}"
two_chars_max = ".{0,2}"
any_chars = ".*"
any_non_digits = "\D*"
any_digits = "\d*"
has_something_before = "(?<!^)"
# date related
month_name = "(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
whoele_month_name = "(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\\b"
day_digit = "\d{1,2}"
month_digit = "\d{2}"
year_digit = "\d{4}"
to_in_string = "\Wto\W"
# price related
price = "(\$)?(\d{1,3},)?\d{1,3}.?.{0,1}\..{0,1}\d{1,2}.{0,1}"  # 1,111.11

# Jan 14 | Jan. 14 | Jan14
whoele_month_day = whoele_month_name + two_chars_max + \
    day_digit
# 14 Jan  | 14. Jan  | 14Jan
whole_day_month = day_digit + two_chars_max + whoele_month_name


def optional_pattern(regex):
    return "(" + regex + ")?"


def twice_pattern(regex):
    return "(" + regex + "){2,}"


def negative_lookahead(regex):
    return "(?!" + regex + ")"


def match(pattern, string):
    return re.search(pattern, string, re.IGNORECASE)


def find_first_match(string, *args):
    for pattern in args:
        if (match(pattern, string)):
            return pattern


def grab(pattern, string):
    return re.search(pattern, string, re.IGNORECASE).group()


def replace(pattern, replacement, string):
    return re.sub(pattern, replacement, string, re.IGNORECASE)
