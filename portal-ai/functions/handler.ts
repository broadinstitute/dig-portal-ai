import { RequiredActionFunctionToolCall } from 'openai/resources/beta/threads/runs/runs'
import { functionRegistry } from '@/functions'

export async function functionCallHandler(
  call: RequiredActionFunctionToolCall
): Promise<string> {
  try {
    const name = call.function.name
    const args = JSON.parse(call.function.arguments || '{}')

    const fn = functionRegistry[name]
    if (!fn) {
      console.warn(`No handler found for function: ${name}`)
      return `Function "${name}" is not yet implemented.`
    }

    return await fn(args)
  } catch (err) {
    console.error('functionCallHandler error:', err)
    return 'An error occurred while processing your request.'
  }
}
