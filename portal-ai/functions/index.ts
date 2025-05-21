import { RequiredActionFunctionToolCall } from 'openai/resources/beta/threads/runs/runs'

export const functionRegistry: Record<
  string,
  (args: Record<string, any>) => Promise<string>
> = {
  get_top_genes: async (args) => {
    console.log(args)
    const res = await fetch(`${process.env.NEXT_PUBLIC_PORTAL_API_BASE_URL}/get_top_genes`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(args),
    })
    const json = await res.json()
    return JSON.stringify(json.result ?? 'No results found.')
  },

  search_phenotypes: async (args) => {
    console.log(args)
    const res = await fetch(`${process.env.NEXT_PUBLIC_PORTAL_API_BASE_URL}/search_phenotypes`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(args),
    })

    const json = await res.json()
    const { result } = json
    if (!result?.length) return 'No matching phenotypes found.'

    // Handle multiquery format: [{ query: string, results: [...] }]
    if (!Array.isArray(result) || result.length === 0) return 'No matching phenotypes found.';

    const responses = result.map((entry: { query: string; results: any[] }) => {
      if (!entry.results?.length) {
        return `Query: "${entry.query}"\nNo matching phenotypes found.`;
      }
      const best = entry.results[0];
      const topList = entry.results
        .slice(0, 3)
        .map(
          (r: { name: string; id: string; cosine_similarity: number }, i: number) =>
            `${i + 1}. ${r.name} (ID: \`${r.id}\`, Score: ${r.cosine_similarity.toFixed(2)})`
        )
        .join('\n');
      return `Query: "${entry.query}"\nBest match: **${best.name}** (ID: \`${best.id}\`)\nOther potential matches:\n${topList}`;
    });

    return responses.join('\n\n');
  },

  get_genesets: async (args) => {
    console.log(args)
    const res = await fetch(`${process.env.NEXT_PUBLIC_PORTAL_API_BASE_URL}/get_genesets`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(args),
    })
    const json = await res.json()
    return JSON.stringify(json.result ?? 'No results found.')
  },

  get_factors: async (args) => {
    console.log(args)
    const res = await fetch(`${process.env.NEXT_PUBLIC_PORTAL_API_BASE_URL}/get_factors`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(args),
    })
    const json = await res.json()
    return JSON.stringify(json.result ?? 'No results found.')
  },

  run_cypher: async (args) => {
    console.log(args)
    const res = await fetch(`${process.env.NEXT_PUBLIC_PORTAL_API_BASE_URL}/get_cipher`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(args),
    })
    const json = await res.json()
    console.log(json)
    return JSON.stringify(json.result ?? 'No results found.')
  }
}

