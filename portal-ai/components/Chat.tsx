'use client'

import { useState, useEffect, useRef } from 'react'
import { Button } from '@/components/ui/button'
import ChatInput from '@/components/ChatInput'
import UserMessage from '@/components/UserMessage'
import AssistantMessage from '@/components/AssistantMessage'
import { RequiredActionFunctionToolCall } from 'openai/resources/beta/threads/runs/runs'
import { AssistantStream } from 'openai/lib/AssistantStream'
import { AssistantStreamEvent } from "openai/resources/beta/assistants";

const sampleQuestions = [
  'What genes are associated with Type 2 Diabetes?',
  'What biological mechanisms comprise PreClampsia?',
  'What can you do?'
]

type Message = {
  role: 'user' | 'assistant' | 'code'
  content: string
}

// const markdownSample = `
// # 🧬 Functional Annotation Summary

// **Gene:** TP53  
// **Organism:** *Homo sapiens*  
// **Function:** Tumor suppressor, DNA binding transcription factor.

// ---

// ## 🔬 Key Annotations

// - **GO:0003700** – DNA-binding transcription factor activity  
// - **GO:0006977** – Response to DNA damage stimulus  
// - **GO:0005634** – Nucleus

// ---

// ### 🔗 Relevant Resources

// - [UniProt Entry for TP53](https://www.uniprot.org/uniprot/P04637)
// - [NCBI Gene Summary](https://www.ncbi.nlm.nih.gov/gene/7157)

// ---

// \`\`\`python
// # Sample query for gene association
// query_gene("TP53", include_annotations=True)
// \`\`\`

// > "Inactivation of TP53 is a common event in human cancers."  
// > — Functional Genomics Handbook
// `

type ChatProps = {
  functionCallHandler?: (
    toolCall: RequiredActionFunctionToolCall
  ) => Promise<string>;
};

