import GoogleProvider from "next-auth/providers/google";

export const authOptions = {
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID as string,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET as string,
    }),
  ],
  pages: {
    signIn: "/signin",
  },
  callbacks: {
    async signIn({ account, profile }: { account: any, profile: any }) {
      if (account?.provider === 'google' && profile?.email) {
        const isAllowed = profile.email.endsWith("@broadinstitute.org");
        return isAllowed;
      }
      return false;
    },
    async session({ session, token}: { session: any, token: any }) {
      session.user.id = token.id as string;
      session.user.firstName = token.firstName as string;
      session.user.lastName = token.lastName as string;
      session.user.email = token.email as string;
      session.user.image = token.image as string;
      return session;
    },
    async jwt({ token, account, profile, user }: { token: any, account: any, profile: any, user: any }) {
        if (account && profile) {
            token.id = user.id;
            token.firstName = profile.given_name;
            token.lastName = profile.family_name;
            token.email = profile.email;
            token.image = profile.image;
        }
        return token;
    },
  },
  secret: process.env.NEXTAUTH_SECRET as string,
};
