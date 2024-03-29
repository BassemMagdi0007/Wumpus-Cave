import os
workingFolder = "example-problems" 
#directory = os.fsencode("problems")
directory = os.fsencode(workingFolder)

#__FUNCTIONS__ 

# Direction with wrap around handling
def goNorth(agent):
    if agent[0] == 0: 
        agent[0] = 11
    else: 
        #Decrease Y by one
        agent[0] = agent[0]-1 
    return agent 

def goSouth(agent): 
    if agent[0] == 11: 
        agent[0] = 0
    else: 
        #Increase Y by one
        agent[0] = agent[0]+1 
    return agent 

def goWest(agent):
    if agent[1] == 0: 
        agent[1] = 17
    else: 
        #Decrease X by one
        agent[1] = agent[1]-1 
    return agent 

def goEast(agent):
    if agent[1] == 17: 
        agent[1] = 0
    else: 
        #Increase X by one
        agent[1] = agent[1]+1 
    return agent 

#________________________________________________________

# Extract the empty squares of the map and the agent position if existed 
def find_mapElements(_map):
    indices = []
    agent = [] 
    
    #find the empty squares and the agent locations
    for row_index, row in enumerate (_map):
        for col_index, element in enumerate (row):
            if element == ' ':       
                indices.append((row_index, col_index))
            elif element == 'S': 
                agent.append(row_index)
                agent.append(col_index)

    indices.append(tuple(agent))
    return (indices, agent)

#_______________________CHECK PLAN_______________________ 
#________________________________________________________

def checkPlan(emptySquares, agent):
    newCoord = []
    
    # Create an empty dictionary to hold all the emptySquares and agent position
    myDict = {}
    # Use a for loop to add the list to the dictionary with values set to 'open'
    for item in emptySquares:
        myDict[item] = 'open'
    myDict[tuple(agent)] = 'visited' 
    
    for char in proposedAns:
        if char == 'N':
            newCoord = goNorth(agent.copy())
        if char == 'S':
            newCoord = goSouth(agent.copy())
        if char == 'E':
            newCoord = goEast(agent.copy())
        if char == 'W':
            newCoord = goWest(agent.copy())

        if tuple(newCoord) in emptySquares: 
            agent = newCoord
            myDict[tuple(newCoord)] = 'visited'

    return(myDict)

#________________________________________________________

def write_solution_with_S(myDict):
    valid = 1
    for item in myDict:
        if myDict[item] == 'open':   
            valid = 0        
            break

    with open('mySolutions/solution_' + X + '_' + YZ, 'w') as f:
        if(valid):    
            f.write('GOOD PLAN')
        else:
            f.write("BAD PLAN\n")
            for item in myDict:
                if myDict[item] == 'open':          
                    f.write(str(item[1]) + ", " + str(item[0]) + '\n')

    f.close()

#________________________________________________________

def checkPlanNoS(emptySquares):
    openElements = []
    for item in emptySquares[:-1]:
        agent = list(item) 
        dictNoS = checkPlan(emptySquares[:-1], agent)
        
        for item in dictNoS:
            if dictNoS[item] == 'open': 
                openElements.append(item)

    unique_set = set(openElements)
    # Convert the set back to a list
    unique_list = list(unique_set)
    return(unique_list)

#________________________________________________________

def write_solution_without_S(openElements):

    with open('mySolutions/solution_' + X + '_' + YZ, 'w') as f:
        if(not openElements):    
            f.write('GOOD PLAN')
        else:
            f.write("BAD PLAN\n")

            for item in openElements:
                f.write(str(item[1]) + ", " + str(item[0]) + '\n')

#_______________________FIND PLAN________________________  
#________________________________________________________