export default function Chat({
  functionCallHandler = () => Promise.resolve(""), // default to return empty string
}: ChatProps) {
  const [userInput, setUserInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputDisabled, setInputDisabled] = useState(false);
  const [threadId, setThreadId] = useState("");
  const [streamStatus, setStreamStatus] = useState<null | string>(null);

  const messagesEndRef = useRef<HTMLDivElement>(null)
  // const { messages, isSending, handleSend } = useAssistantChat({ functionCallHandler })
  const isFirstMessage = messages.length === 0

  // const handleSend = (text: string) => {
  //   if (!text.trim()) return
  
  //   setMessages(prev => [...prev, { role: 'user', content: text }])
  //   setIsSending(true)
  
  //   setTimeout(() => {
  //     setMessages(prev => [
  //       ...prev,
  //       { role: 'assistant', content: markdownSample },
  //     ])
  //     setIsSending(false)
  //   }, 600)
  // }


  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);
  
  // create a new threadID when chat component created
  useEffect(() => {
    const createThread = async () => {
      const res = await fetch(`/api/assistants/threads`, {
        method: "POST",
      });
      const data = await res.json();
      setThreadId(data.threadId);
    };
    createThread();
  }, []);

  const sendMessage = async (text: string) => {
    setStreamStatus("Thinking");
    const response = await fetch(
      `/api/assistants/threads/${threadId}/messages`,
      {
        method: "POST",
        body: JSON.stringify({
          content: text,
        }),
      }
    );
    if (!response.body) throw new Error('No stream returned.')
    const stream = AssistantStream.fromReadableStream(response.body);
    handleReadableStream(stream);
  };

  const submitActionResult = async (
    runId: string,
    toolCallOutputs: { tool_call_id: string; output: string }[]
  ) => {
    const response = await fetch(`/api/assistants/threads/${threadId}/actions`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        runId,
        toolCallOutputs,
      }),
    });
  
    if (!response.body) throw new Error('No stream returned for submitActionResult.');
    const stream = AssistantStream.fromReadableStream(response.body);
    handleReadableStream(stream);
  };
  
  const handleSubmit = (text: string) => {
    if (!text.trim()) return;
  
    setMessages(prev => [...prev, { role: 'user', content: text }]);
    sendMessage(text);
    setUserInput("");
    setInputDisabled(true);
    scrollToBottom();
  };
  
  /* Stream Event Handlers */

  // textCreated - create new assistant message
  const handleTextCreated = () => {
    appendMessage("assistant", "");
  };

  // textDelta - append text to last assistant message
  const handleTextDelta = (delta: any) => {
    if (delta.value != null) {
      appendToLastMessage(delta.value);
    };
    if (delta.annotations != null) {
      annotateLastMessage(delta.annotations);
    }
  };

  // toolCallCreated - log new tool call
  const toolCallCreated = (toolCall: any) => {
    if (toolCall.type != "code_interpreter") return;
    appendMessage("code", "");
  };

  // toolCallDelta - log delta and snapshot for the tool call
  const toolCallDelta = (delta: any) => {
    if (delta.type != "code_interpreter") return;
    if (!delta.code_interpreter.input) return;
    appendToLastMessage(delta.code_interpreter.input);
  };

  // handleRequiresAction - handle function call
  const handleRequiresAction = async (
    event: AssistantStreamEvent.ThreadRunRequiresAction
  ) => {
    const runId = event.data.id;
    if (event.data.required_action) {
      const toolCalls = event.data.required_action.submit_tool_outputs.tool_calls;
  
      // Update UI status: "Calling function XYZ..."
      if (toolCalls.length > 0) {
        const fnName = toolCalls[0].function?.name;
        if (fnName) {
          setStreamStatus(`🔧 Calling function \`${fnName}\``);
        } else {
          setStreamStatus("🔧 Calling function");
        }
      }
  
      const toolCallOutputs = await Promise.all(
        toolCalls.map(async (toolCall) => {
          const result = await functionCallHandler(toolCall);
          return { output: result, tool_call_id: toolCall.id };
        })
      );
  
      setInputDisabled(true);
      await submitActionResult(runId, toolCallOutputs);
      setStreamStatus(null); // clear once response is returned
    }
  };
  
  // handleRunCompleted - re-enable the input form
  const handleRunCompleted = () => {
    setInputDisabled(false);
  };

  const handleReadableStream = (stream: AssistantStream) => {
    // messages
    stream.on("textCreated", handleTextCreated);
    stream.on("textDelta", handleTextDelta);

    // code interpreter
    stream.on("toolCallCreated", toolCallCreated);
    stream.on("toolCallDelta", toolCallDelta);

    // events without helpers yet (e.g. requires_action and run.done)
    stream.on("event", (event) => {
      if (event.event === "thread.run.requires_action")
        handleRequiresAction(event);
      if (event.event === "thread.run.completed") handleRunCompleted();
    });
  };

  /*
    =======================
    === Utility Helpers ===
    =======================
  */

    const appendMessage = (role: 'user' | 'assistant' | 'code', content: string) => {
      setMessages((prevMessages: Message[]) => [...prevMessages, { role, content }]);
    }
    
    const appendToLastMessage = (text: string) => {
      setMessages((prevMessages) => {
        const lastMessage = prevMessages[prevMessages.length - 1];
        if (!lastMessage) return prevMessages;
    
        const updatedLastMessage = {
          ...lastMessage,
          content: lastMessage.content + text,
        };
        return [...prevMessages.slice(0, -1), updatedLastMessage];
      });
    };
    
    const annotateLastMessage = (annotations: any[]) => {
      setMessages((prevMessages) => {
        const lastMessage = prevMessages[prevMessages.length - 1];
        if (!lastMessage) return prevMessages;
    
        const updatedLastMessage = { ...lastMessage };
    
        annotations.forEach((annotation) => {
          if (annotation.type === 'file_path') {
            updatedLastMessage.content = updatedLastMessage.content.replaceAll(
              annotation.text,
              `/api/files/${annotation.file_path.file_id}`
            );
          }
        });
    
        return [...prevMessages.slice(0, -1), updatedLastMessage];
      });
    };
    
  return (
    <div className="relative flex-1">
      {isFirstMessage ? (
        <div className="absolute inset-0 flex items-center justify-center px-4">
          <div className="text-center max-w-xl w-full space-y-6">
            <div className="text-4xl">🕊️</div>
            <p className="text-gray-700">
              Ask a question about genes, functions, or associations.
            </p>
            <div className="flex flex-col sm:flex-row justify-center gap-2">
              {sampleQuestions.map((q, idx) => (
                <Button key={idx} variant="outline" onClick={() => 
                handleSubmit(q)}>
                  {q}
                </Button>
              ))}
            </div>
              <ChatInput 
              onSend={handleSubmit} 
              isLoading={inputDisabled} 
              value={userInput}
              onChange={(v: string) => setUserInput(v)} 
              />
          </div>
        </div>
      ) : (
        <div className="flex-1 overflow-y-auto px-4 pt-6 pb-40">
            <div className="flex flex-col space-y-4 max-w-4xl mx-auto">
                {messages.map((msg, i) => (
                <div key={i}>
                    {msg.role === 'user' ? (
                    <UserMessage content={msg.content} />
                    ) : (
                    <AssistantMessage content={msg.content} />
                    )}
                </div>
                ))}
                {streamStatus && (
                  <div className="flex items-center justify-center gap-1 text-sm text-gray-500 my-2">
                  <span>{streamStatus}</span>
                  <span className="dot-flash">.</span>
                  <span className="dot-flash delay-200">.</span>
                  <span className="dot-flash delay-400">.</span>
                  </div>
                )}
                <div ref={messagesEndRef} />
            </div>
          <div className="fixed bottom-0 left-0 w-full px-4 pb-4 bg-gradient-to-t from-white via-white/90 backdrop-blur">
            <div className="max-w-4xl mx-auto">
              <ChatInput 
              onSend={handleSubmit} 
              isLoading={inputDisabled} 
              value={userInput}
              onChange={(v: string) => setUserInput(v)} 
              />
            </div>
          </div>
        </div>
      )}
    </div>
  )  
}