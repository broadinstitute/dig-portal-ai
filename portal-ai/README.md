# Portal AI Frontend

A modern Next.js application that provides an AI-powered interface for interacting with PIGEAN knowledge graphs. Built with Next.js, Tailwind CSS, and shadcn/ui components, this application leverages the OpenAI Assistants API and includes a custom PIGEAN Agent for intelligent interactions.

## Features

- 🎨 Modern UI with Tailwind CSS and shadcn/ui components
- 🤖 OpenAI Assistants API integration
- 🔍 Custom PIGEAN Agent for specialized knowledge graph interactions
- 📱 Responsive design
- 🚀 Fast development with Next.js 15

## Prerequisites

- Node.js 18+ 
- pnpm 8+
- OpenAI API key

## Getting Started

1. Clone the repository and navigate to the project directory:
   ```bash
   cd portal-ai
   ```

2. Install dependencies:
   ```bash
   pnpm install
   ```

3. Set up your environment variables:
   ```bash
   cp .env.example .env.local
   ```
   Then edit `.env.local` with your configuration:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - Other environment variables as specified in `.env.example`

4. Start the development server:
   ```bash
   pnpm dev
   ```

5. Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Development

The project uses several key technologies:

- **Next.js 15**: For the React framework and server components
- **Tailwind CSS**: For styling
- **shadcn/ui**: For pre-built components
- **OpenAI Assistants API**: For AI interactions
- **PIGEAN Agent**: Custom agent for knowledge graph interactions

### Project Structure

```
portal-ai/
├── app/              # Next.js app directory
├── components/       # React components
├── lib/             # Utility functions and shared code
├── providers/       # Context providers
├── public/          # Static assets
└── styles/          # Global styles
```

### Available Scripts

```bash
# Start development server
pnpm dev

# Build for production
pnpm build

# Start production server
pnpm start

# Run linting
pnpm lint

# Run type checking
pnpm type-check
```

## Environment Variables

Create a `.env.local` file based on `.env.example` with the following variables:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_api_key_here

# Other configuration variables as specified in .env.example
```

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

1. Push your code to a Git repository (GitHub, GitLab, or BitBucket)
2. Import your project into Vercel
3. Configure your environment variables in the Vercel dashboard
4. Deploy!

Check out the [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.

## Learn More

To learn more about the technologies used in this project:

- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [shadcn/ui Documentation](https://ui.shadcn.com)
- [OpenAI Assistants API Documentation](https://platform.openai.com/docs/assistants/overview)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
