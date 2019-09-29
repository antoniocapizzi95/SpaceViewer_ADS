import requests, json, datetime

class Jenkins:
    jenkinsServer = '' #insert name:token@serveraddress:port from Jenkins
    project = '' #insert name of Jenkins project

    def getJenkinsInformation(self, init, end):
        r = requests.get(
            'http://'+self.jenkinsServer+'/job/'+self.project+'/wfapi/runs')
        c = json.loads(r.content)

        init = datetime.datetime.strptime(init, '%Y-%m-%d')
        end = datetime.datetime.strptime(end, '%Y-%m-%d')
        builds = []
        for elem in c:
            date = datetime.datetime.fromtimestamp(elem['startTimeMillis'] // 1000.0)
            date = date.strftime("%Y-%m-%d, %H:%M:%S")
            date = date[0:10]
            date = datetime.datetime.strptime(date, '%Y-%m-%d')
            if date >= init and date <= end:
                builds.append(elem)
        num_builds = 0
        num_tests = 0
        num_deliveries = 0
        for b in builds:
            stages = b['stages']
            for s in stages:
                if s['name'] == 'Build' and s['status'] != 'SUCCESS':
                    num_builds = num_builds + 1
                    continue
                if s['name'] == 'Test' and s['status'] != 'SUCCESS':
                    num_tests = num_tests + 1
                    continue
                if s['name'] == 'Deliver' and s['status'] != 'SUCCESS':
                    num_deliveries = num_deliveries + 1
                    continue
        information = {'failed_builds': num_builds, 'failed_tests': num_tests, 'failed_deliveries': num_deliveries}
        return information

    def proceedAnomalyDetection(self):
        jenkinsServer = self.jenkinsServer
        project = 'SpaceViewer_AnomalyDetection'
        input_id = 'ADJob'
        r = requests.get(
            'http://' + jenkinsServer + '/job/' + project + '/wfapi/runs')
        c = json.loads(r.content)

        latest = c[0]['id']
        status = c[0]['status']
        if (status == 'PAUSED_PENDING_INPUT'):
            r2 = requests.post(
                'http://' + jenkinsServer + '/job/' + project + '/' + latest + '/input/' + input_id + '/proceedEmpty')

    def proceedProduction(self):
        jenkinsServer = self.jenkinsServer
        project = '' #insert the project name from jenkins
        input_id = '' #insert the job id declared in jenkinsfile
        buildToken = '' #insert the build token to start the job
        r = requests.get(
            'http://' + jenkinsServer + '/job/' + project + '/wfapi/runs')
        c = json.loads(r.content)

        latest = c[0]['id']
        status = c[0]['status']
        if (status == 'PAUSED_PENDING_INPUT'):
            r2 = requests.post(
                'http://' + jenkinsServer + '/job/' + project + '/' + latest + '/input/' + input_id + '/proceedEmpty')
            run = 'http://' + jenkinsServer + '/job/' + project + '/build?token=' + buildToken
            r2 = requests.post(run)
        if (status == 'SUCCESS' or status == 'ABORTED' or status == 'FAILURE'):
            run = 'http://' + jenkinsServer + '/job/' + project + '/build?token=' + buildToken
            r2 = requests.post(run)
