(EN: Machining example - drilling a 3 x 2 grid of holes)
(PT: Exemplo de usinagem - furacao em grade 3 x 2)
(EN: Dialect: Generic - M3/M4 on, M5 off)
(PT: Dialeto: Generico - M3/M4 liga, M5 desliga)
(EN: Each hole: rapid to position, drill 6 mm, dwell 0.5 s, retract)
(PT: Cada furo: rapido ate a posicao, fura 6 mm, espera 0.5 s, recua)

G21 G90
G0 Z5
M3 S6000

(EN: hole 1 / PT: furo 1)
G0 X20 Y20
G1 Z-6 F100
G4 P0.5
G0 Z5

(EN: hole 2 / PT: furo 2)
G0 X50 Y20
G1 Z-6 F100
G4 P0.5
G0 Z5

(EN: hole 3 / PT: furo 3)
G0 X80 Y20
G1 Z-6 F100
G4 P0.5
G0 Z5

(EN: hole 4 / PT: furo 4)
G0 X20 Y50
G1 Z-6 F100
G4 P0.5
G0 Z5

(EN: hole 5 / PT: furo 5)
G0 X50 Y50
G1 Z-6 F100
G4 P0.5
G0 Z5

(EN: hole 6 / PT: furo 6)
G0 X80 Y50
G1 Z-6 F100
G4 P0.5
G0 Z5

M5
G0 X0 Y0
M2