class Problem_Params:
    def __init__(self):
        self.timeIncrement = 10.0
        self.startTime = 0.0
        self.timeSteps = 11
        self.diffusionOutputFrequency = 10
        self.conductivity = 0.42
        self.rhoC = 4.0e6 
        self.source = 0.0
        self.convection = 1.68
        self.Tair = 10.0
        self.Tinit = 37.0
        self.tissueElementsFile = "input/cylinder_elements.csv"
        self.tissueNodesFile = "input/cylinder_nodes.csv"
        self.numberOfNodes = 11476
        self.numberOfElements = 49243


    def time_increment_set(self, value):
        self.timeIncrement = value

    def start_time_set(self,value):
        self.startTime = value

    def time_steps_set(self,value):
        self.timeSteps = value

    def output_frequency_set(self,value):
        self.diffusionOutputFrequency = value

    def conductivity_set(self,value):
        self.conductivity = value

    def rhoC_set(self,value):
        self.rhoC = value

    def source_set(self,value):
        self.source = value

    def convection_set(self,value):
        self.convection = value

    def tair_set(self,value):
        self.Tair = value

    def tinit_set(self,value):
        self.Tinit = value

    def tissue_elements_file_set(self,path):
        self.tissueElementsFile = path

    def tissue_nodes_file_set(self,path):
        self.tissueNodesFile = path

    def number_of_nodes_set(self,value):
        self.numberOfNodes = value

    def number_of_elements_set(self,value):
        self.numberOfElements = value
