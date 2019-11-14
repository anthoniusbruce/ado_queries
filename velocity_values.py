class VelocityValues(object):
    def __init__(self, story_points, closers):
        self.story_points = story_points
        self.closers = closers

    def add(self, story_points, closers):
        self.story_points = self.story_points + story_points
        self.closers = self.closers.union(closers)