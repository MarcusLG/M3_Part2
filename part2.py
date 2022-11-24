import part2_class
from math import floor,exp
from random import randint
from numpy.random import rand
import sys
import time
from copy import deepcopy
from part2_util import populate_production

case_param = part2_class.params()
# Definitions of basic parameters

def gen_load(units):
    # Generates the number of loads required for
    # units
    # Param:
    #   units - Number of units in total
    return floor(units / case_param.load_size) + units % case_param.load_size

def monte_carlo_updater(product,customer):
    # This is a Monte Carlo updater
    # Update rule:
    #   
    # Params:
    #    product - product name in char
    #    customer - customer name in char
    #    demand -  demand in int
    case_param.production['A'][product][customer] = randint(0, case_param.demand[customer][product])
    case_param.production['B'][product][customer] = randint(0, max(case_param.demand[customer][product] - case_param.production['A'][product][customer],0))
    case_param.production['C'][product][customer] = randint(0, max(case_param.demand[customer][product] - case_param.production['A'][product][customer] - case_param.production['B'][product][customer],0))
    case_param.production['D'][product][customer] = max(case_param.demand[customer][product] - case_param.production['A'][product][customer] - case_param.production['B'][product][customer] - case_param.production['C'][product][customer],0)

def simple_local_updater(product,customer,plant,mode,movement):
    # This is a simple tabu search algorithm with discrete change of 1
    # Update rule:
    # A  B
    # C  D
    # Going clockwise, mode n balances with n-th next neighbour in clockwise
    # Params: 
    #    product - product name in char
    #    customer - customer name in char
    #    mode - Mode in int based on update rule
    #    movement - Increment / Decrement (1,-1)

    # Okay all the centralised data info is gone aye?
    plant_list = ['A','B','C','D']
    plant_update_list = [0,0,0,0]
    plant_update_list[plant_list.index(plant)] += movement
    plant_update_list[(plant_list.index(plant) + mode) % 4] -= movement
    # Here we decode the mode and movement into the plant_update_list
    case_param.production['A'][product][customer] = case_param.production['A'][product][customer] + plant_update_list[0]
    case_param.production['B'][product][customer] = case_param.production['B'][product][customer] + plant_update_list[1]
    case_param.production['C'][product][customer] = case_param.production['C'][product][customer] + plant_update_list[2]
    case_param.production['D'][product][customer] = case_param.production['D'][product][customer] + plant_update_list[3]

def simple_local_wrapper(num_iter, rand_initializer=True, debug=False, num_initalization=1, record_best=True, overwrite=False):
    for i in range(0,num_initalization):
        simple_local_iterator(num_iter, rand_initializer, debug, record_best, overwrite)

