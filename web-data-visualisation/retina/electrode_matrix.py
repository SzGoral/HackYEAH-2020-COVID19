import numpy as np


class ElectrodeMatrix:

    def __init__(self, path, pattern_limit=None):
        """
            loads data from the electrode coordintes csv
            optionally limits the patterns to a certain subset
            from pattern_limit int array
        """
        with open(path) as f:
            lines = f.readlines()
        self.lut = np.zeros((len(lines), 2))
        self.pattern_limit = pattern_limit
        for line in lines:
            if line:
                index, x, y = line.split(',')
                if self.pattern_limit and int(index) not in self.pattern_limit:
                    self.lut[int(index) - 1] = None, None
                else:
                    self.lut[int(index) - 1, :] = int(x), int(y)

    def get_border_patterns(self):
        """
            list of lists of patterns in the clockwise order
            order: up, right, down, left
        """
        maxY = max(self.lut, key=lambda x: x[1])[1]
        minY = min(self.lut, key=lambda x: x[1])[1]

        maxX = max(self.lut, key=lambda x: x[0])[0]
        maxXIndented = max(
            self.lut, key=lambda x: x[0] if x[0] != maxX else -np.inf)[0]

        minX = min(self.lut, key=lambda x: x[0])[0]
        minXIndented = min(
            self.lut, key=lambda x: x[0] if x[0] != minX else np.inf)[0]

        up, right, down, left = [], [], [], []
        for pattern_idx in range(len(self.lut)):
            if self.pattern_limit and (pattern_idx + 1 not in self.pattern_limit):
                continue
            if self.lut[pattern_idx][1] == maxY:
                up.append(pattern_idx + 1)
            elif self.lut[pattern_idx][1] == minY:
                down.append(pattern_idx + 1)
            elif self.lut[pattern_idx][0] == maxX or self.lut[pattern_idx][0] == maxXIndented:
                right.append(pattern_idx + 1)
            elif self.lut[pattern_idx][0] == minX or self.lut[pattern_idx][0] == minXIndented:
                left.append(pattern_idx + 1)
        return up, right, down, left

    def get_distance_between(self, p1, p2):
        c1 = self.lut[p1 - 1]
        if np.isnan(c1[0]) or np.isnan(c1[1]):
            raise IndexError("Invalid patterns")
        c2 = self.lut[p2 - 1]
        if np.isnan(c2[0]) or np.isnan(c2[1]):
            raise IndexError("Invalid patterns")
        return np.linalg.norm(c1 - c2)

    def get_bounds(self):
        maxY = max(self.lut, key=lambda x: x[1])[1]
        minY = min(self.lut, key=lambda x: x[1])[1]
        minX = min(self.lut, key=lambda x: x[0])[0]
        maxX = max(self.lut, key=lambda x: x[0])[0]
        return minX, maxX, minY, maxY

    def get_neighbours(self, pattern_id, distance=68):
        electrodes = [{
            "index": i + 1,
            "distance": self.get_distance_between(pattern_id, i + 1)
        } for i in range(len(self.get_coords()))]
        electrodes.sort(key=lambda x: x["distance"])
        pattern_ids = []
        for electrode in electrodes:
            if self.pattern_limit and (electrode["index"] not in self.pattern_limit):
                continue
            elif electrode["distance"] <= distance:
                pattern_ids.append(electrode["index"])
        pattern_ids.remove(pattern_id)
        return pattern_ids

    def get_coord_for_pattern(self, pattern_id):
        return self.lut[pattern_id - 1]

    def get_coords(self):
        values = []
        for value in self.lut:
            if not np.isnan(value[0]) and not np.isnan(value[1]):
                values.append(value)
        return values


if __name__ == "__main__":
    electrodes = ElectrodeMatrix('electrodes.csv')
    b = electrodes.get_neighbours(440)
    c = electrodes.get_border_patterns()
    a = 2
