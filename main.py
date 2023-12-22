#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 11:00:15 2020

@author: markus
"""

import cplex
import sys 


nFacilities=0
nCustomers=0

myOpeningCosts=[]
myAssignmentCosts=[]

def readInstance(myFilename):
    myInstance=open(myFilename,"r")
    myContent=myInstance.readlines()
    myInstance.close()
   # print(myContent)
    myLine=myContent[0].split()
   # print(myLine)
    global nFacilities
    global nCustomers
    nFacilities=int(myLine[0])
    nCustomers=int(myLine[1])
    print("nFacilities %d"%nFacilities)
    print("nCustomers %d"%nCustomers)
    
    global myOpeningCosts
    global myAssignmentCosts
    for i in range(nFacilities):
        myLine=myContent[1+i].split()
    #    print(myLine)
        myOpeningCosts.append(float(myLine[1]))
   # print(myOpeningCosts)
    myHelper=[]
    for i in range(len(myContent)-1-nFacilities):
        myLine=myContent[1+i+nFacilities].split()
        if len(myLine)==1:
            if i!=0:
                myAssignmentCosts.append(myHelper)
                myHelper=[]
            continue
    #    print(myLine)
        for j in myLine:
            myHelper.append(float(j))
    myAssignmentCosts.append(myHelper)
   # print(myAssignmentCosts)




     

    

if len(sys.argv)!=4:
    print("USAGE: facLoc instancename modeltype exportmodel")
    sys.exit()
    
print(sys.argv)

myFilename=sys.argv[1]
myModeltype=int(sys.argv[2])
myExportmodel=int(sys.argv[3])

readInstance(myFilename)

cpx = cplex.Cplex()
cpx.parameters.threads.set(1)
cpx.objective.set_sense(cpx.objective.sense.minimize)

y=[]
for i in range(nFacilities):
    varName = "y"+str(i)
    y.append(cpx.variables.get_num())
    cpx.variables.add(obj=[myOpeningCosts[i]],types=["B"],names=[varName])

x=[]
for i in range(nFacilities):
    x2=[]
    for j in range(nCustomers):
        varName = "x"+str(i)+","+str(j)
        x2.append(cpx.variables.get_num())
       # print(myAssignmentCosts[j][i])
       # print(j)
       # print(i)
        cpx.variables.add(obj=[myAssignmentCosts[j][i]],types=["B"],names=[varName])
    x.append(x2)

for j in range(nCustomers):
    myInd=[]
    myVal=[]   
    for i in range(nFacilities):
        myInd.append(x[i][j])
        myVal.append(1)
    cpx.linear_constraints.add(lin_expr=[cplex.SparsePair(ind=myInd, val=myVal)],senses=["E"],rhs=[1],names=["customer%d"%j])

if myModeltype==0:
    for i in range(nFacilities):
        for j in range(nCustomers):
            cpx.linear_constraints.add(lin_expr=[cplex.SparsePair(ind=[y[i],x[i][j]], val=[-1,1])],senses=["L"],rhs=[0],names=["assign%d,%d"%(j,i)])

   
    
if myModeltype==1:
    for i in range(nFacilities):
        myInd=[y[i]]
        myVal=[-nCustomers]
        for j in range(nCustomers):
            myInd.append(x[i][j])
            myVal.append(1)
        cpx.linear_constraints.add(lin_expr=[cplex.SparsePair(ind=myInd, val=myVal)],senses=["L"],rhs=[0],names=["assign%d"%(i)])



if myExportmodel==1:
    cpx.write("myFacLocModel.lp")
    
cpx.solve()   
if cpx.solution.get_status()!=103 and cpx.solution.get_status()!=108:
    myObj=cpx.solution.get_objective_value()
    mySol=cpx.solution.get_values()
    print("Solution value %.2f"%myObj)
    openFacilities=[]
    for i in range(nFacilities):
        if mySol[y[i]]>0.5:
            openFacilities.append(i)
    print(openFacilities)
    for j in range(nCustomers):
        for i in range(nFacilities):
            if mySol[x[i][j]]>0.5:
                print("customer %d gets assigned to facility %d"%(j,i))
                break



    
    
cpx.end()
