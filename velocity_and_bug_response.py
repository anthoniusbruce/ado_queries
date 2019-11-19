class VelocityAndBugResponse(object):
    def __init__(self, year, month, total_story_points, number_of_closers, average, bug_count):
        self.year = year
        self.month = month
        self.total_story_points = total_story_points
        self.number_of_closers = number_of_closers
        self.average_story_points = average
        self.bug_count = bug_count
