import os
#workingFolder = "problems" 
workingFolder = "example-problems" 
#directory = os.fsencode("problems")
directory = os.fsencode(workingFolder)
#__________________________________________________________________________________________________________________


#__FUNCTIONS__ 

def goNorth(agent):
    #print("Go North")
    if agent[0] == 0: 
        agent[0] = 11
    else: 
        #Decrease Y by one
        agent[0] = agent[0]-1 
    return agent 

def goSouth(agent): 
    #print("Go South")
    if agent[0] == 11: 
        agent[0] = 0
    else: 
        #Increase Y by one
        agent[0] = agent[0]+1 
    return agent 

def goWest(agent):
    #print("Go west")
    if agent[1] == 0: 
        agent[1] = 17
    else: 
        #Decrease X by one
        agent[1] = agent[1]-1 
    return agent 

def goEast(agent):
    #print("Go East")
    if agent[1] == 17: 
        agent[1] = 0
    else: 
        #Increase X by one
        agent[1] = agent[1]+1 
    return agent 

#__________________________________________________________________________________________________________________
def find_mapElements(_map):
    indices = []
    agent = [] 
    
    #find the empty squares and the agent locations
    for row_index, row in enumerate (_map):
        for col_index, element in enumerate (row):
            #print(element, end=' ')
            #print()
            if element == ' ':       
                indices.append((row_index, col_index))
            elif element == 'S': 
                agent.append(row_index)
                agent.append(col_index)

    indices.append(tuple(agent))
    #print("indices: ", indices)
    #print(indices)
    return (indices, agent)

#__________________________________________________________________________________________________________________
def check_solution_with_S(myDict):
    valid = 1
    for item in myDict:
        if myDict[item] == 'open':   
            valid = 0          
            break

    with open('mySolutions/solution_' + X + '_' + YZ, 'w') as f:
        if(valid):    
            print("GOOD PLAN")
            f.write('GOOD PLAN')
        else:
            print("BAD PLAN")
            f.write("BAD PLAN\n")
            #print('\n', myDict, '\n')
            for item in myDict:
                # print missed squares 
                if myDict[item] == 'open':          
                    print(item[1],", ", item[0]) 
                    f.write(str(item[1]) + ", " + str(item[0]) + '\n')

    f.close()
#__________________________________________________________________________________________________________________
def check_solution_without_S(openElements):

    with open('mySolutions/solution_' + X + '_' + YZ, 'w') as f:
        if(not openElements):    
            #print("GOOD PLAN")
            f.write('GOOD PLAN')
        else:
            #print("BAD PLAN")
            f.write("BAD PLAN\n")

            for item in openElements:
                # print missed squares 
                print(item[1],", ", item[0]) 
                f.write(str(item[1]) + ", " + str(item[0]) + '\n')

#__________________________________________________________________________________________________________________
def find_solution_with_S(plan):
    with open('mySolutions/solution_' + X + '_' + YZ, 'w') as f:
        if plan:
            f.write(''.join(plan))
            print("plan", ''.join(plan))
        else:
            f.write('BAD PLAN\n') 

#__________________________________________________________________________________________________________________
# 1) create dictionary and sets the initial value 'visited' and empty squares 'open'
# 2) read the proposed answer and move the agent accordingly 
# 3) check if the next coordinate is an empty square, if yes move the agent to it and mark it as 'visited'
# 4) return the dictionary that has all the coordinates "check later in the main if all the dictionary is visited or not and decide GOOD/BAD plan accordingly" 
def checkPlan(emptySquares, agent):

    newCoord = []
    
    # Create an empty dictionary to hold all the emptySquares and agent position
    myDict = {}
    # Use a for loop to add the list to the dictionary with values set to 'open'
    for item in emptySquares:
        myDict[item] = 'open'
    myDict[tuple(agent)] = 'visited'  #Check regression
    
    #print("myDict Check: ",myDict)
    
    #newCoord = agent
    #print("newCoord:" , newCoord)
    for char in proposedAns:
        #print("agent before: ", agent)
        if char == 'N':
            newCoord = goNorth(agent.copy())
        if char == 'S':
            newCoord = goSouth(agent.copy())
        if char == 'E':
            newCoord = goEast(agent.copy())
        if char == 'W':
            newCoord = goWest(agent.copy())

        if tuple(newCoord) in emptySquares: 
            #print("GGGG")
            agent = newCoord
            myDict[tuple(newCoord)] = 'visited'
            print(myDict)
    
        #print("\nnewCoord: ", newCoord)
        #print("\nagent after: ", agent)
        #print(myDict)
    return(myDict)

#__________________________________________________________________________________________________________________    
def checkPlanNoS(emptySquares):
    openElements = []
    for item in emptySquares[:-1]:
        agent = list(item) 
        #print(agent, end=' ')
        dictNoS = checkPlan(emptySquares[:-1], agent)
        
        for item in dictNoS:
        # print missed squares 
            if dictNoS[item] == 'open': 
                openElements.append(item)
                
        #print(dictNoS)

    unique_set = set(openElements)
    # Convert the set back to a list
    unique_list = list(unique_set)


    #print("\nopenElements: ", unique_list)
    #print(agent, end=' ')
    return(unique_list)

