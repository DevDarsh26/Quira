import { ReactNode } from "react";

export default function DocsLayout({ children }: { children: ReactNode }) {
  return (
    <div className="container mx-auto px-6 flex-1 flex flex-col md:flex-row gap-12 py-12">
      <aside className="w-full md:w-64 shrink-0">
        <div className="sticky top-24 space-y-6">
          <div>
            <h4 className="font-semibold mb-3 text-foreground">Getting Started</h4>
            <div className="flex flex-col gap-2 text-sm text-muted-foreground">
              <a href="#introduction" className="hover:text-foreground transition-colors">Introduction</a>
              <a href="#installation" className="hover:text-foreground transition-colors">Installation</a>
            </div>
          </div>
          <div>
            <h4 className="font-semibold mb-3 text-foreground">Core Concepts</h4>
            <div className="flex flex-col gap-2 text-sm text-muted-foreground">
              <a href="#speculative-retrieval" className="hover:text-foreground transition-colors">Speculative Retrieval</a>
              <a href="#context-tetris" className="hover:text-foreground transition-colors">Context Tetris</a>
              <a href="#differential-context" className="hover:text-foreground transition-colors">Differential Context</a>
            </div>
          </div>
          <div>
            <h4 className="font-semibold mb-3 text-foreground">Architecture</h4>
            <div className="flex flex-col gap-2 text-sm text-muted-foreground">
              <a href="#provider-abstraction" className="hover:text-foreground transition-colors">Provider Abstraction</a>
              <a href="#integrations" className="hover:text-foreground transition-colors">Integrations</a>
            </div>
          </div>
        </div>
      </aside>
      
      <main className="flex-1 min-w-0">
        {children}
      </main>
    </div>
  );
}
