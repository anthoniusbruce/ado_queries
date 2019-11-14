import json
import story_point_data
import aft_velocity_response
import datetime

class StoryPointDataJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if (isinstance(o, story_point_data.StoryPointData)):
            return o.__dict__
        if (isinstance(o, set)):
            return list(o)
        if (isinstance(o, aft_velocity_response.AtfVelocityResponse)):
            return o.__dict__
        if (isinstance(o, datetime.datetime)):
            return str(o)

        return super(StoryPointDataJSONEncoder, self).default(o)