def simple_local_iterator(num_iter, rand_initializer=True, debug=False, record_best=True, overwrite=False):
    # Wrapper to run simple tabu
    if rand_initializer:
        simple_local_initializer()
    else:
        case_param.production = populate_production(case_param.production)
    time_start = time.time()
    if overwrite:
        text_file = open("Output_simple_local.csv", "w")
    else:
        text_file = open("Output_simple_local.csv", "a")
    text_file.write("\nCurrent_iter,current_cost,below_max_cap,APH,BPH,CPH,DPH,APJ,BPJ,CPJ,DPJ,APL,BPL,CPL,DPL,APT,BPT,CPT,DPT,AQH,BQH,CQH,DQH,AQJ,BQJ,CQJ,DQJ,AQL,BQL,CQL,DQL,AQT,BQT,CQT,DQT,ARH,BRH,CRH,DRH,ARJ,BRJ,CRJ,DRJ,ARL,BRL,CRL,DRL,ART,BRT,CRT,DRT,ASH,BSH,CSH,DSH,ASJ,BSJ,CSJ,DSJ,ASL,BSL,CSL,DSL,AST,BST,CST,DST")
    current_cost = evaluate_cost()
    print("Initial cost:", current_cost)
    # This is the golden copy of the production quantity, we save it before changing the dynamic dictionary

    # Here we save a copy of the initial state of the optimization (base-state)
    if not record_best:
        current_list = ["Base",current_cost,True,case_param.production['A']['P']['H'],case_param.production['B']['P']['H'],case_param.production['C']['P']['H'],case_param.production['D']['P']['H'],case_param.production['A']['P']['J'],case_param.production['B']['P']['J'],case_param.production['C']['P']['J'],case_param.production['D']['P']['J'],case_param.production['A']['P']['L'],case_param.production['B']['P']['L'],case_param.production['C']['P']['L'],case_param.production['D']['P']['L'],case_param.production['A']['P']['T'],case_param.production['B']['P']['T'],case_param.production['C']['P']['T'],case_param.production['D']['P']['T'],case_param.production['A']['Q']['H'],case_param.production['B']['Q']['H'],case_param.production['C']['Q']['H'],case_param.production['D']['Q']['H'],case_param.production['A']['Q']['J'],case_param.production['B']['Q']['J'],case_param.production['C']['Q']['J'],case_param.production['D']['Q']['J'],case_param.production['A']['Q']['L'],case_param.production['B']['Q']['L'],case_param.production['C']['Q']['L'],case_param.production['D']['Q']['L'],case_param.production['A']['Q']['T'],case_param.production['B']['Q']['T'],case_param.production['C']['Q']['T'],case_param.production['D']['Q']['T'],case_param.production['A']['R']['H'],case_param.production['B']['R']['H'],case_param.production['C']['R']['H'],case_param.production['D']['R']['H'],case_param.production['A']['R']['J'],case_param.production['B']['R']['J'],case_param.production['C']['R']['J'],case_param.production['D']['R']['J'],case_param.production['A']['R']['L'],case_param.production['B']['R']['L'],case_param.production['C']['R']['L'],case_param.production['D']['R']['L'],case_param.production['A']['R']['T'],case_param.production['B']['R']['T'],case_param.production['C']['R']['T'],case_param.production['D']['R']['T'],case_param.production['A']['S']['H'],case_param.production['B']['S']['H'],case_param.production['C']['S']['H'],case_param.production['D']['S']['H'],case_param.production['A']['S']['J'],case_param.production['B']['S']['J'],case_param.production['C']['S']['J'],case_param.production['D']['S']['J'],case_param.production['A']['S']['L'],case_param.production['B']['S']['L'],case_param.production['C']['S']['L'],case_param.production['D']['S']['L'],case_param.production['A']['S']['T'],case_param.production['B']['S']['T'],case_param.production['C']['S']['T'],case_param.production['D']['S']['T']]
        text_file.write("\n%s" % str(current_list))
    print_iter_interval = 2    # This is the output interval for the iteration, console to print status every x print_iter_interval
    total_iterations = 0
    for current_iter in range(0, num_iter):
        # Algorithm for simple tabu iteration:
        # For every golden state (i.e. the current variables that will yield the lowest cost)
        #    we perform a simple tabu search around its neighbour
        #    bear in mind that we may find more than one steps that may result in a reduction of the cost
        #    therefore we will do an exhaustive search to return only the step that yields the lowest cost
        #    among all. This set of variables shall serve as the golden copy for the next iteration.
        #    The iterations will stop when the maximum iterations have reached or a minimal (not guaranteed to
        #    global), then the result is saved to the output_simple_local.csv file)
        #    NOTE: Got to remember to reset / udpate the golden production at the end of the iteration
        #          provided the iteration were to continue.
        # Golden will serve as a copy of the previous state
        golden_production = deepcopy(case_param.production)
        # Next will hold the production quantities that to be updated with
        next_production = deepcopy(case_param.production)
        prev_best_cost = evaluate_cost() # Save the cost, i.e. best cost so far to be compared with
        update_flag = False
        #if current_iter % print_iter_interval == 0:
        #    print('Current iter: ', current_iter)

        # Main loop to iterate through the number of plants / product / customers
        for product in case_param.product:
            for customer in case_param.customer:
                # For each set of product-customer pair, we perform the neighbour search
                for mode in [1,2,3]:
                    for movement in [-1,1,-2,2,-3,3,-4,4,-5,5,-6,6,-7,7,-8,8,-9,9,-10,10,-11,11,-12,12,-13,13]: # Here we only run movement search for 2 steps
                        for plant in ['A','B','C','D']:
                            # Here we pass the variables into the updater to update the value for the 
                            total_iterations += 1
                            simple_local_updater(product,customer,plant,mode,movement)
                            current_cost = evaluate_cost()
                            if debug:
                                print("Iteration: ", current_iter,"\tMode: ",mode, "\tCustomer: ",customer, "\tMovement: ",movement, "\tPlant: ", plant, "\tCost: ",current_cost)
                            below_max_cap = True
                            all_pos = True
                            for plant in case_param.plant:
                                if not capacity_check(plant):
                                    below_max_cap = False
                                if not sanity_check(plant):
                                    all_pos = False
                            if (not below_max_cap) or (not all_pos):
                                # Well if the maximum capacity is exceeded, reset the state and continue
                                case_param.production = deepcopy(next_production)
                                continue
                            # Only check the cost if the capacity is not exceeded
                            if current_cost < prev_best_cost:
                                prev_best_cost = current_cost
                                next_production = deepcopy(case_param.production)
                                current_list = [str(movement) + "-" + str(current_iter),prev_best_cost,True,case_param.production['A']['P']['H'],case_param.production['B']['P']['H'],case_param.production['C']['P']['H'],case_param.production['D']['P']['H'],case_param.production['A']['P']['J'],case_param.production['B']['P']['J'],case_param.production['C']['P']['J'],case_param.production['D']['P']['J'],case_param.production['A']['P']['L'],case_param.production['B']['P']['L'],case_param.production['C']['P']['L'],case_param.production['D']['P']['L'],case_param.production['A']['P']['T'],case_param.production['B']['P']['T'],case_param.production['C']['P']['T'],case_param.production['D']['P']['T'],case_param.production['A']['Q']['H'],case_param.production['B']['Q']['H'],case_param.production['C']['Q']['H'],case_param.production['D']['Q']['H'],case_param.production['A']['Q']['J'],case_param.production['B']['Q']['J'],case_param.production['C']['Q']['J'],case_param.production['D']['Q']['J'],case_param.production['A']['Q']['L'],case_param.production['B']['Q']['L'],case_param.production['C']['Q']['L'],case_param.production['D']['Q']['L'],case_param.production['A']['Q']['T'],case_param.production['B']['Q']['T'],case_param.production['C']['Q']['T'],case_param.production['D']['Q']['T'],case_param.production['A']['R']['H'],case_param.production['B']['R']['H'],case_param.production['C']['R']['H'],case_param.production['D']['R']['H'],case_param.production['A']['R']['J'],case_param.production['B']['R']['J'],case_param.production['C']['R']['J'],case_param.production['D']['R']['J'],case_param.production['A']['R']['L'],case_param.production['B']['R']['L'],case_param.production['C']['R']['L'],case_param.production['D']['R']['L'],case_param.production['A']['R']['T'],case_param.production['B']['R']['T'],case_param.production['C']['R']['T'],case_param.production['D']['R']['T'],case_param.production['A']['S']['H'],case_param.production['B']['S']['H'],case_param.production['C']['S']['H'],case_param.production['D']['S']['H'],case_param.production['A']['S']['J'],case_param.production['B']['S']['J'],case_param.production['C']['S']['J'],case_param.production['D']['S']['J'],case_param.production['A']['S']['L'],case_param.production['B']['S']['L'],case_param.production['C']['S']['L'],case_param.production['D']['S']['L'],case_param.production['A']['S']['T'],case_param.production['B']['S']['T'],case_param.production['C']['S']['T'],case_param.production['D']['S']['T']]
                                text_file.write("\n%s" % str(current_list))
                                update_flag = True # We set this flag to True if there's any improvement, else iteration will break
                            else:
                                case_param.production = deepcopy(next_production)
        case_param.production = deepcopy(next_production)
        if not update_flag:
            print("No improvement.")
            break
    # End of iteration, restore the case_param.production to the best combination so far
    current_cost = evaluate_cost()
    current_list = [current_iter,current_cost,below_max_cap,case_param.production['A']['P']['H'],case_param.production['B']['P']['H'],case_param.production['C']['P']['H'],case_param.production['D']['P']['H'],case_param.production['A']['P']['J'],case_param.production['B']['P']['J'],case_param.production['C']['P']['J'],case_param.production['D']['P']['J'],case_param.production['A']['P']['L'],case_param.production['B']['P']['L'],case_param.production['C']['P']['L'],case_param.production['D']['P']['L'],case_param.production['A']['P']['T'],case_param.production['B']['P']['T'],case_param.production['C']['P']['T'],case_param.production['D']['P']['T'],case_param.production['A']['Q']['H'],case_param.production['B']['Q']['H'],case_param.production['C']['Q']['H'],case_param.production['D']['Q']['H'],case_param.production['A']['Q']['J'],case_param.production['B']['Q']['J'],case_param.production['C']['Q']['J'],case_param.production['D']['Q']['J'],case_param.production['A']['Q']['L'],case_param.production['B']['Q']['L'],case_param.production['C']['Q']['L'],case_param.production['D']['Q']['L'],case_param.production['A']['Q']['T'],case_param.production['B']['Q']['T'],case_param.production['C']['Q']['T'],case_param.production['D']['Q']['T'],case_param.production['A']['R']['H'],case_param.production['B']['R']['H'],case_param.production['C']['R']['H'],case_param.production['D']['R']['H'],case_param.production['A']['R']['J'],case_param.production['B']['R']['J'],case_param.production['C']['R']['J'],case_param.production['D']['R']['J'],case_param.production['A']['R']['L'],case_param.production['B']['R']['L'],case_param.production['C']['R']['L'],case_param.production['D']['R']['L'],case_param.production['A']['R']['T'],case_param.production['B']['R']['T'],case_param.production['C']['R']['T'],case_param.production['D']['R']['T'],case_param.production['A']['S']['H'],case_param.production['B']['S']['H'],case_param.production['C']['S']['H'],case_param.production['D']['S']['H'],case_param.production['A']['S']['J'],case_param.production['B']['S']['J'],case_param.production['C']['S']['J'],case_param.production['D']['S']['J'],case_param.production['A']['S']['L'],case_param.production['B']['S']['L'],case_param.production['C']['S']['L'],case_param.production['D']['S']['L'],case_param.production['A']['S']['T'],case_param.production['B']['S']['T'],case_param.production['C']['S']['T'],case_param.production['D']['S']['T']]
    text_file.write("\n%s" % str(current_list))
    text_file.close()
    time_stop = time.time()
    print("Total time elapse: ", time_stop - time_start, "s\n")
    print("Rate: ", (time_stop - time_start)/total_iterations, "s/iteration\n")
    print("Total Iterations: ", total_iterations, "\n")

