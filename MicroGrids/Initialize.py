
import pandas as pd

def Initialize_years(model, i):

    '''
    This function returns the value of each year of the project. 
    
    :param model: Pyomo model as defined in the Model_Creation script.
    
    :return: The year i.
    '''    
    return i

Energy_Demand = pd.read_excel('Example/Demand.xls',sheetname=None) # open the energy demand file ,sheetname=None

def Initialize_Demand(model, i, t):
    '''
    This function returns the value of the energy demand from a system for each period of analysis from a excel file.
    
    :param model: Pyomo model as defined in the Model_Creation script.
        
    :return: The energy demand for the period t.     
        
    '''
    Demand = Energy_Demand[model.village]
    return float(Demand[i][t])


    
def Marginal_Cost_Generator_1(model,g):
    
    return model.Fuel_Cost[g]/(model.Low_Heating_Value[g]*model.Generator_Efficiency[g])

    
def Battery_Reposition_Cost(model):
   
    unitary_battery_cost = model.Battery_Invesment_Cost - model.Battery_Electronic_Invesmente_Cost
    return unitary_battery_cost/(model.Battery_Cycles*2*(1-model.Deep_of_Discharge))
    
    
Renewable_Energy = pd.read_excel('Example/Renewable_Energy.xls') # open the PV energy yield file

def Initialize_Renewable_Energy(model, s,r,t):
    '''
    This function returns the value of the energy yield by one PV under the characteristics of the system 
    analysis for each period of analysis from a excel file.
    
    :param model: Pyomo model as defined in the Model_Creation script.
    
    :return: The energy yield of one PV for the period t.
    '''
    column = (s-1)*model.Renewable_Source + r 
    return float(Renewable_Energy[column][t])   
    
    
def Min_Bat_Capacity(model):
        
    
    Periods = model.Battery_Independency*24
    Len = int(model.Periods/Periods)
    Grouper = 1
    index = 1
    for i in range(1, Len+1):
        for j in range(1,Periods+1):
            
            Energy_Demand.loc[index, 'Grouper'] = Grouper
            index += 1
            
        Grouper += 1
            
    Period_Energy = Energy_Demand.groupby(['Grouper']).sum()
    
    Period_Average_Energy = Period_Energy.mean()
    
    Available_Energy = sum(Period_Average_Energy[s]*model.Scenario_Weight[s] 
        for s in model.scenario) 

    return  Available_Energy/(1-model.Deep_of_Discharge)

