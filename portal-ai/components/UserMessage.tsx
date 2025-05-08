import { cn } from '@/lib/utils'

export default function UserMessage({ content }: { content: string }) {
    return (
      <div className="w-full flex justify-end">
        <div
          className={cn(
            'bg-blue-100 text-gray-900 rounded-xl px-4 py-2',
            'max-w-[75%] sm:max-w-[60%] md:max-w-[50%]',
            'whitespace-pre-wrap break-words',
            'inline-block'
          )}
        >
          {content}
        </div>
      </div>
    )
  }