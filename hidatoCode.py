

import sys
import copy

import fileinput

sys.path.append("E:/master_robotica/tecnicasIA/dev/hidatos/aima_python")
sys.path.append("./aima_python")
sys.path.append("/usr/lib/python3/dist-packages/aima-python")

from search import Problem, depth_first_tree_search



class CHidatoProblem(Problem):
    """
    Definitions : 

        Region : Set of cells inside the range defined by [ [minRow, maxRow], [minCol, maxCol] ]


    State : 2D matrix where each position can be a number or letters n,b and v. Where v are empty cells
        where number can be placed, n are not usable black cells and b are not usable cells outside the grid

    Actions : Defined by a tuple [ n, [row, col] ] where n is the number to place in the position (row, col) of the grid

    """

    def __init__(self, f_initState):
        self.initial = f_initState
        self.additionList = []
        self.rows = len(f_initState)
        self.cols = len(f_initState[0])
        self.maxNum = 0

        self.setInitState()
        
        Problem.__init__(self, self.initial)



    def setInitState(self):
        
        self.maxNum = -1

        #Loop over initial state to find max value and the current state
        for i in self.initial:
            for j in i:
                if type(j) == int:
                    if j > self.maxNum:
                        self.maxNum = j


    def getCellAdjacentRegion(self, f_cell):
 
        l_region = []

        l_cellRow = f_cell[0]

        if l_cellRow == 0:
            l_region.append([l_cellRow, l_cellRow+1])
        elif l_cellRow == self.rows-1:
            l_region.append([l_cellRow-1, l_cellRow])
        else:
            l_region.append([l_cellRow-1, l_cellRow+1])


        l_cellCol = f_cell[1]
        if l_cellCol == 0:
            l_region.append([l_cellCol, l_cellCol+1])
        elif l_cellCol == self.cols-1:
            l_region.append([l_cellCol-1, l_cellCol])
        else:
            l_region.append([l_cellCol-1, l_cellCol+1])

        return l_region

    def getAdjacentEmpty(self, f_cells, f_state):
        """
        Returns indices of positions adjacent to positions in f_cells
        """

        l_region = [] # [[minRow,maxRow], [minCol,maxCol]]
        l_outCells = []

        l_numCells = len(f_cells)

        if l_numCells > 1:
            
            #Obtain the 2 regions
            l_region1 = self.getCellAdjacentRegion(f_cells[0])
            l_region2 = self.getCellAdjacentRegion(f_cells[1])
             
            #Calcule the intersection between 2 cells

            #Rows intersection
            l_reg1MinRow = l_region1[0][0]
            l_reg1MaxRow = l_region1[0][1]
            l_reg2MinRow = l_region2[0][0]
            l_reg2MaxRow = l_region2[0][1]

            if l_reg1MinRow >= l_reg2MinRow and l_reg1MinRow <= l_reg2MaxRow:
                l_region.append( [l_reg1MinRow, min(l_reg1MaxRow, l_reg2MaxRow)])
            
            elif  l_reg2MinRow >= l_reg1MinRow and l_reg2MinRow <= l_reg1MaxRow:
                l_region.append( [l_reg2MinRow, min(l_reg1MaxRow, l_reg2MaxRow)])

            else:
                pass

        
            #Cols intersection
            l_reg1MinCol = l_region1[1][0]
            l_reg1MaxCol = l_region1[1][1]
            l_reg2MinCol = l_region2[1][0]
            l_reg2MaxCol = l_region2[1][1]


            if l_reg1MinCol >= l_reg2MinCol and l_reg1MinCol <= l_reg2MaxCol:
                l_region.append( [l_reg1MinCol, min(l_reg1MaxCol, l_reg2MaxCol)])
            
            elif  l_reg2MinCol >= l_reg1MinCol and l_reg2MinCol <= l_reg1MaxCol:
                l_region.append( [l_reg2MinCol, min(l_reg1MaxCol, l_reg2MaxCol)])

            else:
                pass

        elif l_numCells == 1:
            l_region = self.getCellAdjacentRegion(f_cells[0])

        else:
            pass

        if len(l_region) == 2:
            l_outCells = self.getEmptyCellsFromRegion(l_region, f_state)

        return l_outCells



    def getEmptyCellsFromRegion(self, f_region, f_state):
        """
        Returns list of empty cells in the region f_region
        The region is defined as [ [minRow, maxRow], [minCol, maxCol] ]  
        """
        l_outCells = []
        for i in range(f_region[0][0], f_region[0][1]+1):
            for j in range(f_region[1][0], f_region[1][1]+1): 

                l_value = f_state[i][j]
                if l_value == "v":
                    l_outCells.append([i, j])

        return l_outCells


    def obtainStatePlacedNums(self, f_state):
        
        """
        Returns [n, nList] where n is the num of numbers placed in the grid
        and nList is a list where each position indicates if the number is placed 
        and the row and col where is placed
        Take note that position 0 must not be taken account
        """

        # list where each element indicates if the num correpondent to 
        # the position of the list is placed and a list of row,col where is placed
        l_numList = [[False, [0,0]] for i in range(self.maxNum+1)]

        l_numCtr = 0

        for i, ival in enumerate(f_state):
            for j,jval in enumerate(ival):

                if type(jval) == int:
                    l_numList[jval][0] = True
                    l_numList[jval][1][0] = i
                    l_numList[jval][1][1] = j

                    l_numCtr += 1

        return [l_numCtr ,l_numList]


    def selectMinAndAdjacent(self, f_numList):

        l_adjacents = []

        l_lastBool = f_numList[1][0]
        l_numToPlace = -1

        #Num 0 does not exist in the game and initialization 
        #flag has been done with index/num 1
        for i in range(2, len(f_numList)):

            l_isCurrNum = f_numList[i][0]

            #Check for bool step
            if l_isCurrNum != l_lastBool:
                #Resolve adjacent placed nums adjacent to the hole
                 
                if l_isCurrNum == False:
                    l_numToPlace = i
                    l_adjacents.append(f_numList[i-1][1])
                    
                    #Add the another adjacent num if is placed
                    if i < len(f_numList)-1:
                        if f_numList[i+1][0]:
                            l_adjacents.append(f_numList[i+1][1])
                else:
                    l_numToPlace = i-1
                    l_adjacents.append(f_numList[i][1])

                    if i-2 >= 1:
                        if f_numList[i-2][0]:
                            l_adjacents.append(f_numList[i-2][1])

                break

            l_lastBool = l_isCurrNum

        return l_numToPlace,l_adjacents


    def actions(self, f_state):
        """"
        Returns all the possible positions (i,j) where the num with least value  
        in the addition list can be situated
        """

        l_outActions = []

        #Obtain list of current placed nums in the state
        l_numCtr, l_numList = self.obtainStatePlacedNums(f_state)

        #If there is no more nums to place return no actions 
        if l_numCtr < self.maxNum:
            #Select next num to place and the postions where the num has to be adjacent to 
            l_numToPlace, l_adjacents = self.selectMinAndAdjacent(l_numList)

            #Obtain cells where to put value
            l_outCells = self.getAdjacentEmpty(l_adjacents, f_state) 

            l_outActions = [ [l_numToPlace, i] for i in l_outCells]

        else:
            l_outActions = []
       

        return l_outActions


    def result(self, f_state, f_action):
        """
        Place the number of the selected action
        in the new state
        """
        l_newState = copy.deepcopy(f_state)
        l_newState[f_action[1][0]][f_action[1][1]] = f_action[0]

        return l_newState


    def goal_test(self, f_state):
        """
        The state is goal if there is no numbers to place in the 
        grid
        """
        for i in f_state:
            for j in i:
                if j == "v":
                    return False

        return True


