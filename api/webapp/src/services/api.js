
const API_BASE = 'http://localhost:8000'; // Backend na porta 8000

export async function getOperadoras() {
  const response = await fetch(`${API_BASE}/api/operadoras`);
  return await response.json();
}

export async function postOperadora(data) {
  const response = await fetch(`${API_BASE}/api/operadoras`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  return await response.json();
}