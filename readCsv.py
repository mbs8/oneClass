import csv 
from Instance import Instance

# atualiza o array de minimo e maximo de cada um dos parametros
def updateMinMax(row, minArg, maxArg):
    row = [float(i) for i in row]
    if (maxArg == []):
        minArg = list(row)
        maxArg = list(row)
        return minArg, maxArg
    else:
        for i, param in enumerate(row):
            if maxArg[i] < param:
                maxArg[i] = param
            if minArg[i] > param:
                minArg[i] = param
    return minArg, maxArg

# ler do arquivo csv e salva as informacoes nos arrays
def readCsv(file): 
    classes = []
    tests = []
    maxArg = []
    minArg = []

    with open(file) as csvFile:
        csvReader = csv.reader(csvFile, delimiter=',')
        line_count = 0
        for row in csvReader:
            if (row != [] and line_count != 0):
                param = [float(i) for i in row[:len(row)-1]]     
                classification = row[len(row)-1]
                test = Instance(line_count-1, param, classification)
                tests.append(test)
                minArg, maxArg = updateMinMax(row[:len(row)-1], minArg, maxArg)
                if not(classification in classes):
                    classes.append(classification)
            line_count += 1
    
    return (classes, tests, minArg, maxArg)