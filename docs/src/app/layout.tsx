import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import Link from "next/link";
import Image from "next/image";
import { ThemeProvider } from "@/components/ThemeProvider";
import { ThemeToggle } from "@/components/ThemeToggle";
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
  alternates: {
    canonical: "/",
  },
  title: "Quira | Fast RAG Framework for Python",
  description: "Quira is a blazing fast, token-efficient Retrieval Augmented Generation (RAG) framework featuring Speculative Retrieval and Context Tetris for zero-latency AI.",
  keywords: ["RAG", "Fast RAG", "Retrieval Augmented Generation", "LLM", "Vector Database", "Speculative Retrieval", "Context Tetris", "Generative AI", "Python", "AI Framework", "Open Source RAG", "Python RAG framework", "Token efficient RAG", "Zero-latency RAG", "Fast Retrieval Augmented Generation"],
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
      suppressHydrationWarning
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased overflow-x-hidden`}
    >
      <body className="min-h-full flex flex-col bg-background text-foreground selection:bg-black/10 dark:selection:bg-white/10 overflow-x-hidden">
        <ThemeProvider attribute="class" defaultTheme="dark" enableSystem={false} disableTransitionOnChange>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify({
              "@context": "https://schema.org",
              "@graph": [
                {
                  "@type": "WebSite",
                  "@id": "https://quira.darshmodii.in/#website",
                  "url": "https://quira.darshmodii.in",
                  "name": "Quira Framework",
                  "description": "High-Performance RAG Framework for the Modern AI Stack",
                  "publisher": {
                    "@type": "Person",
                    "name": "Darsh Modii"
                  }
                },
                {
                  "@type": "SoftwareApplication",
                  "@id": "https://quira.darshmodii.in/#software",
                  "name": "Quira",
                  "description": "Quira is a token-efficient, zero-latency Retrieval Augmented Generation (RAG) framework featuring Speculative Retrieval and Context Tetris.",
                  "url": "https://quira.darshmodii.in",
                  "applicationCategory": "DeveloperApplication",
                  "operatingSystem": "OS Independent",
                  "offers": {
                    "@type": "Offer",
                    "price": "0.00",
                    "priceCurrency": "USD"
                  }
                }
              ]
            })
          }}
        />
        
        {/* Navbar */}
        <header className="sticky top-0 z-50 w-full border-b border-zinc-200 dark:border-white/6 bg-background/70 backdrop-blur-xl">
          <div className="max-w-[1100px] mx-auto px-4 sm:px-6 h-14 flex items-center justify-between">
            <Link href="/" className="flex items-center gap-2.5 hover:opacity-80 transition-opacity">
              <Image src="/quira_logo.png" alt="Quira" width={28} height={28} className="rounded-md" />
              <span className="font-semibold text-[15px] tracking-tight text-zinc-900 dark:text-zinc-100">Quira</span>
            </Link>
            
            <nav className="flex items-center gap-3 sm:gap-6 text-[13px] font-medium text-zinc-500">
              <Link href="/docs" className="hover:text-zinc-900 dark:hover:text-white transition-colors duration-150">Docs</Link>
              <Link href="/#features" className="hover:text-zinc-900 dark:hover:text-white transition-colors duration-150 hidden sm:block">Features</Link>
              <a href="https://pypi.org/project/quira/" target="_blank" rel="noreferrer" className="hover:text-zinc-900 dark:hover:text-white transition-colors duration-150 hidden sm:block">PyPI</a>
              <div className="w-px h-3.5 bg-zinc-200 dark:bg-white/8 hidden sm:block" />
              <a href="https://github.com/DevDarsh26/Quira" target="_blank" rel="noreferrer" className="flex items-center gap-1.5 hover:text-zinc-900 dark:hover:text-white transition-colors duration-150">
                <svg viewBox="0 0 24 24" width="15" height="15" stroke="currentColor" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round"><path d="M15 22v-4a4.8 4.8 0 0 0-1-3.03c3.15-.38 6.5-1.4 6.5-7.17a5.1 5.1 0 0 0-1.4-3.5 4.6 4.6 0 0 0-.1-3.4s-1.1-.35-3.5 1.3a11.5 11.5 0 0 0-6 0C6.1 2.5 5 2.85 5 2.85a4.6 4.6 0 0 0-.1 3.4 5.1 5.1 0 0 0-1.4 3.5c0 5.77 3.35 6.79 6.5 7.17A4.8 4.8 0 0 0 9 18v4" /></svg>
                <span className="hidden sm:inline">GitHub</span>
              </a>
              <ThemeToggle />
            </nav>
          </div>
        </header>

        {/* Main Content */}
        <main className="flex-1 flex flex-col relative w-full">
          {children}
        </main>
        
        {/* Footer */}
        <footer className="border-t border-zinc-200 dark:border-white/6 py-16 bg-zinc-50 dark:bg-black">
          <div className="max-w-[1100px] mx-auto px-4 sm:px-6">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mb-12">
              <div className="col-span-2 md:col-span-1">
                <Link href="/" className="flex items-center gap-2.5 mb-4">
                  <Image src="/quira_logo.png" alt="Quira" width={24} height={24} className="rounded-md grayscale opacity-80" />
                  <span className="font-semibold text-[15px] tracking-tight text-zinc-900 dark:text-zinc-100">Quira</span>
                </Link>
                <p className="text-xs text-zinc-500 max-w-xs leading-relaxed">
                  The high-performance Retrieval Augmented Generation framework built for zero latency.
                </p>
              </div>
              
              <div>
                <h4 className="font-semibold text-zinc-900 dark:text-white text-[13px] mb-4 tracking-tight">Product</h4>
                <ul className="space-y-2.5 text-[13px] text-zinc-500">
                  <li><Link href="/docs" className="hover:text-zinc-900 dark:hover:text-white transition-colors">Documentation</Link></li>
                  <li><Link href="/#features" className="hover:text-zinc-900 dark:hover:text-white transition-colors">Features</Link></li>
                  <li><a href="https://pypi.org/project/quira/" target="_blank" rel="noreferrer" className="hover:text-zinc-900 dark:hover:text-white transition-colors">PyPI</a></li>
                </ul>
              </div>

              <div>
                <h4 className="font-semibold text-zinc-900 dark:text-white text-[13px] mb-4 tracking-tight">Resources</h4>
                <ul className="space-y-2.5 text-[13px] text-zinc-500">
                  <li><a href="https://github.com/DevDarsh26/Quira/issues" target="_blank" rel="noreferrer" className="hover:text-zinc-900 dark:hover:text-white transition-colors">Issues</a></li>
                  <li><a href="https://github.com/DevDarsh26/Quira/discussions" target="_blank" rel="noreferrer" className="hover:text-zinc-900 dark:hover:text-white transition-colors">Discussions</a></li>
                  <li><a href="https://github.com/DevDarsh26/Quira" target="_blank" rel="noreferrer" className="hover:text-zinc-900 dark:hover:text-white transition-colors">GitHub Repository</a></li>
                </ul>
              </div>

              <div>
                <h4 className="font-semibold text-zinc-900 dark:text-white text-[13px] mb-4 tracking-tight">Company</h4>
                <ul className="space-y-2.5 text-[13px] text-zinc-500">
                  <li><a href="https://darshmodii.in" target="_blank" rel="noreferrer" className="hover:text-zinc-900 dark:hover:text-white transition-colors">Darsh Modii</a></li>
                  <li><a href="#" className="hover:text-zinc-900 dark:hover:text-white transition-colors">License</a></li>
                </ul>
              </div>
            </div>
            
            <div className="pt-8 border-t border-zinc-200 dark:border-white/10 flex flex-col md:flex-row items-center justify-between gap-4 text-xs text-zinc-500">
              <p>&copy; {new Date().getFullYear()} Quira. All rights reserved.</p>
              <div className="flex gap-4">
                <a href="#" className="hover:text-zinc-900 dark:hover:text-white transition-colors">Privacy Policy</a>
                <a href="#" className="hover:text-zinc-900 dark:hover:text-white transition-colors">Terms of Service</a>
              </div>
            </div>
          </div>
        </footer>

        </ThemeProvider>
      </body>
    </html>
  );
}
