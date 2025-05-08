export let assistantId = ""; // set your assistant ID here

if (assistantId === "") {
  console.log("OPENAI_ASSISTANT_ID", process.env.OPENAI_ASSISTANT_ID);
  assistantId = process.env.OPENAI_ASSISTANT_ID || "default_value";
}
