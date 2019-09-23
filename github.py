import json
import requests
import datetime

class GitHub:
    token = '' #insert github token
    project = '' #insert github project
    user = '' #insert github username

    def countRowsOnCommits(self, dateInit, dateEnd):
        r = requests.get('https://api.github.com/repos/'+self.user+'/'+self.project+'/commits', auth=(self.user, self.token))
        repos = json.loads(r.content)
        c = self.commitsPeriod(repos, dateInit, dateEnd)
        diff = self.commitsDays(c)
        total_commits = len(c)
        total_rows = 0
        for comm in c:
            id = str(comm['sha'])
            r_comm = requests.get('https://api.github.com/repos/'+self.user+'/'+self.project+'/commits/'+id, auth=(self.user, self.token))
            commit = json.loads(r_comm.content)
            rows = commit['stats']['total']
            total_rows = total_rows + rows
        if(total_commits == 0):
            return {'rows': 0, 'diff': diff}
        else:
            return {'rows': total_rows/total_commits, 'diff': diff}

    def commitsPeriod(self, comm, init, end):
        commits = []
        init = datetime.datetime.strptime(init, '%Y-%m-%d')
        end = datetime.datetime.strptime(end, '%Y-%m-%d')
        for c in comm:
            date = c['commit']['author']['date']
            date = date[0:10]
            date = datetime.datetime.strptime(date, '%Y-%m-%d')
            if date >= init and date <= end:
                commits.append(c)
        return commits

    def commitsDays(self, comm):
        dates = []
        for c in comm:
            date = c['commit']['author']['date']
            date = date[0:10]
            dates.append(date)
        dates = list(dict.fromkeys(dates))
        diff = len(dates)
        if diff == 0:
            return 1
        else:
            return diff

    def getIssues(self, init, end):
        r = requests.get('https://api.github.com/repos/'+self.user+'/'+self.project+'/issues',
                         auth=(self.user, self.token))
        issues = json.loads(r.content)
        count = 0
        for iss in issues:
            date = iss['created_at']
            date = date[0:10]
            date = datetime.datetime.strptime(date, '%Y-%m-%d')
            init = datetime.datetime.strptime(init, '%Y-%m-%d')
            end = datetime.datetime.strptime(end, '%Y-%m-%d')
            #if iss['state'] == 'open' and date >= init and date <= end:
            if date >= init and date <= end:
                count = count + 1
        return count

    '''def git_push(self, newrecord):
        PATH_OF_GIT_REPO = r''  # make sure .git folder is properly configured
        COMMIT_MESSAGE = 'Dataset updated, release id: '+newrecord[0]+'- date: '+newrecord[1]
        repo = Repo(PATH_OF_GIT_REPO)
        repo.git.add(update=True)
        repo.index.commit(COMMIT_MESSAGE)
        repo.git.push("origin", "HEAD:master")
        #origin = repo.remote(name='origin')
        #origin.push()
        try:
            
        except:
            print('Some error occured while pushing the code')
        finally:
            print('Code push from script succeeded')'''


