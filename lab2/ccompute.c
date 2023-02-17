/* CS326 Lab 2
   Author: D. Schuurman
   Compute integral of sin(x) 
*/

#include <math.h>
#include <stdio.h>

// Integrate sin(x) from a to b with n steps
double integrate_sin(double a, double b, int n)
{
   int i;
   double dx = (b-a)/(double)n;
   double sum = 0;
   for (i=0; i<n; i++)
      sum += sin(a + i*dx);
   return sum*dx;
}

int main()
{
   double integral;
   integral = integrate_sin(0, 3.14159, 10000000);
   printf("result = %.16f\n", integral);
   return 0;
}
