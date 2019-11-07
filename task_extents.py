class TaskExtents(object):
    def __init__(self, created, closed):
        self.created_date = created
        self.closed_date = closed

    def __repr__(self):
        return "<created_date:%s closed_date:%s>" % (self.created_date, self.closed_date)
