"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
========================================================================================================================
COMPSCI 2120A/9642A/ DIGIHUM 2220A - Assignment 2
Student Name: YOUR NAME HERE
Student Number: YOUR STUDENT NUMBER HERE
========================================================================================================================
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""
import numpy as np
import networkx as nt
import matplotlib.pyplot as plt

def create_adjacency_matrix(population_size):
    """
    This function creates and returns a randomized population_size x population_size matrix.
    It is an "adjacency" matrix, meaning that it indicates which people are adjacent (in proximity)

    Why use this? The idea: if two people are in proximity, one person can transmit to the other

    How to read it...

    matrix[row 0][column 8] = 1 --> Person 0 is adjacent to Person 8.
    matrix[row 5][column 3] = 0 --> Person 5 is not adjacent to Person 3.

    :param population_size: the given number of people featured in your matrix (and in your system)
    :return: a randomized adjacency matrix of size population_size x population_size
    """

    #create random adjacency matrix with 0's and 1's of size population_size x population_size
    adjacency = np.random.randint(0,2,(population_size,population_size))

    #cut out entries below diagonal to reduce the number of connections
    adjacency = np.triu(adjacency)

    #create a network from the adjacency matrix
    adjacency_network = nt.from_numpy_matrix(adjacency)

    #if the network is not connected, keep creating random ones until you get one that is connected
    if not (nt.is_connected(adjacency_network)):
        while not (nt.is_connected(adjacency_network)):
            adjacency = np.random.randint(0,2,(population_size,population_size))
            adjacency = np.triu(adjacency)
            adjacency_network = nt.from_numpy_matrix(adjacency)

    #fill all person-person connections with value 1 (for each person with themselves)
    np.fill_diagonal(adjacency,1)

    return adjacency

def create_population_list(population_size):
    """
    This function creates and returns a list of lists; specifically, it creates and returns
    a list containing "people". Each "person" is a 3-element list.. i.e ['Person #', Positive_Flag, List of Others in Proximity]

    Let's break down each "person" list: It contains...
     1) A person # such as 'Person 0'
     2) A positive flag --> True if that person is positive for the virus, False otherwise
     3) A list of others in proximity --> a list, such as [0, 3, 4] which would mean that this person is in proximity to persons
     0, 3, and 4

     The list which we return contains these "person" lists.
     i.e. [['Person 0', False, [0, 1]], ['Person 1', False, [1, 2]], ['Person 2', False, [1, 2]]]

    :param population_size: the number of people who will be in your population
    :return: a list which contains all people and their information (#, positive_flag, list_of_others_in_proximity)
    """

    #create a randomized adjacency matrix for this population
    adjacency = create_adjacency_matrix(population_size)

    population_list = []

    # for each person in your population, create list which contains a 'Person #', a positive flag, and a list of others
    # in proximity
    for i in range(population_size):
        person_name = "Person " + str(i)
        positive_flag = False
        others_in_proximity = adjacency[i] #get row of adjacency matrix for that person to get all others in proximity
        #"np.where(condition)[0]" returns an array of all indexes where the condition is met
        others_in_proximity2 = np.where(others_in_proximity == 1)[0]
        others_in_proximity_list = list(others_in_proximity2) #convert it to a list
        population_list.append([person_name, positive_flag, others_in_proximity_list]) #add person to population list

    return population_list

def draw_network(population_list):
    """
    This function creates and draws a "network" of nodes and edges corresponding to the data from population_list.

    For example, person 0 will be represented by node "0"; the node will be red if they are positive for the virus and
    blue otherwise; the node will be connected to other nodes based on its list of others in proximity

    :param population_list: a list which contains a list for each "person" (#, positive_flag, list_of_others_in_proximity)
    :return: nothing, but displays the resulting graph in a new window using matplotlib.pyplot
    """

    #these lists store all of the people who have their positive_flag set to True or False, respectively
    positive_case_list = []
    negative_case_list = []

    #initialize our network
    network = nt.Graph()

    #fill positive and negative case lists with people
    for i in range(len(population_list)):
        #if person i's positive_flag is True, add them to the positive_case list; also add their node to the
        #graph in red
        if(population_list[i][1] == True):
            positive_case_list.append(i)
            network.add_node(i, node_color = 'r')
        # else, if person i's positive_flag is False, add them to the negative_case list; also add their node to the
        # graph in blue
        else:
            negative_case_list.append(i)
            network.add_node(i, node_color = 'b')

        #add all of the edges between nodes... i.e. for each element j in the list of others in proximity, add a new
        #edge (a line) between person i and person in proximity (j)
        for j in population_list[i][2]:
            network.add_edge(i,j)

    #You can uncomment the lines below to print the running lists of positive and negative cases as a check
    #print("Positive_Cases: ", positive_case_list)
    #print("Negative Cases:", negative_case_list)

    #this creates a randomized layout for the network
    node_layout = nt.random_layout(network)

    #these commands draw our nodes, edges, and labels
    nt.draw_networkx_nodes(network, node_layout, nodelist=positive_case_list, node_color='r')
    nt.draw_networkx_nodes(network, node_layout, nodelist=negative_case_list, node_color='b')
    nt.draw_networkx_edges(network, node_layout)
    nt.draw_networkx_labels(network, node_layout)

    plt.show()
    plt.draw()


