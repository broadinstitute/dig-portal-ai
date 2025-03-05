"use client";

import { Button } from "@workspace/ui/components/button"
import { useState } from "react";
import { ChatOpenAI } from "@langchain/openai";
import { ChatPromptTemplate } from "@langchain/core/prompts";
import { StringOutputParser } from "@langchain/core/output_parsers";
import { RunnableSequence } from "@langchain/core/runnables";
import { z } from "zod";

// Define schemas for our structured outputs
const nerSchema = z.object({
  entities: z.array(z.object({
    text: z.string(),
    type: z.string(),
    role: z.string()
  })),
  relationships: z.array(z.object({
    source: z.string(),
    type: z.string(),
    target: z.string()
  }))
});

export default function Page() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const analyzeQuery = async () => {
    setLoading(true);
    try {
      const model = new ChatOpenAI({
        modelName: "gpt-4o-mini",
        temperature: 0,
      });

      // Step 1: NER Analysis
      const nerPrompt = ChatPromptTemplate.fromTemplate(`
        Extract named entities and relationships from the following query.
        Focus on identifying classes, properties, and relationships between entities.
        Format as JSON with arrays of entities and relationships.
        
        Query: {query}
        
        Example format:
        {{
          "entities": [
            {{"text": "Person", "type": "Class", "role": "subject"}},
            {{"text": "Company", "type": "Class", "role": "object"}}
          ],
          "relationships": [
            {{"source": "Person", "type": "WORKS_AT", "target": "Company"}}
          ]
        }}
      `);

      // Step 2: Cypher Query Generation
      const cypherPrompt = ChatPromptTemplate.fromTemplate(`
        Generate a Cypher query based on these extracted entities and relationships:
        {nerResult}
        
        Original query: {query}
        
        Return the Cypher query only, no explanation.
      `);

      // Create the chain
      const chain = RunnableSequence.from([
        // First NER analysis
        {
          query: (input: string) => input,
        },
        nerPrompt,
        model.withStructuredOutput(nerSchema),
        // Then generate Cypher
        async (nerResult: any) => ({
          nerResult: JSON.stringify(nerResult),
          query: query,
        }),
        cypherPrompt,
        model,
        new StringOutputParser(),
      ]);

      const response = await chain.invoke(query);

      setResult({
        cypher: response,
        // In a real app, you would execute the Cypher query here
        // and format the results
        sampleResults: [
          { name: "Example", relationship: "SAMPLE", target: "Data" }
        ]
      });

    } catch (error) {
      console.error("Analysis error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-svh">
      <div className="flex flex-col items-center justify-center gap-4 w-full max-w-2xl p-4">
        <h1 className="text-2xl font-bold">Knowledge Graph Query Analysis</h1>
        
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="w-full p-4 border rounded-lg shadow-sm"
          rows={4}
          placeholder="Enter your query (e.g., 'Find people who work at tech companies')"
        />

        <Button 
          size="lg" 
          onClick={analyzeQuery}
          disabled={loading || !query.trim()}
        >
          {loading ? "Analyzing..." : "Analyze Query"}
        </Button>

        {result && (
          <div className="w-full space-y-4 mt-8">
            <div className="bg-gray-50 p-4 rounded-lg">
              <h3 className="font-medium">Generated Cypher Query:</h3>
              <pre className="bg-gray-100 p-2 rounded mt-2 overflow-x-auto">
                {result.cypher}
              </pre>
              
              <h3 className="font-medium mt-4">Results:</h3>
              <div className="overflow-x-auto mt-2">
                <table className="min-w-full">
                  <thead>
                    <tr className="bg-gray-100">
                      {Object.keys(result.sampleResults[0]).map((header) => (
                        <th key={header} className="px-4 py-2 text-left">
                          {header}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {result.sampleResults.map((row: any, i: number) => (
                      <tr key={i}>
                        {Object.values(row).map((value: any, j: number) => (
                          <td key={j} className="border px-4 py-2">
                            {value}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
