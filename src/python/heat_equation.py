#!> Main program
import numpy,sys,os,time,csv
from shutil import copyfile


#================================================================================================================================
#  Initialise OpenCMISS
#================================================================================================================================

# Intialise OpenCMISS-Iron start
from opencmiss.iron import iron
t=time.time()
# Diagnostics
#iron.DiagnosticsSetOn(iron.DiagnosticTypes.IN,[1,2,3,4,5],"Diagnostics",["DOMAIN_MAPPINGS_LOCAL_FROM_GLOBAL_CALCULATE"])
#iron.DiagnosticsSetOn(iron.DiagnosticTypes.ALL,[1,2,3,4,5],"Diagnostics",[""])
#iron.ErrorHandlingModeSet(iron.ErrorHandlingModes.TRAP_ERROR)
#iron.OutputSetOn("Testing")

# Set the OpenCMISS random seed so that we can test this example by using the
# same parallel decomposition.
numberOfRandomSeeds = iron.RandomSeedsSizeGet()
randomSeeds = [0]*numberOfRandomSeeds
randomSeeds[0] = 100
iron.RandomSeedsSet(randomSeeds)

# Get the computational nodes info
#computationEnvironment = iron.ComputationEnvironment()
numberOfComputationalNodes = iron.ComputationalNumberOfNodesGet()
computationalNodeNumber    = iron.ComputationalNodeNumberGet()

#================================================================================================================================
#  Start Program
#================================================================================================================================
 
controlLoopNode             = 0
coordinateSystemUserNumber  = 1
regionUserNumber            = 2
basisUserNumber             = 3
generatedMeshUserNumber     = 4
meshUserNumber              = 5
decompositionUserNumber     = 6
geometricFieldUserNumber    = 7
equationsSetFieldUserNumber = 8
dependentFieldUserNumber    = 9
materialsFieldUserNumber    = 10
equationsSetUserNumber      = 11
problemUserNumber           = 12
sourceFieldUserNumber       = 13
analyticFieldUserNumber     = 14  

#================================================================================================================================
#  Initial Data & Default values
#================================================================================================================================
# Base quantities units for the problem. The base units are SI units and corresponding values for them is 1
Ls  = 1000         # Length      (1000: m -> mm)
Ms  = 1            # Mass        (kg)
Ts  = 1            # Time        (second)
THs = 1            # Temperature (Celcius)

# Derived quantities units
ACs  = Ls/(Ts**2)           # Acceleration
Ns   = Ms*ACs               # Force
Es   = Ns*Ls                # Energy
POs  = Es/Ts                 # Power


# Ks   = Ms*Ls/(Ts**3*THs)    # Thermal conductivity 
RHOs = Ms/(Ls**3)           # Density
# CPs  = Ls**2/(Ts**2*THs)    # Specific heat
# Hs   = Ms/(Ts**3*THs)       # Convection heat transfer coefficient
Ks = POs/(Ls*THs)
CPs = Es/(Ms*THs)
Hs = POs/(Ls**2*THs)

# Set the time parameters
timeIncrement   = 10.0*Ts
startTime       = 0.0*Ts
stopTime  = 121*timeIncrement

# Set the output parameters
DYNAMIC_SOLVER_DIFFUSION_OUTPUT_FREQUENCY = 1

# Set the solver parameters
MAXIMUM_ITERATIONS   = 1000   # default: 100000

Kcond       = 0.42*Ks 
AlphaDiff   = Kcond/(4.0e6*RHOs*CPs)
Ssrc        = 0.0 
Hconv       = 1.68*Hs
Tair        = 10*Ts
#================================================================================================================================
#  Problem Control Panel
#=========================   =======================================================================================================

meshOrigin = [0.0,0.0,0.0]
ProgressDiagnostics = False   # Set to diagnostics

#================================================================================================================================
#  Coordinate System
#================================================================================================================================

if (ProgressDiagnostics):
    print( " == >> COORDINATE SYSTEM << == ")
    
# Start the creation of RC coordinate system    
coordinateSystem = iron.CoordinateSystem()
coordinateSystem.CreateStart(coordinateSystemUserNumber)
coordinateSystem.dimension = 3
coordinateSystem.CreateFinish()

#================================================================================================================================
#  Region
#================================================================================================================================

if (ProgressDiagnostics):
    print( " == >> COORDINATE SYSTEM << == ")

# Start the creation of SPACE region
region = iron.Region()
region.CreateStart(regionUserNumber,iron.WorldRegion)
region.label = "DiffusionRegion"
region.coordinateSystem = coordinateSystem
region.CreateFinish()    

#================================================================================================================================
#  Bases
#================================================================================================================================

if (ProgressDiagnostics):
    print( " == >> BASIS << == ")

