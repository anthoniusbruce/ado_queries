class StoryPointData(object):
    def __init__(self, workitemid, firstactive, resolved):
        self.workitemid = workitemid
        self.firstactive= firstactive
        self.resolved = resolved
        self.storypoints = 0
        self.closers = set()

    def __repr__(self):
        return "<workitemid:%s firstactive:%s resolved:%s storypoints:%s>\n" % (self.workitemid, self.firstactive, self.resolved, self.storypoints)

