#Name: CHEW WAN THENG RUTH, Matric No: A0144132W, Tutorial Grp : TG6
#Name: Umaiyal Ramanathan, Matric No: A0243806E, Tutorial Grp : TG6  
#Collaborators: None
#Sources: (Reference) https://stackoverflow.com/questions/47004844/is-it-possible-to-have-type-comparison-in-pddl



SUBMISSION = False 
import gym
import gym_grid_driving
from gym_grid_driving.envs.grid_driving import LaneSpec, Point
import os 
import sys

test_config = [{'lanes' : [LaneSpec(2, [0, 0])] *3,'width' :5, 'seed' : 13},
               {'lanes' : [LaneSpec(2, [0, 0])] *3,'width' :5, 'seed' : 10},
               {'lanes' : [LaneSpec(3, [0, 0])] *4,'width' :10, 'seed' : 25},
               {'lanes' : [LaneSpec(4, [0, 0])] *4,'width' :10, 'seed' : 25},
               {'lanes' : [LaneSpec(8, [0, 0])] *7,'width' :20, 'seed' : 25},
               {'lanes' : [LaneSpec(7, [0, 0])] *10,'width' :20, 'seed' : 125}]

test_case_number = 0 # Change the index for a different test case
LANES = test_config[test_case_number]['lanes']
WIDTH = test_config[test_case_number]['width']
RANDOM_SEED = test_config[test_case_number]['seed']

if not SUBMISSION :
    FAST_DOWNWARD_DIRECTORY_ABSOLUTE_PATH = "/fast_downward/"
else :
    FAST_DOWNWARD_DIRECTORY_ABSOLUTE_PATH = ""
PDDL_FILE_ABSOLUTE_PATH = ""