def simple_local_initializer():
    # Function to initialize the production random and within bound
    # Basically mc_iterator
    below_max_cap = False
    while not below_max_cap:
        below_max_cap = True
        mc_iterator()
        for plant in case_param.plant:
            if not capacity_check(plant):
                below_max_cap = False

def capacity_check(plant):
    # Return true if capacity is not exceeded
    # Param:
    #    plant - the plant to check
    """
    current_cap = (case_param.labour_hours[plant]['P'] * sum(case_param.production[plant]['P'].values()) + 
            case_param.labour_hours[plant]['Q'] * sum(case_param.production[plant]['Q'].values()) +
            case_param.labour_hours[plant]['R'] * sum(case_param.production[plant]['R'].values()) +
            case_param.labour_hours[plant]['S'] * sum(case_param.production[plant]['S'].values()))
    print("Current Capa for plant ", plant, ":",current_cap)
    print("Current Max for plant ", plant, ": ", case_param.max_capacity[plant])
    print("If max exceeded for plant ", plant, ": ", current_cap <= case_param.max_capacity[plant])
    """
    return (case_param.labour_hours[plant]['P'] * sum(case_param.production[plant]['P'].values()) + 
    		case_param.labour_hours[plant]['Q'] * sum(case_param.production[plant]['Q'].values()) +
    		case_param.labour_hours[plant]['R'] * sum(case_param.production[plant]['R'].values()) +
    		case_param.labour_hours[plant]['S'] * sum(case_param.production[plant]['S'].values())) <= case_param.max_capacity[plant]

def sanity_check(plant):
    # Apparently movement will yield negative production numbers, who would have expected right?
    assume_pos = True
    for product in ['P','Q','R','S']:
        for customer in ['H','J','L','T']:
            if case_param.production[plant][product][customer] < 0:
                assume_pos = False
    return assume_pos

def mc_iterator():
    # Just a generic iterator for updater
    # Params:
    #     updater - doesn't really do anything at this point
    for product in case_param.product:
        for customer in case_param.customer:
            monte_carlo_updater(product,customer)

def func_cost(plant):
    # Separate the computation of cost for plant A
    #cost = case_param.labour_hours[plant]['P'] * sum(case_param.production[plant]['P'].values())
    cost = (case_param.labour_cost[plant] * (
    	case_param.labour_hours[plant]['P'] * sum(case_param.production[plant]['P'].values()) + 
    		case_param.labour_hours[plant]['Q'] * sum(case_param.production[plant]['Q'].values()) +
    		case_param.labour_hours[plant]['R'] * sum(case_param.production[plant]['R'].values()) +
    		case_param.labour_hours[plant]['S'] * sum(case_param.production[plant]['S'].values())) +
        case_param.cost_per_mile * (
        	case_param.distance[plant]['H'] * gen_load(sum([case_param.production[plant]['P']['H'], case_param.production[plant]['Q']['H'], case_param.production[plant]['R']['H'], case_param.production[plant]['S']['H']])) + 
        	case_param.distance[plant]['J'] * gen_load(sum([case_param.production[plant]['P']['J'], case_param.production[plant]['Q']['J'], case_param.production[plant]['R']['J'], case_param.production[plant]['S']['J']])) + 
        	case_param.distance[plant]['L'] * gen_load(sum([case_param.production[plant]['P']['L'], case_param.production[plant]['Q']['L'], case_param.production[plant]['R']['L'], case_param.production[plant]['S']['L']])) + 
        	case_param.distance[plant]['T'] * gen_load(sum([case_param.production[plant]['P']['T'], case_param.production[plant]['Q']['T'], case_param.production[plant]['R']['T'], case_param.production[plant]['S']['T']]))))
    return cost

def evaluate_cost():
    # Run the cost calculation
    cost = 0
    for plant in case_param.plant:
        cost += func_cost(plant)
    return cost

