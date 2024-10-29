#!/usr/bin/env python
"""
Provides functions for writing a file named with the type of filtered material (slope #) with the format:
    Value for Stiffness, Value for Density, Value for Modulus of Elasticity
    if they are higher or lower based on the chosen value; example: higher, lower, higher
    Name, Density, Modulus of Elasticity (for all filtered materials)
"""
import matplotlib
matplotlib.use('Agg')
import csv
import os

__author__ = "Bruno Paucar, Giovanny Chunga and Miguel Realpe"
__credits__ = ["Bruno Paucar", "Giovanny Chunga", "Miguel Realpe",
                    "Clotario Tapia"]
__license__ = "GNU GPL"
__version__ = "1.0.1"
__maintainer__ = "Miguel Realpe"
__email__ = "mrealpe@fiec.espol.edu.ec"
__status__ = "Prototype"

def writeFiles(finalMaterialsList, finalDensityList, finalModulusList, family, stiffness, density, modulus, slope_value, density_value, modulus_value, slope):
    stiffness_ = ""
    density_ = ""
    modulus_ = ""
    if slope_value == 1:
        stiffness_ += "Higher values for stiffness"
    else:
        stiffness_ += "Lower values for stiffness"
    if density_value == 1:
        density_ += "Higher values for density"
    else:
        density_ += "Lower values for density"
    if modulus_value == 1:
        modulus_ += "Higher values for modulus of elasticity"
    else:
        modulus_ += "Lower values for modulus of elasticity"
    name = "{}(slope {}, stiffness {}, density {}, modulus of elasticity {}).csv".format(family, slope, stiffness,
                                                                                         density, modulus)

    file = open(name, 'w', newline="\n")
    writer = csv.writer(file, delimiter=',', quotechar='"')

    writer.writerow(["---- Description ----"])
    writer.writerow(["Value for stiffness: {} --- Value for Density: {} ---- Value for Modulus of Elasticity: {}".format(stiffness, density, modulus)])
    writer.writerow(["{} --- {} ---- {}".format(stiffness_, density_, modulus_)])
    writer.writerow(["---- Data ----"])
    writer.writerow(["name", "density", "modulus of elasticity"])
    for counter in range(len(finalMaterialsList)):
        row = [finalMaterialsList[counter], finalDensityList[counter], finalModulusList[counter]]
        writer.writerow(row)
    file.close()

#!/usr/bin/env python
"""
Provides functions for loading data from a CSV with the format:
    Name, Category, URL, Density, Modulus of Elasticity
"""

import csv

__author__ = "Bruno Paucar, Giovanny Chunga and Miguel Realpe"
__credits__ = ["Bruno Paucar", "Giovanny Chunga", "Miguel Realpe",
                    "Clotario Tapia"]
__license__ = "GNU GPL"
__version__ = "1.0.1"
__maintainer__ = "Miguel Realpe"
__email__ = "mrealpe@fiec.espol.edu.ec"
__status__ = "Prototype"


def readFile(csvFile):
    file = open(csvFile, 'r', newline='\n')
    reader = csv.reader(file, delimiter=",", quotechar='"')
    header = next(reader)
    names = []
    types = []
    urls = []
    densities = []
    moduliOfElasticity = []
    data = {}
    namesNoValue = []
    for line in reader:
        name, category, url, density, modulus = line
        category = category.split(';')
        if len(category) > 1:
            if category[0] == 'Ceramic' and category[1] == ' Glass':
                type_ = category[1][1:]
            else:
                type_ = category[0]
        else:
            type_ = category[0]
        if density == '0' or modulus == '0' or density == '' or modulus == '':
            namesNoValue.append(name)
        else:
            names.append(name)
            types.append(type_)
            urls.append(url)
            densities.append(float(density))
            moduliOfElasticity.append(float(modulus))
    for i in range(len(names)):
        materialData = {}
        materialData["Family"] = types[i]
        materialData["Density"] = densities[i]
        materialData["Modulus of Elasticity"] = moduliOfElasticity[i]
        materialData["URL"] = urls[i]
        data[names[i]] = materialData
    file.close()
    return data

def getModulusDensity(data):
    materialList = []
    densityList = []
    modulusList = []
    typeList = []
    for key, value in data.items():
        materialList = list(data.keys())
        densityList.append(data[key]["Density"])
        modulusList.append(data[key]["Modulus of Elasticity"])
        typeList.append(data[key]["Family"])
    return materialList, typeList, densityList, modulusList

