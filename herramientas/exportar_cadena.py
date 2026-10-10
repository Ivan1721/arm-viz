"""
Exporta la cadena cinemática del brazo de Milo para pegarla en index.html.

La página no lee el URDF: tiene la cadena escrita a mano en la constante CHAIN (orígenes, ejes y
límites de cada joint) y unos valores de referencia en window.__REF para comprobarse sola.
Este script saca esos datos del URDF real usando la misma clase que el robot (ArmKinematics),
así que si cambia la geometría del brazo en milo_ws, se corre de nuevo y se copian los números.

Se corre DENTRO del contenedor de milo_ws, con el workspace compilado:
    ./sim.sh shell
    source /ros2_ws/install/setup.bash
    python3 exportar_cadena.py > cadena.json

Salida (JSON):
    chain  lista de joints de base_footprint a gripper_tcp: name, type, xyz, rpy, axis, lower, upper
           -> va en CHAIN de index.html
    ref    pose del TCP en cero, una postura de prueba q, su pose (tcp) y su jacobiano (J)
           -> q, tcp y J van en window.__REF; q0_tcp en REF.tcp0
"""
import json

import numpy as np

from andesrobot_arm.kinematics import LIFT_BASE, ArmKinematics, matrix_to_rpy

# Cadena de 7 ejes: desde base_footprint (suelo) hasta gripper_tcp, con el lift incluido.
k = ArmKinematics.from_xacro(base=LIFT_BASE)

out = {'base': k.base, 'tip': k.tip, 'chain': []}
for j in k.chain:
    out['chain'].append({
        'name': j.name, 'type': j.type, 'parent': j.parent, 'child': j.child,
        'xyz': j.origin[:3, 3].round(6).tolist(),                      # traslación del origin
        'rpy': np.round(matrix_to_rpy(j.origin[:3, :3]), 6).tolist(),  # rotación del origin
        'axis': j.axis.round(6).tolist(),                              # eje, unitario
        'lower': j.lower, 'upper': j.upper,                            # None si es fija
    })

# Postura de prueba cualquiera (lift + joint_1..6): la página compara su pose y su jacobiano.
q = np.array([0.1, 0.3, 0.35, 0.9, -0.4, 0.6, 0.2])
out['ref'] = {
    'q0_tcp': k.fk(np.zeros(7)).round(6).tolist(),
    'q': q.tolist(),
    'tcp': k.fk(q).round(6).tolist(),
    'J': k.jacobian(q).round(6).tolist(),
}
print(json.dumps(out, indent=1))
