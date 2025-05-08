import OpenAI from "openai";

const openai = new OpenAI();

// Send a new message to a thread
export async function POST(
  request: Request,
  context: any
) {
  const threadId = await context.params.threadId;

  const { toolCallOutputs, runId } = await request.json();

  const stream = await openai.beta.threads.runs.submitToolOutputsStream(
    threadId,
    runId,
    { tool_outputs: toolCallOutputs }
  );

  return new Response(stream.toReadableStream());
}