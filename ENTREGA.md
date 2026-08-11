
## Evencias
*Ver openspecevidence1.png y openspecevidence2.png*

## 3 Pilares
*Micro-tarea:* Parser de tareas/behaviors de usuario a BDD/Gherkin

*Pilar 1 — Herramienta:* Claude Code + OpenSpec
 Por familiaridad con sos capabilities y por la experiencia que tengo habiendo logrado buenos resultados en el desarrollo de tools.

*Pilar 2 — Contexto:* 
En config.yaml defino tech stack + descripción general del utility a desarrollar y detalle de uso/intagración + notas de arquitectura + rules específicas para tasks y proposals 

*Pilar 3 — Prompt:* 
Para el prompt de los specs, primero hice un pre-work donde pedí a claude dividir el objetivo final de la utility en una serie de tasks "como si fueran tasks tecnicas de implementación definidas dentro de un tracker tipo jira o similar". Estas tasks fueron establecidas en un cierto orden para prevenir re-trabajo y agrupadas en grupos (valga la redundancia) que luego serían leídos por el comando "propose". Todos los grupos y sus tasks individuales se encuentran definidas dentro del archivo PLAN.md el cual es utilizado como contexto a la hora de escribir los prompts.
Ejemplo:
>/openspec-propose Group 2 from PLAN.md

Esta operación y sus subsiguientes comandos fue repetida para cada grupo (4 en total). Por lo tanto, podemos resumir que el prompt fue estructurado en partes: una descripción general dentro de config.yaml + una especificación y agrupación de tareas dentro de PLAN.md + un mini prompt referenciando a PLAN.md a la hora de usar el comando "propose"

*Resultado:* 
 Teniendo en cuenta que hubo un pre-work que hizo las veces de lo que el comando "propose" hace a partir de un prompt "general", lo cual atomizó y especificó más aún el detalle de la implementación, no hubo necesidad de iterar. El resultado final funcionó perfectamente. Un pendiente digno de explorar sería NO hacer el prework de PLAN.MD y ver cómo resuelve OpenSpec a partir de un prompt general directo dentro del comando "propose".

## Observaciones
- Entiendo que config.yaml vendría a funcionar como una especie de agents.md/claude.md especifico para openspec pero ¿puede llegar a hacer override de esas rules? 
- De la misma manera ¿cual sería la diferencia entre el comando "propose" y el comando "plan" nativo de claude?
- Por default, los comandos de openclaude no estaban disponibles dentro del directorio específico del ejercico, tuve que moverlos al root del repo.
- Solo por las dudas, en cada prompt de "propose" le dije al agente explícitamente que ante cualquier duda o ambiguedad detuviera el proceso. No estoy seguro de si por default lo hace, pero parece una buena práctica a ser incorporada en config.yaml.