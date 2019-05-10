import math
import operator

class Instance:
    def __init__(self, id, params, classification):
        self.id = id
        self.params = params
        self.classification = classification
        self.distancesToInstances = []

    # Calcula a distancia para determinada instancia usando os vetores de min e max 
    # para a normalização do cálculo da distância
    def euclideanDistance(self, datasetInstance, minArg, maxArg):
        distance = 0
        for i, param in enumerate(datasetInstance.params):
            distance += ((param - self.params[i]) ** 2) / (maxArg[i] - minArg[i])
        distance = math.sqrt(distance)       
        return distance
    
    # Insere ordenadamente no array de distancias a distancia para determinada instancia
    def insertDistance(self, distanceToInstance, instance, k): 
        distInst = (distanceToInstance, instance)
        if self.distancesToInstances == []:
            self.distancesToInstances.append(distInst)
        else:
            for i, (dist, _) in enumerate(self.distancesToInstances):
                if dist > distanceToInstance:
                    self.distancesToInstances.insert(i, distInst)
                    size = len(self.distancesToInstances)
                    if size > k:
                        del(self.distancesToInstances[size-1])
                    return
            if len(self.distancesToInstances) < k:
                self.distancesToInstances.append(distInst)
                
    # Retorna a classe pertencente da instancia
    def classify(self, numNeighbor, classes):
        dictClass = {}

        print(self.distancesToInstances[0][0])

        for clas in classes:
            dictClass[clas] = 0

        for i in range(0, numNeighbor):
            classification = self.distancesToInstances[i][1].classification
            dictClass[classification] += 1

        return max(dictClass.items(), key=operator.itemgetter(1))[0]