import csv
import numpy as np
from prettytable import PrettyTable
from prettytable import MSWORD_FRIENDLY
from airtable.airtable import Airtable

#returns a matrix with all values in the dictionary stored in their respective categories
#ex, if we have category fills in index 0 of all values, we will store all index 0 in fills array
#alex will be a matrix where each row is the lists
def fillArr(keys):
    alex = []
    for key,val in data.items():
        keys.append(key)
        for i in range(0, len(val)):
            if len(alex) < len(val):
                alex.insert(i, [val[i]])
            else:
                alex[i].append(val[i])
    return alex;
        
##    for element in times:
##        print(element, end=" ")
        

#returns a matrix with 0's, 1's and -1's based on how they compare to the first value in each row
def fillChart(alex):

    chart = np.zeros((len(data.items()), len(categories)))

    #printChart(chart)

    #lmfao so we need to convert str to int because the user inputs are str and str comparison is different
    #for example, comparing '100' and '85' as strings will give '85' as the larger one bc '8' > '5' from left to right
    for i in range(0, len(alex)):
        for j in range(1, len(alex[0])):
            #print(alex[i][0] + ' ' + alex[i][j])
            if int(alex[i][j]) > int(alex[i][0]):
                chart[j][i] = 1
                #print('pass1')
            elif int(alex[i][j]) < int(alex[i][0]):
                chart[j][i] = -1
                #print('pass2')
            #else: print('pass3')
    print('--------')
    
    return chart

#prints an unformatted chart
def printChart(chart):
    for row in chart:
        for col in row:
            print (col, end=" ")
        print('\n')
    print('---------')

#prints a pretty chart
def printPretty(keys, categories, scoreweight, chart):
    #need to transpose the chart LOL idk why i did it so shit in the beginning
    chart = np.transpose(chart)
    #newchart is a matrix that has empty "objects" that will be filled with strings
    #note the size of newchart, specificallly the cols
    newchart = np.empty([len(chart), len(chart[0])+1], dtype=object)
    #creates a pretty table
    x = PrettyTable()
    #keys needs to insert a blank as the first thing, because categories need to take up the first col
    keys.insert(0, '')
    #setting field names to be the keys
    x.field_names = keys
    #scores is a list that starts with all 0's

    scores = np.zeros([len(newchart[0])], dtype=object)
    #print(scores)

    #replace all 0's, 1's, -1's with the proper symbols
    for i in range(0, len(newchart)):
        newchart[i][0] = categories[i]
        for j in range(1, len(newchart[0])):
            if(chart[i][j-1] == 0):
                newchart[i][j] = '*'
            elif(chart[i][j-1] == 1):
                newchart[i][j] = '+'
            else:
                newchart[i][j] = '-'
        x.add_row(newchart[i])

    countScores(scores, scoreweight, newchart)
    scores[0] = 'Scores'
    x.add_row(scores)

    print('* means no change, + means better soln, - means worse soln')
    #x.set_style(MSWORD_FRIENDLY)
    x.padding_width = 0
    print(x)

#algorithm for counting scores
#if we see a +, then we add with the score weight, else we subtract if it is -
def countScores(scores, scoreweight, newchart):
    for j in range(1, len(newchart[0])):
        for i in range(0, len(newchart)):
            if(newchart[i][j] == '+'):
                scores[j] = int(scores[j]) + scoreweight[i]
            elif(newchart[i][j] == '-'):
                scores[j] = int(scores[j]) - scoreweight[i]
        #print(scores)
    #print(scores)
    

tablename = input("Input name of table (cAsE sENsiTiVE): ")
airtable = Airtable('base_key', tablename, api_key= 'api_key')

#create dictionary, key is solution name, value is list containing recorded data from each category
data = {}

accept = input("Names of Columns to take (cAsE sENsiTiVE): ")

solncol = input("Input name of solution column (cAsE sENsiTiVE): ")

#obtain the weights that the user wants, store them in score weight
scoreweightin = input("Weights of columns (negative values to min, seperate by commas): ")
scoreweight = list(map(int,scoreweightin.split(",")))

categories = []

#fields = [k for k in airtable.get_all()[0]['fields']]

acceptlist = accept.split(',')

for entry in acceptlist:
    categories.append(entry)

for row in airtable.get_all():
    newdata = []
    for entry in acceptlist:
        newdata.append(row['fields'][entry])
    soln = row['fields'][solncol]
    #if the soln is already a key inside data, we want the average value, else we just add the key with value
    if soln in data:
        olddata = list(map(float,data.get(soln)))
        newdata = list(map(float,newdata))
        for i in range(len(olddata)):
            olddata[i] = (olddata[i]+newdata[i])/2
        data[soln] = list(map(str, olddata))
    else:
        data[soln] = newdata

keys = []
alex = fillArr(keys)

chart = fillChart(alex)

printPretty(keys, categories, scoreweight, chart)
