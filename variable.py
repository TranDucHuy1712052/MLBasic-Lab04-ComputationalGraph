import math

## "Node" in graph
class Variable:

    count = 0                   ## total count of variables

    def __init__(self, name):
        self.name = name        ## Names should be unique
        self.val = None
        self.next = []          ## Other vars that this var send its value to (all different)
        self.prev = []          ## Other vars that send value to this var (all different)
        Variable.count += 1

    ## abstract - each concrete Variable must override!
    ## calculate this variable's value by its own function
    def Calculate(self):
        return self.val

    ## get its value, or calculate it if value not found yet
    def Value(self):
        if (self.val is None):
            self.val = self.Calculate()
        return self.val

    ## differentate its function by another var. Using chain rule
    def Derive(self, var):
        if (var is self):
            return 1.0
        else:
            sum = 0.0
            for v in self.prev:
                sum += self.InnerDerive(v) * v.Derive(var)          #chain rule
            return sum

    ## abstract - each concrete Variable must override!
    def InnerDerive(self, var):
        return 1.0

    ## print info about this variable
    def Print(self):
        print(self.name, " = ", self.val, end='\n')
    
    ## set next variable of this one, add it to "next" list
    def AddNextVariable(self, var):
        self.next.append(var)
        var.prev.append(self)


## ==========================================
## CONCRETE VARIABLES
## ==========================================

## store value only, also called "initial variable"
class PlaceholderVar(Variable):

    __count = 0                       ## count the number of placeholder, for naming purpose.

    def __init__(self, name, val = 0):
        super().__init__(name)
        self.name = name
        self.val = val
        PlaceholderVar.__count += 1

    def SetValue(self, val):
        self.val = val

    def Calculate(self):
        return self.val

    def Derive(self, var):
        if (var is self):
            return 1.0
        else: 
            return 0.0

    def PrintToScreen(self):
        print(self.name, " = ", self.val)

## ===== MULTIPLE VARIABLES OPERATOR =====

## add var
## f(x1,x2,...,xn) = (x1 + x2 + ... + xn) (xi != xj)
class AddVar(Variable):
    def __init__(self, name, vars):
        super().__init__(name)
        for var in vars:
            var.AddNextVariable(self)
        self.name = name

    def Calculate(self):
        sum = 0.0
        for var in self.prev:
            sum += var.Value()
        return sum

    def InnerDerive(self, var):
        return 1                    ## df/dvar = 1, with all var


## multiply var
## f(x1, x2, ..., xn) = (x1 * x2 * ... * xn) (xi != xj)
class MulVar(Variable):
    def __init__(self, name, vars):
        super().__init__(name)
        for var in vars:
            var.AddNextVariable(self) 
        self.name = name

    def Calculate(self):
        product = 1.0
        for var in self.prev:
            product *= var.Value()
        return product

    def InnerDerive(self, var):
        return ( self.Value() / var.Value() )


## ========= SINGLE VARIABLE OPERATOR ==========

## minus var
## f(x) = -x
class MinusVar(Variable):
    def __init__(self,name, var):
        super().__init__(name)
        var.AddNextVariable(self)
        self.name = name

    def Calculate(self):
        return -1.0*self.prev[0].Value()

    def InnerDerive(self, var):
        return -1.0


## divide var => inverse
## f(x) = 1/x
class InverseVar(Variable):
    def __init__(self, name, var):
        super().__init__(name)
        var.AddNextVariable(self)
        self.name = name

    def Calculate(self):
        return 1/self.prev[0].Value()

    def InnerDerive(self, var):
        tmp = self.prev[0].Value()
        return -1.0 / (tmp * tmp)


## square var : f(x) = x^2
class SquareVar(Variable):
    def __init__(self, name, var):
        super().__init__(name)
        var.AddNextVariable(self)
        self.name = name

    def Calculate(self):
        tmp = self.prev[0].Value()
        return tmp*tmp

    def InnerDerive(self, var):
        tmp = self.prev[0].Value()
        return 2*tmp


## exp var: f(x) = exp(x) = e^x
class ExpVar(Variable):
    def __init__(self, name, var):
        super().__init__(name)
        var.AddNextVariable(self)
        self.name = name

    def Calculate(self):
        return math.exp(self.prev[0].Value())

    def InnerDerive(self, var):
        return self.Value()             # d(e^x)/dx = e^x


## cos var : f(x) = cos(x)
class CosineVar(Variable):
    def __init__(self, name, var):
        super().__init__(name)
        var.AddNextVariable(self)
        self.name = name

    def Calculate(self):
        return math.cos(self.prev[0].Value())

    def InnerDerive(self, var):
        return -1.0*math.sin(self.prev[0].Value())

## sin var : f(x) = sin(x)
class SineVar(Variable):
    def __init__(self, name, var):
        super().__init__(name)
        var.AddNextVariable(self)
        self.name = name

    def Calculate(self):
        return math.sin(self.prev[0].Value())
    
    def InnerDerive(self, var):
        return math.cos(self.prev[0].Value())

## tan var : f(x) = tan(x)
class TanVar(Variable):
    def __init__(self, name, var):
        super().__init__(name)
        var.AddNextVariable(self)
        self.name = name

    def Calculate(self):
        return math.tan(self.prev[0].Value())

    def InnerDerive(self, var):
       # return 1.0/ math.pow( math.cos(self.prev[0].Value()), 2)
        return 1 + math.pow(self.Value(), 2)


## sigmoid var : f(x) = sigmoid(x) 
class SigmoidVar(Variable):
    def __init__(self, name, var):
        super().__init__(name)
        var.AddNextVariable(self)
        self.name = name

    def Calculate(self):
        return 1.0/(1.0 + math.exp(-self.prev[0].Value()))

    def InnerDerive(self, var):
        tmp = self.Value()
        return tmp*(1-tmp)


## ===========================================
## =========== DOUBLE VAR OPERATORS  =============
## ===========================================


## Power var : f(x,n) = x^n
## prev[0] = x, prev[1] = n
class PowerVar(Variable):
    def __init__(self, name, baseVar, powerVar):
        super().__init__(name)
        self.baseVar = baseVar
        self.powerVar = powerVar
        self.prev = [baseVar, powerVar]
        self.name = name

    def Calculate(self):
        return math.pow(self.baseVar.Value(), self.powerVar.Value())

    def InnerDerive(self, var):
        p = self.powerVar.Value()
        b = self.baseVar.Value()
        if (var is self.baseVar):
            return p * (math.pow(b, p-1))
        else:
            return self.Value() * math.log(b)