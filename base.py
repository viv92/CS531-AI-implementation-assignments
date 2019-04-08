import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

#max iters
MAX_ITERS = 200

#grid - global for debugging
# TODO: turn local at the end
grid = np.ones((10,10)).astype('bool')


class roomed_environment:
    global grid
    #constructor
    def __init__(self):
        #signals to agent
        self.home = True
        self.wall = False
        #position and oreintation of agent (only for environment to generate next percept)
        self.direction = "north" #since agent starts pointing upwards
        self.x = 0
        self.y = 9 #since agent starts from bottom-left corner

        #door positions
        self.d1 = np.array([4.5,5])
        self.d2 = np.array([5,4.5])
        self.d3 = np.array([4.5,4])
        self.d4 = np.array([4,4.5])

    #function to generate next percept
    def step(self, action):

        if action == "suck":
            #update current cell state to clean
            grid[self.y][self.x] = False
            return (grid[self.y][self.x], self.home, self.wall)


        if action == "forward":
            #verify no wall in front
            if self.wall == False:
                #move agent forward in current direction and check for wall in new position
                if self.direction == "north":
                    self.y -= 1
                    if self.y == 0: #outer wall
                        self.wall = True
                    if self.y == 5: #room wall
                        if self.x == self.d2[0] or self.x == self.d4[0]: #door
                            self.wall = False
                        else:
                            self.wall = True
                if self.direction == "south":
                    self.y += 1
                    if self.y == 9: #outer wall
                        self.wall = True
                    if self.y == 4: #room wall
                        if self.x == self.d2[0] or self.x == self.d4[0]: #door
                            self.wall = False
                        else:
                            self.wall = True
                if self.direction == "east":
                    self.x += 1
                    if self.x == 9: #outer wall
                        self.wall = True
                    if self.x == 4: #room wall
                        if self.y == self.d1[1] or self.y == self.d3[1]: #door
                            self.wall = False
                        else:
                            self.wall = True
                if self.direction == "west":
                    self.x -= 1
                    if self.x == 0: #outer wall
                        self.wall = True
                    if self.x == 5: #room wall
                        if self.y == self.d1[1] or self.y == self.d3[1]: #door
                            self.wall = False
                        else:
                            self.wall = True

                #check if new position is home
                if self.x == 0 and self.y == 0:
                    self.home = True

            return (grid[self.y][self.x], self.home, self.wall)


        if action == "turn_left":
            #update direction and check for wall in new orientation
            self.wall = False
            if self.direction == "north":
                self.direction = "west"
                if self.x == 0: #outer wall
                    self.wall = True
                if self.x == 5: #room wall
                    if self.y == self.d1[1] or self.y == self.d3[1]: #door
                        self.wall = False
                    else:
                        self.wall = True
            elif self.direction == "west":
                self.direction = "south"
                if self.y == 9: #outer wall
                    self.wall = True
                if self.y == 4: #room wall
                    if self.x == self.d2[0] or self.x == self.d4[0]: #door
                        self.wall = False
                    else:
                        self.wall = True
            elif self.direction == "south":
                self.direction = "east"
                if self.x == 9: #outer wall
                    self.wall = True
                if self.x == 4: #room wall
                    if self.y == self.d1[1] or self.y == self.d3[1]: #door
                        self.wall = False
                    else:
                        self.wall = True
            else:
                self.direction = "north"
                if self.y == 0: #outer wall
                    self.wall = True
                if self.y == 5: #room wall
                    if self.x == self.d2[0] or self.x == self.d4[0]: #door
                        self.wall = False
                    else:
                        self.wall = True

            return (grid[self.y][self.x], self.home, self.wall)


        if action == "turn_right":
            #update direction and check for wall in new orientation
            self.wall = False
            if self.direction == "south":
                self.direction = "west"
                if self.x == 0: #outer wall
                    self.wall = True
                if self.x == 5: #room wall
                    if self.y == self.d1[1] or self.y == self.d3[1]: #door
                        self.wall = False
                    else:
                        self.wall = True
            elif self.direction == "east":
                self.direction = "south"
                if self.y == 9: #outer wall
                    self.wall = True
                if self.y == 4: #room wall
                    if self.x == self.d2[0] or self.x == self.d4[0]: #door
                        self.wall = False
                    else:
                        self.wall = True
            elif self.direction == "north":
                self.direction = "east"
                if self.x == 9: #outer wall
                    self.wall = True
                if self.x == 4: #room wall
                    if self.y == self.d1[1] or self.y == self.d3[1]: #door
                        self.wall = False
                    else:
                        self.wall = True
            else:
                self.direction = "north"
                if self.y == 0: #outer wall
                    self.wall = True
                if self.y == 5: #room wall
                    if self.x == self.d2[0] or self.x == self.d4[0]: #door
                        self.wall = False
                    else:
                        self.wall = True

            return (grid[self.y][self.x], self.home, self.wall)

        if action == "turn_off":
            #nothing to be done to generate next percept
            return (grid[self.y][self.x], self.home, self.wall)



