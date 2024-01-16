class Client:
    def __init__(self):
        self.id = ""
        self.name = ""
        self.coordinate_x = 0.0
        self.coordinate_y = 0.0

    # CSV data extraction
    def assing(self, data_set):
        data = data_set.strip().split(',')
        if len(data) == 4:
            self.id, self.name, coordinate_x, coordinate_y = data
            try:
                self.coordinate_x = float(coordinate_x)
                self.coordinate_y = float(coordinate_y)
            except ValueError:
                raise ValueError("incorrect coordinates format")
        else:
            raise ValueError("incorrect data format")