#Your functions below...

def new_positive_case(population_list, person_number):
    """
    This function takes your population list population_list
    as a parameter and an integer person_number corresponding
    to the person whom will now be positive.

    :param population_list: a list which contains a list for each "person" (#, positive_flag, list_of_others_in_proximity)
    :param person_number: an integer that identifies to one and only one person
    :return: an updated list of the list of persons,inclusive of the new positive case
    """

    #set the person's positive flag to True
    population_list[person_number][1] = True
    #print("New case: Person ", person_number)

    return population_list


def transmit(population_list, person_number, p_transmission):
    """
    This function takes your population list,
    the person # of the person who may transmit the virus,
    and the probability of transmission as arguments.

    :param population_list: a list which contains a list for each "person" (#, positive_flag, list_of_others_in_proximity)
    :param person_number: an integer that identifies to one and only one person
    :param p_transmission: probability of the given person transmitting the virus to others in the population
    :return: the refreshed population list with updated values for virus-positive flags
    """

    #if the given person's positive flag is True
    if(population_list[person_number][1] == True):
        #for everyone in their list of proximity
        for i in (population_list[person_number][2]):
            #if person i doesn't already have the virus and their random probability is less
            #than the probability of transmission
            if(population_list[i][1] == False) and (np.random.rand() < p_transmission):
                #turn their positive flag into True
                population_list[i][1] = True
                #print("Person", person_number,"infects Person",i)

    return population_list


def recover(population_list, person_number):
    """
    This function takes your population list population_list
    as a parameter and an integer person_number corresponding
    to the person whom has recovered from the virus and is now negative.

    :param population_list: a list which contains a list for each "person" (#, positive_flag, list_of_others_in_proximity)
    :param person_number: an integer that identifies to one and only one person
    :return: the updated population list with refreshed values for person(s) who recovered
    """

    #turn the recovered person's positive flag into False
    population_list[person_number][1] = False
    #print("Recovered case: Person ", person_number)

    return population_list


def simulate_step(population_list, p_transmission, p_recovery):
    """
    This function will execute one step of your simulation
    (i.e. one round of transmission from each
    positive_case to all of those in proximity).

    :param population_list: a list which contains a list for each "person" (#, positive_flag, list_of_others_in_proximity)
    :param p_transmission: probability of transmission from person to person
    :param p_recovery: probability of a person recovering
    :return: the updated list of all persons with their positive flags, taking into account the transmission and recovery
    """

    #if the probability of transmission is greater than the random probability
    if(np.random.rand() < p_transmission):
        #make a random person catch the virus
        new_positive_case(population_list, int(np.random.choice(len(population_list), 1)))

    #for each person in our population
    for i in range(len(population_list)):
        #if they have the virus
        if(population_list[i][1] == True):
            #transmit the virus to the people around them
            transmit(population_list, i, p_transmission)
        #if they have the virus and are likely to recover
        if(population_list[i][1] == True) and (np.random.rand() < p_recovery):
            #change their virus-positive flag
            recover(population_list,i)

    return population_list


def all_cases_positive(population_list):
    """
    This function returns True if all
    cases are positive and False otherwise.

    :param population_list: a list which contains a list for each "person" (#, positive_flag, list_of_others_in_proximity)
    :return: True or False based on if everyone has the virus or not
    """

    #if all cases are positive, return True
    all_cases = True

    #for everyone in the population
    for i in range(len(population_list)):
        #if there is even a single person without the virus
        if not (population_list[i][1] == True):
            #return False
            all_cases = False
            break

    #print(all_cases)
    return all_cases


