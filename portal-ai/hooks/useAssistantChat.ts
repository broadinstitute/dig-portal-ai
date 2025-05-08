'use client'

import { useCallback, useRef, useState } from 'react'
import { RequiredActionFunctionToolCall } from 'openai/resources/beta/threads/runs/runs'

type Message = {
  role: 'user' | 'assistant'
  content: string
}

export function useAssistantChat({
  functionCallHandler,
}: {
  functionCallHandler: (call: RequiredActionFunctionToolCall) => Promise<string>
}) {
  const [messages, setMessages] = useState<Message[]>([])
  const [isSending, setIsSending] = useState(false)
  const [threadId, setThreadId] = useState<string | null>(null)
  const [runId, setRunId] = useState<string | null>(null)
  const decoder = useRef(new TextDecoder())

  const appendMessage = (message: Message) => {
    setMessages((prev) => [...prev, message])
  }

  const updateAssistantMessage = (content: string) => {
    setMessages((prev) => [
      ...prev.filter((m) => m.role !== 'assistant'),
      { role: 'assistant', content },
    ])
  }

  const handleSend = useCallback(
    async (text: string) => {
      if (!text.trim()) return

      appendMessage({ role: 'user', content: text })
      setIsSending(true)

      try {
        let currentThreadId = threadId
        if (!currentThreadId) {
          const res = await fetch('/api/assistants/threads', { method: 'POST' })
          const json = await res.json()
          currentThreadId = json.threadId
          setThreadId(currentThreadId)
        }

        const res = await fetch(`/api/assistants/threads/${currentThreadId}/messages`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ content: text }),
        })
        console.log(res.body)

        if (!res.body) throw new Error('No stream returned.')

        const reader = res.body.getReader()
        let assistantContent = ''
        let buffer = ''
        let tempRunId = ''

        const processChunk = async (chunk: string) => {
          buffer += chunk
          const lines = buffer.split('\n')
          buffer = lines.pop() ?? ''

          for (const line of lines) {
            if (!line.startsWith('data: ')) continue
            const dataStr = line.replace('data: ', '')
            if (dataStr === '[DONE]') return

            const data = JSON.parse(dataStr)

            if (data?.run?.id) {
              tempRunId = data.run.id
              setRunId(tempRunId)
            }

            if (data?.delta?.content) {
              assistantContent += data.delta.content
              updateAssistantMessage(assistantContent)
            }

            if (data?.required_action?.submit_tool_outputs?.tool_calls) {
              const toolCalls = data.required_action.submit_tool_outputs.tool_calls
              const outputs = []

              for (const call of toolCalls) {
                const output = await functionCallHandler(call)
                outputs.push({ tool_call_id: call.id, output })
              }

              const submitRes = await fetch(
                `/api/assistants/threads/${currentThreadId}/actions`,
                {
                  method: 'POST',
                  headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({ runId: tempRunId, toolCallOutputs: outputs }),
                }
              )

              if (!submitRes.body) throw new Error('No stream returned for tool output')

              const submitReader = submitRes.body.getReader()
              let toolContent = ''

              while (true) {
                const { value, done } = await submitReader.read()
                if (done) break
                const chunk = decoder.current.decode(value, { stream: true })
                console.log(`[Chunk] ${chunk}`)
                toolContent += chunk
                updateAssistantMessage(toolContent)
              }
            }
          }
        }

        while (true) {
          const { value, done } = await reader.read()
          if (done) break
          const chunk = decoder.current.decode(value, { stream: true })
          await processChunk(chunk)
        }
      } catch (err) {
        console.error('Assistant stream error:', err)
        appendMessage({
          role: 'assistant',
          content: '⚠️ Assistant encountered an error.',
        })
      } finally {
        setIsSending(false)
      }
    },
    [threadId, functionCallHandler]
  )

  return {
    messages,
    isSending,
    handleSend,
  }
}