def get_direction(current, next_pos):
    x_curr, y_curr = current
    x_next, y_next = next_pos

    if x_next == x_curr + 1:
        return 'N'
    elif x_next == x_curr - 1:
        return 'S'
    elif y_next == y_curr + 1:
        return 'W'
    elif y_next == y_curr - 1:
        return 'E'
    elif x_next == 0:
        return 'N'
    elif x_next == 11:
        return 'S'
    elif y_next == 0:
        return 'W'
    elif y_next == 17:
        return 'E'

#________________________________________________________                

def is_valid_move_dfs(maze, x, y, visited):
    rows, cols = len(maze), len(maze[0])
    return 0 <= x < rows and 0 <= y < cols and maze[x][y] != 'X' and (x, y) not in visited

#________________________________________________________

def dfs(maze, current_position, goal, visited, path):
    x, y = current_position

    if current_position == goal:
        path.append(current_position)
        return True

    visited.add(current_position)
    
    for neighbor in [tuple(goSouth(list(current_position))),tuple(goNorth(list(current_position))), tuple(goWest(list(current_position))), tuple(goEast(list(current_position)))]:
        if is_valid_move_dfs(maze, *neighbor, visited):
            if dfs(maze, neighbor, goal, visited, path):
                path.append(current_position)
                return True
            
    # If all neighbors are visited or walls, backtrack
    return False

#________________________________________________________

def finPlan(maze, emptySquares, start):

    visited_set = set()
    path = []
    all_paths_coordinates = []

    for goal in emptySquares:
        if not dfs(maze, start, goal, visited_set, path):
            return

        path_coordinates = [get_direction(path[i], path[i + 1]) for i in range(len(path) - 1)]
        if path_coordinates != None:
            path_coordinates_str = ''.join(path_coordinates[::-1])

        # Update start_position to the reached goal
        start = goal

        # Accumulate path coordinates
        all_paths_coordinates.append(path_coordinates_str)
        find_solution(''.join(all_paths_coordinates))
        # Clear visited set and path for the next iteration
        visited_set.clear()
        path.clear()

#________________________________________________________

def find_solution(plan):
    with open('mySolutions/solution_' + X + '_' + YZ, 'w') as f:
        if plan:
            f.write(''.join(plan))
        else:
            f.write('NO PLAN FOUND\n')  

#________________________________________________________          

def findPlanNoS(maze, emptySquares):
    all_paths_coordinates = []
    for start_position in emptySquares[:-1]:
        finPlan(maze, emptySquares[:-1], start_position)
    return ''.join(all_paths_coordinates)

#_________________________MAIN____________________________        

# Open the file for reading
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    l = filename.split("_")
    X = l[1]
    YZ = l[2]


    if X in ['a', 'b', 'c', 'd', 'e', 'f']: #ALL EXAMPLE PROBLEMS
        with open(workingFolder + '\\' + filename, 'r') as file2:

            line = file2.readlines()
            _map = [item.replace('\n', "") for item in line]
            # Extract the first line (type of the problem)
            problemType = _map[0]
            
            # Check for type of problem 
            # CHECK PLAN
            if problemType == "CHECK PLAN": 
                # Extract the second line (solution of the problem)
                proposedAns = _map[1]
                # Extract the rest (the cave)
                cave = _map[2:]
                emptySquares, agent = find_mapElements(cave)

                # Check CHECK PLAN type_____________________________________
                # With Agent
                if agent:  
                    finalDict = checkPlan(emptySquares.copy(), agent.copy())
                    write_solution_with_S(finalDict)
                # Without Agent
                else:
                    finalList = checkPlanNoS(emptySquares.copy())
                    write_solution_without_S(finalList)

        # FIND PLAN       
        if problemType == "FIND PLAN":
            cave = _map[1:]
            emptySquares , agent = find_mapElements(cave)
            start_position = tuple(agent)

            # Check FIND PLAN type_____________________________________
            # With Agent
            if start_position:
                findAgentFinal = finPlan(cave, emptySquares, start_position)
            
            # Without Agent
            else:
                findFinal = findPlanNoS(cave, emptySquares)