import os
import re
import urllib.request

import pep8

gh_pr_url = 'https://api.github.com/repos/pybites/challenges/pulls/{}/files'
url_pattern = re.compile(r'https[^"]+')


def lambda_handler(event, context):
    # get code from payload
    prid = get_prid(event)
    raw_python_files = get_files_from_pr(prid)
    results = pep8_files(raw_python_files)
    print_report(results)


def get_prid(event):
    try:
        return int(event['prid'])
    except ValueError:
        print('ERROR: not an int')
        raise


def get_files_from_pr(prid):
    response = urllib.request.urlopen(gh_pr_url.format(prid))
    # https://stackoverflow.com/a/19156107
    content = response.read().decode(response.headers.get_content_charset())

    urls = url_pattern.findall(content)
    raw_python_files = [url for url in urls if '.py' in url
                        and '/raw/' in url]

    return raw_python_files


def pep8_files(raw_python_files):
    results = {}
    for pyfile in raw_python_files:
        tempfile = os.path.basename(pyfile)
        num_faults = check_file(pyfile, tempfile)
        results[tempfile] = num_faults

    return results


def check_file(pyfile, tempfile):
    try:
        urllib.request.urlretrieve(pyfile, tempfile)
    except Exception as exc:
        print('ERROR: could not retrieve file')
        return None

    num_faults = pep8.Checker(tempfile, show_source=True).check_all()

    if os.path.isfile(tempfile):
        os.remove(tempfile)

    return num_faults


def print_report(results):
    print('\nRESULTS')
    print('File -> issues')
    for filename, num_faults in results.items():
        print('{:<20} | {}'.format(filename, num_faults))