class GeneratePDDL_Stationary :
    def __init__ (self, env, num_lanes, width, file_name) :
        self.state = env.reset()
        self.num_lanes = num_lanes
        self.width = width
        self.file_name = file_name
        self.problem_file_name = self.file_name + 'problem.pddl' 
        self.domain_file_name = self.file_name + 'domain.pddl' 
        self.domain_string = ""
        self.type_string = ""
        self.predicate_strings = self.addHeader("predicates")
        self.action_strings = ""
        self.problem_string = ""
        self.object_strings = self.addHeader("objects")


    def addDomainHeader(self, name='default_header') :
        '''
        Adds the header in the domain file.

        Parameters : 
        name (string): domain name.
        '''
        self.domain_header = "(define (domain " + name +" ) \n" +"(:requirements :strips :typing) \n"


    def addTypes(self, types={}) :
        '''
        Adds the object types to the PDDL domain file.

        Parameters : 
        types (dict): contains a dictionary of (k,v) pairs, where k is the object type, and v is the supertype. If k has no supertype, v is None.
        '''
        type_string = "(:types "

        for _type, _supertype in types.items() :
            if _supertype is None :
                type_string += _type +  "\n"
            else : 
                type_string += _type + " - " + _supertype + "\n"
        type_string += ") \n"
        self.type_string = type_string


    def addPredicate(self, name='default_predicate', parameters = (), isLastPredicate=False) :
        '''
        Adds predicates to the PDDL domain file

        Parameters : 
        name (string) : name of the predicate.
        parameters (tuple or list): contains a list of (var_name, var_type) pairs, where var_name is an instance of object type var_type.
        isLastPredicate (bool) : True for the last predicate added.
        '''
        predicate_string = "(" + name
        for var_name, var_type in parameters :
            predicate_string += " ?" + var_name + " - " + var_type
        predicate_string += ") \n"
        self.predicate_strings+= predicate_string

        print(name, parameters)

        if isLastPredicate :
            self.predicate_strings += self.addFooter()


    def addAction(self, name='default_action', parameters=(), precondition_string= "", effect_string= "") :
        '''
        Adds actions to the PDDL domain file

        Parameters : 
        name (string) : name of the action.
        parameters (tuple or list): contains a list of (var_name, var_type) pairs, where var_name is an instance of object type var_type.
        precondition_string (string) : The precondition for the action.
        effect_string (string) : The effect of the action.
        '''
        action_string = name + "\n"
        parameter_string = ":parameters ("
        for var_name, var_type in parameters :
            parameter_string += " ?" + var_name + " - " + var_type
        parameter_string += ") \n"
        
        precondition_string = ":precondition " + precondition_string + "\n"
        effect_string = ":effect " + effect_string + "\n"
        action_string += parameter_string + precondition_string + effect_string
        action_string = self.addHeader("action") + action_string + self.addFooter()
        self.action_strings+= action_string

    def generateDomainPDDL(self) :
        '''
        Generates the PDDL domain file after all actions, predicates and types are added
        '''
        domain_file = open(PDDL_FILE_ABSOLUTE_PATH + self.domain_file_name, "w")
        PDDL_String = self.domain_header + self.type_string + self.predicate_strings + self.action_strings + self.addFooter()
        domain_file.write(PDDL_String)
        domain_file.close()

   
    def addProblemHeader(self, problem_name='default_problem_name', domain_name='default_domain_name') :
        '''
        Adds the header in the problem file.

        Parameters : 
        problem_name (string): problem name.
        domain_name (string): domain name.
        '''
        self.problem_header = "(define (problem " + problem_name + ") \n (:domain " + domain_name + ") \n"
    

    def addObjects(self, obj_type, obj_list=[], isLastObject=False) :
        '''
        Adds object instances of the same type to the problem file

        Parameters :
        obj_type (string) : the object type of the instances that are being added
        obj_list (list(str)) : a list of object instances to be added
        isLastObject (bool) : True for the last set of objects added.
        '''
        obj_string = ""
        for obj in obj_list :
            obj_string += obj + " "
        obj_string += " - " + obj_type
        self.object_strings += obj_string + "\n "
        if isLastObject :
            self.object_strings += self.addFooter()


    def addInitState(self) :
        initString = self.generateInitString()
        self.initString = self.addHeader("init") + initString + self.addFooter()


    def addGoalState(self) :
        goalString = self.generateGoalString()
        self.goalString = self.addHeader("goal") + goalString + self.addFooter()


    def generateGridCells(self) :
        '''
        Generates the grid cell objects. 
        
        For a |X| x |Y| sized grid, |X| x |Y| objects to represent each grid cell are created. 
        pt0pt0, pt1pt0, .... ptxpt0
        pt0pt1, pt1pt1, .... ptxpt1
        ..       ..            ..
        ..       ..            ..
        pt0pty, pt1pty, .... ptxpty


        '''
        self.grid_cell_list = []
        for w in range(self.width) :
            for lane in range(self.num_lanes) :
                self.grid_cell_list.append("pt{}pt{}".format(w, lane))
 

    def generateInitString(self) :
        '''
        Generates the init string in the problem PDDL file
        '''

        initString = "(on A B)(on B C)(on C T)(not (clear B))(not (clear C))(clear A)(clear T)(isblock A)(isblock B)(isblock C)"     
        
        #Solution not found without initialising isblock
        #initString = "(on A B)(on B C)(on C T)(not (clear B))(not (clear C))(clear A)(clear T)"     
       
        return initString


    def generateGoalString(self) :
        '''
        Generates the Goal string in the problem PDDL file
        '''

        #Works even when goal state = init state
        #A on C, B on T
        return "(and (on A C) (not (clear C)) (clear A) (on B T) (clear B))"

        #A on B on C
        #return "(and (on A B) (not (clear B)) (not (clear C)) (on B C) (on C T) (clear A))"
        
        #B on C, A on T, notice soln is found even if we did not mention goal state of A
        #return "(and (on B C) (not (clear C)) (on C T) (on A T))"
        #return "(and (on B C) (not (clear C)) (on C T))"
        #return "(and (on B A) (not (clear A)) (on C T) (on A T) (clear B) (clear C) (clear T))"

        #A on B, C on T, notice solution is found even if we did not mention goal state of C
        #return "(and (on A B) (not (clear B)) (on B T) (on C T))"
        #return "(and (on A B) (not (clear B)) (on B T))"

        #doesn't work when there is no state change
        #return "(and (on B T)(on A T)(on C B)(clear A)(clear C))"


       
    def generateProblemPDDL(self) :
        '''
        Generates the PDDL problem file after the object instances, init state and goal state are added
        '''
        problem_file = open(PDDL_FILE_ABSOLUTE_PATH + self.problem_file_name, "w")
        PDDL_String = self.problem_header + self.object_strings + self.initString + self.goalString + self.addFooter()
        problem_file.write(PDDL_String)
        problem_file.close()


    '''
    Helper Functions 
    '''
    def addHeader(self, name) :
        return "(:" + name + " "


    def addFooter(self) :
        return ") \n"


      

