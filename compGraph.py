import variable

class ComputationalGraph:

    def __init__(self):
        self.initVars = []
        self.otherVars = []
        self.endVar = None                                # last var in the graph

    def SetVariables(self, initVars, otherVars, endVar):
        self.initVars = initVars
        self.otherVars = otherVars
        self.endVar = endVar

    ## Calculate the outputs
    ## @params: values = list of values for each initial var
    def CalculateOutput(self, values):
        for i in range(len(values)):
            self.initVars[i].SetValue(values[i])
        ## Call the calculation from end var
        return self.endVar.Value()


    def PrintValues(self):
        for var in self.initVars:
            var.Print()
        for var in self.otherVars:
            var.Print()
        self.endVar.Print()

    def PrintDerivaties(self, var):
        d = self.endVar.Derive(var)
        print("d", self.endVar.name, "/d", var.name, " = ", str(d))

    ## print all derivaties of this function with respect to each initial variable
    def PrintAllDerivaties(self):
        for var in self.initVars:
            self.PrintDerivaties(var)