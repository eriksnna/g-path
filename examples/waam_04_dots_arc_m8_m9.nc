(EN: WAAM example - dot by dot deposition, 5 layers)
(PT: Exemplo de WAAM - deposicao ponto a ponto, 5 camadas)
(EN: Dialect: Arc on M8/M9 - M8 turns the arc on, M9 off)
(PT: Dialeto: Arco em M8/M9 - M8 abre o arco, M9 fecha)
(EN: The default profile uses the Generic dialect: G-Path suggests switching)
(PT: O perfil padrao usa o dialeto Generico: o G-Path sugere a troca)
(EN: Switch the mode to "Deposition" to see the deposited dots)
(PT: Troque o modo para "Deposicao" para ver os pontos depositados)

#1=4        (EN: step between dots, mm / PT: passo entre pontos, mm)
#2=1.5      (EN: arc-on time per dot, s / PT: tempo de arco aberto por ponto, s)
#3=0.5      (EN: wait after arc off, s / PT: espera apos fechar o arco, s)
#4=15       (EN: dots per layer / PT: pontos por camada)
#5=3        (EN: layer height, mm / PT: altura de cada camada, mm)
#6=5        (EN: number of layers / PT: numero de camadas)

G21 G90
G1 F400
G0 X20 Y50 Z0

M98 P1000 L#6

G90
G0 Z40
M30

O1000 (EN: one layer - dots, rise, return / PT: uma camada - pontos, sobe, volta)
M98 P2000 L#4
G91
G0 Z#5
G90
G0 X20
M99

O2000 (EN: one dot - arc on, wait, off, wait, step / PT: um ponto - abre, espera, fecha, espera, avanca)
M8
G4 P#2
M9
G4 P#3
G91
G1 X#1
G90
M99