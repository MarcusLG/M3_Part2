import part2_class
from math import floor
from random import randint
import sys
import time

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

def capacity_check(plant):
    # Return true if capacity is not exceeded
    # Param:
    #    plant - the plant to check
    return (case_param.labour_hours[plant]['P'] * sum(case_param.production[plant]['P'].values()) + 
    		case_param.labour_hours[plant]['Q'] * sum(case_param.production[plant]['Q'].values()) +
    		case_param.labour_hours[plant]['R'] * sum(case_param.production[plant]['R'].values()) +
    		case_param.labour_hours[plant]['S'] * sum(case_param.production[plant]['S'].values())) <= case_param.max_capacity[plant]

def updater_iterator():
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

def run_and_print(num_iter):
    time_start = time.time()
    text_file = open("Output.csv", "w")
    text_file.write("Current_iter,current_cost,below_max_cap,APH,BPH,CPH,DPH,APJ,BPJ,CPJ,DPJ,APL,BPL,CPL,DPL,APT,BPT,CPT,DPT,AQH,BQH,CQH,DQH,AQJ,BQJ,CQJ,DQJ,AQL,BQL,CQL,DQL,AQT,BQT,CQT,DQT,ARH,BRH,CRH,DRH,ARJ,BRJ,CRJ,DRJ,ARL,BRL,CRL,DRL,ART,BRT,CRT,DRT,ASH,BSH,CSH,DSH,ASJ,BSJ,CSJ,DSJ,ASL,BSL,CSL,DSL,AST,BST,CST,DST")
    top_x_list = []
    top_x_cost = []
    top_x = 500
    print_iter_interval = 500
    for current_iter in range(0, num_iter):
        if current_iter % print_iter_interval == 0:
            print('Current iter: ', current_iter)
        updater_iterator()
        current_cost = evaluate_cost()
        below_max_cap = True
        for plant in case_param.plant:
            below_max_cap & (capacity_check(plant))
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
