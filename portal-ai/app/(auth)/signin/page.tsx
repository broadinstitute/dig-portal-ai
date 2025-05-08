"use client";

import { getProviders, signIn } from "next-auth/react";
import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";

export default function SignInPage() {
  const [providers, setProviders] = useState<Record<string, any> | null>(null);

  useEffect(() => {
    const loadProviders = async () => {
      const res = await getProviders();
      setProviders(res);
    };
    loadProviders();
  }, []);

  if (!providers) {
    return <div>Loading...</div>;
  }

  return (
    <div className="min-h-screen flex justify-center items-center bg-gray-50 p-4">
      <Card className="w-full max-w-md shadow-md">
      <CardHeader>
        <CardTitle className="text-2xl">
          Sign In
        </CardTitle>
        <CardDescription>
          Please sign in with your Broad Institute Google account. This preview is limited to Broad affiliates only.
        </CardDescription>
      </CardHeader>
      <CardContent className="flex flex-col space-y-4">
        {Object.values(providers).map((provider) => (
          <Button
            key={provider.name}
            onClick={() =>
              signIn(provider.id, {
                callbackUrl: "/chat",
              })
            }
            className="w-full"
          >
            Sign in with {provider.name}
          </Button>
        ))}
      </CardContent>
      {/* <CardFooter className="justify-center">
        <p className="text-sm">
          Already have an account?{" "}
          <Button variant="link" className="p-0 h-auto" onClick={() => location.href = "/signin"}>
              Sign In
            </Button>
          </p>
        </CardFooter> */}
      </Card>
    </div>
  );
}
