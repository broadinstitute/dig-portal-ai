# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Package Management
- `pnpm install` - Install dependencies
- `pnpm dev` - Start development server with Turbopack (runs on localhost:3000)
- `pnpm build` - Build for production
- `pnpm start` - Start production server
- `pnpm lint` - Run ESLint

### Type Checking
- Note: The project uses TypeScript but no explicit type-check script is defined in package.json. Run `npx tsc --noEmit` for type checking.

## Architecture Overview

Portal AI is a Next.js 15 application that provides an AI-powered interface for interacting with PIGEAN knowledge graphs. The application uses the OpenAI Assistants API with custom function calling capabilities.

### Key Components

**Frontend Architecture:**
- Next.js 15 with App Router
- React 19 with TypeScript
- Tailwind CSS + shadcn/ui components
- NextAuth.js for authentication (Google OAuth)

**AI Integration:**
- OpenAI Assistants API with streaming responses
- Custom function registry for PIGEAN knowledge graph queries
- Real-time chat interface with tool calling support

**Backend Integration:**
- Portal Tools API integration (`NEXT_PUBLIC_PORTAL_API_BASE_URL`)
- RESTful API endpoints for assistant interactions
- Custom function handlers for biological data queries

### Core Function Registry

The application supports specialized functions for biological data queries:
- `get_top_genes` - Retrieve top genes for specific conditions
- `search_phenotypes` - Search and match phenotype descriptions
- `get_genesets` - Retrieve gene set information
- `get_factors` - Get factor data
- `run_cypher` - Execute Cypher queries against Neo4j database

### File Structure

```
app/
├── (auth)/signin/          # Authentication pages
├── api/assistants/         # OpenAI Assistant API routes
├── chat/                   # Main chat interface
└── layout.tsx             # Root layout with SessionProvider

components/
├── Chat.tsx               # Main chat component with streaming
├── ChatInput.tsx          # Input component
├── AssistantMessage.tsx   # Message display components
├── UserMessage.tsx
└── ui/                    # shadcn/ui components

functions/
├── index.ts               # Function registry for tool calls
└── handler.ts             # Function handler utilities

hooks/
└── useAssistantChat.ts    # Chat state management hook
```

## Environment Setup

Required environment variables (see `.env.example`):
- `OPENAI_API_KEY` - OpenAI API key
- `OPENAI_ASSISTANT_ID` - OpenAI Assistant ID (must enable file search and code interpreter)
- `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` - Google OAuth credentials
- `NEXTAUTH_SECRET` / `NEXTAUTH_URL` - NextAuth configuration
- `NEXT_PUBLIC_PORTAL_API_BASE_URL` - Portal Tools API endpoint

## Key Implementation Details

### Assistant Integration
- Uses OpenAI Assistants API with streaming responses
- Implements custom function calling for biological data queries
- Assistant configuration managed in `assistant-config.ts`

### Chat System
- Real-time streaming chat with tool calling support
- Message state management with proper streaming handling
- Function call status indicators and error handling

### Authentication
- NextAuth.js with Google OAuth provider
- Session management with SessionProvider wrapper

### API Routes
- `/api/assistants/threads` - Create new conversation threads
- `/api/assistants/threads/[threadId]/messages` - Send messages with streaming
- `/api/assistants/threads/[threadId]/actions` - Submit tool call outputs

## Development Notes

### Function Development
When adding new functions to the registry:
1. Add the function to `functions/index.ts`
2. Ensure proper error handling and JSON response formatting
3. Test with the Portal Tools API endpoint
4. Update the OpenAI Assistant configuration to include the new function

### Component Development
- Follow existing patterns in components directory
- Use shadcn/ui components for consistency
- Implement proper TypeScript types for all props
- Handle loading and error states appropriately

### API Integration
- All Portal Tools API calls go through the function registry
- Responses are formatted as JSON strings for the Assistant
- Function calls are handled asynchronously with proper error handling