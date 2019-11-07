import json
import story_point_data

class StoryPointDataJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if (isinstance(o, story_point_data.StoryPointData)):
            return o.__dict__

        return super(StoryPointDataJSONEncoder, self).default(o)