def mc_run_and_print(num_iter):
    time_start = time.time()
    text_file = open("Output.csv", "w")
    text_file.write("Current_iter,current_cost,below_max_cap,APH,BPH,CPH,DPH,APJ,BPJ,CPJ,DPJ,APL,BPL,CPL,DPL,APT,BPT,CPT,DPT,AQH,BQH,CQH,DQH,AQJ,BQJ,CQJ,DQJ,AQL,BQL,CQL,DQL,AQT,BQT,CQT,DQT,ARH,BRH,CRH,DRH,ARJ,BRJ,CRJ,DRJ,ARL,BRL,CRL,DRL,ART,BRT,CRT,DRT,ASH,BSH,CSH,DSH,ASJ,BSJ,CSJ,DSJ,ASL,BSL,CSL,DSL,AST,BST,CST,DST")
    top_x_list = []
    top_x_cost = []
    top_x = 5
    print_iter_interval = 5000
    for current_iter in range(0, num_iter):
        if current_iter % print_iter_interval == 0:
            print('Current iter: ', current_iter)
        mc_iterator()
        current_cost = evaluate_cost()
        below_max_cap = True
        for plant in case_param.plant:
            if not capacity_check(plant):
                below_max_cap = False
            #below_max_cap & (capacity_check(plant))
        if not below_max_cap:
            continue
        if len(top_x_list) <= top_x:
            current_list = [current_iter,current_cost,below_max_cap,case_param.production['A']['P']['H'],case_param.production['B']['P']['H'],case_param.production['C']['P']['H'],case_param.production['D']['P']['H'],case_param.production['A']['P']['J'],case_param.production['B']['P']['J'],case_param.production['C']['P']['J'],case_param.production['D']['P']['J'],case_param.production['A']['P']['L'],case_param.production['B']['P']['L'],case_param.production['C']['P']['L'],case_param.production['D']['P']['L'],case_param.production['A']['P']['T'],case_param.production['B']['P']['T'],case_param.production['C']['P']['T'],case_param.production['D']['P']['T'],case_param.production['A']['Q']['H'],case_param.production['B']['Q']['H'],case_param.production['C']['Q']['H'],case_param.production['D']['Q']['H'],case_param.production['A']['Q']['J'],case_param.production['B']['Q']['J'],case_param.production['C']['Q']['J'],case_param.production['D']['Q']['J'],case_param.production['A']['Q']['L'],case_param.production['B']['Q']['L'],case_param.production['C']['Q']['L'],case_param.production['D']['Q']['L'],case_param.production['A']['Q']['T'],case_param.production['B']['Q']['T'],case_param.production['C']['Q']['T'],case_param.production['D']['Q']['T'],case_param.production['A']['R']['H'],case_param.production['B']['R']['H'],case_param.production['C']['R']['H'],case_param.production['D']['R']['H'],case_param.production['A']['R']['J'],case_param.production['B']['R']['J'],case_param.production['C']['R']['J'],case_param.production['D']['R']['J'],case_param.production['A']['R']['L'],case_param.production['B']['R']['L'],case_param.production['C']['R']['L'],case_param.production['D']['R']['L'],case_param.production['A']['R']['T'],case_param.production['B']['R']['T'],case_param.production['C']['R']['T'],case_param.production['D']['R']['T'],case_param.production['A']['S']['H'],case_param.production['B']['S']['H'],case_param.production['C']['S']['H'],case_param.production['D']['S']['H'],case_param.production['A']['S']['J'],case_param.production['B']['S']['J'],case_param.production['C']['S']['J'],case_param.production['D']['S']['J'],case_param.production['A']['S']['L'],case_param.production['B']['S']['L'],case_param.production['C']['S']['L'],case_param.production['D']['S']['L'],case_param.production['A']['S']['T'],case_param.production['B']['S']['T'],case_param.production['C']['S']['T'],case_param.production['D']['S']['T']]
            top_x_list.append(current_list)
            top_x_cost.append(current_cost)
        elif current_cost < max(top_x_cost):
            current_list = [current_iter,current_cost,below_max_cap,case_param.production['A']['P']['H'],case_param.production['B']['P']['H'],case_param.production['C']['P']['H'],case_param.production['D']['P']['H'],case_param.production['A']['P']['J'],case_param.production['B']['P']['J'],case_param.production['C']['P']['J'],case_param.production['D']['P']['J'],case_param.production['A']['P']['L'],case_param.production['B']['P']['L'],case_param.production['C']['P']['L'],case_param.production['D']['P']['L'],case_param.production['A']['P']['T'],case_param.production['B']['P']['T'],case_param.production['C']['P']['T'],case_param.production['D']['P']['T'],case_param.production['A']['Q']['H'],case_param.production['B']['Q']['H'],case_param.production['C']['Q']['H'],case_param.production['D']['Q']['H'],case_param.production['A']['Q']['J'],case_param.production['B']['Q']['J'],case_param.production['C']['Q']['J'],case_param.production['D']['Q']['J'],case_param.production['A']['Q']['L'],case_param.production['B']['Q']['L'],case_param.production['C']['Q']['L'],case_param.production['D']['Q']['L'],case_param.production['A']['Q']['T'],case_param.production['B']['Q']['T'],case_param.production['C']['Q']['T'],case_param.production['D']['Q']['T'],case_param.production['A']['R']['H'],case_param.production['B']['R']['H'],case_param.production['C']['R']['H'],case_param.production['D']['R']['H'],case_param.production['A']['R']['J'],case_param.production['B']['R']['J'],case_param.production['C']['R']['J'],case_param.production['D']['R']['J'],case_param.production['A']['R']['L'],case_param.production['B']['R']['L'],case_param.production['C']['R']['L'],case_param.production['D']['R']['L'],case_param.production['A']['R']['T'],case_param.production['B']['R']['T'],case_param.production['C']['R']['T'],case_param.production['D']['R']['T'],case_param.production['A']['S']['H'],case_param.production['B']['S']['H'],case_param.production['C']['S']['H'],case_param.production['D']['S']['H'],case_param.production['A']['S']['J'],case_param.production['B']['S']['J'],case_param.production['C']['S']['J'],case_param.production['D']['S']['J'],case_param.production['A']['S']['L'],case_param.production['B']['S']['L'],case_param.production['C']['S']['L'],case_param.production['D']['S']['L'],case_param.production['A']['S']['T'],case_param.production['B']['S']['T'],case_param.production['C']['S']['T'],case_param.production['D']['S']['T']]
            list_idx = top_x_cost.index(max(top_x_cost))
            top_x_cost[list_idx] = current_cost
            top_x_list[list_idx] = current_list
    for element in top_x_list:
        text_file.write("\n%s" % str(element))
            #text_file.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (current_iter,current_cost,below_max_cap,case_param.production['A']['P']['H'],case_param.production['B']['P']['H'],case_param.production['C']['P']['H'],case_param.production['D']['P']['H'],case_param.production['A']['P']['J'],case_param.production['B']['P']['J'],case_param.production['C']['P']['J'],case_param.production['D']['P']['J'],case_param.production['A']['P']['L'],case_param.production['B']['P']['L'],case_param.production['C']['P']['L'],case_param.production['D']['P']['L'],case_param.production['A']['P']['T'],case_param.production['B']['P']['T'],case_param.production['C']['P']['T'],case_param.production['D']['P']['T'],case_param.production['A']['Q']['H'],case_param.production['B']['Q']['H'],case_param.production['C']['Q']['H'],case_param.production['D']['Q']['H'],case_param.production['A']['Q']['J'],case_param.production['B']['Q']['J'],case_param.production['C']['Q']['J'],case_param.production['D']['Q']['J'],case_param.production['A']['Q']['L'],case_param.production['B']['Q']['L'],case_param.production['C']['Q']['L'],case_param.production['D']['Q']['L'],case_param.production['A']['Q']['T'],case_param.production['B']['Q']['T'],case_param.production['C']['Q']['T'],case_param.production['D']['Q']['T'],case_param.production['A']['R']['H'],case_param.production['B']['R']['H'],case_param.production['C']['R']['H'],case_param.production['D']['R']['H'],case_param.production['A']['R']['J'],case_param.production['B']['R']['J'],case_param.production['C']['R']['J'],case_param.production['D']['R']['J'],case_param.production['A']['R']['L'],case_param.production['B']['R']['L'],case_param.production['C']['R']['L'],case_param.production['D']['R']['L'],case_param.production['A']['R']['T'],case_param.production['B']['R']['T'],case_param.production['C']['R']['T'],case_param.production['D']['R']['T'],case_param.production['A']['S']['H'],case_param.production['B']['S']['H'],case_param.production['C']['S']['H'],case_param.production['D']['S']['H'],case_param.production['A']['S']['J'],case_param.production['B']['S']['J'],case_param.production['C']['S']['J'],case_param.production['D']['S']['J'],case_param.production['A']['S']['L'],case_param.production['B']['S']['L'],case_param.production['C']['S']['L'],case_param.production['D']['S']['L'],case_param.production['A']['S']['T'],case_param.production['B']['S']['T'],case_param.production['C']['S']['T'],case_param.production['D']['S']['T']))
    text_file.close()
    time_stop = time.time()
    print("Total time elapse: ", time_stop - time_start, "s\n")
    print("Rate: ", (time_stop - time_start)/num_iter, "s/iteration\n")

