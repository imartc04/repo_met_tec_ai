
import sys
import fileinput


sys.path.append("./aima_python")
sys.path.append("/usr/lib/python3/dist-packages/aima-python")

#from csp import CSP
from constraint import *


def getRestrictionValueFromStr(f_str, f_colValue):

    l_cId = f_str.find("c")
    l_fId = f_str.find("f")

    l_return = None

    if f_colValue:
        if l_fId != -1:
            l_return = f_str[l_fId+1:l_cId]
        else:
            l_return = f_str[:l_cId]

    else:
        l_return = f_str[:l_fId]

    return int(l_return)

def generateCSPProblem(f_grid):

    l_problem = Problem()

    l_letters = "fc"
    l_varsDomain = [i for i in range(1,10)]

    #Generate csp variables
    for i,ival in enumerate(f_grid):
        for j,jval in enumerate(ival):

            if jval == "b":
                l_name = str(i) + "_" + str(j)
                l_problem.addVariable(l_name, l_varsDomain)

                #print("Added variable with name, ", l_name , " domain : ", l_varsDomain)


    #Create problem data from grid
    for i,ival in enumerate(f_grid):
        for j,jval in enumerate(ival):

            #Check if cell is restriction one 
            if "c" in jval:

                #Obtain value of the restriction 
                l_restVal =  getRestrictionValueFromStr(jval ,True)

                #Create condition group
                l_condNeighbour = []

                #Loop over rows to append variables to group
                for k in range( i+1, len(f_grid)):
                    l_val = f_grid[k][j]
                    if l_val == "b":
                        l_condNeighbour.append(str(k)+ "_" +str(j))
                    elif "c" in l_val or "f" in l_val:
                        #End of group 
                        break
                    else:
                        pass

                #Generate constraint with neighbour
                generateConstraints(l_problem, l_restVal, l_condNeighbour)

                #print("Added contraint sum value ", l_restVal, ", vars: ", l_condNeighbour)

            if "f" in jval:

                #Obtain value of the restriction 
                l_restVal =  getRestrictionValueFromStr(jval ,False)

                #Create condition group
                l_condNeighbour = []

                #Loop over columns to append variables to group
                for k in range( j+1, len(f_grid[0])):
                    l_val = f_grid[i][k]
                    if l_val == "b":
                        l_condNeighbour.append(str(i)+ "_" +str(k))
                    elif "c" in l_val or "f" in l_val:
                        #End of group 
                        break
                    else:
                        pass

                #Generate constraint with neighbour
                generateConstraints(l_problem, l_restVal, l_condNeighbour)


                #print("Added contraint sum value ", l_restVal, ", vars: ", l_condNeighbour)

    return l_problem


def generateConstraints(f_problem, f_sumVal, f_neighbour):

    #Generate sum constraint 
    f_problem.addConstraint(ExactSumConstraint(f_sumVal) ,f_neighbour)


    #Generate all different cell values constraint
    f_problem.addConstraint(AllDifferentConstraint(), f_neighbour)



def parseInput():


    l_letters = "nbfc"

    l_grid = []

    #print("Input problem ")

    for line in fileinput.input():

        #print("\nLine value \n", line )

        #Check end of input
        if line == "\n":
            break

        #Remove break line character
        line = line[:-1]
        
        #Obtain input values as list
        l_lineValues = line.split(" ")

        #Append line to grid
        l_grid.append(l_lineValues)

    return l_grid


def main():

    l_grid = parseInput()
    l_problem = generateCSPProblem(l_grid)

    #print("Obtaining solutions... ")

    l_solution = l_problem.getSolutions()

    #Print result formatted
    for key,val in l_solution[0].items():
        l_rowCol = key.split("_")
        l_grid[int(l_rowCol[0])][int(l_rowCol[1])] = val

    for i in l_grid:
        l_line = ""
        for j in i:
            l_line = l_line + str(j) + " "
            
        l_line = l_line[:-1]
        print(l_line)

    print()



if __name__ == "__main__":

    main()

    