# Create a tri-simplex basis
basis = iron.Basis()
basis.CreateStart(basisUserNumber)
basis.type = iron.BasisTypes.SIMPLEX  
basis.numberOfXi = 3	
basis.interpolationXi = [iron.BasisInterpolationSpecifications.LINEAR_SIMPLEX]*3
basis.QuadratureOrderSet(2)

basis.CreateFinish()

#================================================================================================================================
#  Mesh
#================================================================================================================================

if (ProgressDiagnostics):
    print( " == >> MESH << == ")
    
FileName_ele = "input/cylinder_elements.csv"
numberOfNodes    = 11476
numberOfElements = 49243
numberOfLocalNodes = 4
offset = 1 # offset is 1 if nodes and elements number begin from 0, offset for default = 0

# Label for parts
muscleRegionLabel      = 2

muscleElements      = []

mesh = iron.Mesh()
mesh.CreateStart(meshUserNumber,region,3)
mesh.origin = meshOrigin
mesh.NumberOfComponentsSet(1)
mesh.NumberOfElementsSet(numberOfElements)
# Define nodes for the mesh
nodes = iron.Nodes()
nodes.CreateStart(region,numberOfNodes)
nodes.CreateFinish()

meshElements = iron.MeshElements()
meshComponentNumber = 1
meshElements.CreateStart(mesh, meshComponentNumber, basis)


localNodes=[0]*numberOfLocalNodes
elementNumber=0
totalNumberOfElements=1
elementNodes = False

# print( "Elapsed time before reading ele file is: ", time.time()-t)

with open(FileName_ele,'r') as elementscsv:
  reader = csv.reader(elementscsv)
  elementNumber=0
  for row in reader:
      elementNumber=elementNumber+1
      
      for elemIdx in range(numberOfLocalNodes):
        localNodes[elemIdx]=int(row[elemIdx])+1
      muscleElements.append(elementNumber)
      meshElements.NodesSet(elementNumber,localNodes)

# print( "Elapsed time after reading ele file is: ", time.time()-t)

meshElements.CreateFinish()
mesh.CreateFinish()

#================================================================================================================================
#  Decomposition
#================================================================================================================================

if (ProgressDiagnostics):
    print( " == >> MESH DECOMPOSITION << == ")

# Create a decomposition for the mesh
decomposition = iron.Decomposition()
decomposition.CreateStart(decompositionUserNumber,mesh)
decomposition.type = iron.DecompositionTypes.CALCULATED
decomposition.numberOfDomains = numberOfComputationalNodes
decomposition.calculateFaces = True  
decomposition.CreateFinish()

#================================================================================================================================
#  Geometric Field
#================================================================================================================================

if (ProgressDiagnostics):
    print( " == >> GEOMETRIC FIELD << == ")
     
geometricField = iron.Field()
geometricField.CreateStart(geometricFieldUserNumber,region)
geometricField.meshDecomposition = decomposition
geometricField.ComponentMeshComponentSet(iron.FieldVariableTypes.U,1,1)
geometricField.ComponentMeshComponentSet(iron.FieldVariableTypes.U,2,1)

geometricField.ComponentMeshComponentSet(iron.FieldVariableTypes.U,3,1)

geometricField.CreateFinish()

# Set geometry from the generated mesh

# Get nodes
nodes = iron.Nodes()
region.NodesGet(nodes)
numberOfNodes = nodes.numberOfNodes
print( numberOfNodes)
# Get or calculate geometric Parameters

# print( "Elapsed time before reading node file is: ", time.time()-t)

FileName_node = "input/cylinder_nodes.csv"

boundaryMarker=0
nodeNumber = 0

boundary = []
choppedBoundary=[]
skinMarker = 2
choppedMarker = 3

with open(FileName_node) as nodescsv:
  reader = csv.reader(nodescsv)
  nodeNumber=0
  for row in reader:
      nodeNumber=nodeNumber+1
      x=float(row[0])*10 # times 10 to convert cm to mm. Ls
      y=float(row[1])*10
      z=float(row[2])*10
      boundaryMarker = int(row[3])
      if boundaryMarker == skinMarker:
        boundary.append(nodeNumber)
      elif boundaryMarker == choppedMarker:
        choppedBoundary.append(nodeNumber)
      nodeDomain = decomposition.NodeDomainGet(nodeNumber,1)
      if nodeDomain == computationalNodeNumber:
        geometricField.ParameterSetUpdateNodeDP(iron.FieldVariableTypes.U,iron.FieldParameterSetTypes.VALUES,1,1,
        nodeNumber,1,x)
        geometricField.ParameterSetUpdateNodeDP(iron.FieldVariableTypes.U,iron.FieldParameterSetTypes.VALUES,1,1,
        nodeNumber,2,y)
        geometricField.ParameterSetUpdateNodeDP(iron.FieldVariableTypes.U,iron.FieldParameterSetTypes.VALUES,1,1,
        nodeNumber,3,z)

