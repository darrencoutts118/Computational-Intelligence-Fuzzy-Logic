#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Darren Coutts
#
# Created:     01/11/2015
# Copyright:   (c) Darren Coutts 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import sys;
import re;
import math;


def main():

    print ("a = ");
    a = sys.stdin.readline();

    print ("b = ");
    b = sys.stdin.readline();

    print ("alpha = ");
    c = sys.stdin.readline();

    print ("beta = ");
    d = sys.stdin.readline();


    x = Curve(a,b,c,d,"Name");

    print ("Input = ");

    val = sys.stdin.readline();

    print("Membership = ",)
    print( x.membershipOf(val));


    pass

# This is a class which is used to store data on the memebership curves.
#
# The method membershipOf takes an integer value, and computes that values
# memebership of the curve.
class Curve:

    name = "";

    def __init__(self, a, b, alpha, beta, name):
        self.a = int(a);
        self.b = int(b);
        self.alpha = int(alpha);
        self.beta = int(beta);
        self.name = name;

    def getName():
        return self.name;

    def membershipOf( self, value ):

        value = int(value);

        if(value < (self.a - self.alpha)):
            return 0;
        elif(value in range (self.a - self.alpha, self.a)):
            return (value - self.a + self.alpha) / self.alpha;
        elif(value in range(self.a,self.b)):
            return 1;
        elif(value in range(self.b, self.b+self.beta)):
            return (self.b + self.beta - value) / self.beta;
        elif(value > (self.b + self.beta)):
            return 0;

        return;


if __name__ == '__main__':
    main()

