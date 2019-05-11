import math
import operator
import time
from Instance import Instance
from readCsv import readCsv 		

# Calcula o threshold (fronteira)
def calculateThreshold(instances, minArg, maxArg):
	threshold = 0
	centroid = Instance(-1, [], instances[0].classification)
	distances = []
	alpha = 0.45

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
		distances.append(distance)
		threshold += distance
	
	threshold = (threshold / len(instances)) * alpha

	return threshold, centroid

# Calcula os vizinhos mais próximos de cada uma das instancias do conjunto de dados
def knnClassif(classes, centroid, minArg, maxArg, instance, k, threshold): 
	distanceToInstance = instance.euclideanDistance(centroid, minArg, maxArg)
	instance.insertDistance(distanceToInstance, centroid, k)

	return instance.classify(k, classes, threshold)


def measureAccuracy(classes, centroid, tests, minArg, maxArg, k, threshold):
	hit    = 0                      # numero de acertos em cada teste de crossfold
	accuracy = 0                    # taxa de acurácia
	size = len(tests)

	# calcula todas as distancias para i-esima instancia do conjunto de teste e classifica de acordo com os k vizinhos mais proximos
	print("threshold: " + str(threshold))
	for i, testInstance in enumerate(tests):
		knnClassification = knnClassif(classes, centroid, minArg, maxArg, testInstance, k, threshold)
		#print(testInstance.distancesToInstances[0])
		if knnClassification == testInstance.classification:
			#print(testInstance.distancesToInstances[0][0])
			hit += 1

	accuracy += (hit/len(tests))
	
	return ("Accuracy: %.2f%%\n" % (accuracy * 100))

def knnThreshold():
	classes = []
	instances = []
	minArg = []
	maxArg = []
	kValues = [1]
	oneClassDatasets = ["./oneClassDatasets/JM1_software_defect_prediction.csv", "./oneClassDatasets/PC1_software_defect_prediction.csv"]
	testDatasets = ["./testDatasets/testJM1_software_defect_prediction.csv", "./testDatasets/testJM1_software_defect_prediction.csv"]

	for i, trainDataset in enumerate(oneClassDatasets):
		
		datasetName = trainDataset.split("/")
		print("\nDataset: " + datasetName[2])
		
		startTime = time.time()
		classes, instances, minArg, maxArg = readCsv(trainDataset)
		_, testInstances, _, _ = readCsv(testDatasets[i])
		threshold, centroid = calculateThreshold(instances, minArg, maxArg)
		print(measureAccuracy(classes, centroid, testInstances, minArg, maxArg, 1, threshold))
		print("Tempo gasto: " + str(time.time() - startTime))
		print("------------------------------------------------------------------------------------")

knnThreshold()