import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { redirect } from 'next/navigation'
import Navbar from '@/components/Navbar'
import FunctionChat from '@/components/FunctionChat'
import { AuthOptions } from 'next-auth'

export default async function ChatPage() {
  const session = await getServerSession(authOptions as AuthOptions)

  if (!session) {
    redirect('/signin') // Your custom signin page
  }

  return (
    <div className="h-screen w-full flex flex-col bg-white">
      <Navbar />
      <FunctionChat />
    </div>
  )
}