# print( "Elapsed time after reading node file is: ", time.time()-t)

# Update the geometric field
geometricField.ParameterSetUpdateStart(iron.FieldVariableTypes.U,iron.FieldParameterSetTypes.VALUES)
geometricField.ParameterSetUpdateFinish(iron.FieldVariableTypes.U,iron.FieldParameterSetTypes.VALUES)

#================================================================================================================================
#  Equations Sets
#================================================================================================================================

if (ProgressDiagnostics):
    print( " == >> EQUATIONS SET << == ")

# Create standard Diffusion equations set
equationsSetField = iron.Field()
equationsSet = iron.EquationsSet()
equationsSetSpecification = [iron.EquationsSetClasses.CLASSICAL_FIELD,
        iron.EquationsSetTypes.DIFFUSION_EQUATION,
        iron.EquationsSetSubtypes.CONSTANT_SOURCE_DIFFUSION]
equationsSet.CreateStart(equationsSetUserNumber,region,geometricField,
        equationsSetSpecification,equationsSetFieldUserNumber,equationsSetField)
equationsSet.CreateFinish()

#================================================================================================================================
#  Dependent Field
#================================================================================================================================

if (ProgressDiagnostics):
    print( " == >> DEPENDENT FIELD << == ")
    
# Create dependent field
dependentField = iron.Field()
equationsSet.DependentCreateStart(dependentFieldUserNumber,dependentField)
dependentField.DOFOrderTypeSet(iron.FieldVariableTypes.U,iron.FieldDOFOrderTypes.SEPARATED)
dependentField.DOFOrderTypeSet(iron.FieldVariableTypes.DELUDELN,iron.FieldDOFOrderTypes.SEPARATED)
equationsSet.DependentCreateFinish()

# Initialise dependent field
dependentField.ComponentValuesInitialise(iron.FieldVariableTypes.U,iron.FieldParameterSetTypes.VALUES,1,37.0*THs)

dependentField.ParameterSetUpdateStart(iron.FieldVariableTypes.U,iron.FieldParameterSetTypes.VALUES)
dependentField.ParameterSetUpdateFinish(iron.FieldVariableTypes.U,iron.FieldParameterSetTypes.VALUES)

#================================================================================================================================
#  Materials Field
#================================================================================================================================
    
if (ProgressDiagnostics):
    print( " == >> MATERIALS FIELD << == ")

materialsField = iron.Field()
equationsSet.MaterialsCreateStart(materialsFieldUserNumber,materialsField)
equationsSet.MaterialsCreateFinish()

for elementNumber in muscleElements:
    elementDomain = decomposition.ElementDomainGet(elementNumber)
    if elementDomain == computationalNodeNumber:
      materialsField.ParameterSetUpdateElement(iron.FieldVariableTypes.U,iron.FieldParameterSetTypes.VALUES, 
  elementNumber,1, AlphaDiff) #0.42*1e-3
      materialsField.ParameterSetUpdateElement(iron.FieldVariableTypes.U,iron.FieldParameterSetTypes.VALUES, 
  elementNumber,2, AlphaDiff)
      materialsField.ParameterSetUpdateElement(iron.FieldVariableTypes.U,iron.FieldParameterSetTypes.VALUES, 
  elementNumber,3, AlphaDiff)


materialsField.ParameterSetUpdateStart(iron.FieldVariableTypes.U,iron.FieldParameterSetTypes.VALUES)
materialsField.ParameterSetUpdateFinish(iron.FieldVariableTypes.U,iron.FieldParameterSetTypes.VALUES)

#================================================================================================================================
#  Source Field
#================================================================================================================================
  
if (ProgressDiagnostics):
    print( " == >> SOURCE FIELD << == ")

sourceField = iron.Field()
equationsSet.SourceCreateStart(sourceFieldUserNumber,sourceField)
equationsSet.SourceCreateFinish()  

for elementNumber in muscleElements:
    elementDomain = decomposition.ElementDomainGet(elementNumber)
    if elementDomain == computationalNodeNumber:
      sourceField.ParameterSetUpdateElement(iron.FieldVariableTypes.U,iron.FieldParameterSetTypes.VALUES,elementNumber,1,0.0*THs/Ts)

sourceField.ParameterSetUpdateStart(iron.FieldVariableTypes.U,iron.FieldParameterSetTypes.VALUES)
sourceField.ParameterSetUpdateFinish(iron.FieldVariableTypes.U,iron.FieldParameterSetTypes.VALUES)
#================================================================================================================================
#  Equations
#================================================================================================================================

if (ProgressDiagnostics):
    print( " == >> EQUATIONS << == ")

