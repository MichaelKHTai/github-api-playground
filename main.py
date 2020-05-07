import argparse
import json
import requests
import settings
import sys
import time
from pathlib import Path

def alert_server(data):
    r = requests.post('http://127.0.0.1/newrepo', json={"data": data})
    if r.status_code == 200:
        print('New repo list sent.')
    else:
        print(f'Server Error Status: {r.status_code}')
        raise Exception

def write_complete_record(data):
    epoch = str(int(time.time()))
    file_name = f'repository_info_${epoch}.json'
    data_file_path = Path(__file__).parent / file_name
    with open(data_file_path, 'w') as record:
        json.dump(data, record)
    print(f'Saved new detail data in {file_name}')

def run(detail=False):
    r = requests.get(f'https://api.github.com/search/repositories?q={settings.SEARCH_KEYWORD}')
    # Indeed Github has 1000 items limitation per search, and they do not gaurantee a method for querying all data.
    # But, fortunately the repos using the asking keyword are still in adequate amount.
    if r.status_code == 200:
        full_data = r.json()
        repo_list = [x.get('full_name') for x in full_data['items']]

        ## Compare with the previous data
        # It should be done in database, but for convenience I simply use a json this time.
        data_file_path = Path(__file__).parent / 'repo_list.json'
        with open(data_file_path, 'w+') as f:
            pre_repo_list = []
            if f.read():
                pre_repo_list = json.load(f)
            new_repo = set(repo_list) - set(pre_repo_list)
        
            if len(new_repo) > 0:
                alert_server(list(new_repo))
                # Update the list only when the server is correctly updated.
                json.dump(repo_list, f)

        if detail:
            write_complete_record(full_data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Github Repo Searching Playground")
    parser.add_argument('--detail','-D', help='Export Repo detail to json file.', action='store_true')

    args = parser.parse_args()

    if args.detail:
        run(True)
    else:
        run()

    sys.exit(0)

