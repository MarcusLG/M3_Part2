import part2_class
from math import floor
from random import randint
import sys
import time
from copy import deepcopy

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

def simple_tabu_updater(product,customer,plant,mode,movement):
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

def simple_tabu_iterator():
    time_start = time.time()
    text_file = open("Output_simple_tabu.csv", "w")
    text_file.write("Current_iter,current_cost,below_max_cap,APH,BPH,CPH,DPH,APJ,BPJ,CPJ,DPJ,APL,BPL,CPL,DPL,APT,BPT,CPT,DPT,AQH,BQH,CQH,DQH,AQJ,BQJ,CQJ,DQJ,AQL,BQL,CQL,DQL,AQT,BQT,CQT,DQT,ARH,BRH,CRH,DRH,ARJ,BRJ,CRJ,DRJ,ARL,BRL,CRL,DRL,ART,BRT,CRT,DRT,ASH,BSH,CSH,DSH,ASJ,BSJ,CSJ,DSJ,ASL,BSL,CSL,DSL,AST,BST,CST,DST")
    current_cost = evaluate_cost()
    # This is the golden copy of the production quantity, we save it before changing the dynamic dictionary

    # Here we save a copy of the initial state of the optimization (base-state)
    current_list = [current_iter,current_cost,below_max_cap,case_param.production['A']['P']['H'],case_param.production['B']['P']['H'],case_param.production['C']['P']['H'],case_param.production['D']['P']['H'],case_param.production['A']['P']['J'],case_param.production['B']['P']['J'],case_param.production['C']['P']['J'],case_param.production['D']['P']['J'],case_param.production['A']['P']['L'],case_param.production['B']['P']['L'],case_param.production['C']['P']['L'],case_param.production['D']['P']['L'],case_param.production['A']['P']['T'],case_param.production['B']['P']['T'],case_param.production['C']['P']['T'],case_param.production['D']['P']['T'],case_param.production['A']['Q']['H'],case_param.production['B']['Q']['H'],case_param.production['C']['Q']['H'],case_param.production['D']['Q']['H'],case_param.production['A']['Q']['J'],case_param.production['B']['Q']['J'],case_param.production['C']['Q']['J'],case_param.production['D']['Q']['J'],case_param.production['A']['Q']['L'],case_param.production['B']['Q']['L'],case_param.production['C']['Q']['L'],case_param.production['D']['Q']['L'],case_param.production['A']['Q']['T'],case_param.production['B']['Q']['T'],case_param.production['C']['Q']['T'],case_param.production['D']['Q']['T'],case_param.production['A']['R']['H'],case_param.production['B']['R']['H'],case_param.production['C']['R']['H'],case_param.production['D']['R']['H'],case_param.production['A']['R']['J'],case_param.production['B']['R']['J'],case_param.production['C']['R']['J'],case_param.production['D']['R']['J'],case_param.production['A']['R']['L'],case_param.production['B']['R']['L'],case_param.production['C']['R']['L'],case_param.production['D']['R']['L'],case_param.production['A']['R']['T'],case_param.production['B']['R']['T'],case_param.production['C']['R']['T'],case_param.production['D']['R']['T'],case_param.production['A']['S']['H'],case_param.production['B']['S']['H'],case_param.production['C']['S']['H'],case_param.production['D']['S']['H'],case_param.production['A']['S']['J'],case_param.production['B']['S']['J'],case_param.production['C']['S']['J'],case_param.production['D']['S']['J'],case_param.production['A']['S']['L'],case_param.production['B']['S']['L'],case_param.production['C']['S']['L'],case_param.production['D']['S']['L'],case_param.production['A']['S']['T'],case_param.production['B']['S']['T'],case_param.production['C']['S']['T'],case_param.production['D']['S']['T']]
    text_file.write("\n%s" % str(current_list))

    print_iter_interval = 5000    # This is the output interval for the iteration, console to print status every x print_iter_interval
    for current_iter in range(0, num_iter):
        # Algorithm for simple tabu iteration:
        # For every golden state (i.e. the current variables that will yield the lowest cost)
        #    we perform a simple tabu search around its neighbour
        #    bear in mind that we may find more than one steps that may result in a reduction of the cost
        #    therefore we will do an exhaustive search to return only the step that yields the lowest cost
        #    among all. This set of variables shall serve as the golden copy for the next iteration.
        #    The iterations will stop when the maximum iterations have reached or a minimal (not guaranteed to
        #    global), then the result is saved to the output_simple_tabu.csv file)
        #    NOTE: Got to remember to reset / udpate the golden production at the end of the iteration
        #          provided the iteration were to continue.
        # Golden will serve as a copy of the previous state
        golden_production = deepcopy(case_param.production)
        # Next will hold the production quantities that to be updated with
        next_production = deepcopy(case_param.production)
        prev_best_cost = evaluate_cost() # Save the cost, i.e. best cost so far to be compared with
        update_flag = False

        if current_iter % print_iter_interval == 0:
            print('Current iter: ', current_iter)
       
        # Main loop to iterate through the number of plants / product / customers
        for product in case_param.product:
            for customer in case_param.customer:
                # For each set of product-customer pair, we perform the neighbour search
                for mode in [1,2,3]:
                    for movement in [-1,1]: # Here we only run movement search for 2 steps
                        # Here we pass the variables into the updater to update the value for the 
                        simple_tabu_updater(product,customer,plant,mode,movement)
                        current_cost = evaluate_cost()
                        below_max_cap = True
                        for plant in case_param.plant:
                            if not capacity_check(plant):
                                below_max_cap = False
                        if not below_max_cap:
                            # Well if the maximum capacity is exceeded, reset the state and continue
                            case_param.production = deepcopy(golden_production)
                            continue
                        # Only check the cost if the capacity is not exceeded
                        if current_cost < prev_best_cost:
                            prev_best_cost = current_cost
                            next_production = deepcopy(case_param.production)
                            update_flag = True # We set this flag to True if there's any improvement, else iteration will break
        case_param.production = deepcopy(next_production)
        if not update_flag:
            break
    # End of iteration, restore the case_param.production to the best combination so far
    current_cost = evaluate_cost()
    current_list = [current_iter,current_cost,below_max_cap,case_param.production['A']['P']['H'],case_param.production['B']['P']['H'],case_param.production['C']['P']['H'],case_param.production['D']['P']['H'],case_param.production['A']['P']['J'],case_param.production['B']['P']['J'],case_param.production['C']['P']['J'],case_param.production['D']['P']['J'],case_param.production['A']['P']['L'],case_param.production['B']['P']['L'],case_param.production['C']['P']['L'],case_param.production['D']['P']['L'],case_param.production['A']['P']['T'],case_param.production['B']['P']['T'],case_param.production['C']['P']['T'],case_param.production['D']['P']['T'],case_param.production['A']['Q']['H'],case_param.production['B']['Q']['H'],case_param.production['C']['Q']['H'],case_param.production['D']['Q']['H'],case_param.production['A']['Q']['J'],case_param.production['B']['Q']['J'],case_param.production['C']['Q']['J'],case_param.production['D']['Q']['J'],case_param.production['A']['Q']['L'],case_param.production['B']['Q']['L'],case_param.production['C']['Q']['L'],case_param.production['D']['Q']['L'],case_param.production['A']['Q']['T'],case_param.production['B']['Q']['T'],case_param.production['C']['Q']['T'],case_param.production['D']['Q']['T'],case_param.production['A']['R']['H'],case_param.production['B']['R']['H'],case_param.production['C']['R']['H'],case_param.production['D']['R']['H'],case_param.production['A']['R']['J'],case_param.production['B']['R']['J'],case_param.production['C']['R']['J'],case_param.production['D']['R']['J'],case_param.production['A']['R']['L'],case_param.production['B']['R']['L'],case_param.production['C']['R']['L'],case_param.production['D']['R']['L'],case_param.production['A']['R']['T'],case_param.production['B']['R']['T'],case_param.production['C']['R']['T'],case_param.production['D']['R']['T'],case_param.production['A']['S']['H'],case_param.production['B']['S']['H'],case_param.production['C']['S']['H'],case_param.production['D']['S']['H'],case_param.production['A']['S']['J'],case_param.production['B']['S']['J'],case_param.production['C']['S']['J'],case_param.production['D']['S']['J'],case_param.production['A']['S']['L'],case_param.production['B']['S']['L'],case_param.production['C']['S']['L'],case_param.production['D']['S']['L'],case_param.production['A']['S']['T'],case_param.production['B']['S']['T'],case_param.production['C']['S']['T'],case_param.production['D']['S']['T']]
    text_file.write("\n%s" % str(current_list))
    text_file.close()
    time_stop = time.time()
    print("Total time elapse: ", time_stop - time_start, "s\n")
    print("Rate: ", (time_stop - time_start)/num_iter, "s/iteration\n")


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