def hooke_jeeves_updater(product,customer,plant,mode,movement):
    # This is a simple tabu search algorithm with discrete change of 1
    # Update rule:
    # A  B
    # C  D
    # Going clockwise, mode n balances with n-th next neighbour in clockwise
    # Params: 
    #    product - product name in char
    #    customer - customer name in char
    #    mode - Mode in int based on update rule
    #    movement - Increment / Decrement (1,-1)

    # Okay all the centralised data info is gone aye?
    plant_list = ['A','B','C','D']
    plant_update_list = [0,0,0,0]
    plant_update_list[plant_list.index(plant)] += movement
    plant_update_list[(plant_list.index(plant) + mode) % 4] -= movement
    # Here we decode the mode and movement into the plant_update_list
    case_param.production['A'][product][customer] = case_param.production['A'][product][customer] + plant_update_list[0]
    case_param.production['B'][product][customer] = case_param.production['B'][product][customer] + plant_update_list[1]
    case_param.production['C'][product][customer] = case_param.production['C'][product][customer] + plant_update_list[2]
    case_param.production['D'][product][customer] = case_param.production['D'][product][customer] + plant_update_list[3]

def hooke_jeeves_wrapper(num_iter, rand_initializer=True, debug=False, num_initalization=1, record_best=True, overwrite=False):
    for i in range(0,num_initalization):
        hooke_jeeves_iterator(num_iter, rand_initializer, debug, record_best, overwrite)

