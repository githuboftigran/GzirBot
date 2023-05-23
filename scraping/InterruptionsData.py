class InterruptionsData:
    inter_id = None
    """A unique id for this instance"""
    type = None
    """Type of interruption. water, electricity, etc."""
    start_time = None
    end_time = None
    location = None

    def __init__(self, utility_type, inter_id, location, start_time, end_time):
        self.type = utility_type
        self.id = inter_id
        self.location = location
        self.start_time = start_time
        self.end_time = end_time
