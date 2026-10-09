// Evento: registrarResultados480 (agente Main)
// Trigger: timeout, ocurrencia en t = 480 min
// Escribe una fila por replica en el CSV del estudio activo
if (tipoEstudio != 0 && getExperiment() instanceof com.anylogic.engine.ExperimentParamVariation) {
    com.anylogic.engine.ExperimentParamVariation experimento =
        (com.anylogic.engine.ExperimentParamVariation) getExperiment();
    java.io.File salida = new java.io.File(tipoEstudio == 1 ?
        "resultados_matriz.csv" : "resultados_demanda.csv");
    boolean encabezado = !salida.exists() || salida.length() == 0;
    try (java.io.PrintWriter csv = new java.io.PrintWriter(new java.io.FileWriter(salida, true))) {
        if (encabezado) csv.println("estudio,iteracion,replica,operarios,mesas,factor_demanda,llegadas,terminadas,wip,cola_ensamblaje_final,cola_pruebas_final,cola_ensamblaje_media,cola_pruebas_media,tiempo_medio_sistema_min,produccion_hora,utilizacion_operarios,utilizacion_mesas,fallos_mesa");
        csv.printf(java.util.Locale.US,
            "%s,%d,%d,%d,%d,%.4f,%d,%d,%d,%d,%d,%.6f,%.6f,%.6f,%.6f,%.6f,%.6f,%d%n",
            tipoEstudio == 1 ? "matriz" : "demanda",
            experimento.getCurrentIteration(), experimento.getCurrentReplication(),
            numOperarios, numMesas, factorDemanda,
            totalLlegadas, terminadas, totalLlegadas - terminadas,
            Cola_Ensamblaje.size(), Cola_Pruebas.size(),
            Cola_Ensamblaje.statsSize.mean(), Cola_Pruebas.statsSize.mean(),
            tiempoPromedioSistema, terminadas / 8.0,
            Operarios_Ensamblaje.utilization(), Mesa_Pruebas.utilization(), fallosMesa);
    } catch (java.io.IOException e) {
        throw new RuntimeException("No se pudo escribir " + salida.getAbsolutePath(), e);
    }
    traceln("CSV: " + salida.getAbsolutePath());
}
