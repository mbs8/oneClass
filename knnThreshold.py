import math
import operator
from Instance import Instance
from readCsv import readCsv
              
# Retorna a classificação de uma instancia dado um nome de dataset e um k (número de vizinhos)
def knnThreshold(classes, tests, minArg, maxArg, instance, k, threshold): 
    
    for inst in tests:
        if inst.id != instance.id:
            distanceToInstance = instance.euclideanDistance(inst, minArg, maxArg)
            instance.insertDistance(distanceToInstance, inst, k)

    return instance.classify(k, classes), instance.distancesToInstances[0:k]

def measureAccuracy(classes, train, tests, minArg, maxArg, k, threshold):
    hit    = 0                      # numero de acertos em cada teste de crossfold
    accuracy = 0                    # taxa de acurácia

    # calcula todas as distancias para i-esima instancia do conjunto de teste e classifica de acordo com os k vizinhos mais proximos
    for testInstance in tests:
        knnClassification, _ = knnThreshold(classes, train, minArg, maxArg, testInstance, k, threshold)
        if knnClassification == testInstance.classification:
            hit += 1
    
    accuracy += (hit/len(testingSet))
    hit = 0
    
    return ("Accuracy: %.2f%%" % ((accuracy/div) * 100))

def main():
	classes = []
	instances = []
	minArg = []
	maxArg = []
	oneClassDatasets = ["./oneClassDatasets/JM1_software_defect_prediction.csv", "./oneClassDatasets/PC1_software_defect_prediction.csv"]
	testDatasets = ["./testDatasets/testJM1_software_defect_prediction.csv", "./testDatasets/testJM1_software_defect_prediction.csv"]

	for trainDataset in oneClassDatasets:
		classes, instances, minArg, maxArg = readCsv(trainDataset)
	
