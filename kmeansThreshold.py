import math
import operator
import time
from Instance import Instance
from readCsv import readCsv 		

# Calcula o threshold (fronteira)
def calculateThreshold(instances, minArg, maxArg):
	threshold = 0
	centroid = Instance(-1, [], instances[0].classification)

	for instance in instances: 
		for i, param in enumerate(instance.params):
			if (len(centroid.params) <= i):
				centroid.params.append(param)
			else:
				centroid.params[i] += param
	
	for i, elem in enumerate(centroid.params):
		centroid.params[i] = centroid.params[i] / len(instances)

	for instance in instances:
		distance = centroid.euclideanDistance(instance, minArg, maxArg)
		threshold += distance
	
	threshold = threshold / len(instances)

	return threshold, centroid

# Calcula os vizinhos mais próximos de cada uma das instancias do conjunto de dados
def knnClassif(classes, centroid, minArg, maxArg, instance, k, threshold): 
	distanceToInstance = instance.euclideanDistance(centroid, minArg, maxArg)
	instance.insertDistance(distanceToInstance, centroid, k)

	return instance.classify(k, classes, threshold)


def measureAccuracy(classes, centroid, tests, minArg, maxArg, k, threshold):
	size = len(tests)						# Tamanho do conjunto de dados
	trueNegative = 0						# Número de verdadeiros negativos 
	truePositive = 0						# Número verdadeiros positivos 
	falseNegative = 0						# Número de falsos negativos
	falsePositive = 0						# Número de falsos positivos

	# calcula todas as distancias para i-esima instancia do conjunto de teste e classifica de acordo com os k vizinhos mais proximos
	for i, testInstance in enumerate(tests):
		knnClassification = knnClassif(classes, centroid, minArg, maxArg, testInstance, k, threshold)
		
		# Conta o numero de instancias, negativos verdadeiros, positivos verdadeiros, falso negativos e falsos positivos do dataset
		if knnClassification == testInstance.classification:
			if knnClassification == "true":
				trueNegative += 1
			else:
				truePositive += 1
		else:
			if knnClassification == "true":
				falseNegative += 1
			else:
				falsePositive += 1
		
	# calcula os parametros de medida de acurácia
	precision = truePositive / (truePositive + falsePositive)
	recall = truePositive / (truePositive + falseNegative)
	f_measure = (2 * truePositive) / ((2 * truePositive) + falsePositive + falseNegative)

	print("Recall: %.2f%%" % (recall * 100))
	print("Precision: %.2f%%" % (precision * 100))
	print("F1-measure: %.2f%%\n" % (f_measure * 100))
	

def kmeansThreshold():
	classes = []
	instances = []
	minArg = []
	maxArg = []
	kValues = [1]
	oneClassDatasets = ["./oneClassDatasets/JM1_software_defect_prediction.csv", "./oneClassDatasets/PC1_software_defect_prediction.csv"]
	testDatasets = ["./testDatasets/testJM1_software_defect_prediction.csv", "./testDatasets/testPC1_software_defect_prediction.csv"]

	for i, trainDataset in enumerate(oneClassDatasets):
		
		datasetName = trainDataset.split("/")
		print("\nDataset: " + datasetName[2] + "\n")
		
		startTime = time.time()
		classes, instances, minArg, maxArg = readCsv(trainDataset)
		_, testInstances, _, _ = readCsv(testDatasets[i])
		threshold, centroid = calculateThreshold(instances, minArg, maxArg)
		measureAccuracy(classes, centroid, testInstances, minArg, maxArg, 1, threshold)
		print("Tempo gasto: " + str(time.time() - startTime))
		print("------------------------------------------------------------------------------------")

kmeansThreshold()