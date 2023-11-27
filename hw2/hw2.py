"""hw2 module."""
import json
import re
import statistics

AGE = "age"
MAX_AGE = "max_age"
MIN_AGE = "min_age"
AVERAGE_AGE = "average_age"
MEDIAN_AGE = "median_age"


def process_data(src_file: str, dst_file: str) -> None:
    """
    Process data from the source file and write the result to the destination file.

    Args:
        src_file (str): The path to the source file.
        dst_file (str): The path to the destination file.
    """
    with open(src_file, "r") as input_json:
        users = json.load(input_json)

    years_result = year_percentage(users)
    age_result = age_stats(users)
    full_result = {
        **age_result,
    }
    full_result.update({"years_statistics": years_result})
    with open(dst_file, "x") as output_json:
        json.dump(full_result, output_json, indent=4)


def age_stats(users: dict) -> dict:
    """
    Calculate age stats.

    Args:
        users (dict): dict of users.

    Returns:
        dict: age stats - max, min and median
    """
    result_ages = {}
    ages = [users[user][AGE] for user in users]
    result_ages.update({MAX_AGE: max(ages)})
    result_ages.update({MIN_AGE: min(ages)})
    result_ages.update({AVERAGE_AGE: sum(ages) / max(len(ages), 1)})
    result_ages.update({MEDIAN_AGE: statistics.median(ages)})
    return result_ages


def year_percentage(users: dict) -> dict:
    """
    Calculate year percentage.

    Args:
        users (dict): dict of users.

    Returns:
        dict: dict of years and their percentage

    Raises:
        ValueError: Incorrect date format
    """
    years = {}
    for user in users.keys():
        if "registered" not in users[user]:
            raise ValueError('No "registered" entry')
        year = users[user]["registered"]
        if re.match(r"\d{4}-\d{2}-\d{2}", year):
            year = year.split("-")[0]
        else:
            raise ValueError("Incorrect date format")
        if year in years:
            years.update({year: years.get(year, 0) + 1})
        else:
            years.update({year: 1})
    count_of_years = len(years)
    for elem in years:
        years[elem] = (years.get(elem, 0) / count_of_years) * 100
    return years