#!/usr/bin/env python
"""
Provides filter functions for Ashby Methodology
"""

import numpy as np

__author__ = "Bruno Paucar, Giovanny Chunga and Miguel Realpe"
__credits__ = ["Bruno Paucar", "Giovanny Chunga", "Miguel Realpe",
                    "Clotario Tapia"]
__license__ = "GNU GPL"
__version__ = "1.0.1"
__maintainer__ = "Miguel Realpe"
__email__ = "mrealpe@fiec.espol.edu.ec"
__status__ = "Prototype"


def filterType(materialsList, typesList, densitiesList, moduliList, type_):
    filteredMaterials = []
    filteredDensities = []
    filteredModuli = []
    for i in range(len(materialsList)):
        if typesList[i] == type_:
            filteredMaterials.append(materialsList[i])
            filteredDensities.append(densitiesList[i])
            filteredModuli.append(moduliList[i])
    return filteredMaterials, filteredDensities, filteredModuli

def filterDensity(materialsList, densitiesList, moduliList, density, is_density_higher):
    filteredMaterials = []
    filteredDensities = []
    filteredModuli = []
    for i in range(len(densitiesList)):
        if is_density_higher and densitiesList[i] > density:
                filteredDensities.append(densitiesList[i])
                filteredMaterials.append(materialsList[i])
                filteredModuli.append(moduliList[i])
        elif not is_density_higher and densitiesList[i] < density:
                filteredDensities.append(densitiesList[i])
                filteredMaterials.append(materialsList[i])
                filteredModuli.append(moduliList[i])
    return filteredMaterials, filteredDensities, filteredModuli

def filterModulus(materialsList, densitiesList, moduliList, modulus, is_modulus_higher):
    filteredMaterials = []
    filteredDensities = []
    filteredModuli = []
    for i in range(len(densitiesList)):
        if is_modulus_higher and densitiesList[i] > modulus:
                filteredDensities.append(densitiesList[i])
                filteredMaterials.append(materialsList[i])
                filteredModuli.append(moduliList[i])
        elif not is_modulus_higher and densitiesList[i] < modulus:
                filteredDensities.append(densitiesList[i])
                filteredMaterials.append(materialsList[i])
                filteredModuli.append(moduliList[i])
    return filteredMaterials, filteredDensities, filteredModuli

def filterMaterials(materialsList, densitiesList, moduliList, slope, threshold, is_slope_higher):
    filteredMaterials, filteredDensities, filteredModuli = [], [], []
    if slope == 1:
        if is_slope_higher:
            for i in range(len(materialsList)):
                if moduliList[i] > threshold * densitiesList[i]:
                    filteredMaterials.append(materialsList[i])
                    filteredDensities.append(densitiesList[i])
                    filteredModuli.append(moduliList[i])
        else:
            for i in range(len(materialsList)):
                if moduliList[i] < threshold * densitiesList[i]:
                    filteredMaterials.append(materialsList[i])
                    filteredDensities.append(densitiesList[i])
                    filteredModuli.append(moduliList[i])
    elif slope == 2:
        if is_slope_higher:
            for i in range(len(materialsList)):
                if moduliList[i] > (threshold * densitiesList[i])**2:
                    filteredMaterials.append(materialsList[i])
                    filteredDensities.append(densitiesList[i])
                    filteredModuli.append(moduliList[i])
        else:
            for i in range(len(materialsList)):
                if moduliList[i] < (threshold * densitiesList[i])**2:
                    filteredMaterials.append(materialsList[i])
                    filteredDensities.append(densitiesList[i])
                    filteredModuli.append(moduliList[i])
    elif slope == 3:
        if is_slope_higher:
            for i in range(len(materialsList)):
                if moduliList[i] > (threshold * densitiesList[i])**3:
                    filteredMaterials.append(materialsList[i])
                    filteredDensities.append(densitiesList[i])
                    filteredModuli.append(moduliList[i])
        else:
            for i in range(len(materialsList)):
                if moduliList[i] < (threshold * densitiesList[i])**3:
                    filteredMaterials.append(materialsList[i])
                    filteredDensities.append(densitiesList[i])
                    filteredModuli.append(moduliList[i])
    return filteredMaterials, filteredDensities, filteredModuli



