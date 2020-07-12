# 1712052 - Tran Duc Huy - 17TN
# Run this file to test

import graphBuilder

print("Demo Computational Graph")

## demo
builder = graphBuilder.GraphBuilder()

print("1st example : f(x,y) = (x^2 * y) + cos(x + y), values = [0.8,3.7]")
builder.FirstSample()

print("2nd example : f(x,y) = x + xy, values = [1.5,6]")
builder.SecondSample()

print("3rd example : f = x^(sigmoid(y)), values = [7,9]")
builder.ThirdSample()

print("4rd example : f(a,x,y,z) = (axy)/z + x^y + tan(-z), values = [3,2,3,5]")
builder.FourthSample()