# arm-viz

Página interactiva para entender cómo se calcula el movimiento del brazo de **Milo**, un robot
manipulador móvil: una base con ruedas, un elevador (*lift*) en una columna y un brazo de 6 ejes
con pinza. Está pensada también para quien no viene de la robótica: cada concepto tiene una
explicación en palabras simples, cada fórmula viene con su lectura y un ejemplo con números,
y hay un glosario al final.

**Verla:** abre `index.html` en el navegador (doble clic). Necesita internet solo para cargar
three.js y las fuentes.

## Qué muestra

| Pestaña | Pregunta que responde | Qué se puede hacer |
| --- | --- | --- |
| Directa | ¿Dónde queda la pinza si cada motor está en tal ángulo? | Mover los 7 ejes con sliders; armar la cuenta joint por joint y ver cada matriz |
| Jacobiano | ¿Cuánto y hacia dónde se mueve la pinza si muevo un motor un poquito? | Ver el eje, la palanca y la velocidad que da cada motor; la matriz de 6×7; comprobar la predicción; el elipsoide de manipulabilidad |
| Inversa | ¿Qué ángulos necesito para llevar la pinza a un punto? | Elegir la meta y ver la búsqueda paso a paso (error, pasos de cada motor, reinicios); cambiar el peso del lift, el amortiguamiento y el paso máximo |

## De dónde salen los datos

- La cadena del brazo (posición de cada motor, su eje y sus límites) viene del URDF de Milo, en
  el repositorio [milo_ws](https://github.com/Ivan1721/milo_ws/tree/brazo)
  (`andesrobot_description`). Va de `base_footprint` (el suelo bajo las ruedas) a `gripper_tcp`
  (el punto entre los dedos de la pinza).
- El cálculo es una traducción a JavaScript de `andesrobot_arm/kinematics.py`: cinemática directa
  como producto de transformaciones, jacobiano geométrico y cinemática inversa por mínimos
  cuadrados amortiguados con pesos (lift con peso 10) y reinicios al azar, igual que el robot.
- Al abrirse, la página se compara con valores calculados en Python: la pose de la pinza en cero
  (0.3551, 0, 1.7764) m y, en una postura de prueba, la pose y el jacobiano (diferencia máxima
  ~6·10⁻⁷). El resultado se ve al pie de la página.
- Base, columna y pinza están dibujadas como cajas y cilindros: la página explica la cinemática,
  no la apariencia del robot.

## Actualizar si cambia el brazo

Si cambia la geometría en milo_ws, corre `herramientas/exportar_cadena.py` dentro del contenedor
de milo_ws (instrucciones en el propio archivo) y copia la cadena en `CHAIN` y los valores de
referencia en `window.__REF` de `index.html`.

## Limitaciones

- Los límites de los motores son los provisorios del modelo (±180°), no los del brazo real.
- La cinemática inversa no revisa choques, igual que en el robot: puede atravesar la base.
