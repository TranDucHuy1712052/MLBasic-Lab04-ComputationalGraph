import compGraph
import variable

class GraphBuilder:
    def __init__(self):
       self.graph = None


    ## first sample to demo
    ## f(x,y) = (x^2 * y) + cos(x + y) = h2 + h4
    ## h = x^2, h2 = (h * y), h3 = (x + y), h4 = cos(h3)
    def FirstSample(self):
        graph = compGraph.ComputationalGraph()

        x = variable.PlaceholderVar("x")
        y = variable.PlaceholderVar("y")

        h = variable.SquareVar("h", x)          # h = x^2
        h2 = variable.MulVar("h2", [h,y])       # h2 = h*y
        h3 = variable.AddVar("h3", [x,y])       # h3 = x + y
        h4 = variable.CosineVar("h4", h3)       # h4 = cos(h3)

        f = variable.AddVar("f", [h2, h4])      # f = h2 + h4

        graph.initVars = [x,y]
        graph.otherVars = [h, h2, h3, h4]
        graph.endVar = f

        graph.CalculateOutput([0.8,3.7])
        graph.PrintValues()
        graph.PrintDerivaties(x)
        graph.PrintDerivaties(y)

    
    # f(x,y) = x + xy
    def SecondSample(self):
        x = variable.PlaceholderVar("x")
        y = variable.PlaceholderVar("y")

        v1 = variable.MulVar("v1", [x,y])
        f = variable.AddVar("f", [x, v1])

        graph2 = compGraph.ComputationalGraph()
        graph2.SetVariables([x,y], [v1], f)

        graph2.CalculateOutput([1.5,6])
        graph2.PrintValues()
        graph2.PrintDerivaties(x)
        graph2.PrintDerivaties(y)

    ## f(x,y) = x^(sig(y))
    def ThirdSample(self):
        x = variable.PlaceholderVar("x")
        y = variable.PlaceholderVar("y")

        v1 = variable.SigmoidVar("v1", y)       # v1 = sigmoid(y)
        f = variable.PowerVar("f", x, v1)       # f = x^v1
        
        graph = compGraph.ComputationalGraph()
        graph.SetVariables([x,y], [v1], f)

        graph.CalculateOutput([7,9])
        graph.PrintValues()
        graph.PrintDerivaties(x)
        graph.PrintDerivaties(y)


    ## f(a,x,y,z) = (axy)/z + x^y + tan(-z)
    def FourthSample(self):
        a = variable.PlaceholderVar("a")
        x = variable.PlaceholderVar("x")
        y = variable.PlaceholderVar("y")
        z = variable.PlaceholderVar("z")

        v1 = variable.InverseVar("v1", z)         # v1 = 1/z  
        vv1 = variable.MulVar("vv1", [a,x,y,v1])     # vv1 = axy*v1

        vv2 = variable.PowerVar("vv2", x, y)        # vv2 = x^y

        v3 = variable.MinusVar("v3", z)             # v3 = -z
        vv3 = variable.TanVar("vv3", v3)              # vv3 = tan(v3)

        f = variable.AddVar("f", [vv1,vv2,vv3])     # f = vv1 + vv2 + vv3

        graph = compGraph.ComputationalGraph()
        graph.SetVariables([a,x,y,z], [v1, vv1, vv2, v3, vv3], f)
        graph.CalculateOutput([3, 2, 3, 5])
        graph.PrintValues()
        graph.PrintAllDerivaties()