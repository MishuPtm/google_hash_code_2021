from collections import defaultdict


class Street:
    intersections = defaultdict(list)
    streets = {}
    street_scores = {}

    def __init__(self, line):
        parameters = line.strip().split()
        self.start = int(parameters[0])
        self.end = int(parameters[1])
        self.name = parameters[2]
        self.length = int(parameters[3])
        Street.intersections[self.end].append(self.name)
        self.score = 0
        Street.street_scores[self.name] = 0
        Street.streets[self.name] = self

    def __repr__(self):
        return f"{self.name}\t Start: {self.start}, End: {self.end}, Length: {self.length}\n"

    @classmethod
    def get_intersection_score(cls, streets):
        output = 0
        for street in streets:
            output += cls.street_scores[street]
        return output


class Car:
    cars_list = []
    def __init__(self, line):
        self.nb_of_roads = line.strip().split()[0]
        self.path = line.strip().split()[1:]
        Car.cars_list.append(self)

    @classmethod
    def drive(cls, duration, bonus_points):
        cars_to_be_removed = []
        for car in Car.cars_list:
            time_required = 0
            for road in car.path:
                time_required += Street.streets[road].length
            if time_required >= duration*0.8:
                cars_to_be_removed.append(car)

        print(f"Removing {len(cars_to_be_removed)} cars that cannot make it in time")
        for car in cars_to_be_removed:
            Car.cars_list.remove(car)
            
        for car in Car.cars_list:            
            for road in car.path:
                Street.street_scores[road] += 1
                Street.streets[road].score += 1


class Simulation:
    def __init__(self, cars, streets, duration, bonus, intersections):
        self.cars = cars
        self.street = streets
        self.duration = duration
        self.bonus = bonus
        self.intersections = intersections
        Street.streets = {}

    def sort_cars(self):
        
        pass

    def begin_simulation(self):
        for i in range(self.duration):
            pass


def exportFile(intersections, fileName, min_intersection_score=-1):
    lines = []
    empty_inersections = []
    for intersectionId, streetNames in intersections.items():
        intersection_score = Street.get_intersection_score(streetNames)
        avg = intersection_score / len(streetNames)
        for street in streetNames:
            if Street.street_scores[street] < 1:
                streetNames.remove(street)

        if len(streetNames) == 0:
            empty_inersections.append(intersectionId)
        elif intersection_score < min_intersection_score:
            empty_inersections.append(intersectionId)
            

    for intersection in empty_inersections:
        intersections.pop(intersection)

    lines.append(f"{len(intersections)}\n")
    counter = 0
    for intersectionId, streetNames in intersections.items():
        lines.append(f"{intersectionId}\n")
        lines.append(f"{len(streetNames)}\n")
        intersection_total = 0
        for street in streetNames:
            intersection_total += Street.streets[street].score
            
        intersection_score = Street.get_intersection_score(streetNames)
        avg = intersection_score / len(streetNames)

        for street in streetNames:
            
            seconds = 1

            if Street.streets[street].score > (avg * 4):
                seconds += 1
                counter += 1
            if Street.streets[street].score > (avg * 2):

                seconds += 1
                pass

            lines.append(f"{street} {seconds}\n")

    lines[-1] = lines[-1].replace("\n", "")
    print(f"{counter} roads were higher than average")
    with open(fileName, "w") as f:
        f.writelines(lines)


def importFile(filename):
    duration = 0
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
            Street(f.readline())

        for y in range(vehicles):
            Car(f.readline())
    
    #print(carsList, streetList)
    #print(Street.intersections)
    return duration, bonus_points


def process(file):
    duration, bonus_points = importFile(file+".txt")    
    Car.drive(duration, bonus_points)
    if file == "d":
        exportFile(Street.intersections, file+".out", -1)
    else:
        exportFile(Street.intersections, file+".out")
    Street.intersections = defaultdict(list)
    Car.cars_list = []
    Street.street_scores = {}

if __name__ == "__main__":
    files = ["a", "b", "c", "d", "e", "f"]
    for file in files:        
        process(file)

