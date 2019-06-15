from guroby import *



modelo = Model('otimizacaoEnergia')


#VARIAVEIS
demanda = []
tempo = []
custo_bomba_ligada = []
acionamento_de_bomba = []
vazao_da_bomba = []
vazao_da_bomba_para_reservatorio=[]
volume_minimo_reservatorio = 1
volume_maximo_reservatorio = 1
volume_do_reservatorio_inicio = 1
volume_do_reservatorio_final_do_periodo_t = 1
fracao_de_t = []
custo_transferir_agua =[]
#a bomba começa desligada
estado_inicial_da_bomba = 0

# VARIAVEIS GUROBI


Yjt = modelo.addVar(vtype = GRB.BINARY, name="Yjt")

#aciona a bomba
ALFAjt = modelo.addVar(vtype = GRB.BINARY, name="alfajt")


#demanda do centro consumidor - no caso da gente vai ser continua
Dkt = modelo.addVars(demanda ,vtype = GRB.CONTINUOUS, name = "Dkt")
# custo para manter a bomba ligada no tempo t
Ctj = modelo.addVars(custo_bomba_ligada,vtype = GRB.CONTINUOUS, name = "Ctj")

SCjt = modelo.addVars(acionamento_de_bomba,vtype = GRB.CONTINUOUS, name = "SCjt")

Vjt = modelo.addVars(vazao_da_bomba,vtype = GRB.CONTINUOUS, name = "Vjt")

Wjlt = modelo.addVars(vazao_da_bomba_para_reservatorio,vtype = GRB.CONTINUOUS, name = "Wjlt")

Hjmin = modelo.addVar(volume_minimo_reservatorio ,vtype = GRB.CONTINUOUS, name = "Hjmin")

Hjmax = modelo.addVar(volume_maximo_reservatorio ,vtype = GRB.CONTINUOUS, name = "Hjmax")

Hjzero = modelo.addVar(volume_do_reservatorio_inicio ,vtype = GRB.CONTINUOUS, name = "Hjzero")

#talvez não use Gama
#Restricao 9
GAMAjlt = modelo.addVars(custo_transferir_agua,vtype = GRB.CONTINUOUS, name = "GAMAjlt")
#Restricao 9
Xjzero = modelo.addVar(estado_inicial_da_bomba ,vtype = GRB.BINARY, name = "Xjzero")

Ijt = modelo.addVar(volume_do_reservatorio_final_do_periodo_t ,vtype = GRB.CONTINUOUS, name = "Ijt")

Xjt = modelo.addVars(fracao_de_t,vtype = GRB.CONTINUOUS, name = "Xjt")


#Objetivo
modelo.setObjective( quicksum(Ctj[t]*Xjt[t] + SCjt[t]*ALFAjt[t]  for t in tempo) , GRB.MINIMIZE) 

# restricao 2 do modelo


# restricao 3 do modelo
modelo.addConstrs(Xjt[t]<=Yjt[t]  for t in tempo)

#restricao 4 do modelo
modelo.addConstrs(ALFAjt[t]  >= (Yjt[t] - Xjt[t-1])  for t in tempo)

#restricao 5 do modelo
modelo.addConstrs(Xjt[t] <= Yjt[t]  for t in tempo)

#restricao 6
modelo.addConstrs(Hjmin <= Ijt[t] <= Hjmax  for t in tempo)

#restricao 7
modelo.addConstrs(Xjt > 0)

#restricao 8
modelo.addConstrs(Xjzero = fracao_de_t)
#restricao 8
modelo.addConstrs(Ijt[0] = Hjzero)







#Restricao


#RUN
modelo.optimize()


#Printar Resultados


