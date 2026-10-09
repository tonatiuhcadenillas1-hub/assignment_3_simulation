// Bloque: productoTerminado (Sink) - Accion "On enter"
// Actualiza los indicadores y alimenta el histograma del tiempo en el sistema
terminadas++;
double ciclo = time() - agent.horaLlegada;
tiempoTotalSistema += ciclo;
tiempoPromedioSistema = tiempoTotalSistema / terminadas;
histTiempoSistema.add(ciclo);
