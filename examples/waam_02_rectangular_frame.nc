(EN: WAAM example - rectangular frame, 3 layers)
(PT: Exemplo de WAAM - quadro retangular, 3 camadas)
(EN: Dialect: Generic - M3 turns the arc on, M5 off)
(PT: Dialeto: Generico - M3 liga o arco, M5 desliga)
(EN: Each layer follows the same closed contour, rising 3 mm per layer)
(PT: Cada camada percorre o mesmo contorno fechado, subindo 3 mm por camada)

G21 G90
G0 Z1
G0 X0 Y0

(EN: layer 1, Z = 0 / PT: camada 1, Z = 0)
M3
G1 X0 Y0 Z0 F180
G1 X80 Y0 F180
G1 X80 Y60 F180
G1 X0 Y60 F180
G1 X0 Y0 F180
M5
G4 P4            ; cooling between layers / resfriamento entre camadas

(EN: layer 2, Z = 3 mm / PT: camada 2, Z = 3 mm)
G0 Z3
M3
G1 X0 Y0 Z3 F180
G1 X80 Y0 F180
G1 X80 Y60 F180
G1 X0 Y60 F180
G1 X0 Y0 F180
M5
G4 P4

(EN: layer 3, Z = 6 mm / PT: camada 3, Z = 6 mm)
G0 Z6
M3
G1 X0 Y0 Z6 F180
G1 X80 Y0 F180
G1 X80 Y60 F180
G1 X0 Y60 F180
G1 X0 Y0 F180
M5

G0 Z25           ; retract the torch / retrai a tocha
M2