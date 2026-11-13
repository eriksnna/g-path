(EN: Machining example - rectangular pocket cut in 4 depth passes)
(PT: Exemplo de usinagem - cavidade retangular aberta em 4 passes de profundidade)
(EN: Dialect: Generic - M3/M4 on, M5 off)
(PT: Dialeto: Generico - M3/M4 liga, M5 desliga)
(EN: Shows #n variables, variable math, M98 subroutine and L repeat)
(PT: Demonstra variaveis #n, contas com variaveis, sub-rotina M98 e repeticao L)
(EN: Use the layer filter or "Color by depth" to see each pass)
(PT: Use o filtro de camada ou "Colorir por profundidade" para ver cada passe)

#1=2        (EN: depth of each pass, mm / PT: profundidade de cada passe, mm)
#2=4        (EN: number of passes / PT: numero de passes)
#3=0        (EN: current depth / PT: profundidade atual)

G21 G90
G0 Z5
M3 S9000
G0 X30 Y30

M98 P1000 L#2        ; repeat the contour / repete o contorno

G0 Z5
M5
G0 X0 Y0
M30

O1000 (EN: one pass around the 60 x 40 mm rectangle / PT: um passe no retangulo de 60 x 40 mm)
#3=#3-#1
G1 Z#3 F150
G1 X90 F500
G1 Y70
G1 X30
G1 Y30
M99