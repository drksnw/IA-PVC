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

    def draw(self, screen, color, radius):
        pygame.draw.circle(screen, color, (self.x, self.y), radius)


# Global vars
nogui_param = False
file_param = None
maxtime_param = 0
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
def ga_solve(file=None, gui=True, maxtime=0):
    import sys
    if file is not None:
        fill_cities(file)

    def draw(screen, color, radius, font):
        global font_color
        screen.fill(0)
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
                    draw(screen, point_color, point_radius, font)

        screen.fill(0)



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
        if argv.index(arg) is not 0:
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
                    if file_param is not None:
                        print("Wrong argument.")
                        show_help()
                    else:
                        file_param = arg
            else:
                skip_val = False

    ga_solve(file=file_param, gui=(not nogui_param), maxtime=maxtime_param)
