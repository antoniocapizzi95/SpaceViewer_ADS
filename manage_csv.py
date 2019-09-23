import csv
from datetime import date, timedelta
import datetime

class Manage_csv:
    git = None
    codeclimate = None
    jenkins = None
    def __init__(self, git, codeclimate, jenkins):
        self.git = git
        self.codeclimate = codeclimate
        self.jenkins = jenkins

    def create_csv(self): #to use only first time with dataset empty
        init = '2019-05-15'
        today = date.today()
        today = today.strftime('%Y-%m-%d')
        roc = self.git.countRowsOnCommits(init, today)
        diff = roc['diff'] #days between
        rowscommits = roc['rows'] / diff
        cc_issues = self.codeclimate.getIssues() / diff
        jeninfo = self.jenkins.getJenkinsInformation(init, today)
        gh_issues = self.git.getIssues(init, today) / diff

        with open('dataset.csv', 'w') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(['id', 'date', 'code_rows_commits', 'builds_failed', 'tests_failed', 'deliveries_failed', 'cc_issues', 'gh_issues', 'anomaly'])
            filewriter.writerow(['1', today, rowscommits, jeninfo['failed_builds'] / diff, jeninfo['failed_tests'] / diff, jeninfo['failed_deliveries'] / diff, cc_issues, gh_issues, 0])

        with open('dataset_clean.csv', 'w') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(['id', 'date', 'code_rows_commits', 'builds_failed', 'tests_failed', 'deliveries_failed', 'cc_issues', 'gh_issues', 'anomaly'])
            filewriter.writerow(['1', today, rowscommits, jeninfo['failed_builds'] / diff, jeninfo['failed_tests'] / diff, jeninfo['failed_deliveries'] / diff, cc_issues, gh_issues, 0])

    def getLatestInformation(self, dateinit):
        last_dataset = self.read_csv()
        last_dataset = last_dataset['dataset']
        last_dataset_len = len(last_dataset)
        last_record = last_dataset[last_dataset_len - 1]
        last_id = last_record[0]
        last_id = int(last_id)
        today = date.today()
        today = today.strftime('%Y-%m-%d')
        if dateinit != today:
            dateinit = self.addOneDay(dateinit)
        roc = self.git.countRowsOnCommits(dateinit, today)
        diff = roc['diff'] #days between
        rowscommits = roc['rows'] / diff
        cc_issues = self.codeclimate.getIssues() / diff
        jeninfo = self.jenkins.getJenkinsInformation(dateinit, today)
        gh_issues = self.git.getIssues(dateinit, today) / diff
        new_record = [str(last_id + 1), today, rowscommits, jeninfo['failed_builds'] / diff, jeninfo['failed_tests'] / diff, jeninfo['failed_deliveries'] / diff, cc_issues, gh_issues]
        return new_record


    def addOneDay(self, date):
        newdate = datetime.datetime.strptime(date, "%Y-%m-%d")
        newdate = newdate + timedelta(days=1)
        newdate = newdate.strftime("%Y-%m-%d")
        return newdate


    def read_csv(self):
        dataset = []
        with open('dataset.csv', 'r') as f:
            reader = csv.reader(f)
            i = 0
            for row in reader:
                if len(row) > 0 and i != 0:
                    dataset.append(row)
                i = 1
        dataset_clean = []
        with open('dataset_clean.csv', 'r') as f:
            reader = csv.reader(f)
            i = 0
            for row in reader:
                if len(row) > 0 and i != 0:
                    dataset_clean.append(row)
                i = 1
        return {'dataset': dataset, 'dataset_clean': dataset_clean}

    def addRow(self, newrecord, anomaly):
        newrecord.append(anomaly)
        with open(r'dataset.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow(newrecord)
        if not anomaly:
            with open(r'dataset_clean.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow(newrecord)
        self.writeResult(anomaly)

    def writeResult(self, anomaly):
        with open('result.csv', 'w') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow([anomaly])

    @staticmethod
    def readResult():
        result = 0
        with open('result.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) > 0:
                    result = row[0]
                    result = int(result)
        return result


