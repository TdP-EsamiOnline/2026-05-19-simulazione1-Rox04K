from model.model import Model

myModel = Model()
myModel.creaGrafo(1)

nodi,vertici = myModel.getInfo()
print(nodi)
print(vertici)

infl = myModel.getArtista()
print(infl)

archi = myModel.getArchi()
print(archi)
