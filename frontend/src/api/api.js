const API_BASE_URL = "http://127.0.0.1:8000/api"

async function runSimulation() {
const response = await fetch(`${API_BASE_URL}/simulate`, {
	method: "POST",
})

if (!response.ok) {
	throw new Error("No se pudo ejecutar la simulación")
}

return response.json()
}

async function getResults() {
const response = await fetch(`${API_BASE_URL}/results`)

if (!response.ok) {
	throw new Error("No se pudieron cargar los resultados")
}

return response.json()
}

async function getSimulation(id) {
const response = await fetch(`${API_BASE_URL}/simulations/${id}`)

if (!response.ok) {
	throw new Error("No se pudo cargar la simulación")
}

return response.json()
}

async function getTeams() {
  const response = await fetch(`${API_BASE_URL}/teams`)

  if (!response.ok) {
    throw new Error("No se pudo cargar la lista de equipos")
  }

  return response.json()
}

export { runSimulation, getResults, getSimulation, getTeams }