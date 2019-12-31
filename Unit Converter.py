def input_data_output_calculation():
    valid = False
    #series of rules output to the user for the input of conversions
    print("Rules for entering conversions:")
    print("1. Enter conversions in the format <value> <initial units> to <converted units>. e.g. 5 metres to kilometres")
    print("2. Use full names for units e.g. kilograms and not kilos")
    print("3. When entering units, enter with a '/' character instead of 'per' e.g. 10 metres/second")
    while valid == False:
        input_string = input("Enter the conversion you want: ")
        valid = validate_conversion(input_string) #validation routine to make sure that the conversion input is typed correctly and is supported
    word_list = input_string.split(' ') #creates a list of the words in the input string, splitting them apart by the space characters
    value = float(word_list[0])
    initial_units = word_list[1].split('/') #extracts the initial units from the input string
    converted_units = word_list[3].split('/') #extracts the units to be converted to from the input string
    new_value = calculate_new_units(value, initial_units, converted_units) #function calculating the new units using the given units and the value
    print(str(value) + " " + word_list[1] + " equals " + str(new_value) + " " + word_list[3]) #outputs the conversion after calculation


def calculate_new_units(value, initial_units, converted_units):
    #the code below takes care of singulars and plurals input e.g. 'foot' instead of 'feet' because plurals are used in the conversion table
    if value == 1:
        if initial_units[0] == "foot":
            initial_units[0] = "feet"
        elif initial_units[0] == "inch":
            initial_units[0] = "inches"
        else:               
            initial_units[0] = initial_units[0] + 's'
    if len(initial_units) == 2:
        if initial_units[1] == "foot":
            initial_units[1] = "feet"
        elif initial_units[1] == "inch":
            initial_units[1] == "inches"
        else:
            initial_units[1] = initial_units[1] + 's'

        if converted_units[1] == "foot":
            converted_units[1] = "feet"
        elif converted_units[1] == "inch":
            converted_units[1] = "inches"
        else:
            converted_units[1] = converted_units[1] + 's'
            
    indices = find_indices(initial_units) #calls upon a function that finds the correct column number (zero indexed) of the conversion table based on the units input

    for i in range(len(indices)): #loops for the number of units input e.g. 'metres' is 1 unit and 'metres/second' is 2 units
        file = open("Conversion Table.txt", "r") #opens text file containing conversion table
        file_data = "#####" #initialises file_data to a starting value
        while file_data != "": #loops until end of file
            file_data = file.readline()
            units = file_data.split(',')
            if find_unit_name(units[0]) != "miles": #checks if it's the last line in the file, if not, then it takes off the new line (\n) character for the last element of units
                units[len(units) - 1] = units[len(units) - 1][:-1]
            if initial_units[i] == find_unit_name(units[indices[i]]): #checking if the given index of the initial units input matches the current unit name in the table
                unit_value = find_unit_value(units[indices[i]])
                #actual calculation of units by dividing or multiplying by the unit value, depending on the value of i
                if i == 0:
                    new_value = value / unit_value
                else:
                    new_value = new_value * unit_value
                break
        file.close()

        #the following code does the same thing as above, except does it for the units that's supposed to be converted to
        file = open("Conversion Table.txt", "r")
        file_data = "#####"
        while file_data != "":
            file_data = file.readline()
            units = file_data.split(',')
            if find_unit_name(units[0]) != "miles":
                units[len(units) - 1] = units[len(units) - 1][:-1]
            if converted_units[i] == find_unit_name(units[indices[i]]):
                unit_value = find_unit_value(units[indices[i]])
                if i == 0:
                    new_value = new_value * unit_value
                else:
                    new_value = new_value / unit_value
                break
        file.close()
    return new_value



def find_unit_name(random_string): #function to extract the unit name from a unit in the conversion table e.g. find_unit_name('0.001kilometres') returns 'kilometres'
    for i in range(len(random_string)): #loops until an alphabetic character is found, then returns the unit name
        if (random_string[i] >= 'a') and (random_string[i] <= 'z'):
            return random_string[i : len(random_string)]


