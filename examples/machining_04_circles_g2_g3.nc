(EN: Machining example - circular contours with G2/G3 arcs)
(PT: Exemplo de usinagem - contornos circulares com arcos G2/G3)
(EN: Dialect: Generic - M3/M4 on, M5 off)
(PT: Dialeto: Generico - M3/M4 liga, M5 desliga)
(EN: Circular interpolation with I/J: center relative to the arc start point)
(PT: Interpolacao circular com I/J: centro relativo ao ponto inicial do arco)

G21 G90
G0 Z5
M3 S10000

(EN: circle 1 - clockwise, G2, radius 20 mm, center at X50 Y40)
(PT: circulo 1 - sentido horario, G2, raio 20 mm, centro em X50 Y40)
G0 X70 Y40
G1 Z-3 F120
G2 X70 Y40 I-20 J0 F500
G0 Z5

(EN: circle 2 - counterclockwise, G3, radius 10 mm, center at X150 Y40)
(PT: circulo 2 - sentido anti-horario, G3, raio 10 mm, centro em X150 Y40)
G0 X160 Y40
G1 Z-3 F120
G3 X160 Y40 I-10 J0 F500
G0 Z5

M5
G0 X0 Y0
M2