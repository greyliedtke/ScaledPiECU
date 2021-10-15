"""
Simple file loggger to record and save speed data
"""

# necessary imports
import pandas
from datetime import datetime


# run log object to create and write to log
class RunLog:
    def __init__(self):
        self.df_format = {".25 S": [0], "PFC": [0], "N2": [0], "Res_level": [0]}
        self.name = None
        self.df = None
        self.pfc = []
        self.n2 = []
        self.res = []

    def create_log(self):
        # reformat for file format name
        now = datetime.now()
        fn = now.strftime("%d/%m/%Y %H:%M:%S")
        fn = fn.replace("/", "-")
        fn = fn.replace(":", "")

        self.name = fn

    def add(self, pfc, n2, res):
        self.pfc.append(pfc)
        self.n2.append(n2)
        self.res.append(res)

    def end_log(self):
        log = {"PFC": self.pfc, "N2": self.n2, "Res": self.res}
        df_log = pandas.DataFrame(log)
        # Save to csv file
        df_log.to_csv("ECU_log/"+self.name, index=True)

        # wipe arrays
        self.pfc = []
        self.n2 = []
        self.res = []


# initialize run logger object
rl = RunLog()


# END
