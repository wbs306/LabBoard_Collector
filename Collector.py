class Collector:
    def __init__(self, name, have_task=True):
        self.name = name
        self.have_task = have_task
        self.data_dict = None

    def run_task(self):
        pass

    def get_data(self):
        pass
