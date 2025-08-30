export async function classify({ text, file }: { text?: string; file?: File }) {
  const formData = new FormData()
  if (text) formData.append('text', text)
  if (file) formData.append('file', file)

  const resp = await fetch('/api/classify', { method: 'POST', body: formData })

  if (!resp.ok) {
    const err = await resp.json().catch(() => ({ detail: 'Erro desconhecido' }))
    throw new Error(err.detail || 'Falha na classificação')
  }

  return resp.json() as Promise<{
    category: string
    probability: number
    reply: string
  }>
}
