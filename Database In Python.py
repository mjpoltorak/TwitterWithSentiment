import json
import requests
import sys

'''
See https://www.openfigi.com/api for more information.
'''

openfigi_url = 'https://api.openfigi.com/v1/mapping'
openfigi_apikey = '28fd4b05-17d4-4d89-8d72-294e480749c5'  # Put API Key here
openfigi_headers = {'Content-Type': 'text/json'}

if openfigi_apikey:
    openfigi_headers['X-OPENFIGI-APIKEY'] = openfigi_apikey

jobs = [{'idType': 'TICKER', 'idValue': 'GOOG', 'exchCode': 'US'},
        {'idType': 'TICKER', 'idValue': 'GOOGL', 'exchCode': 'US'}]


def map_jobs(jobs):
    '''
    Send an collection of mapping jobs to the API in order to obtain the
    associated FIGI(s).
    Parameters
    ----------
    jobs : list(dict)
        A list of dicts that conform to the OpenFIGI API request structure. See
        https://www.openfigi.com/api#request-format for more information. Note
        rate-limiting requirements when considering length of `jobs`.
    Returns
    -------
    list(dict)
        One dict per item in `jobs` list that conform to the OpenFIGI API
        response structure.  See https://www.openfigi.com/api#response-fomats
        for more information.
    '''
    too_many_mapping_jobs = len(jobs) > (100 if openfigi_apikey else 10)
    assert not too_many_mapping_jobs, 'Too many mapping jobs'
    response = requests.post(url=openfigi_url, headers=openfigi_headers,
                             data=json.dumps(jobs))
    if response.status_code != 200:
        print(response.status_code)
        sys.exit(1)
    return response.json()


def job_results_handler(jobs, job_results):

    for job, result in zip(jobs, job_results):
        figi_list = [d['name'] for d in result.get('data', [])]
        print(figi_list)


def main():
    '''
    Map the defined `jobs` and handle the results.
    Returns
    -------
        None
    '''
    job_results = map_jobs(jobs)
    job_results_handler(jobs, job_results)

main()
