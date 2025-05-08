'use client'

import Chat from '@/components/Chat'
import { functionCallHandler } from '@/functions/handler'   

export default function GeneralFunctionCallingChat() {
  return <Chat functionCallHandler={functionCallHandler} />
}
