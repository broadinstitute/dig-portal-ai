'use client'

import { useRef, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { cn } from '@/lib/utils'
import { SendHorizonal, Loader2 } from 'lucide-react'

export default function ChatInput({
  onSend,
  isLoading,
  value,
  onChange,
}: {
  onSend: (message: string) => void
  isLoading: boolean
  value: string
  onChange: (value: string) => void
}) {
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  const handleSubmit = () => {
    const trimmed = value.trim()
    if (trimmed) {
      onSend(trimmed)
      onChange('')
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit()
    }
  }

  // Resize the textarea based on content
  useEffect(() => {
    const textarea = textareaRef.current
    if (textarea) {
      textarea.style.height = 'auto' // Reset height
      textarea.style.height = Math.min(textarea.scrollHeight, 150) + 'px'
    }
  }, [value])

  return (
    <Card className="w-full p-3 rounded-2xl shadow-lg border bg-white">
      <div className="flex items-end gap-3">
        <textarea
          ref={textareaRef}
          rows={1}
          placeholder="Type your question..."
          value={value}
          onChange={e => onChange(e.target.value)}
          onKeyDown={handleKeyDown}
          className={cn(
            'flex-grow resize-none overflow-auto rounded-md border border-gray-200 px-4 py-2 text-sm leading-relaxed text-gray-900 placeholder:text-gray-400',
            'focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-blue-400',
          )}
          style={{
            maxHeight: '150px',
            lineHeight: '1.5',
          }}
        />
        <Button
          onClick={handleSubmit}
          disabled={isLoading || !value.trim()}
          size="icon"
          variant="default"
        >
          {isLoading ? (
            <Loader2 className="animate-spin h-5 w-5" />
          ) : (
            <SendHorizonal className="h-5 w-5" />
          )}
        </Button>
      </div>
    </Card>
  )
}