def filter(materialList, typeList, densityList, modulusList, materialType, density, density_higher, modulus, modulus_higher, slope, stiffness, slope_higher):
    materialList2, densityList2, modulusList2 = filterType(materialList, typeList, densityList, modulusList, materialType)
    materialList3, densityList3, modulusList3 = filterDensity(materialList2, densityList2, modulusList2, density, density_higher)
    materialList4, densityList4, modulusList4 = filterModulus(materialList3, densityList3, modulusList3, modulus, modulus_higher)
    finalMaterialList, finalDensityList, finalModulusList = filterMaterials(materialList4, densityList4, modulusList4, slope, stiffness, slope_higher)
    return finalMaterialList, finalDensityList, finalModulusList


# When there are more than 10k materials in total or more than 500 filtered materials expected, it is preferable to use the filter by arrays
def filterArrays(materialList, typeList, densityList, modulusList, materialType, density, density_higher, modulus, modulus_higher):
    arrayMaterials = np.array(materialList)
    arrayTypes = np.array(typeList)
    arrayDensities = np.array(densityList)
    arrayModulus = np.array(modulusList)
    condition1 = arrayTypes == materialType
    if density_higher:
        condition2 = arrayDensities > density
    else:
        condition2 = arrayDensities < density
    if modulus_higher:
        condition3 = arrayModulus > modulus
    else:
        condition3 = arrayModulus < modulus
    return arrayMaterials[(condition1) & (condition2) & (condition3)], \
           arrayDensities[(condition1) & (condition2) & (condition3)], \
           arrayModulus[(condition1) & (condition2) & (condition3)]

#!/usr/bin/env python
"""
Provides functions for plotting the "DENSITY vs MODULUS OF E" chart for the Ashby Methodology.
"""

import matplotlib.pyplot as plt
import numpy as np

__author__ = "Bruno Paucar, Giovanny Chunga and Miguel Realpe"
__credits__ = ["Bruno Paucar", "Giovanny Chunga", "Miguel Realpe", "Clotario Tapia"]
__license__ = "GNU GPL"
__version__ = "1.0.1"
__maintainer__ = "Miguel Realpe"
__email__ = "mrealpe@fiec.espol.edu.ec"
__status__ = "Prototype"

def line1(n):
    x = np.linspace(0.0001, 1000)
    y = n * x
    plt.loglog(x, y, '-', label='E/ρ,{}'.format(n))

def line2(n):
    x = np.linspace(0.0001, 1000)
    y = (n * x) ** 2
    plt.loglog(x, y, '-', label='E^(1/2)/ρ,{}'.format(n))

def line3(n):
    x = np.linspace(0.0001, 1000)
    y = (n * x) ** 3
    plt.loglog(x, y, '-', label='E^(1/3)/ρ,{}'.format(n))

def verticalDensity(density, maxDensity):
    plt.loglog([density, density], [0, maxDensity], 'C1')

def horizontalModulus(modulus, maxModulus):
    plt.loglog([0, maxModulus], [modulus, modulus], 'C3')

