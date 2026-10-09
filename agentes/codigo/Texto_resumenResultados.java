// Texto dinamico: resumenResultados (agente Main)
"Escenario: " + (tipoEstudio == 0 ? (escenarioOptimizado ? "Optimizado" : "Base") : "Estudio")
+ "\nOperarios: " + numOperarios + " | Mesas: " + numMesas + " | Demanda: " + factorDemanda
+ "\nMinutos transcurridos: " + roundToDecimal(time(), 1)
+ "\nPlacas llegadas: " + totalLlegadas
+ "\nPlacas terminadas: " + terminadas
+ "\nEn proceso (WIP): " + (totalLlegadas - terminadas)
+ "\nTipo alta complejidad: " + placasAlta
+ "\nCola ensamblaje actual: " + Cola_Ensamblaje.size()
+ "\nCola pruebas actual: " + Cola_Pruebas.size()
+ "\nCola pruebas media: " + roundToDecimal(Cola_Pruebas.statsSize.mean(), 2)
+ "\nTiempo medio de ciclo: " + roundToDecimal(tiempoPromedioSistema, 2) + " min"
+ "\nProduccion por hora: " + roundToDecimal(60.0 * terminadas / Math.max(1.0, time()), 2)
+ "\nFallos de mesa: " + fallosMesa
+ "\nMesa en reparacion: " + (mesaEnReparacion ? "Si" : "No")