#environment
class environment:

    global grid
    #constructor
    def __init__(self):
        #signals to agent
        self.home = True
        self.wall = False
        #position and oreintation of agent (only for environment to generate next percept)
        self.direction = "north" #since agent starts pointing upwards
        self.x = 0
        self.y = 9 #since agent starts from bottom-left corner

    #function to generate next percept
    def step(self, action):

        if action == "suck":
            #update current cell state to clean
            grid[self.y][self.x] = False
            return (grid[self.y][self.x], self.home, self.wall)


        if action == "forward":
            #verify no wall in front
            if self.wall == False:
                #move agent forward in current direction and check for wall in new position
                if self.direction == "north":
                    self.y -= 1
                    if self.y == 0:
                        self.wall = True
                if self.direction == "south":
                    self.y += 1
                    if self.y == 9:
                        self.wall = True
                if self.direction == "east":
                    self.x += 1
                    if self.x == 9:
                        self.wall = True
                if self.direction == "west":
                    self.x -= 1
                    if self.x == 0:
                        self.wall = True

                #check if new position is home
                if self.x == 0 and self.y == 0:
                    self.home = True

            return (grid[self.y][self.x], self.home, self.wall)


        if action == "turn_left":
            #update direction and check for wall in new orientation
            self.wall = False
            if self.direction == "north":
                self.direction = "west"
                if self.x == 0:
                    self.wall = True
            elif self.direction == "west":
                self.direction = "south"
                if self.y == 9:
                    self.wall = True
            elif self.direction == "south":
                self.direction = "east"
                if self.x == 9:
                    self.wall = True
            else:
                self.direction = "north"
                if self.y == 0:
                    self.wall = True

            return (grid[self.y][self.x], self.home, self.wall)


        if action == "turn_right":
            #update direction and check for wall in new orientation
            self.wall = False
            if self.direction == "south":
                self.direction = "west"
                if self.x == 0:
                    self.wall = True
            elif self.direction == "east":
                self.direction = "south"
                if self.y == 9:
                    self.wall = True
            elif self.direction == "north":
                self.direction = "east"
                if self.x == 9:
                    self.wall = True
            else:
                self.direction = "north"
                if self.y == 0:
                    self.wall = True

            return (grid[self.y][self.x], self.home, self.wall)

        if action == "turn_off":
            #nothing to be done to generate next percept
            return (grid[self.y][self.x], self.home, self.wall)


#simple agent
class simple_reflex_agent:

    def __init__(self):
        print("Blabla_simple") #no internal state here

    def decide_action(self, percept):
        done = False
        dirt = percept[0]
        home = percept[1]
        wall = percept[2]
        if dirt:
            action = "suck"
        elif wall:
            action = "turn_right"
        else:
            action = "forward"
        return (action, done)