def plot(dictionary, densityList, modulusList, filteredMaterialList, filteredDensityList, filteredModulusList, density, modulus, stiffness, slope):
    familyLegend = {
        'Glass': 'm.',
        'Ceramic': 'c.',
        'Carbon': 'k+',
        'Metal': 'r.',
        'Wood and Natural Products': 'g+',
        'Polymer': 'y.',
        'Fluid': 'b.',
        'Pure Element': 'r+',
        'Other Engineering Material': 'c^'
    }
    
    # Chart 1
    plt.figure('Chart 1')
    plt.title('Ashby Chart')
    types = []
    for keys, data in dictionary.items():
        family = data['Family']
        density = data['Density']
        modulus = data['Modulus of Elasticity']
        sign = familyLegend.get(family, 'bX')
        plt.plot(density, modulus, sign)
        if family not in types:
            types.append(family)
            plt.plot(density, modulus, sign, label=family)
    if slope == 1:
        line1(stiffness)
    elif slope == 2:
        line2(stiffness)
    elif slope == 3:
        line3(stiffness)
    verticalDensity(density, max(modulusList))
    horizontalModulus(modulus, max(densityList))
    plt.grid()
    plt.xlabel('Density. ρ (Kg/m^3)')
    plt.ylabel('Modulus of Elasticity. E(GPa)')
    plt.legend(loc='upper left')

    # Chart 2
    plt.figure('Chart 2')
    plt.title('Filtered Materials')
    types = []
    for filteredIndex in range(len(filteredMaterialList)):
        family = dictionary[filteredMaterialList[filteredIndex]]['Family']
        density = filteredDensityList[filteredIndex]
        modulus = filteredModulusList[filteredIndex]
        sign = familyLegend.get(family, 'bX')
        plt.plot(density, modulus, sign)
        if family not in types:
            types.append(family)
            plt.plot(density, modulus, sign, label=family)
    if slope == 1:
        line1(stiffness)
    elif slope == 2:
        line2(stiffness)
    elif slope == 3:
        line3(stiffness)
    verticalDensity(density, max(modulusList))
    horizontalModulus(modulus, max(densityList))
    plt.grid()
    plt.xlabel('Density. ρ (Kg/m^3)')
    plt.ylabel('Modulus of Elasticity. E(GPa)')
    plt.legend(loc='upper left')