def hooke_jeeves_iterator(num_iter, rand_initializer=True, debug=False, record_best=True, overwrite=False):
    # Wrapper to run simple tabu
    if rand_initializer:
        simple_local_initializer()
    else:
        case_param.production = populate_production(case_param.production)
    time_start = time.time()
    if overwrite:
        text_file = open("Output_hooke_jeeves.csv", "w")
    else:
        text_file = open("Output_hooke_jeeves.csv", "a")
    text_file.write("\nCurrent_iter,current_cost,below_max_cap,APH,BPH,CPH,DPH,APJ,BPJ,CPJ,DPJ,APL,BPL,CPL,DPL,APT,BPT,CPT,DPT,AQH,BQH,CQH,DQH,AQJ,BQJ,CQJ,DQJ,AQL,BQL,CQL,DQL,AQT,BQT,CQT,DQT,ARH,BRH,CRH,DRH,ARJ,BRJ,CRJ,DRJ,ARL,BRL,CRL,DRL,ART,BRT,CRT,DRT,ASH,BSH,CSH,DSH,ASJ,BSJ,CSJ,DSJ,ASL,BSL,CSL,DSL,AST,BST,CST,DST")
    current_cost = evaluate_cost()
    print("Initial cost:", current_cost)
    # This is the golden copy of the production quantity, we save it before changing the dynamic dictionary

    # Here we save a copy of the initial state of the optimization (base-state)
    if not record_best:
        current_list = ["Base",current_cost,True,case_param.production['A']['P']['H'],case_param.production['B']['P']['H'],case_param.production['C']['P']['H'],case_param.production['D']['P']['H'],case_param.production['A']['P']['J'],case_param.production['B']['P']['J'],case_param.production['C']['P']['J'],case_param.production['D']['P']['J'],case_param.production['A']['P']['L'],case_param.production['B']['P']['L'],case_param.production['C']['P']['L'],case_param.production['D']['P']['L'],case_param.production['A']['P']['T'],case_param.production['B']['P']['T'],case_param.production['C']['P']['T'],case_param.production['D']['P']['T'],case_param.production['A']['Q']['H'],case_param.production['B']['Q']['H'],case_param.production['C']['Q']['H'],case_param.production['D']['Q']['H'],case_param.production['A']['Q']['J'],case_param.production['B']['Q']['J'],case_param.production['C']['Q']['J'],case_param.production['D']['Q']['J'],case_param.production['A']['Q']['L'],case_param.production['B']['Q']['L'],case_param.production['C']['Q']['L'],case_param.production['D']['Q']['L'],case_param.production['A']['Q']['T'],case_param.production['B']['Q']['T'],case_param.production['C']['Q']['T'],case_param.production['D']['Q']['T'],case_param.production['A']['R']['H'],case_param.production['B']['R']['H'],case_param.production['C']['R']['H'],case_param.production['D']['R']['H'],case_param.production['A']['R']['J'],case_param.production['B']['R']['J'],case_param.production['C']['R']['J'],case_param.production['D']['R']['J'],case_param.production['A']['R']['L'],case_param.production['B']['R']['L'],case_param.production['C']['R']['L'],case_param.production['D']['R']['L'],case_param.production['A']['R']['T'],case_param.production['B']['R']['T'],case_param.production['C']['R']['T'],case_param.production['D']['R']['T'],case_param.production['A']['S']['H'],case_param.production['B']['S']['H'],case_param.production['C']['S']['H'],case_param.production['D']['S']['H'],case_param.production['A']['S']['J'],case_param.production['B']['S']['J'],case_param.production['C']['S']['J'],case_param.production['D']['S']['J'],case_param.production['A']['S']['L'],case_param.production['B']['S']['L'],case_param.production['C']['S']['L'],case_param.production['D']['S']['L'],case_param.production['A']['S']['T'],case_param.production['B']['S']['T'],case_param.production['C']['S']['T'],case_param.production['D']['S']['T']]
        text_file.write("\n%s" % str(current_list))
    print_iter_interval = 2    # This is the output interval for the iteration, console to print status every x print_iter_interval
    #for movement in range(-10,10, 1):
    #for movement in [-20,20,-19,19,-18,18,-17,17,-16,16,-15,15,-14,14,-13,13,-12,12,-11,11,-10,10,-9,9,-8,8,-7,7-6,6,-5,5,-4,4,-3,3,-2,2,-1,1]:
    #for movement in [-10,10,-9,9,-8,8,-7,7-6,6,-5,5,-4,4,-3,3,-2,2,-1,1]:
    for movement in [-5,5,-4,4,-3,3,-2,2,-1,1]:
        print("Current movement: ", movement)
    #for current_iter in range(0, num_iter):
        # Algorithm for simple tabu iteration:
        # For every golden state (i.e. the current variables that will yield the lowest cost)
        #    we perform a simple tabu search around its neighbour
        #    bear in mind that we may find more than one steps that may result in a reduction of the cost
        #    therefore we will do an exhaustive search to return only the step that yields the lowest cost
        #    among all. This set of variables shall serve as the golden copy for the next iteration.
        #    The iterations will stop when the maximum iterations have reached or a minimal (not guaranteed to
        #    global), then the result is saved to the output_hooke_jeeves.csv file)
        #    NOTE: Got to remember to reset / udpate the golden production at the end of the iteration
        #          provided the iteration were to continue.
        # Golden will serve as a copy of the previous state
        golden_production = deepcopy(case_param.production)
        # Next will hold the production quantities that to be updated with
        #if current_iter % print_iter_interval == 0:
        #    print('Current iter: ', current_iter)

        # Main loop to iterate through the number of plants / product / customers

        for current_iter in range(0, num_iter):
        #for movement in range(10,-11,-1):
            current_base = deepcopy(case_param.production)
            prev_best_cost = evaluate_cost() # Save the cost, i.e. best cost so far to be compared with
            #print("Current iteration: ", current_iter, " Current best cost: ", prev_best_cost)
            current_list = [str(movement) + "-" + str(current_iter),prev_best_cost,True,case_param.production['A']['P']['H'],case_param.production['B']['P']['H'],case_param.production['C']['P']['H'],case_param.production['D']['P']['H'],case_param.production['A']['P']['J'],case_param.production['B']['P']['J'],case_param.production['C']['P']['J'],case_param.production['D']['P']['J'],case_param.production['A']['P']['L'],case_param.production['B']['P']['L'],case_param.production['C']['P']['L'],case_param.production['D']['P']['L'],case_param.production['A']['P']['T'],case_param.production['B']['P']['T'],case_param.production['C']['P']['T'],case_param.production['D']['P']['T'],case_param.production['A']['Q']['H'],case_param.production['B']['Q']['H'],case_param.production['C']['Q']['H'],case_param.production['D']['Q']['H'],case_param.production['A']['Q']['J'],case_param.production['B']['Q']['J'],case_param.production['C']['Q']['J'],case_param.production['D']['Q']['J'],case_param.production['A']['Q']['L'],case_param.production['B']['Q']['L'],case_param.production['C']['Q']['L'],case_param.production['D']['Q']['L'],case_param.production['A']['Q']['T'],case_param.production['B']['Q']['T'],case_param.production['C']['Q']['T'],case_param.production['D']['Q']['T'],case_param.production['A']['R']['H'],case_param.production['B']['R']['H'],case_param.production['C']['R']['H'],case_param.production['D']['R']['H'],case_param.production['A']['R']['J'],case_param.production['B']['R']['J'],case_param.production['C']['R']['J'],case_param.production['D']['R']['J'],case_param.production['A']['R']['L'],case_param.production['B']['R']['L'],case_param.production['C']['R']['L'],case_param.production['D']['R']['L'],case_param.production['A']['R']['T'],case_param.production['B']['R']['T'],case_param.production['C']['R']['T'],case_param.production['D']['R']['T'],case_param.production['A']['S']['H'],case_param.production['B']['S']['H'],case_param.production['C']['S']['H'],case_param.production['D']['S']['H'],case_param.production['A']['S']['J'],case_param.production['B']['S']['J'],case_param.production['C']['S']['J'],case_param.production['D']['S']['J'],case_param.production['A']['S']['L'],case_param.production['B']['S']['L'],case_param.production['C']['S']['L'],case_param.production['D']['S']['L'],case_param.production['A']['S']['T'],case_param.production['B']['S']['T'],case_param.production['C']['S']['T'],case_param.production['D']['S']['T']]
            text_file.write("\n%s" % str(current_list))
            update_flag = False
            total_change = []
            for product in case_param.product:
                for customer in case_param.customer:
                    # For each set of product-customer pair, we perform the neighbour search
                    for mode in [1,2,3]:
                        for plant in ['A','B','C','D']:
                            # Here we pass the variables into the updater to update the value for the 
                            current_change = [product,customer,plant,mode,movement]
                            hooke_jeeves_updater(product,customer,plant,mode,movement)
                            current_cost = evaluate_cost()
                            if debug:
                                print("Iteration: ", current_iter,"\tMode: ",mode, "\tCustomer: ",customer, "\tMovement: ",movement, "\tPlant: ", plant, "\tCost: ",current_cost)
                            below_max_cap = True
                            all_pos = True
                            for plant in case_param.plant:
                                if not capacity_check(plant):
                                    below_max_cap = False
                                if not sanity_check(plant):
                                    all_pos = False
                            if (not below_max_cap) or (not all_pos):
                                # Well if the maximum capacity is exceeded, reset the state and continue
                                case_param.production = deepcopy(current_base)
                                continue
                            # Only check the cost if the capacity is not exceeded
                            if current_cost < prev_best_cost:
                                if debug:
                                    print("\nUpdate from neighbour: Old Cost: ", prev_best_cost, " New Cost: ", current_cost)
                                prev_best_cost = current_cost
                                current_base = deepcopy(case_param.production)
                                total_change.append(current_change)
                                
                                update_flag = True # We set this flag to True if there's any improvement, else iteration will break
                            else:
                                case_param.production = deepcopy(current_base)
            # Here we apply the same direction again to see if it works
            current_base = deepcopy(case_param.production)
            cost_base = evaluate_cost()
            if update_flag:
                for change in total_change:
                    hooke_jeeves_updater(change[0],change[1],change[2],change[3],change[4])
                # After direction move we check if capacity is exceeded
                for plant in case_param.plant:
                    if not capacity_check(plant):
                        below_max_cap = False
                    if not sanity_check(plant):
                        all_pos = False
                        if debug:
                            print("Leveraged movement negative detected")
                if (not below_max_cap) or (not all_pos):
                    # Well if the maximum capacity is exceeded, reset the state and continue
                    if debug:
                        print("Production reset due to below_max_cap or all_pos")
                    case_param.production = deepcopy(current_base)
                    continue
                else:
                    cost_move = evaluate_cost()
                    if cost_move > cost_base:
                        if debug:
                            print("Patern move yielded higher cost")
                        case_param.production = deepcopy(current_base)
                    elif debug:
                            print("Update!")
            else:
                # No point iteration, move to the next step size
                break
    # End of iteration, restore the case_param.production to the best combination so far
    current_cost = evaluate_cost()
    current_list = [current_iter,current_cost,below_max_cap,case_param.production['A']['P']['H'],case_param.production['B']['P']['H'],case_param.production['C']['P']['H'],case_param.production['D']['P']['H'],case_param.production['A']['P']['J'],case_param.production['B']['P']['J'],case_param.production['C']['P']['J'],case_param.production['D']['P']['J'],case_param.production['A']['P']['L'],case_param.production['B']['P']['L'],case_param.production['C']['P']['L'],case_param.production['D']['P']['L'],case_param.production['A']['P']['T'],case_param.production['B']['P']['T'],case_param.production['C']['P']['T'],case_param.production['D']['P']['T'],case_param.production['A']['Q']['H'],case_param.production['B']['Q']['H'],case_param.production['C']['Q']['H'],case_param.production['D']['Q']['H'],case_param.production['A']['Q']['J'],case_param.production['B']['Q']['J'],case_param.production['C']['Q']['J'],case_param.production['D']['Q']['J'],case_param.production['A']['Q']['L'],case_param.production['B']['Q']['L'],case_param.production['C']['Q']['L'],case_param.production['D']['Q']['L'],case_param.production['A']['Q']['T'],case_param.production['B']['Q']['T'],case_param.production['C']['Q']['T'],case_param.production['D']['Q']['T'],case_param.production['A']['R']['H'],case_param.production['B']['R']['H'],case_param.production['C']['R']['H'],case_param.production['D']['R']['H'],case_param.production['A']['R']['J'],case_param.production['B']['R']['J'],case_param.production['C']['R']['J'],case_param.production['D']['R']['J'],case_param.production['A']['R']['L'],case_param.production['B']['R']['L'],case_param.production['C']['R']['L'],case_param.production['D']['R']['L'],case_param.production['A']['R']['T'],case_param.production['B']['R']['T'],case_param.production['C']['R']['T'],case_param.production['D']['R']['T'],case_param.production['A']['S']['H'],case_param.production['B']['S']['H'],case_param.production['C']['S']['H'],case_param.production['D']['S']['H'],case_param.production['A']['S']['J'],case_param.production['B']['S']['J'],case_param.production['C']['S']['J'],case_param.production['D']['S']['J'],case_param.production['A']['S']['L'],case_param.production['B']['S']['L'],case_param.production['C']['S']['L'],case_param.production['D']['S']['L'],case_param.production['A']['S']['T'],case_param.production['B']['S']['T'],case_param.production['C']['S']['T'],case_param.production['D']['S']['T']]
    text_file.write("\n%s" % str(current_list))
    text_file.close()
    time_stop = time.time()
    print("Total time elapse: ", time_stop - time_start, "s\n")
    print("Rate: ", (time_stop - time_start)/num_iter, "s/iteration\n")

