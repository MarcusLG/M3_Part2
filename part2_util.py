# This contains all the utilities to be used in the main function

def populate_production(production):
    # This is a function to populate production with the desired data
    #input_list = [93,7,0,0,105,38,37,20,16,4,0,0,15,14,5,16,19,179,2,0,20,262,12,6,94,3,0,103,29,0,20,1,43,4,3,50,10,135,293,62,277,75,22,26,10,31,58,1,6,1,0,3,67,120,15,198,615,54,34,97,183,13,275,329]
    input_list = [1,12,87,0,2,53,145,0,19,1,0,0,0,22,27,1,14,184,2,0,25,272,2,1,187,13,0,0,39,10,0,1,92,8,0,0,258,135,105,2,397,0,2,1,2,97,0,1,1,7,2,0,0,123,277,0,796,1,1,2,1,66,733,0]
    base = 0
    counter = 0
    for plant in ['A','B','C','D']:
        for product in ['P','Q','R','S']:
            for customer in ['H','J','L','T']:
                production[plant][product][customer] = input_list[counter]
                counter += 4
                if counter >= len(input_list):
                    base += 1
                    counter = base
    return production