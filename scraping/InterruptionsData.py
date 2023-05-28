class InterruptionsData:
    icon = ''  # Should be set in deriving classes
    type = ''  # Should be set in deriving classes

    def __init__(self, inter_id, location, start_time, end_time):
        self.id = inter_id
        self.location = location
        self.start_time = start_time
        self.end_time = end_time