# simulated annealing algorithm
def simulated_annealing(num_initialization, n_iterations, step_size, temp, overwrite=False):
    for j in range(0, num_initialization):
        # generate an initial point
        #best = bounds[:, 0] + rand(len(bounds)) * (bounds[:, 1] - bounds[:, 0])    

        # Hyperparameter (consider tuning these)
        amount_change = 1    
        t = temp
        beta_param = 2
        alpha_param = 0.9999

        simple_local_initializer()    

        # evaluate the initial point
        #best_eval = objective(best)
        best_eval = evaluate_cost()
        best = deepcopy(case_param.production)
        # current working solution
        curr_eval = best_eval
        curr = deepcopy(case_param.production)    

        # Here we perform the routine to run the output-to-text file
        if overwrite:
            text_file = open("Output_SA.csv", "w")
        else:
            text_file = open("Output_SA.csv", "a")
        text_file.write("\nCurrent_iter,current_cost,below_max_cap,APH,BPH,CPH,DPH,APJ,BPJ,CPJ,DPJ,APL,BPL,CPL,DPL,APT,BPT,CPT,DPT,AQH,BQH,CQH,DQH,AQJ,BQJ,CQJ,DQJ,AQL,BQL,CQL,DQL,AQT,BQT,CQT,DQT,ARH,BRH,CRH,DRH,ARJ,BRJ,CRJ,DRJ,ARL,BRL,CRL,DRL,ART,BRT,CRT,DRT,ASH,BSH,CSH,DSH,ASJ,BSJ,CSJ,DSJ,ASL,BSL,CSL,DSL,AST,BST,CST,DST")    

        # run the algorithm
        for i in range(n_iterations):
            # take a step    

            # Here we need a new function for the update rule
            # candidate = curr + randn(len(bounds)) * step_size
            gen_sa_candidate(step_size, amount_change)
            # evaluate candidate point    

            #candidate_eval = objective(candidate)
            candidate_eval = evaluate_cost()    

            # check for new best solution
            if candidate_eval < best_eval:
                # store new best point
                best_eval = candidate_eval
                best = deepcopy(case_param.production)
                # report progress
                print('>%d f(%s) = %.5f' % (i, best, best_eval))
                current_list = [str(j) + "-" + str(i),candidate_eval,True,case_param.production['A']['P']['H'],case_param.production['B']['P']['H'],case_param.production['C']['P']['H'],case_param.production['D']['P']['H'],case_param.production['A']['P']['J'],case_param.production['B']['P']['J'],case_param.production['C']['P']['J'],case_param.production['D']['P']['J'],case_param.production['A']['P']['L'],case_param.production['B']['P']['L'],case_param.production['C']['P']['L'],case_param.production['D']['P']['L'],case_param.production['A']['P']['T'],case_param.production['B']['P']['T'],case_param.production['C']['P']['T'],case_param.production['D']['P']['T'],case_param.production['A']['Q']['H'],case_param.production['B']['Q']['H'],case_param.production['C']['Q']['H'],case_param.production['D']['Q']['H'],case_param.production['A']['Q']['J'],case_param.production['B']['Q']['J'],case_param.production['C']['Q']['J'],case_param.production['D']['Q']['J'],case_param.production['A']['Q']['L'],case_param.production['B']['Q']['L'],case_param.production['C']['Q']['L'],case_param.production['D']['Q']['L'],case_param.production['A']['Q']['T'],case_param.production['B']['Q']['T'],case_param.production['C']['Q']['T'],case_param.production['D']['Q']['T'],case_param.production['A']['R']['H'],case_param.production['B']['R']['H'],case_param.production['C']['R']['H'],case_param.production['D']['R']['H'],case_param.production['A']['R']['J'],case_param.production['B']['R']['J'],case_param.production['C']['R']['J'],case_param.production['D']['R']['J'],case_param.production['A']['R']['L'],case_param.production['B']['R']['L'],case_param.production['C']['R']['L'],case_param.production['D']['R']['L'],case_param.production['A']['R']['T'],case_param.production['B']['R']['T'],case_param.production['C']['R']['T'],case_param.production['D']['R']['T'],case_param.production['A']['S']['H'],case_param.production['B']['S']['H'],case_param.production['C']['S']['H'],case_param.production['D']['S']['H'],case_param.production['A']['S']['J'],case_param.production['B']['S']['J'],case_param.production['C']['S']['J'],case_param.production['D']['S']['J'],case_param.production['A']['S']['L'],case_param.production['B']['S']['L'],case_param.production['C']['S']['L'],case_param.production['D']['S']['L'],case_param.production['A']['S']['T'],case_param.production['B']['S']['T'],case_param.production['C']['S']['T'],case_param.production['D']['S']['T']]
                text_file.write("\n%s" % str(current_list))
            # difference between candidate and current point evaluation
            diff = candidate_eval - curr_eval
            # calculate temperature for current epoch
            #t = temp / float(i + 1)
            t = alpha_param * t
            #t = t / (1 + beta_param * t)
            # calculate metropolis acceptance criterion
            # This is absolutely necessary
            print("-diff/t:\t", (-diff/t))
            metropolis = exp(-diff / t)
            # check if we should keep the new point
            if diff < 0 or rand() < metropolis:
                # store the new current point
                curr_eval = candidate_eval
                curr = deepcopy(case_param.production)
            else:
                case_param.production = deepcopy(curr)
        text_file.close()

