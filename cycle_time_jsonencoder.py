import json
import cycle_time
import datetime

class CycleTimeJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if (isinstance(o, cycle_time.CycleTime)):
            return o.__dict__
        if (isinstance(o, datetime.datetime)):
            return str(o)

        return super(CycleTimeJSONEncoder, self).default(o)