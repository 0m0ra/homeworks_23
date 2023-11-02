"""Module for calculate stats."""

import json
import re
from math import ceil

import dateparser

DAYS_CONST = 60 * 60 * 24
HALF_YEAR = 183


def validate_email(email: str) -> bool:
    """Check email for accuracy.

    Args:
        email (str): user email

    Returns:
        bool: valid or invalid email
    """
    pattern = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'
    return re.match(pattern, email) is not None


def duration_dispersion(clients: dict[str, dict]) -> tuple[dict[str, dict], ...]:
    """Calculate duration on site for each user.

    Args:
        clients (dict[str, dict]): dict of users information

    Returns:
        tuple[dict[str, dict]]: calculated durations and sum of all timelines
    """
    duration_disp = {
        'under_2_days': 0,
        'under_week': 0,
        'under_half_year': 0,
        'over_half_year': 0,
    }
    count_durations = 0
    for users in clients.items():
        try:
            registered = dateparser.parse(clients[users[0]]['registered'])
            last_login = dateparser.parse(clients[users[0]]['last_login'])
        except KeyError:
            continue
        count_durations +=1
        how_long = ceil((last_login.timestamp() - registered.timestamp()) / DAYS_CONST)

        if how_long < 2:
            duration_disp['under_2_days'] += 1
        elif how_long < 7:
            duration_disp['under_week'] += 1
        elif how_long < HALF_YEAR:
            duration_disp['under_half_year'] += 1
        else:
            duration_disp['over_half_year'] += 1
    if count_durations:
        return duration_disp, sum(duration_disp.values())
    else:
        return duration_disp, 1


def email_dispersion(clients: dict[str, dict]) -> tuple[dict[str, dict], ...]:
    """Calculate email dispersion among users.

    Args:
        clients (dict[str, dict]): users and information about them

    Returns:
        tuple[dict[str, dict]]: stat of usage each email and sum of all usages
    """
    email_disp = {}
    count_emails = 0

    for users in clients.items():
        try:
            if not validate_email(clients[users[0]]['email']):
                continue
            email_host = clients[users[0]]['email'].split('@')[1]
        except KeyError:
            continue
        count_emails +=1
        if email_host in email_disp.keys():
            email_disp[email_host] += 1
        else:
            email_disp[email_host] = 1
    if not count_emails:
        raise KeyError('data doesn`t have email fields!')
    return email_disp, sum(email_disp.values()) 


def process_data(path_in: str, path_out: str) -> None:
    """Calculate email hosts and site experience duration dispersion.

    Args:
        path_in (str): path to input file
        path_out (str): path to output file

    Raises:
        FileNotFoundError: file or directory not found
        JSONDecodeError: fail to decode file in json

    Result:
        Json file with calculated stats
    """
    try:
        with open(path_in, 'r') as data_file:
            clients = json.loads(data_file.read())
    except FileNotFoundError:
        raise FileNotFoundError(f'file <{path_in}> not found')
    except json.decoder.JSONDecodeError:
        raise ValueError(f'file <{path_in}> is not valid')

    if not clients:
        raise ValueError('data file is empty!')

    email_disp, duration_disp = email_dispersion(clients), duration_dispersion(clients)

    stats = {'email_scatter': {}, 'duration_scatter': {}}
    for host in email_disp[0].keys():
        stats['email_scatter'][host] = (email_disp[0][host] / email_disp[1]) * 100

    for duration in duration_disp[0].keys():
        stats['duration_scatter'][duration] = (duration_disp[0][duration] / duration_disp[1]) * 100

    try:
        with open(path_out, 'w') as output_file:
            json.dump(stats, fp=output_file, indent=4)
    except FileNotFoundError:
        raise FileNotFoundError(f'file <{path_in}> not found')
process_data('hw2/test_data_hw2/data_emty.json', 'hw2/test_data_hw2/output.json')