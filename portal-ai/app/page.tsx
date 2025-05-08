import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import Navbar from '@/components/Navbar'
import Link from 'next/link'

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white flex flex-col">
      <Navbar />

      <main className="flex-1 flex items-center justify-center px-4">
        <Card className="w-full max-w-2xl shadow-2xl border-0">
          <CardHeader>
            <CardTitle className="text-4xl font-bold text-center">
              Welcome to <span className="text-blue-600">PigeanGPT</span> 🕊️
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-6 text-center">
            <p className="text-lg text-gray-700">
              You&apos;ve landed at the gateway to our <strong>Association to Function (A2F)</strong> knowledge portal.
            </p>
            <p className="text-gray-600">
              PigeanGPT is your AI-powered guide for navigating and reasoning over the
              biological and functional insights captured in our A2F datasets.
            </p>
            <p className="text-gray-600">
              Ask questions, explore associations, and discover functions—just like chatting
              with a domain expert.
            </p>
            <Button asChild size="lg">
              <Link href="/chat">Start Chatting</Link>
            </Button>
          </CardContent>
        </Card>
      </main>
    </div>
  )
}
