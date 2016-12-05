# ga_solve method
def ga_solve(file=None, gui=True, maxtime=0):
    if(gui):
        import pygame
    pass

# Global vars
nogui_param = False
file_param = None
maxtime_param = 0

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
    flags_dict = dict([("--nogui", nogui_handler), ("--maxtime", maxtime_handler)]);


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
