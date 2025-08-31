import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { vi } from 'vitest'
import App from './App'

const mockClassify = vi.fn()
const mockRegenerate = vi.fn()

vi.mock('./api', () => ({
  classify: (...args: any[]) => mockClassify(...args),
  regenerateReply: (...args: any[]) => mockRegenerate(...args)
}))

beforeEach(() => {
  vi.clearAllMocks()
})

test('mostra mensagem de copiado e exibe categoria e probabilidade', async () => {
  mockClassify.mockResolvedValue({
    category: 'Produtivo',
    probability: 0.92,
    reply: 'Obrigado pelo seu contato!'
  })

  render(<App />)

  // digita no textarea
  const textarea = screen.getByRole('textbox')
  await userEvent.type(textarea, 'Obrigado pelo contato')

  // clica em "Processar"
  const processBtn = screen.getByRole('button', { name: /processar/i })
  await userEvent.click(processBtn)

  // espera aparecer a categoria no resultado
  expect(await screen.findByText(/Categoria:/i)).toBeInTheDocument()

  // agora o botão "Copiar" existe
  const copyBtn = await screen.findByRole('button', { name: /copiar/i })
  await userEvent.click(copyBtn)

  // deve mudar para "Copiado"
  expect(
    await screen.findByRole('button', { name: /copiado/i })
  ).toBeInTheDocument()
})

test('regenera a resposta ao clicar em "Regenerar"', async () => {
  mockClassify.mockResolvedValue({
    category: 'Produtivo',
    probability: 0.85,
    reply: 'Resposta inicial'
  })
  mockRegenerate.mockResolvedValue({
    reply: 'Aqui está uma nova resposta regenerada!'
  })

  render(<App />)

  const textarea = screen.getByRole('textbox')
  await userEvent.type(textarea, 'Preciso de ajuda com minha conta')

  const processBtn = screen.getByRole('button', { name: /processar/i })
  await userEvent.click(processBtn)

  // espera aparecer a primeira resposta
  expect(await screen.findByText(/Resposta inicial/i)).toBeInTheDocument()

  // clica em "Regenerar"
  const regenBtn = await screen.findByRole('button', { name: /regenerar/i })
  await userEvent.click(regenBtn)

  // espera a nova resposta mockada
  expect(
    await screen.findByText(/Aqui está uma nova resposta regenerada!/i)
  ).toBeInTheDocument()
})

test('exibe mensagem de erro se classify falhar', async () => {
  mockClassify.mockRejectedValue(new Error('Falha na API'))

  render(<App />)

  const textarea = screen.getByRole('textbox')
  await userEvent.type(textarea, 'Erro de teste')

  const processBtn = screen.getByRole('button', { name: /processar/i })
  await userEvent.click(processBtn)

  // valida que a mensagem de erro aparece
  expect(await screen.findByText(/Erro:/i)).toBeInTheDocument()
  expect(await screen.findByText(/Falha na API/i)).toBeInTheDocument()
})
