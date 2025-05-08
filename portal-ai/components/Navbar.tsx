"use client";

import { signOut, useSession } from "next-auth/react";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { useRouter } from "next/navigation";
import Image from "next/image";

export default function Navbar() {
  const { data: session } = useSession();
  const router = useRouter();
  return (
    <nav className="fixed top-0 left-0 w-full flex justify-between items-center px-6 py-4">
      <div className="flex items-center">
        <Image
          src="/a2fkp.png"
          alt="PigeanGPT Logo"
          className="h-10 w-auto"
          width={100}
          height={100}
        />
      </div>

      <div className="flex items-center gap-4">
        {session ? (
          <>
            <Avatar>
              <AvatarImage src={session.user?.image || ""} alt={session.user?.name || "User"} />
              <AvatarFallback>{session.user?.name?.[0] ?? "U"}</AvatarFallback>
            </Avatar>

            <Button variant="outline" onClick={() => signOut({ callbackUrl: "/" })}>
              Sign Out
            </Button>
          </>
        ) : (
          <Button onClick={() => router.push("/signin")}>
            Sign In
          </Button>
        )}
      </div>
    </nav>
  );
}