def simulate_run(population_list, p_transmission, p_recovery, first_positive_person):
    """
    This function runs a simulation given a population list,
    probabilities for transmission and recovery,
    and an initial positive_case (integer for person number).

    :param population_list: a list which contains a list for each "person" (#, positive_flag, list_of_others_in_proximity)
    :param p_transmission: probability of one person spreading the virus to another
    :param p_recovery: probability of an infected person recovering from the virus
    :param first_positive_person: integer identifying the first person with the virus
    :return: an updated population list of who has the virus or not after transmissions and recoveries
    """

    #the first person catches the virus
    new_positive_case(population_list, first_positive_person)
    draw_network(population_list)

    #for everyone in the population
    for i in range(len(population_list)):
        #until everyone has the virus
        while not (all_cases_positive(population_list)):
            #keep the virus ongoing with transmissions and recoveries
            simulate_step(population_list, p_transmission, p_recovery)

    #draw the final diagram w/ everyone having the virus
    draw_network(population_list)

    return population_list


def simulate_run_no_draw(population_list, p_transmission, p_recovery, first_positive_person):
    """
    This function runs a simulation given a population list,
    probabilities for transmission and recovery,
    and an initial positive_case (integer for person number).

    It counts the number of steps it takes
    in order for all cases to become positive.

    :param population_list: a list which contains a list for each "person" (#, positive_flag, list_of_others_in_proximity)
    :param p_transmission: probability of one person spreading the virus to another
    :param p_recovery: probability of someone recovering after catching the virus
    :param first_positive_person: first person to set off the chain reaction
    :return: the number of steps it takes in the simulation before everyone has the virus
    """

    #first person in the population catches the virus
    new_positive_case(population_list, first_positive_person)
    #setup a counter for the number of steps it takes
    steps = 0

    #for everyone in the population
    for i in range(len(population_list)):
        #if even one person doesn't have the virus yet
        while not (all_cases_positive(population_list)):
            #keep counting the number of steps
            steps += 1
            #keep the virus ongoing
            simulate_step(population_list, p_transmission, p_recovery)

    #print("It took",steps,"steps for all cases to become positive.")
    return steps


def simulate_many(population_size, p_transmission, p_recovery, first_positive_person, num_runs):
    """
    This function calls the simulate_run_no_draw function (num_runs) # of times,
    and will return the average number of steps required for all cases to
    become positive (across all of your runs).

    :param population_size: the number of people to be used to make the population list
    :param p_transmission: probability of one person spreading the virus to another
    :param p_recovery: probability of someone recovering from the virus
    :param first_positive_person: first person to catch the virus
    :param num_runs: number of times you want to run the simulation
    :return: average number of simulation steps it took until everyone in the population has the virus
    """

    #create a list of the number of steps for each simulation
    num_steps_list = []
    #start totalling the sum
    sum = 0

    #run the simulation as many times as we want
    for each_run in range(num_runs):
        #make a new population list every time
        population_list = create_population_list(population_size)
        #count the number of steps it takes until everyone has the virus
        num_steps = simulate_run_no_draw(population_list, p_transmission, p_recovery, first_positive_person)
        #store that value in an overarching list
        num_steps_list.append(num_steps)

    #add up all the steps from each individual simulation
    for each_value in num_steps_list:
        sum += each_value

    #find the average number of steps it takes for a simulation to reach all-positive cases
    average_of_list = sum / len(num_steps_list)

    return average_of_list


#Your other code below...
simulate_run(create_population_list(15), 0.8, 0.1, 0)
average_steps = simulate_many(15, 0.8, 0.1, 0, 10000)
print("Avg. steps for complete transmission: ", average_steps)


"""
#previously tested code

my_population = create_population_list(15)
draw_network(my_population)
new_positive_case(my_population, 0)
draw_network(my_population)


#transmit(my_population, 0, 80)
#draw_network(my_population)


simulate_step(my_population, 0.8, 0.1)
draw_network(my_population)

simulate_step(my_population, 0.8, 0.1)
draw_network(my_population)

simulate_step(my_population, 0.8, 0.1)
draw_network(my_population)

def test_random(population_list):
    print(int(np.random.choice(len(population_list), 1)))
    return population_list
"""