"""
Provides interface for Ashby Methodology
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

__author__ = "Bruno Paucar, Giovanny Chunga and Miguel Realpe"
__credits__ = ["Bruno Paucar", "Giovanny Chunga", "Miguel Realpe", "Clotario Tapia"]
__license__ = "GNU GPL"
__version__ = "1.0.1"
__maintainer__ = "Miguel Realpe"
__email__ = "mrealpe@fiec.espol.edu.ec"
__status__ = "Prototype"



import tkinter as tk
from tkinter import ttk, messagebox

def interface():
    def close_program():
        exit()

    interface = tk.Tk()
    interface.title("Density vs Young's Modulus Charts")
    interface.geometry('360x380')
    interface.protocol('WM_DELETE_WINDOW', close_program)

    # First line
    title = ttk.Label(interface, text='Select the options to optimize the values').place(x=70, y=0)
    # Slope
    slope_label = ttk.Label(interface, text='Slope').place(x=20, y=40)
    combo_slope = ttk.Combobox(interface, width=9, state='readonly')
    combo_slope.place(x=80, y=40)
    combo_slope['values'] = (1, 2, 3)
    combo_slope.set(1)

    # Family
    family_label = ttk.Label(interface, text='Family').place(x=20, y=70)
    combo_family = ttk.Combobox(interface, width=22, state='readonly')
    combo_family.place(x=80, y=70)
    combo_family['values'] = ("Carbon", "Ceramic", "Glass", "Fluid", "Metal", 
                              "Other Engineering Material", "Polymer", "Pure Element", "Wood and Natural Products")
    combo_family.current(4)

    # Stiffness
    stiffness_label = ttk.Label(interface, text='Stiffness').place(x=20, y=100)
    stiffness_entry = ttk.Entry(interface, width=12)
    stiffness_entry.place(x=80, y=100)
    stiffness_entry.insert(0, 0.0)
    check_slope_value = tk.IntVar()
    slope_higher = ttk.Radiobutton(interface, text='Higher values', value=1, variable=check_slope_value).place(x=25, y=130)
    slope_lower = ttk.Radiobutton(interface, text='Lower values', value=0, variable=check_slope_value).place(x=150, y=130)

    # Density
    general_property_label = ttk.Label(interface, text='General property').place(x=15, y=155)
    density_label = ttk.Label(interface, text='Density').place(x=20, y=180)
    density_entry = ttk.Entry(interface, width=12)
    density_entry.place(x=80, y=180)
    density_entry.insert(0, 0.0)
    density_units = ttk.Label(interface, text='kg/m^3').place(x=170, y=180)
    check_density_value = tk.IntVar()
    density_higher = ttk.Radiobutton(interface, text='Higher values', value=1, variable=check_density_value).place(x=25, y=210)
    density_lower = ttk.Radiobutton(interface, text='Lower values', value=0, variable=check_density_value).place(x=150, y=210)

    # Modulus of Elasticity
    mechanical_property_label = ttk.Label(interface, text='Mechanical property').place(x=15, y=240)
    modulus_label = ttk.Label(interface, text='Modulus of Elasticity').place(x=15, y=265)
    modulus_entry = ttk.Entry(interface, width=12)
    modulus_entry.place(x=150, y=265)
    modulus_entry.insert(0, 0.0)
    modulus_units = ttk.Label(interface, text='GPa').place(x=238, y=265)
    check_modulus_value = tk.IntVar()
    modulus_higher = ttk.Radiobutton(interface, text='Higher values', value=1, variable=check_modulus_value).place(x=25, y=290)
    modulus_lower = ttk.Radiobutton(interface, text='Lower values', value=0, variable=check_modulus_value).place(x=150, y=290)

    # Buttons
    def submit_action():
        messagebox.showinfo('PAY ATTENTION', "Select options carefully. Leaving boxes empty ('') will plot a default value; '0.0' will plot nothing.")
        print(
            f'Chosen index: "{combo_slope.get()}" for optimizing stiffness with a value of "{stiffness_entry.get()}", '
            f'density "{density_entry.get()}", and modulus of elasticity "{modulus_entry.get()}", '
            f'with higher, lower, or both values. Material family: "{combo_family.get()}".')

    submit_button = ttk.Button(interface, text='Submit', command=submit_action)
    submit_button.place(x=20, y=330)

    continue_button = ttk.Button(interface, text='Continue', command=interface.quit)
    continue_button.place(x=270, y=330)

    def show_info():
        messagebox.showinfo('IMPORTANT', "Select at most 3 options (stiffness, density, modulus), each with a different slope, "
                                        "choose a material family, enter numbers, and select higher or lower values.")

    info_button = ttk.Button(interface, text='Info', command=show_info)
    info_button.place(x=270, y=40)

    interface.mainloop()
    
    slope = int(combo_slope.get())
    family = str(combo_family.get())
    slope_higher_value = bool(check_slope_value.get())
    stiffness = float(stiffness_entry.get())
    density = float(density_entry.get())
    modulus = float(modulus_entry.get())
    density_higher_value = bool(check_density_value.get())
    modulus_higher_value = bool(check_modulus_value.get())
    
    interface.destroy()

    return slope, family, slope_higher_value, 0, stiffness, density, modulus, density_higher_value, 0, modulus_higher_value, 0

# Main program
"""
Material selection software using Ashby Methodology
Chart: DENSITY vs MODULUS OF ELASTICITY
Dataset: data.csv
"""
__author__ = "Bruno Paucar, Giovanny Chunga, and Miguel Realpe"
__credits__ = ["Bruno Paucar", "Giovanny Chunga", "Miguel Realpe", "Clotario Tapia"]
__license__ = "GNU GPL"
__version__ = "1.0.1"
__maintainer__ = "Miguel Realpe"
__email__ = "mrealpe@fiec.espol.edu.ec"
__status__ = "Prototype"

print('----------SOFTWARE "DENSITY vs MODULUS OF ELASTICITY" CHART----------')
print('Loading Dataset...')

# Load material data from the database
dictionary = readFile("data.csv")
# Extract data into lists
materials_list, types_list, density_list, modulus_list = getModulusDensity(dictionary)
print('Dataset Loaded')

# Get input variables from the graphical interface
slope, family, slope_greater, slope_less, stiffness, density, modulus, density_greater, density_less, modulus_greater, modulus_less = interface()

# Filter data by Family, Modulus, Density, and Slope
final_materials_list, final_density_list, final_modulus_list = filter(
    materials_list, types_list, density_list, modulus_list, family, density, density_greater, modulus, modulus_greater, slope, stiffness, slope_greater)

# If the number of filtered materials is over 500, consider using arrays for faster processing
# final_materials_list, final_density_list, final_modulus_list = filter_module.filter_arrays(
#     materials_list, types_list, density_list, modulus_list, family, density, density_greater, modulus, modulus_greater)

# Write to text files
writeFiles(final_materials_list, final_density_list, final_modulus_list, family, stiffness, density, modulus, slope_greater, density_greater, modulus_greater, slope)

# Plot values
g = plot(dictionary, density_list, modulus_list, final_materials_list, final_density_list, final_modulus_list, density, modulus, stiffness, slope)

# Report results
print("Filtered materials: ", final_materials_list)
print("Corresponding densities: ", final_density_list)
print("Corresponding modulus values: ", final_modulus_list)
plt.show(g)


