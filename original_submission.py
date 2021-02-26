from collections import defaultdict


class Street:
    intersections = defaultdict(list)
    street_scores = {}

    def __init__(self, line):
        parameters = line.strip().split()
        self.start = int(parameters[0])
        self.end = int(parameters[1])
        self.name = parameters[2]
        self.length = int(parameters[3])
        Street.intersections[self.end].append(self.name)
        Street.street_scores[self.name] = 0

    def __repr__(self):
        return f"{self.name}\t Start: {self.start}, End: {self.end}, Length: {self.length}\n"


class Car:
    cars_list = []

    def __init__(self, line):
        self.nb_of_roads = line.strip().split()[0]
        self.path = line.strip().split()[1:]
        Car.cars_list.append(self)

    def __repr__(self):
        return f"Car with {self.nb_of_roads} roads\n"

    @classmethod
    def drive(cls):
        """
        This function will score each road depending on how many cars travel on it.
        :return:
        """
        for car in Car.cars_list:
            for road in car.path:
                if road in Street.street_scores:
                    Street.street_scores[road] += 1


class Simulation:
    """
    We were very ambitious when we started the challenge, but soon realised that we don't have time to implement
    anything of what was discussed. So instead we went with the blind approach to just set all lights green for a
    fixed period of time.
    """
    def __init__(self, cars, streets, duration, bonus, intersections):
        self.cars = cars
        self.street = streets
        self.duration = duration
        self.bonus = bonus
        self.intersections = intersections

    def sort_cars(self):
        pass

    def begin_simulation(self):
        for i in range(self.duration):
            pass


def exportFile(intersections, fileName):
    """
    This started as an export function, but ended up as having a lot of logic happening in it.

    """
    lines = []
    for intersectionId, streetNames in intersections.items():
        for street in streetNames:
            # Remove a road from the schedule if that road is not traveled by any car
            if Street.street_scores[street] == 0:
                streetNames.remove(street)

        # This was supposed to remove intersections that are not traveled by any car
        if len(streetNames) == 0:
            # this was writen on the last few mins of the challenge,
            # my brain stopped working and i was not able to find a way to pop elements from a dictionary
            # this output will mess some files, as we are trying to add to the schedule intersection without any green
            # intersections.pop(intersectionId)
            pass

    lines.append(f"{len(intersections)}\n")
    for intersectionId, streetNames in intersections.items():
        lines.append(f"{intersectionId}\n")
        lines.append(f"{len(streetNames)}\n")
        for street in streetNames:
            lines.append(f"{street} 2\n")
    lines[-1] = lines[-1].replace("\n", "")

    with open(fileName, "w") as f:
        f.writelines(lines)


def importFile(filename):
    carsList = []    # Now when commenting i realised these are redundant, as i am using the class variable instead
    streetList = []  # Now when commenting i realised these are redundant, as i am using the class variable instead
    duration = 0
    intersections = 0
    streets = 0
    vehicles = 0
    bonus_points = 0

    with open(filename, "r") as f:
        line = f.readline()
        parameters = line.strip().split()
        duration = int(parameters[0])
        intersections = int(parameters[1])
        streets = int(parameters[2])
        vehicles = int(parameters[3])
        bonus_points = int(parameters[4])

        for x in range(streets):
            streetList.append(Street(f.readline()))

        for y in range(vehicles):
            carsList.append(Car(f.readline()))
    # print(carsList, streetList)
    # print(Street.intersections)


def process(file):
    importFile(file+".txt")
    Car.drive()     # this will score each road so we can see which are traveled an which are not

    exportFile(Street.intersections, file+".out")
    Street.intersections = defaultdict(list)    # Clears the intersections for next file
    Car.cars_list = []                          # Clears the cars for next file
    # Now when writing the comments i realised i forgot to also clear the street scores.
    # This could be an issue if same road is present across multiple input files.


if __name__ == "__main__":
    files = ["a", "b", "c", "d", "e", "f"]
    for file in files:
        process(file)
