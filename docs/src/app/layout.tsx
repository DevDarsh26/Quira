import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import Link from "next/link";
import Image from "next/image";
import { FileText } from "lucide-react";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  metadataBase: new URL("https://quira.darshmodii.in"),
  title: "Quira | High-Performance RAG Framework",
  description: "Quira is a token-efficient, zero-latency Retrieval Augmented Generation (RAG) framework featuring Speculative Retrieval and Context Tetris.",
  keywords: ["RAG", "LLM", "Vector Database", "Speculative Retrieval", "Context Tetris", "Generative AI", "Python", "AI Framework"],
  authors: [{ name: "Darsh Modii" }],
  openGraph: {
    title: "Quira | High-Performance RAG Framework",
    description: "Build incredibly fast AI apps with Quira's zero-latency RAG engine.",
    url: "https://quira.darshmodii.in",
    siteName: "Quira",
    images: [{ url: "/quira_logo.png", width: 800, height: 600, alt: "Quira Logo" }],
    locale: "en_US",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "Quira | High-Performance RAG Framework",
    description: "Build incredibly fast AI apps with Quira's zero-latency RAG engine.",
    images: ["/quira_logo.png"],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased dark`}
    >
      <body className="min-h-full flex flex-col bg-background text-foreground selection:bg-primary/30">
        
        {/* Sleek Minimal Navbar */}
        <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-backdrop-filter:bg-background/60">
          <div className="container mx-auto px-6 h-16 flex items-center justify-between">
            <Link href="/" className="flex items-center gap-3 font-bold text-xl tracking-tighter hover:opacity-80 transition-opacity">
              <Image src="/quira_logo.png" alt="Quira Logo" width={36} height={36} className="object-contain rounded-md shadow-sm" priority />
              <span className="hidden sm:inline-block">Quira</span>
            </Link>
            
            <nav className="flex items-center gap-6 text-sm font-medium text-muted-foreground">
              <Link href="/docs" className="hover:text-foreground transition-colors hidden sm:block">Documentation</Link>
              <Link href="/#quickstart" className="hover:text-foreground transition-colors hidden sm:block">Quickstart</Link>
              
              <div className="w-px h-4 bg-border hidden sm:block"></div>
              
              <a href="https://github.com/DevDarsh26/Quira" target="_blank" rel="noreferrer" className="flex items-center gap-2 hover:text-foreground transition-colors">
                <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round" className="lucide lucide-github"><path d="M15 22v-4a4.8 4.8 0 0 0-1-3.03c3.15-.38 6.5-1.4 6.5-7.17a5.1 5.1 0 0 0-1.4-3.5 4.6 4.6 0 0 0-.1-3.4s-1.1-.35-3.5 1.3a11.5 11.5 0 0 0-6 0C6.1 2.5 5 2.85 5 2.85a4.6 4.6 0 0 0-.1 3.4 5.1 5.1 0 0 0-1.4 3.5c0 5.77 3.35 6.79 6.5 7.17A4.8 4.8 0 0 0 9 18v4"></path></svg>
                <span className="hidden sm:inline">GitHub</span>
              </a>
              <a href="https://pypi.org/project/quira/" target="_blank" rel="noreferrer" className="flex items-center gap-2 hover:text-foreground transition-colors">
                <FileText className="w-4 h-4" />
                <span className="hidden sm:inline">PyPI</span>
              </a>
            </nav>
          </div>
        </header>

        {/* Main Content */}
        <main className="flex-1 flex flex-col">
          {children}
        </main>
        
        {/* Footer */}
        <footer className="border-t border-border/40 py-8 text-center text-sm text-muted-foreground">
          <div className="container mx-auto px-6">
            <p>Built for the modern AI stack. Open source under the MIT License.</p>
            <p className="mt-2">Made by <a href="https://darshmodii.in" target="_blank" rel="noreferrer" className="text-foreground hover:underline font-medium">Darsh Modii</a></p>
          </div>
        </footer>

      </body>
    </html>
  );
}
