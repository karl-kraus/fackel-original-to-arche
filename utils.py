def fix_date(date_str):
    parts = date_str.split('-')
    if len(parts) == 3:
        day, month, year = parts
    elif len(parts) == 2:
        month, year = parts
        day = '01'
    else:
        print(date_str)
        return date_str
    day = f"{day:0>2}"
    month = f"{month:0>2}"
    return f"{year}-{month}-{day}"
