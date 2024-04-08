# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    pila = util.Stack() # Definimos una pila para almacenar el camino
    estados = set() # Lista de estados visitados
    pila.push((problem.getStartState(),[], 0)) # Colocamos el estado inicial en la pila
    while not pila.isEmpty():
        (state, action, cost) = pila.pop() # Leemos de la pila
        if problem.isGoalState(state): # Condicion de salida
            return action
        if state not in estados: 
            estados.add(state) # Marcamos como visitado
        for estado, accion, costo  in problem.getSuccessors(state): # Revisamos todos los nodos sucesores
            if estado not in estados: # Si aun no fue visitado
                pila.push((estado, action + [accion], cost + costo)) # Se agrega a la pila
    # util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    cola = util.Queue() # Utilizamos una cola para almacenar el camino
    estados = set() # Lista de estados visitados
    cola.push((problem.getStartState(),[], 0)) # Colocamos el estado inicial en la cola
    while not cola.isEmpty():
        (state, action, cost) = cola.pop() # Leemos de la cola
        if problem.isGoalState(state): # Condicion de salida
            return action
        if state not in estados: 
            estados.add(state) # Marcamos como visitado
        for estado, accion, costo  in problem.getSuccessors(state): # Revisamos todos los nodos sucesores
            if estado not in estados: # Si aun no fue visitado
                cola.push((estado, action + [accion], cost + costo)) # Se agrega a la cola
    # util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    cola = util.PriorityQueue() # Utilizamos una cola con prioridad para almacenar el camino
    estados = set() # Lista de estados visitados
    cola.push((problem.getStartState(),[], 0),0) # Colocamos el estado inicial en la cola
    while not cola.isEmpty():
        (state, action, cost) = cola.pop() # Leemos de la cola
        if problem.isGoalState(state): # Condicion de salida
            return action
        if state not in estados: 
            estados.add(state) # Marcamos como visitado
        for estado, accion, costo  in problem.getSuccessors(state): # Revisamos todos los nodos sucesores
            if estado not in estados: 
                cola.push((estado, action + [accion], cost + costo), cost * costo) # Se agrega a la cola
    # util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueueWithFunction

    def funcionCosto(node):
        return node[2] + 10 * heuristic(node[0], problem)

    # El costo minimo guardamos en un diccionario donde las claves son los estados y los valores los costos
    # Asi podemos reducir el tamaño del nodo de la pila y simplificar la logica, para evadir ciclos
    costos = dict()
    # Los caminos tambien se almacenan de la misma manera
    paths = dict()
    
    state = problem.getStartState()
    costos[state] = 0
    path = []
    _fringe = PriorityQueueWithFunction(funcionCosto)

    if problem.isGoalState(state):
        return path

    for st, action, cost in problem.getSuccessors(state):
        node = (st, [action], cost)
        _fringe.push(node)

    while True:
        if _fringe.isEmpty():
            break

        node, path, node_cost = _fringe.pop()

        if problem.isGoalState(node):
            return path

        # Si es un estado ya visitado y tiene un costo menor, continua
        if node in costos and node_cost > costos[node]:
            continue

        # Si no guarda el estado y el nuevo costo minimo
        costos[node] = node_cost
        paths[node] = path

        # Expandir nodo
        succ = problem.getSuccessors(node)
        for st, action, cost in succ:
            next_path = list(path)
            next_path.append(action)
            next_node = (st, next_path, node_cost + cost)
            _fringe.push(next_node)

    # Goal not found
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch