(EN: Machining example - rectangular contour with a center hole)
(PT: Exemplo de usinagem - contorno retangular com furo central)
(EN: Dialect: Generic - M3/M4 on, M5 off - matches the default profile)
(PT: Dialeto: Generico - M3/M4 liga, M5 desliga - compativel com o perfil padrao)

G21 G90          ; millimeters, absolute / milimetros, absoluto
G0 Z5            ; safe height / altura de seguranca
M3 S8000         ; spindle on at 8000 RPM / liga o spindle a 8000 RPM

(EN: rectangular contour, 60 x 40 mm, 5 mm deep)
(PT: contorno retangular, 60 x 40 mm, profundidade 5 mm)
G0 X10 Y10
G1 Z-5 F150      ; plunge cutting / desce cortando
G1 X70 Y10 F600
G1 X70 Y50
G1 X10 Y50
G1 X10 Y10
G0 Z5            ; retract before moving / sobe antes de deslocar

(EN: center hole, 8 mm deep)
(PT: furo central, profundidade 8 mm)
G0 X40 Y30
G1 Z-8 F100
G4 P1            ; dwell 1 s at the bottom / espera 1 s no fundo
G0 Z5

M5               ; spindle off / desliga o spindle
G0 X0 Y0
M2               ; end of program / fim do programa