#__________________________________________________________________________________________________________________
def findPlan(emptySquares, agent):
    visited = set()
    # naughty_squares = []
    plan = []
    initial_agent = agent
    global north_blocked 
    global south_blocked
    global west_blocked 
    global east_blocked
    north_blocked = 0
    south_blocked = 0
    east_blocked = 0
    west_blocked = 0

    def dfs(agent):
        global north_blocked 
        global south_blocked
        global west_blocked 
        global east_blocked

        print("Recursion agent", agent)
        # add last reached square to the visited 
        visited.add(tuple(agent))
        print("\nvisited: \n", visited)
        for square in emptySquares[:-1]:
            print("Target Square: ",square)
            #print("Empty Squares: ",emptySquares)
            reached = 0
            if tuple(square) not in visited:
                while tuple(agent) != tuple(square):
                    #current_position = tuple(agent)
                   
                    if agent[0] < square[0] and not south_blocked:
                    # if agent[0] < square[0]:
                        new_agent = goSouth(list(agent).copy())
                        print("S","square: ", square, "Agent: ", agent, "newAgent: ", new_agent)
                        if tuple(new_agent) not in emptySquares:
                            # emptySquares.remove(square)
                            # emptySquares.append(square)
                            print("S BREAK Square ", square)
                            south_blocked = 1
                            break
                        else:
                            plan.append('S')
                            # visited.add(tuple(new_agent))
                            print(plan)
                            agent = tuple(new_agent)
                            reached = 1
                            west_blocked = 0
                            north_blocked = 0
                            east_blocked = 0
                            print("Agent TTTT South: ", agent)
                   
                    # elif agent[0] > square[0]:
                    elif agent[0] > square[0] and not north_blocked:
                        new_agent = goNorth(list(agent).copy())
                        print("N","square: ", square, "Agent: ", agent, "newAgent: ", new_agent)
                        if tuple(new_agent) not in emptySquares:
                            # emptySquares.remove(square)
                            # emptySquares.append(square)
                            print("N BREAK Square ", square)
                            north_blocked = 1
                            break
                        else:
                            plan.append('N')
                            south_blocked = 0
                            # visited.add(tuple(new_agent))
                            print(plan)
                            agent = tuple(new_agent)
                            reached = 1
                            west_blocked = 0
                            south_blocked = 0
                            east_blocked = 0
                            print("Agent TTTT North: ", agent)

                    # if agent[1] < square[1]:
                    if agent[1] < square[1] and not east_blocked:
                        new_agent = goEast(list(agent).copy())
                        print("E","square: ", square, "Agent: ", agent, "newAgent: ", new_agent)
                        if tuple(new_agent) not in emptySquares:
                            # emptySquares.remove(square)
                            # emptySquares.append(square)
                            print("E BREAK Square ", square)
                            east_blocked = 1
                            break
                        else: 
                            plan.append('E')
                            south_blocked = 0
                            # visited.add(tuple(new_agent))
                            print(plan)
                            agent = tuple(new_agent)
                            reached = 1
                            west_blocked = 0
                            south_blocked = 0
                            north_blocked = 0
                            print("Agent TTTT East: ", agent)
                    
                    # elif agent[1] > square[1]:
                    elif agent[1] > square[1] and not west_blocked:
                        new_agent = goWest(list(agent).copy())
                        print("W", "square: ", square, "Agent: ", agent, "newAgent: ", new_agent)
                        if tuple(new_agent) not in emptySquares:
                            # emptySquares.remove(square)
                            # emptySquares.append(square)
                            print("W BREAK Square ", square)
                            west_blocked = 1
                            break
                        else:
                            plan.append('W')
                            # visited.add(tuple(new_agent))
                            print(plan)
                            agent = tuple(new_agent)
                            reached = 1
                            east_blocked = 0
                            south_blocked = 0
                            north_blocked = 0
                            print("Agent TTTT West: ", agent)

                if reached:
                    print("calling square dfs")
                    print("Recursion square", square)
                    dfs(square)
                else: 
                    print("calling agent dfs")
                    dfs(tuple(agent))

    dfs(agent)
    return plan
#__________________________________________________________________________________________________________________
#__MAIN__

# Open the file for reading
#problemFile = 'problems\problem_a_00.txt'
#problemFile = 'example-problems\problem_a_04.txt'
#with open(problemFile, 'r') as file:
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    l = filename.split("_")
    #print(filename, l)
    X = l[1]
    YZ = l[2]

    #if X != 'd': #or YZ != '01.txt':
        #continue
    ##if X != 'd':
        ##continue
    #if X == 'a' or X == 'b' or X == 'c':
        #break
    if X == 'd' and YZ == '02.txt':
    #else:
        #print("printed")
        with open(workingFolder + '\\' + filename, 'r') as file2:
            # Read the first line
            line = file2.readlines()
            _map = [item.replace('\n', "") for item in line]
            #print(_map)
            #check type of question (Check plan or find plan)
            
            # Extract the first line (type of the problem)
            problemType = _map[0]
            #print(problemType)
            if problemType == "CHECK PLAN": 
                # Extract the second line (solution of the problem)
                proposedAns = _map[1]
                #print(proposedAns)       
                #print("Here")
                cave = _map[2:]
                #print(cave,'\n\n')
                emptySquares, agent = find_mapElements(cave)
                #print("emptySquares:", emptySquares)
                #print("Agent Position:", agent)
                if agent:  
                    finalDict = checkPlan(emptySquares.copy(), agent.copy())
                    #print(finalDict)
                    check_solution_with_S(finalDict)
                else:
                    finalList = checkPlanNoS(emptySquares.copy())
                    check_solution_without_S(finalList)
                    
                
            if problemType == "FIND PLAN":
                print("Find")

                cave = _map[1:]
                emptySquares, agent = find_mapElements(cave)
                print("HEREemptySquares: ", emptySquares)
                print("Agent: ", agent)
                solution = findPlan(emptySquares.copy(), agent.copy())
                find_solution_with_S(solution)
                print(solution)
                # print("Solution:", solution)

                # Write the solution to a file
                
                        
