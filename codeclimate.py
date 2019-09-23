import json
import requests
class Codeclimate:
    headers = {
        'Accept': 'application/vnd.api+json',
        'Authorization': 'Token token=', #insert codeclimate token
    }

    repos_id = '' #insert the repos id of CodeClimate project

    def getIssues(self):
        r = requests.get('https://api.codeclimate.com/v1/repos/'+self.repos_id, headers=self.headers)
        s = r.content.decode('utf-8')
        d = json.loads(s)
        snap_id = d['data']['relationships']['latest_default_branch_snapshot']['data']['id']

        iss_url = 'https://api.codeclimate.com/v1/repos/'+self.repos_id+'/snapshots/'+snap_id+'/issues'
        r = requests.get(iss_url, headers=self.headers)
        s = r.content.decode('utf-8')
        d = json.loads(s)
        #iss_count = d['data']['meta']['issues_count']
        iss_count = 0
        for elem in d['data']:
            try:
                status = elem['attributes']['status']['name']
            except:
                iss_count = iss_count + 1
                continue
            if status == 'wontfix' or status == 'invalid':
                continue
            else:
                iss_count = iss_count + 1
        return iss_count