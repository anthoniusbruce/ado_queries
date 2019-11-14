class AtfVelocityResponse(object):
    def __init__(self, year, month, total_story_points, number_of_closers):
        self.year = year
        self.month = month
        self.total_story_points = total_story_points
        self.number_of_closers = number_of_closers
        if (self.number_of_closers == 0):
            self.average_story_points = self.total_story_points
        else:
            self.average_story_points = self.total_story_points / self.number_of_closers
