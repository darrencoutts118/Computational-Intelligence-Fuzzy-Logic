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

    print ("Please enter the filename to be processed.");

    inputfile = sys.stdin.readline();
    data = readFile(inputfile.replace("\n",""));

    print(data);

    pass


def readFile(file):

    systemData = open(file, 'r', encoding="ISO-8859-1")
    parts = (re.split(r'\n\n',systemData.read()));

    RuleBaseName = parts[0];
    Rules = parts[1];
    MemberClasses = {};
    RealWorldValues = parts[len(parts)-1];

    data = {};

    for i in range(2,len(parts)-1,2):

        Memeberships = []
        Groups = parts[i+1].split("\n")

        for j in range(0,len(Groups)):
            x = Groups[j].split(" ");

            y = {x[1],x[2],x[3],x[4],x[0]};

            Memeberships.append(y)

        MemberClasses[parts[i].strip()] = Memeberships;


    RealWorldValues = RealWorldValues.split("\n");
    RealWorld = []
    for i in range(0,len(RealWorldValues)):
        x = RealWorldValues[i].split(" = ");
        if x is not None:
            RealWorld.append(dict({"name" : x[0], "value":x[1]}));

    data['RuleBaseName'] = RuleBaseName
    data['Curves'] = MemberClasses;
    data['RealWorld'] = RealWorld;
    data['Rules'] = Rules.split("\n")

    return data;



if __name__ == '__main__':
    main()