def find_unit_value(random_string): #function to extract the unit value from a unit in the conversion table e.g. find_unit_value('0.001kilometres') returns 0.001
    for i in range(len(random_string)): #loops until an alphabetic character is found, then assigns a value to value_string
        if (random_string[i] >= 'a') and (random_string[i] <= 'z'):
            value_string = random_string[0 : i]
            break
    #some unit values for time have a division sign e.g. '1/60' in '1/60minutes', the following code evaluates the quotient and then returns the floating point unit value
    values = value_string.split('/') 
    if len(values) == 2:
        unit_value = float((int(values[0])) / (int(values[1])))
    else:
        unit_value = float(values[0])

    return unit_value

def find_indices(initial_units): #function to find the correct column number (zero indexed) of the conversion table based on the units input
    indices = [] #the list of column numbers (indices) to be returned is initialised
    for i in range(len(initial_units)): #loops for the number of units in initial_units e.g. for 'metres/second' it will loop twice
        found = False #initialises the flag variable for whether the correct index for each unit has been found
        file = open("Conversion Table.txt", "r")
        file_data = "#####"
        while (file_data != "") and (found == False): #loops until end of file or until the correct index has been found
            file_data = file.readline()
            units = file_data.split(',') #extracts the units from each line in the file
            if find_unit_name(units[0]) != "miles":
                units[len(units) - 1] = units[len(units) - 1][:-1]
            for n in range(len(units)):
                if initial_units[i] == find_unit_name(units[n]): #checks whether the unit matches unit name for each unit in the current line
                    indices.append(n) #if so, adds the index (column number) of that unit to the list and sets the flag variable to true
                    found = True
                    break
        file.close()    
    return indices

def validate_conversion(input_string): #function to validate the input string and check whether it is a valid conversion
    valid = False #initialises flag variable to indicate whether the input string is valid or not
    word_list = input_string.split(' ') #creates a list of words in the input string, splitting them apart by the space characters

    if len(word_list) == 4: #ensures that there's only 4 words, otherwise the user input the conversion in an invalid format
        #the following section of code ensure that the value input is either a floating point number or an integer and doesn't contain any alphabetic characters
        value = word_list[0]
        for i in range(len(value)):
            if ((value[i] >= '0') and (value[i] <= '9')) or (value[i] == '.'):
                valid = True
            else:
                valid = False
                break

        if valid == True:
            initial_units = word_list[1].split('/') #extracts the initial units from the input string
            converted_units = word_list[3].split('/') #extracts the units to be converted to from the input string

            if len(initial_units) == len(converted_units): #ensures that the initial units and the units to be converted to have the same number of units e.g. '10 metres/second to metres' is not valid
                if (len(initial_units) == 1) or (len(initial_units) == 2): #ensures only one or two units is used e.g. '10 metres/second/second to kilometres/hour/hour' is invalid because 3 units are used
                    #the code below takes care of singulars and plurals input e.g. 'foot' instead of 'feet' because plurals are used in the conversion table
                    if value == '1':
                        if initial_units[0] == "foot":
                            initial_units[0] = "feet"
                        elif initial_units[0] == "inch":
                            initial_units[0] = "inches"
                        else:
                            initial_units[0] = initial_units[0] + 's'
                    if len(initial_units) == 2:
                        if initial_units[1] == "foot":
                            initial_units[1] = "feet"
                        elif initial_units[1] == "inch":
                            initial_units[1] = "inches"
                        else:
                            initial_units[1] = initial_units[1] + 's'

                        if converted_units[1] == "foot":
                            converted_units[1] = "feet"
                        elif converted_units[1] == "inch":
                            converted_units[1] = "inches"
                        else:
                            converted_units[1] = converted_units[1] + 's'

                    #calls upon find_indices() for both the initial units and the units to be converted to ensure that each unit used is a unit in the conversion table
                    numbers1 = find_indices(initial_units)
                    numbers2 = find_indices(converted_units)

                    if numbers1 == numbers2: #this then checks that the indexes (column numbers) for each set of units is the same e.g. '10 metres to seconds' is not valid
                        valid = True
                    else:
                        valid = False

                else:
                    valid = False
            else:
                valid = False

    if valid == False:
        print("Sorry, either that conversion was input incorrectly or it's not supported") #outputs error message if the input string is invalid

    return valid

input_data_output_calculation()
