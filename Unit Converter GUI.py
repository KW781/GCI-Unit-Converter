import tkinter as tk
converter_backend = __import__("Unit Converter") #imports unit converter back end functions

#button function to change the units when the user wants to change quantity e.g. change the units to 'Kilograms' when the user switches to 'Mass'
def update_quantity():
    quantity_num = quantities_dict.get(quantity.get())
    initial_drop.children["menu"].delete(0, "end")
    final_drop.children["menu"].delete(0, "end")
    for unit in units[quantity_num]:
        initial_drop.children["menu"].add_command(label = unit, command = tk._setit(initial_unit, unit))
        final_drop.children["menu"].add_command(label = unit, command = tk._setit(final_unit, unit))
    initial_unit.set(units[quantity_num][0])
    final_unit.set(units[quantity_num][0])

#button function to convert the units, using the converter back end functions
def convert():
    new_units = converter_backend.calculate_new_units(float(entry.get()), [initial_unit.get().lower()], [final_unit.get().lower()])
    conversion_label = tk.Label(window, text = str(entry.get()) + " " + initial_unit.get() + " equals " + str(new_units) + " " + final_unit.get())
    conversion_label.grid(row = 16, column = 0)

#button function to close GUI and switch to CLI upon user request
def switch_interface():
    window.destroy()
    while True:
        converter_backend.input_data_output_calculation()
    

#instantiate Tkinter GUI window    
window = tk.Tk()
window.title("Unit Converter")

#define the quantities dictionary to map each quantity to an index (this makes indexing for lists when creating widgets easier)
#define the units list to store every unit
quantities_dict = {"Distance" : 0, "Mass" : 1, "Time" : 2, "Current" : 3}
units = [["Metres", "Millimetres", "Centimetres", "Kilometres", "Inches", "Feet", "Miles"],
         ["Kilograms", "Milligrams", "Centigrams", "Grams", "Tonnes"],
         ["Seconds", "Minutes", "Hours", "Milliseconds"],
         ["Amperes", "Milliamperes"]]

#create the switch button to switch to the CLI
switch_btn = tk.Button(window, text = "Swtich to CLI for more advanced features", command = switch_interface)
switch_btn.grid(row = 0, column = 0)

#empty labels to create empty space between widgets
empty_label1 = tk.Label(window)
empty_label1.grid(row = 1, column = 0)
empty_label2 = tk.Label(window)
empty_label2.grid(row = 2, column = 0)

#create widgets for allowing the user to change between quantities
quantity = tk.StringVar(window) #StringVar() is Tkinter type which allows for the information in the drop down box to be stored as a string
quantity.set("Distance")
quantity_label = tk.Label(window, text = "Select quantity you want to convert in")
quantity_label.grid(row = 3, column = 0)
quantity_drop = tk.OptionMenu(window, quantity, "Distance", "Mass", "Time", "Current")
quantity_drop.grid(row = 4, column = 0)
quantity_num = quantities_dict.get(quantity.get()) #extract index from quantity_dict corresponding to the quantity selected by the user
update_btn = tk.Button(window, text = "Update Quantity", command = update_quantity)
update_btn.grid(row = 5, column = 0)

#empty label to create space between widgets
empty_label3 = tk.Label(window)
empty_label3.grid(row = 6, column = 0)

#create widgets for the user to input the number to convert from, and also the unit to convert from
initial_unit = tk.StringVar(window)
initial_unit.set(units[quantity_num][0])
initial_label1 = tk.Label(window, text = "Select unit to be converted from")
initial_label1.grid(row = 7, column = 0)
initial_drop = tk.OptionMenu(window, initial_unit, *units[quantity_num])
initial_drop.grid(row = 8, column = 0)
initial_label2 = tk.Label(window, text = "Enter the number:")
initial_label2.grid(row = 9, column = 0)
entry = tk.Entry(window)
entry.grid(row = 10, column = 0)

#empty label to create space between widgets
empty_label4 = tk.Label(window)
empty_label4.grid(row = 11, column = 0)

#create widgets for the user to select the unit to convert to
final_unit = tk.StringVar(window)
final_unit.set(units[quantity_num][0])
final_label1 = tk.Label(window, text = "Select unit to convert to")
final_label1.grid(row = 12, column = 0)
final_drop = tk.OptionMenu(window, final_unit, *units[quantity_num]) #asterisk operator unpacks the list
final_drop.grid(row = 13, column = 0)

#empty label to create space between widgets
empty_label5 = tk.Label(window)
empty_label5.grid(row = 14, column = 0)

#create the 'convert' button
conversion_button = tk.Button(window, text = "Convert", command = convert)
conversion_button.grid(row = 15, column = 0)


window.mainloop()


        
        
        
                                           
