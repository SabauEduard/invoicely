import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Providers } from './providers';
import { Poppins, Roboto } from 'next/font/google';
import { AuthProvider } from "./context/AuthProvider";

const poppins = Poppins({
  weight: ['400', '500', '600'],
  subsets: ['latin'],
})

export const metadata = {
  title: "Invoicely",
  description: "Generated by create next app",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body
        className={`${poppins.className} antialiased text-black`}
      >
        <AuthProvider>
          <Providers>
            {children}
          </Providers>
        </AuthProvider>
      </body>
    </html>
  );
}
