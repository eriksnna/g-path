(EN: WAAM example - straight wall, 4 layers)
(PT: Exemplo de WAAM - parede reta, 4 camadas)
(EN: Dialect: Generic - M3 turns the arc on, M5 off - matches the default profile)
(PT: Dialeto: Generico - M3 liga o arco, M5 desliga - compativel com o perfil padrao)
(EN: Switch the mode to "Deposition" in the top bar to see the bead metrics)
(PT: Troque o modo para "Deposicao" na barra superior para ver as metricas de cordao)

G21 G90
G0 Z0.5          ; start height / altura inicial

(EN: layer 1, Z = 0 / PT: camada 1, Z = 0)
G0 X0 Y0
M3               ; arc on / abre o arco
G1 X0 Y0 Z0 F200
G1 X100 Y0 F200
M5               ; arc off / fecha o arco
G4 P3            ; cool down 3 s / espera 3 s para resfriar

(EN: layer 2, Z = 3 mm / PT: camada 2, Z = 3 mm)
G0 X100 Y0 Z3
M3
G1 X100 Y0 Z3 F200
G1 X0 Y0 F200
M5
G4 P3

(EN: layer 3, Z = 6 mm / PT: camada 3, Z = 6 mm)
G0 X0 Y0 Z6
M3
G1 X0 Y0 Z6 F200
G1 X100 Y0 F200
M5
G4 P3

(EN: layer 4, Z = 9 mm / PT: camada 4, Z = 9 mm)
G0 X100 Y0 Z9
M3
G1 X100 Y0 Z9 F200
G1 X0 Y0 F200
M5

G0 Z25           ; retract the torch / retrai a tocha
M2