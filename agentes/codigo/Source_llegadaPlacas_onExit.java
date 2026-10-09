// Bloque: llegadaPlacas (Source) - Accion "On exit"
// Asigna los atributos de la entidad y actualiza contadores
agent.horaLlegada = time();
agent.tipoPlaca = uniform(0, 1) < 0.25 ? "Alta" : "Baja";
totalLlegadas++;
if ("Alta".equals(agent.tipoPlaca)) placasAlta++;
