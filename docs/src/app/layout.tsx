import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { Github, FileText, Cpu } from "lucide-react";
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
  title: "Quira | Next-Gen RAG",
  description: "Faster and smarter Retrieval Augmented Generation using Speculative Retrieval and Context Tetris.",
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
        <header className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
          <div className="container mx-auto px-6 h-16 flex items-center justify-between">
            <div className="flex items-center gap-2 font-bold text-xl tracking-tighter">
              <div className="bg-primary text-primary-foreground p-1.5 rounded-lg">
                <Cpu className="w-5 h-5" />
              </div>
              Quira
            </div>
            
            <nav className="flex items-center gap-6 text-sm font-medium text-muted-foreground">
              <a href="#features" className="hover:text-foreground transition-colors hidden sm:block">Features</a>
              <a href="#quickstart" className="hover:text-foreground transition-colors hidden sm:block">Quickstart</a>
              
              <div className="w-px h-4 bg-border hidden sm:block"></div>
              
              <a href="https://github.com/DevDarsh26/Quira" target="_blank" rel="noreferrer" className="flex items-center gap-2 hover:text-foreground transition-colors">
                <Github className="w-4 h-4" />
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
          </div>
        </footer>

      </body>
    </html>
  );
}
