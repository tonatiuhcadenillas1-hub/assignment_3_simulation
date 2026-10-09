// Evento: falloMesaCada8h (agente Main)
// Trigger: timeout, ocurrencia en t = 240 min
if (habilitarFallas) {
    fallosMesa++;
    mesaEnReparacion = true;
    Mesa_Pruebas.set_capacity(numMesas - 1);
}