# Create equations
equations = iron.Equations()
equationsSet.EquationsCreateStart(equations)
equations.sparsityType = iron.EquationsSparsityTypes.SPARSE
equations.outputType = iron.EquationsOutputTypes.NONE
equationsSet.EquationsCreateFinish()

#================================================================================================================================
#  Problems
#================================================================================================================================

if (ProgressDiagnostics):
    print( " == >> PROBLEM << == ")

# Create diffusion problem
problem = iron.Problem()
problemSpecification = [iron.ProblemClasses.CLASSICAL_FIELD,
        iron.ProblemTypes.DIFFUSION_EQUATION,
        iron.ProblemSubtypes.LINEAR_SOURCE_DIFFUSION] 
problem.CreateStart(problemUserNumber, problemSpecification)
problem.CreateFinish()

#================================================================================================================================
#  Control Loops
#================================================================================================================================

if (ProgressDiagnostics):
    print( " == >> PROBLEM CONTROL LOOP << == ")

# Create control loops
problem.ControlLoopCreateStart()
TimeLoop = iron.ControlLoop()
problem.ControlLoopGet([iron.ControlLoopIdentifiers.NODE],TimeLoop)
TimeLoop.LabelSet('Time Loop')
TimeLoop.TimesSet(startTime,stopTime,timeIncrement)
TimeLoop.TimeOutputSet(DYNAMIC_SOLVER_DIFFUSION_OUTPUT_FREQUENCY)
problem.ControlLoopCreateFinish()

#================================================================================================================================
#  Solvers
#================================================================================================================================

# Create problem solver
solver = iron.Solver()
LinearSolver = iron.Solver()
problem.SolversCreateStart()
problem.SolverGet([iron.ControlLoopIdentifiers.NODE],1,solver)
solver.DynamicLinearSolverGet(LinearSolver)
problem.SolversCreateFinish()

#================================================================================================================================
#  Solver Equations
#================================================================================================================================

if (ProgressDiagnostics):
    print( " == >> SOLVER EQUATIONS << == ")

# Create solver equations and add equations set to solver equations
solver = iron.Solver()
solverEquations = iron.SolverEquations()
problem.SolverEquationsCreateStart()
problem.SolverGet([iron.ControlLoopIdentifiers.NODE],1,solver)
solver.SolverEquationsGet(solverEquations)
solverEquations.sparsityType = iron.SolverEquationsSparsityTypes.SPARSE
equationsSetIndex = solverEquations.EquationsSetAdd(equationsSet)
problem.SolverEquationsCreateFinish()

#================================================================================================================================
#  Boundary Conditions
#================================================================================================================================

if (ProgressDiagnostics):
    print( " == >> BOUNDARY CONDITIONS << == ")

boundaryConditions = iron.BoundaryConditions()
solverEquations.BoundaryConditionsCreateStart(boundaryConditions)

nodes = iron.Nodes()
region.NodesGet(nodes)

#q=alpha*gradT.n which alpha=sigma/rhoC.
# So for Robin BCs you need to pass h/rhoC and q_h/rhoC.

for nodeNumber in boundary:
  nodeDomain = decomposition.NodeDomainGet(nodeNumber,1)
  if nodeDomain == computationalNodeNumber:

    boundaryConditions.SetNode(dependentField,iron.FieldVariableTypes.DELUDELN,1,1,nodeNumber,1,
      iron.BoundaryConditionsTypes.ROBIN,[(1.68*Hs)/(4.0e6*RHOs*CPs),(16.8*Hs*THs)/(4.0e6*RHOs*CPs)]) 
  
for nodeNumber in choppedBoundary:
  nodeDomain = decomposition.NodeDomainGet(nodeNumber,1)
  if nodeDomain == computationalNodeNumber:
    boundaryConditions.SetNode(dependentField,iron.FieldVariableTypes.DELUDELN,1,1,nodeNumber,1,
      iron.BoundaryConditionsTypes.NEUMANN_POINT,[0.0*THs/Ls])

dependentField.ParameterSetUpdateStart(iron.FieldVariableTypes.U,iron.FieldParameterSetTypes.VALUES)
dependentField.ParameterSetUpdateFinish(iron.FieldVariableTypes.U,iron.FieldParameterSetTypes.VALUES)

solverEquations.BoundaryConditionsCreateFinish()

#================================================================================================================================
#  Run Solvers
#================================================================================================================================

print( "Solving problem...")
start = time.time()
# Solve the problem
problem.Solve()
end = time.time()
elapsed = end - start
print( "Total Number of Elements = %d " %totalNumberOfElements)
print( "Total Number of nodes = %d " %numberOfNodes)
print( "Calculation Time = %3.4f" %elapsed)
print( "Problem solved!")
print( "#")


iron.Finalise() 

