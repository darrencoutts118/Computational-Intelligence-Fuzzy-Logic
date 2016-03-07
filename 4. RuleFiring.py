#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Darren Coutts
#
# Created:     05/10/2015
# Copyright:   (c) Darren Coutts 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import sys;
import re;
import math;

expression = "Rule (?P<RuleID>[0-9]*) if the (?P<Condition1>[0-1A-Za-z_]+) is (?P<Value1>[0-1A-Za-z_]+) ((?P<Conjunctive>and|or) the (?P<Condition2>[0-1A-Za-z_]+) is (?P<Value2>[0-1A-Za-z_]+) )*then the (?P<Output>[0-1A-Za-z]+) will be (?P<Value>[0-1A-Za-z]+)";
ruleExpression = re.compile(expression, re.MULTILINE | re.IGNORECASE);

expression2 = " the (?P<Condition>[0-1A-Za-z_]+) is (?P<Value>[0-1A-Za-z_]+) ";
ruleExpantionExpression = re.compile(expression2, re.MULTILINE | re.IGNORECASE);

expression3 = "(?P<Condition>[0-1A-Za-z_]+) = (?P<Value>[0-1A-Za-z_]+)";
realWorldExpression = re.compile(expression3, re.MULTILINE | re.IGNORECASE);

inputfile = "";

def main():

    print("Please enter the rule file name.");

    inputfile = sys.stdin.readline();
    data = readFile(inputfile.replace("\n",""));

    Name = data["RuleBaseName"];
    Rules = data["Rules"];
    RealWorld = data["RealWorld"];
    Curves = data["Curves"];

    CompRules = [];

    print ( "Loading the " + Name + " Rule Base" )

    #print(Curves);

    #print(RealWorld);

    AllMemeberships = {};

    for i in range(0,len(RealWorld)):
        Var = RealWorld[i]["name"];
        Value = RealWorld[i]["value"];

        MemebershipGoup = {};

        for j in range(0, len(Curves.get(Var))):
            MemebershipGoup[ Curves.get(Var)[j].name ] =  str(Curves.get(Var)[j].membershipOf(Value));
            #print ( "Searching for " + Var + "'s memebership in the group " + Curves.get(Var)[j].name + ". Value found as: " +  str(Curves.get(Var)[j].membershipOf(Value)));

        AllMemeberships[Var] = MemebershipGoup;

        #print(Curves.get(Var));

    #print (AllMemeberships);

    processRules(Rules,AllMemeberships,Curves);

    return;
    pass;


def processRules(Rules, FuzzyValues, Curves):

    mappings = {};

    for i in range(0,len(Rules)):
        rule = parseRule(Rules[i]);



        conditions = rule["Conditions"];
        conditionValues = {};
        conditionValueInts = [];


        for k,v in conditions.items():
            conditionValues[k] = FuzzyValues[k][v]
            conditionValueInts.append(FuzzyValues[k][v]);

        if(rule['Conjunction'] == "and"):
            totalValue = min(conditionValueInts);
        elif(rule['Conjunction'] == "or"):
            totalValue = max(conditionValueInts);
        else:
            totalValue = conditionValueInts[0];


        totalValue = float(totalValue);

        outputValue = (next (iter (rule["Output"].values())));
        outputKey = (next (iter (rule["Output"].keys())));
        if(outputValue in mappings.keys()):
            mappings[outputValue].append(totalValue);
        else:
            mappings[outputValue] = [totalValue]

    finalMappings = {}
    curvesToCheck = [];

    for k,v in mappings.items():
        maximum = max(v);
        if(maximum != 0.0):
            finalMappings[k] = maximum;
            curvesToCheck.append(k);


    print(finalMappings);



def parseRule(rule):

    store = {}
    s = re.search(ruleExpression,rule)

    if(s is None):
        print("This rule does not compute");
        return False;

    ruleID = s.group("RuleID");
    conditions = {s.group(2):s.group(3)}

    findAll = re.findall(ruleExpression,rule);

    if(s.group("Conjunctive")):
        conditions[s.group("Condition2")] = s.group("Value2")

        conjunctive = s.group("Conjunctive");
        allconditions = rule.split(conjunctive);

        for i in range(1,len(allconditions)-1):
            search = re.match(ruleExpantionExpression,allconditions[i]);
            if search is not None:
                conditions[search.group("Condition")] = search.group("Value")

    store = {"ID": ruleID, "Conditions":conditions, "Conjunction":s.group("Conjunctive"), "Output":{s.group("Output"):s.group("Value")}}

    return (store);

# This function reads the rulebase file, and processes it into the parts that
# the remainder of the application will need to run successfully.

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

            y = Curve(x[1],x[2],x[3],x[4],x[0]);

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

