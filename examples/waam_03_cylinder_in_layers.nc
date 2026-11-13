(EN: WAAM example - cylindrical wall, 12 layers)
(PT: Exemplo de WAAM - parede cilindrica, 12 camadas)
(EN: Dialect: Generic - M3 turns the arc on, M5 off)
(PT: Dialeto: Generico - M3 liga o arco, M5 desliga)
(EN: Switch the mode to "Deposition" in the top bar to see the bead metrics)
(PT: Troque o modo para "Deposicao" na barra superior para ver as metricas de cordao)
(EN: Shows a full circle with G3 and a subroutine repeated with L)
(PT: Demonstra circulo completo com G3 e sub-rotina repetida com L)

#1=3        (EN: layer height, mm / PT: altura de cada camada, mm)
#2=12       (EN: number of layers / PT: numero de camadas)

G21 G90
G0 Z5
G0 X90 Y60           ; start: center X60 Y60, radius 30 / partida: centro X60 Y60, raio 30
G0 Z0

M98 P2000 L#2

G90
G0 Z50               ; retract the torch / retrai a tocha
M30

O2000 (EN: one layer - full circle, dwell, rise / PT: uma camada - circulo, espera, sobe)
G90
M3
G3 X90 Y60 I-30 J0 F300
M5
G4 P2
G91
G0 Z#1
M99