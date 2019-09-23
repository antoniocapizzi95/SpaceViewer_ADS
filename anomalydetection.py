from sklearn.neighbors import LocalOutlierFactor
import slack

class AnomalyDetection:

    csv = None
    jenkins = None
    doAD = 0

    def __init__(self, jenkins, csv, ad):
        self.csv = csv
        self.jenkins = jenkins
        self.doAD = ad

    def lof(self, train, test, n):
        clf = LocalOutlierFactor(n_neighbors=n, novelty=True, contamination=0.1)
        clf.fit(train)
        pred_test = clf.predict(test)
        return pred_test

    def prepareDataset(self, dataset):
        datasetmod = []
        for row in dataset:
            if int(row[8]) == 0:
                newrecord = [row[2], row[3], row[4], row[5], row[6], row[7]]
                newrecord = self.toNumber(newrecord)
                datasetmod.append(newrecord)
        return datasetmod

    def createTest(self, lastrecord, newrecord):
        test = []
        lastrecord = [lastrecord[2], lastrecord[3], lastrecord[4], lastrecord[5], lastrecord[6], lastrecord[7]]
        lastrecord = self.toNumber(lastrecord)
        newrecord = [newrecord[2], newrecord[3], newrecord[4], newrecord[5], newrecord[6], newrecord[7]]
        newrecord = self.toNumber(newrecord)
        test.append(lastrecord)
        test.append(newrecord)
        return test

    def executeAD(self, dataset):
        datasetlen = len(dataset)
        lastrecord = dataset[datasetlen - 1]
        lastdate = lastrecord[1]
        dataset = self.prepareDataset(dataset)
        newrecord = self.csv.getLatestInformation(lastdate)
        result = []
        if self.doAD == 1:
            test = self.createTest(lastrecord, newrecord)
            result = self.lof(dataset, test, len(dataset) - 1)
        else:
            result = [0, 1]
        sl = slack.Slack()
        if result[1] == 1:
            self.csv.addRow(newrecord, 0)
            print("no anomalies detected")
            sl.sendMessage("SpaceViewer: no anomalies detected, the release to production will continue automatically")
        if result[1] == -1:
            self.csv.addRow(newrecord, 1)
            print("anomalies detected")
            sl.sendMessage("SpaceViewer: anomalies detected, the release to production is suspended, you can choose to continue the release from Jenkins")

    def toNumber(self, array):
        newarray = []
        for elem in array:
            newarray.append(float(elem))
        return newarray