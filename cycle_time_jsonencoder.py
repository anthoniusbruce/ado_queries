import json
import cycle_time

class CycleTimeJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if (isinstance(o, cycle_time.CycleTime)):
            return o.__dict__

        return super(CycleTimeJSONEncoder, self).default(o)