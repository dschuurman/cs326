# CS326 Lab 2
# Compute integral of sin(x)

from math import sin

def integrate_sin(a,b,n):
   ''' Integrate sin(x) from a to b with n steps
   '''
   dx = (b-a)/n
   sum = 0
   for i in range(0,n):
      sum += sin(a+i*dx)
   return sum*dx

integral = integrate_sin(0, 3.14159, 10000000)
print(f'result = {integral}')
