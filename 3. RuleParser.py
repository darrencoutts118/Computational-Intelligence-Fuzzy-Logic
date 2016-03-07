#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Darren Coutts
#
# Created:     02/11/2015
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

def main():

    print ("Please enter the Rule you wish to parse.");
    rule = sys.stdin.readline();

    parsed = parseRule(rule);
    print ("The Rule has been parsed as.")
    print(parsed);

    pass

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


if __name__ == '__main__':
    main()
