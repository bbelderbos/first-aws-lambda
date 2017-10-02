import os
from pprint import pprint as pp
import re
import urllib.request

import pep8

gh_pr_url = 'https://api.github.com/repos/pybites/challenges/pulls/{}/files'
url_pattern = re.compile(r'https[^"]+')

TMP = '/tmp'


def lambda_handler(event, context):
    try:
        prid = int(event.get('prid', os.environ.get('prid')))
    except ValueError as ve:
        print(ve)
        raise

    raw_python_files = get_files_from_pr(prid)

    ret = pep8_files(raw_python_files)
    print('result: {}'.format(ret))
    return ret


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
        tempfile = os.path.join(TMP, os.path.basename(pyfile))
        num_faults = check_file(pyfile, tempfile)
        results[tempfile] = num_faults

    pp(results)

    return sum(results.values()) == 0


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