#random agent
class random_reflex_agent:

    def __init__(self):
        print("Blabla_random") #no internal state here

    def decide_action(self, percept):
        done = False

        #take any of the 5 actions randomly

        return (action, done)


#model based agent
class model_based_reflex_agent:

    def __init__(self):
        print("Blabla_model")
        #define internal state here (3 bits available)
        '''
        state - bit0 and bit1 defined as:
        00 - north
        01 - east
        10 - south
        11 - west

        state - bit2 used as east step flag
        0 - agent can take an east step
        1 - agent can't take an east step
        '''
        self.state = [False, False, False] #initial state

    def decide_action(self, percept):
        done = False

        return (action, done)

def simple_reflex_agent_in_room_grid():
    #create environment and agent
    myenv = roomed_environment()
    agent = simple_reflex_agent()

    global grid
    #for plot
    number_of_clean_cells = []
    iter_list = []

    #define initial percept
    dirt = True
    home = True
    wall = False
    percept = [dirt, home, wall]

    #terminate flag
    done = False
    #iteration number
    iter = 0

    while not done and iter < MAX_ITERS:
        iter += 1
        print "\niter: ", iter
        print "grid at iter ", iter, " :"
        print grid
        #get action as decided by agent program
        action, done = agent.decide_action(percept)
        print "action decided at iter ", iter, ": ", action

        #count number of clean cells for plot
        unique, counts = np.unique(grid, return_counts=True)
        d = dict(zip(unique, counts))
        c = d.get(False)
        print "current clean cells count = ", c
        number_of_clean_cells.append(c)
        iter_list.append(iter)

        #take the decided action and get new percept from environment
        percept = myenv.step(action)

    #print final grid
    print "\nfinal grid:"
    print grid

    #plot graph
    plt.figure()
    plt.plot(iter_list, number_of_clean_cells, label = "simple_reflex_agent",color='blue', linestyle='solid', linewidth = 1.5 )
    plt.xlabel('Number of actions', fontsize=12)
    plt.ylabel('Number of clean cells')
    plt.title('Performance curve', fontsize=11)
    #plt.legend(loc=7)
    plt.grid()
    # changingY-axis range
    #x1,x2,y1,y2 = plt.axis()
    plt.savefig("Performance_curve.png", dpi = 300,bbox_inches="tight")



def simple_reflex_agent_in_open_grid():
    #create environment and agent
    myenv = environment()
    agent = simple_reflex_agent()

    global grid
    #for plot
    number_of_clean_cells = []
    iter_list = []

    #define initial percept
    dirt = True
    home = True
    wall = False
    percept = [dirt, home, wall]

    #terminate flag
    done = False
    #iteration number
    iter = 0

    while not done and iter < MAX_ITERS:
        iter += 1
        print "\niter: ", iter
        print "grid at iter ", iter, " :"
        print grid
        #get action as decided by agent program
        action, done = agent.decide_action(percept)
        print "action decided at iter ", iter, ": ", action

        #count number of clean cells for plot
        unique, counts = np.unique(grid, return_counts=True)
        d = dict(zip(unique, counts))
        c = d.get(False)
        print "current clean cells count = ", c
        number_of_clean_cells.append(c)
        iter_list.append(iter)

        #take the decided action and get new percept from environment
        percept = myenv.step(action)

    #print final grid
    print "\nfinal grid:"
    print grid


    #plot graph
    plt.figure()
    plt.plot(iter_list, number_of_clean_cells, label = "simple_reflex_agent",color='blue', linestyle='solid', linewidth = 1.5 )
    plt.xlabel('Number of actions', fontsize=12)
    plt.ylabel('Number of clean cells')
    plt.title('Performance curve', fontsize=11)
    #plt.legend(loc=7)
    plt.grid()
    # changingY-axis range
    #x1,x2,y1,y2 = plt.axis()
    plt.savefig("Performance_curve.png", dpi = 300,bbox_inches="tight")


def main():
    simple_reflex_agent_in_room_grid()

if __name__ == '__main__':
    main()
