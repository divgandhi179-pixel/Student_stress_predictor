import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Mental Health Predictive Analytics",
  description: "Enterprise student stress analysis and telemetry ecosystem.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.className} bg-[color:var(--background)] text-[color:var(--foreground)]`}>
        {children}
      </body>
    </html>
  );
}
