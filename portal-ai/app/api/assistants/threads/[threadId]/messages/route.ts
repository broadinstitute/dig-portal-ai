import { assistantId } from "@/assistant-config";
import OpenAI from "openai";

const openai = new OpenAI();

// Send a new message to a thread
export async function POST(
  request: Request,
  context: any
) {
  const threadId = await context.params.threadId;
  const { content } = await request.json();

  await openai.beta.threads.messages.create(threadId, {
    role: "user",
    content,
  })

  const stream = await openai.beta.threads.runs.stream(threadId, {
    assistant_id: assistantId,
  })

  return new Response(stream.toReadableStream())
}
