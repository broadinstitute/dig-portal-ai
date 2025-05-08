import ReactMarkdown from 'react-markdown'
import { cn } from '@/lib/utils'

export default function AssistantMessage({ content }: { content: string }) {
  return (
    <div
    className={cn(
      'mr-auto',
      'px-6 py-3',
      'w-full max-w-[90%] md:max-w-3xl',
      // 'prose prose-sm prose-blue dark:prose-invert',
      'whitespace-pre-wrap break-words'
    )}
  >
    <ReactMarkdown>
    {content}
  </ReactMarkdown> 
    <hr className="my-4 border-t border-gray-200 dark:border-gray-700" />
  </div>
)
} 