def readAndParseInput():

    # print("Input hidato problem in the correct formated input. \nExample : ")
    # print("""
    # 10 10
    # b b v 36 v v 3 v b b
    # v v v v 7 26 v v v v
    # v 39 34 v v v 9 1 19 v
    # v v v 32 v v 11 17 v v
    # b b v 31 29 12 v v b b
    # b b v v n n 15 v b b
    # v 47 v v n n 78 v v v
    # v 51 v v n n v v v v
    # v 58 v v v 67 v 71 v v
    # b b 60 v v v 68 v b b
    # """)

    l_firstLine = True
    l_state = []

    #Count the num of lines to parse due some terminal can be reading forever
    l_numLinesParse = 0
    l_parsedCtr = 0

    for line in fileinput.input():

        #Remove break line character
        line = line[:-1]
        
        #Obtain input values as list
        l_lineValues = line.split(" ")


        l_parsedCtr +=1

        #Parse data
        if l_firstLine:
            l_firstLine = False

            #Parse only num of lines correspondent to the num of rows
            l_numLinesParse = int(l_lineValues[0])
            l_parsedCtr = 0

        else: 
           #Change numeric list values as int type
            for id, i in enumerate(l_lineValues):

                if i != "b" and i != "v" and i != "n":
                    l_lineValues[id] = int(i)

            #Add list to the state grid
            l_state.append(l_lineValues) 


        if l_parsedCtr >= l_numLinesParse:
            break


    return l_state

def main():


    l_initState = readAndParseInput() 

    l_problem = CHidatoProblem(l_initState)


    #print("\nCalculating ...")
    l_result = depth_first_tree_search(l_problem)

    #print("\n\nResult : ")

    for i in l_result.state:
        l_outLine = ""
        for j in i:
            l_outLine = l_outLine + str(j) + " "
            
        l_outLine = l_outLine[:-1]
        print(l_outLine)

if __name__ == "__main__":

    main()