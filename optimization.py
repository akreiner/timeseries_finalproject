from gurobipy import *
import random
import numpy as np

SP500_Return=0.05

#Create fake returns, to be adjusted with the real data
Stock_Size=5000
Stock_Returns=[random.gauss(0.12, 0.05) for i in range(Stock_Size)]

#Minimum Number of Stocks to be returned from optimizer
Desired_Stocks=1000

Stock_Indicators={}

m=Model()

#create variable for each stock
for i in range(Stock_Size):
    Stock_Indicators[i]=m.addVar(vtype=GRB.BINARY, name="x")

Total_Return=m.addVar(vtype=GRB.CONTINUOUS, name="x")
Total_Return2=m.addVar(vtype=GRB.CONTINUOUS, name="x")

#min stock constraint
m.addConstr(quicksum(Stock_Indicators[i] for i in range(Stock_Size))>=Desired_Stocks)


#create objective function
m.addConstr(Total_Return==quicksum(Stock_Indicators[i]*Stock_Returns[i] for i in range(Stock_Size))-SP500_Return*quicksum(Stock_Indicators[i] for i in range(Stock_Size)))
m.addConstr(Total_Return2 == abs_(Total_Return))
m.setObjective(Total_Return2)
m.optimize()

Return=0

Num_Stocks=sum([Stock_Indicators[i].X for i in range(Stock_Size)])

#get results
print(Num_Stocks)

for i in range(Stock_Size):
    Return=Return+Stock_Indicators[i].X*Stock_Returns[i]

print(Return/Num_Stocks,SP500_Return)
