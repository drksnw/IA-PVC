import pygame

# Classes
class City:
    def __init__(self, name, x, y):
        self.name = name
        self.x = int(x)
        self.y = int(y)
        self.parent = None

    def __str__(self):
        return self.name

    def distance_to(self, other):
        from math import sqrt
        x_dist = abs(self.x - other.x)
        y_dist = abs(self.y - other.y)
        return sqrt(x_dist ** 2 + y_dist ** 2)

    def draw(self, screen, color, radius):
        pygame.draw.circle(screen, color, (self.x, self.y), radius)

class Manager:
    dest_cities = []

    @staticmethod
    def add_city(city):
        Manager.dest_cities.append(city)

    @staticmethod
    def get_city(index):
        return Manager.dest_cities[index]

    @staticmethod
    def get_nearest_city(city, added_cities):
        nearest = None
        dist = 10000
        for cx in Manager.dest_cities:
            if cx != city:
                if city.distance_to(cx) < dist:
                    if cx not in added_cities:
                        nearest = cx
                        dist = city.distance_to(cx)
        return nearest

    @staticmethod
    def number_of_cities():
        return len(Manager.dest_cities)

class Individual:
    def __init__(self, indiv=None):
        from copy import deepcopy
        self._individual = []
        self._fitness = 0
        self._distance = 0
        if indiv != None:
            self._individual = deepcopy(indiv)
        else:
            for i in range(0, Manager.number_of_cities()):
                self._individual.append(None)

    def set_city(self, pos, city):
        self._individual[pos] = city
        self._fitness = 0
        self._distance = 0

    def get_city(self, pos):
        return self._individual[pos]

    def generate_individual(self):
        from random import randrange
        self.set_city(0, Manager.get_city(0))
        for city_index in range(1, Manager.number_of_cities()):
            self.set_city(city_index, Manager.get_nearest_city(self.get_city(city_index-1), self._individual))


    def get_distance(self):
        if self._distance is 0:
            tour_dist = 0
            for city_index in range(0, len(self._individual)):
                from_city = self.get_city(city_index)
                if city_index+1 < len(self._individual):
                    dest_city = self.get_city(city_index+1)
                else:
                    dest_city = self.get_city(0)
                tour_dist += from_city.distance_to(dest_city)
            self._distance = tour_dist
        return self._distance

    def get_fitness(self):
        if self._fitness is 0:
            self._fitness = 1/self.get_distance()
        return self._fitness

    def contains_city(self, city):
        return city in self._individual

    def individual_size(self):
        return len(self._individual)

    def __str__(self):
        return_str = "|"
        for i in range(self.individual_size()):
            return_str += str(self.get_city(i))+"|"
        return return_str


class Population:
    def __init__(self, size, init):
        self._individuals = [None]*size

        if init:
            for i in range(self.pop_size()):
                new_individual = Individual()
                new_individual.generate_individual()
                self.save_individual(i, new_individual)


    def save_individual(self, index, individual):
        self._individuals[index] = individual

    def get_individual(self, index):
        return self._individuals[index]

    def has_individual(self, individual):
        return individual in self._individuals

    def get_fittest(self):
        fittest = self._individuals[0]
        for i in range(0, self.pop_size()):
            if fittest.get_fitness() <= self.get_individual(i).get_fitness():
                fittest = self.get_individual(i)
        return fittest

    def pop_size(self):
        return len(self._individuals)


class GeneticalAlgorithm:
    mutation_rate = 0.003
    tournament_size = 7
    elitism = True

    @staticmethod
    def tournament_selection(pop):
        global cities
        from random import randrange

        tournament = Population(GeneticalAlgorithm.tournament_size, False)
        for i in range(GeneticalAlgorithm.tournament_size):
            rand_id = randrange(pop.pop_size())
            tournament.save_individual(i, pop.get_individual(rand_id))

        fittest = tournament.get_fittest()
        return fittest

    @staticmethod
    def crossover(parent_1, parent_2):
        from random import randrange
        child = Individual()
        start_pos = randrange(parent_1.individual_size())
        end_pos = randrange(parent_1.individual_size())

        for i in range(child.individual_size()):
            if start_pos < end_pos and i > start_pos and i < end_pos:
                child.set_city(i, parent_1.get_city(i))
            elif start_pos > end_pos:
                if not (i < start_pos and i > end_pos):
                    child.set_city(i, parent_1.get_city(i))

        for i in range(parent_2.individual_size()):
            if not child.contains_city(parent_2.get_city(i)):
                for ii in range(child.individual_size()):
                    if child.get_city(ii) is None:
                        child.set_city(ii, parent_2.get_city(i))
                        break

        return child

    @staticmethod
    def mutate(individual):
        from random import random, randrange
        for tour_pos_1 in range(individual.individual_size()):
            if random() <= GeneticalAlgorithm.mutation_rate:
                tour_pos_2 = randrange(individual.individual_size())

                city_1 = individual.get_city(tour_pos_1)
                city_2 = individual.get_city(tour_pos_2)

                individual.set_city(tour_pos_2, city_1)
                individual.set_city(tour_pos_1, city_2)
                GeneticalAlgorithm.mutation_rate = 0.003

    @staticmethod
    def evolve_population(pop):
        new_population = Population(pop.pop_size(), False)

        elitism_offset = 0
        if GeneticalAlgorithm.elitism:
            new_population.save_individual(0, pop.get_fittest())
            elitism_offset = 1

        for i in range(elitism_offset, new_population.pop_size()):
            parent_1 = GeneticalAlgorithm.tournament_selection(pop)
            parent_2 = GeneticalAlgorithm.tournament_selection(pop)
            child = GeneticalAlgorithm.crossover(parent_1, parent_2)
            new_population.save_individual(i, child)

        for i in range(elitism_offset, new_population.pop_size()):
            GeneticalAlgorithm.mutate(new_population.get_individual(i))

        return new_population