def initializeSystem(env):
    gen = GeneratePDDL_Stationary(env, len(env.lanes), width=env.width, file_name='blocks_world')
    return gen


def generateDomainPDDLFile(gen):
    gen.addDomainHeader("Blocks_World_Problem")
    gen.addTypes(types = {"surface" : None, "block" : "surface", "table" : "surface"})
    gen.addPredicate(name="on", parameters=(("X" , "block"), ("Y", "surface")))
    #For single parameter predicate, impt to remember square bracket
    gen.addPredicate(name="isblock", parameters=[("X" , "block")])
    gen.addPredicate(name="clear", parameters=[("Y" , "surface")], isLastPredicate=True)

    gen.addAction(name="MOVE",
                   parameters=(("K","block"), ("Kfrom","surface"), ("Kto","surface")),
                   precondition_string="(and (clear ?Kto) (clear ?K) (on ?K ?Kfrom) (not (on ?K ?Kto)) (not (= ?K ?Kfrom)) (not (= ?K ?Kto)) (not (= ?Kto ?Kfrom)) )",
                   effect_string="(and (not (on ?K ?Kfrom)) (on ?K ?Kto) (when (isblock ?Kto) (not (clear ?Kto))) (when (isblock ?Kfrom) (clear ?Kfrom)))")

    # gen.generateDomainPDDL()
    pass

def generateProblemPDDLFile(gen):
    gen.addProblemHeader("Blocks_World","Blocks_World_Problem")
    gen.addObjects("block", ["A","B","C"])
    gen.addObjects("table", ["T"], isLastObject=True)
    gen.addInitState()
    gen.addGoalState()
    gen.generateProblemPDDL()
    pass

def runPDDLSolver(gen):
    os.system(FAST_DOWNWARD_DIRECTORY_ABSOLUTE_PATH + 'fast-downward.py ' + PDDL_FILE_ABSOLUTE_PATH + gen.domain_file_name + ' ' + PDDL_FILE_ABSOLUTE_PATH + gen.problem_file_name + ' --search  \"lazy_greedy([ff()], preferred=[ff()])\"')


def delete_files(gen) :
    os.remove(PDDL_FILE_ABSOLUTE_PATH + gen.domain_file_name)
    os.remove(PDDL_FILE_ABSOLUTE_PATH + gen.problem_file_name)
    os.remove('sas_plan')

def simulateSolution(env):
    plan_file = open('sas_plan', 'r')
    print("   Plan   ")
    print("----------")
    for line in plan_file.readlines() :
        print (line)
        if line[0] == '(' :
            action = line.split()[0][1:]
            if action == 'up' :
                env.step(env.actions[0])
            if action == 'down' :
                env.step(env.actions[1])
            if action == 'forward' :
                env.step(env.actions[2])

def generatePlan(env):
    plan_file = open('sas_plan', 'r')
    action_sequence = []
    for line in plan_file.readlines() :
        if line[0] == '(' :
            action = line.split()[0][1:]
            if action == 'up' :
                action_sequence.append(env.actions[0])
            if action == 'down' :
                action_sequence.append(env.actions[1])
            if action == 'forward' :
                action_sequence.append(env.actions[2])
    return action_sequence

def test() :
    env=gym.make('GridDriving-v0', lanes=LANES, width=WIDTH, random_seed=RANDOM_SEED, agent_speed_range=(-1,-1))
    gen = initializeSystem(env)
    generateDomainPDDLFile(gen)
    generateProblemPDDLFile(gen)
    runPDDLSolver(gen)
    simulateSolution(env)

if SUBMISSION :
    from runner.abstracts import Agent
    class PDDLAgent(Agent):
        def initialize(self, params):
            global FAST_DOWNWARD_DIRECTORY_ABSOLUTE_PATH
            FAST_DOWNWARD_DIRECTORY_ABSOLUTE_PATH = params[0]
            self.env = params[1]
            gen = initializeSystem(self.env)
            generateDomainPDDLFile(gen)
            generateProblemPDDLFile(gen)
            runPDDLSolver(gen)
            self.action_plan = generatePlan(self.env)
            self.time_step = 0
            delete_files(gen)

        def step(self, state, *args, **kwargs):
            action = self.action_plan[self.time_step]
            self.time_step +=1
            return action

    def create_agent(test_case_env, *args, **kwargs):
        return PDDLAgent() 
else :
    test()
