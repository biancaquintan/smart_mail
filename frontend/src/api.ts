const API_URL = import.meta.env.VITE_API_URL || '';

export async function classify({ text, file }: { text?: string; file?: File }) {
  const formData = new FormData();
  if (text) formData.append('text', text);
  if (file) formData.append('file', file);

  const resp = await fetch(`${API_URL}/classify`, { method: 'POST', body: formData });

  if (!resp.ok) {
    const err = await resp.json().catch(() => ({ detail: 'Erro desconhecido' }));
    throw new Error(err.detail || 'Falha na classificação');
  }

  return resp.json() as Promise<{
    category: string;
    probability: number;
    reply: string;
  }>;
}

export async function regenerateReply(category: string, text: string) {
  const resp = await fetch(`${API_URL}/reply`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ category, text }),
  });

  if (!resp.ok) {
    const err = await resp.json().catch(() => ({ detail: 'Erro desconhecido' }));
    throw new Error(err.detail || 'Falha ao regenerar resposta');
  }

  return resp.json() as Promise<{ reply: string }>;
}
