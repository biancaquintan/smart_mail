// App.tsx
import React, { useState } from 'react'
import { classify, regenerateReply } from './api'
import { Upload, Send, AlertCircle, Copy, Sparkles } from 'lucide-react'

type Result = {
  category: string
  probability: number
  reply: string
}

export default function App() {
  const [text, setText] = useState('')
  const [file, setFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<Result | null>(null)
  const [error, setError] = useState<string | null>(null)

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setResult(null)
    setLoading(true)

    try {
      const data = await classify({
        text: text.trim() || undefined,
        file: file || undefined
      })
      setResult(data)
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const copyReply = () => {
    if (result?.reply) navigator.clipboard.writeText(result.reply)
  }

  const handleRegenerate = async () => {
    if (!result) return
    setLoading(true)
    try {
      const data = await regenerateReply(result.category, text)
      setResult({ ...result, reply: data.reply })
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-950 text-slate-800 dark:text-slate-100 flex flex-col items-center justify-center px-4 py-8">
      <header className="w-full max-w-2xl mb-6 text-center">
        <h1 className="text-2xl font-bold tracking-tight">
          ✉️ Classificador de Emails <span className="text-indigo-500">IA</span>
        </h1>
        <p className="text-slate-600 dark:text-slate-400 mt-2 text-sm">
          Envie um arquivo (.txt/.pdf) ou cole o texto do email.
        </p>
      </header>

      <form
        onSubmit={onSubmit}
        className="w-full max-w-2xl bg-white dark:bg-slate-900 rounded-2xl shadow-lg p-6 space-y-4"
      >
        <textarea
          value={text}
          onChange={e => setText(e.target.value)}
          rows={5}
          placeholder="Cole aqui o texto do email (opcional se enviar arquivo)"
          className="w-full rounded-xl p-3 border border-slate-300 dark:border-slate-700 bg-transparent focus:ring-2 focus:ring-indigo-500 outline-none text-sm"
        />

        <label className="flex items-center gap-2 cursor-pointer border border-dashed border-slate-400 dark:border-slate-600 p-3 rounded-xl hover:bg-slate-50 dark:hover:bg-slate-800 transition text-sm">
          <Upload className="w-4 h-4 text-indigo-500" />
          <span>
            {file ? file.name : 'Arraste ou clique para selecionar um arquivo'}
          </span>
          <input
            type="file"
            accept=".txt,application/pdf"
            onChange={e => setFile(e.target.files?.[0] || null)}
            className="hidden"
          />
        </label>

        <button
          type="submit"
          disabled={loading}
          className="flex items-center justify-center gap-2 w-full bg-indigo-600 text-white rounded-xl py-2.5 font-medium hover:bg-indigo-700 transition disabled:opacity-60 text-sm"
        >
          {loading ? (
            'Processando…'
          ) : (
            <>
              <Send className="w-4 h-4" /> Processar
            </>
          )}
        </button>
      </form>

      {error && (
        <div className="w-full max-w-2xl mt-6 flex items-center gap-2 text-red-600 bg-red-50 dark:bg-red-900/20 p-4 rounded-xl text-sm">
          <AlertCircle className="w-4 h-4" />
          <span>
            <strong>Erro:</strong> {error}
          </span>
        </div>
      )}

      {result && (
        <div className="w-full max-w-2xl mt-8 bg-white dark:bg-slate-900 rounded-2xl shadow-lg p-6 space-y-4">
          <div className="text-base font-medium">
            <strong>Categoria:</strong> {result.category}{' '}
            <span className="text-slate-500">
              ({(result.probability * 100).toFixed(1)}%)
            </span>
          </div>
          <div>
            <strong className="text-sm">Resposta sugerida:</strong>
            <div className="relative mt-2">
              <pre className="whitespace-pre-wrap bg-slate-50 dark:bg-slate-800 p-4 rounded-xl text-sm">
                {result.reply}
              </pre>
              <div className="flex gap-2 mt-3">
                <button
                  onClick={copyReply}
                  className="flex items-center gap-1 px-3 py-2 rounded-xl border hover:bg-slate-100 dark:hover:bg-slate-800 transition text-sm"
                >
                  <Copy className="w-4 h-4" /> Copiar
                </button>
                <button
                  onClick={handleRegenerate}
                  disabled={loading}
                  className="flex items-center gap-1 px-3 py-2 rounded-xl border hover:bg-slate-100 dark:hover:bg-slate-800 transition text-sm"
                >
                  <Sparkles className="w-4 h-4" /> Regenerar
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      <footer className="mt-10 text-xs text-slate-500">
        © 2025 SmartMail AI – Powered by IA
      </footer>
    </div>
  )
}
