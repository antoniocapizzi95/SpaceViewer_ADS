import manage_csv, jenkins, time
jen = jenkins.Jenkins()
time.sleep(5)
result = manage_csv.Manage_csv.readResult()
if not result:
    jen.proceedAnomalyDetection()


