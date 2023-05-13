class InterruptionsData:
    type = None
    start_time = None
    end_time = None
    location = None

    def __init__(self, utility_type, location, start_time, end_time):
        self.type = utility_type
        self.start_time = start_time
        self.end_time = end_time
        self.location = location

    def get_id(self):
        #TODO try to find something better
        return '{}_{}_{}-{}'.format(self.type, self.location, self.start_time, self.end_time)