# Global vars
nogui_param = False
file_param = None
maxtime_param = 20
screen_x = 500
screen_y = 500

point_color = [10, 10, 200]
point_radius = 3

font_color = [255,255,255]

cities = []

def fill_cities(file_name):
    cities_data = ""
    with open(file_name, 'r') as f:
        cities_data = f.readlines()
    for city_data in cities_data:
        line = city_data.split(" ")
        cities.append(City(line[0], line[1], line[2]))


# ga_solve method
def ga_solve(_file=None, gui=True, maxtime=0):
    import sys
    import time
    if _file != None:
        fill_cities(_file)

    def draw(screen, color, radius, font):
        global font_color
        for city in cities:
            city.draw(screen, color, radius)
        text = font.render("Nombre %i" % len(cities), True, font_color)
        textRect = text.get_rect()
        screen.blit(text, textRect)
        pygame.display.flip()
    if(gui):
        global screen_x, screen_y, point_color, point_radius, font_color, cities
        from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN, K_ESCAPE

        pygame.init()
        window = pygame.display.set_mode((screen_x, screen_y))
        pygame.display.set_caption("Algorithmes génétiques")
        screen = pygame.display.get_surface()
        font = pygame.font.Font(None, 30)
        draw(screen, point_color, point_radius, font)

        collecting = True
        while collecting:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)
                elif event.type == KEYDOWN and event.key == K_RETURN:
                    collecting = False
                elif event.type == MOUSEBUTTONDOWN:
                    cities.append(City("v"+str(len(cities)+1), pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]))
                    screen.fill(0)
                    draw(screen, point_color, point_radius, font)

        for city in cities:
            Manager.add_city(city)

        pop = Population(len(cities), True)
        print("Initial distance", pop.get_fittest().get_distance())
        pop = GeneticalAlgorithm.evolve_population(pop)
        start_time = time.time()
        last_fittest = None
        while True:
            act_time = time.time()
            elapsed_time = act_time - start_time
            if elapsed_time > maxtime:
                print("Time elapsed.")
                break
            pop = GeneticalAlgorithm.evolve_population(pop)
            if last_fittest != str(pop.get_fittest()):
                first_city_pos = [pop.get_fittest().get_city(0).x, pop.get_fittest().get_city(0).y]
                previous_city_pos = [pop.get_fittest().get_city(0).x, pop.get_fittest().get_city(0).y]
                last_city_pos = []
                screen.fill(0)
                for ii in range(1, pop.get_fittest().individual_size()):
                    draw(screen, point_color, point_radius, font)
                    actual_city = pop.get_fittest().get_city(ii)
                    pygame.draw.line(screen, [0, 255, 255], (previous_city_pos[0], previous_city_pos[1]), (actual_city.x, actual_city.y))
                    previous_city_pos[0] = actual_city.x
                    previous_city_pos[1] = actual_city.y
                    last_city_pos = [actual_city.x, actual_city.y]
                pygame.draw.line(screen, [0, 255, 255], (first_city_pos[0], first_city_pos[1]), (last_city_pos[0], last_city_pos[1]))
                pygame.display.update()
                last_fittest = str(pop.get_fittest())
            else:
                GeneticalAlgorithm.mutation_rate = 1

        print("Finished")
        print("Final distance", pop.get_fittest().get_distance())
        print("Solution")
        print(str(pop.get_fittest()))

        while True:
            pass



# Main method
if __name__ == "__main__":
    from sys import argv

    def show_help():
        print("Usage:")
        print(argv[0], "<--nogui>", "<--maxtime <time>>", "<file name>")
        exit()

    skip_val = False

    def nogui_handler(dummy):
        global nogui_param
        nogui_param = True
    def maxtime_handler(maxtime):
        global maxtime_param
        global skip_val
        if maxtime is None:
            raise ValueError
        maxtime_int = int(maxtime)
        maxtime_param = maxtime_int
        skip_val = True
    def help_handler(dummy):
        show_help()
    flags_dict = dict([("--nogui", nogui_handler), ("--maxtime", maxtime_handler), ("--help", help_handler)]);


    for arg in argv:
        if argv.index(arg) != 0:
            if not skip_val:
                if(arg[0] == '-'):
                    # Is a flag
                    try:
                        if len(argv) <= argv.index(arg)+1:
                            flags_dict[arg](None)
                        else:
                            flags_dict[arg](argv[argv.index(arg)+1])
                    except ValueError:
                        print("Argument error")
                        show_help()
                else:
                    if file_param != None:
                        print("Wrong argument.")
                        show_help()
                    else:
                        file_param = arg
            else:
                skip_val = False

    ga_solve(_file=file_param, gui=(not nogui_param), maxtime=maxtime_param)
