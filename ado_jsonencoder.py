import json
import story_point_data
import atf_velocity_response
import datetime
import cycle_time
import velocity_and_bug_response

class AdoJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if (isinstance(o, story_point_data.StoryPointData)):
            return o.__dict__
        if (isinstance(o, set)):
            return list(o)
        if (isinstance(o, atf_velocity_response.AtfVelocityResponse)):
            return o.__dict__
        if (isinstance(o, datetime.datetime)):
            return str(o)
        if (isinstance(o, cycle_time.CycleTime)):
            return o.__dict__
        if (isinstance(o, velocity_and_bug_response.VelocityAndBugResponse)):
            return o.__dict__

        return super(AdoJSONEncoder, self).default(o)