def constrain_check():
    # Now there is surely a valid reason to run a rroutine to check for constrains
    # Basically is a combination of the capacity check and the positive check
    # May be able to add more checks if needed.
    pass_check = True
    below_max_cap = True
    all_pos = True
    for plant in case_param.plant:
        if not capacity_check(plant):
            below_max_cap = False
        if not sanity_check(plant):
            all_pos = False
    if (not below_max_cap) or (not all_pos):
        # Well if the maximum capacity is exceeded, reset the state and continue
        pass_check = False
    return pass_check

def gen_sa_candidate(step_size, amount_change):
    # Technically what we need is just the step_size, may not even 
    """
    # Update rule:
    We randomly generate a list of combinations to alter for each generation of candidate,
    We also limit the number of changes for each new candidate, this is to ensure the candidate
    is not differ from the previous best candidate by too much, effectively a Monte-Carlo method is 
    disguise. Make it sensible.
    """
    
    # Here we generate the list of udpate to be made

    # What we need. Here we can reuse the updater for Hooke and Jeeves

    # Consider adding a hard-stop to prevent stack overflow
    mode_list = [1,2,3]
    for i in range(0, amount_change):
        # Update rule will need to consider the constrains
        candidate_backup = deepcopy(case_param.production)
        product = case_param.product[randint(0,len(case_param.product)-1)]
        customer = case_param.customer[randint(0,len(case_param.customer)-1)]
        plant = case_param.plant[randint(0,len(case_param.plant)-1)]
        mode = mode_list[randint(0,len(mode_list)-1)]
        # Just lazy to look up the API documentation
        movement_direction = randint(0,1)
        if movement_direction == 0:
            movement_direction -= 1
        movement = step_size * movement_direction
        hooke_jeeves_updater(product,customer,plant,mode,movement)
        # We don't do cost check here because it's irrelevant
        if not constrain_check():
            # If the constrain is exceeded, we revert the production to the previous set,
            # and at the same time we reduce the counter
            i -= 1
            case_param.production = deepcopy(candidate_backup)