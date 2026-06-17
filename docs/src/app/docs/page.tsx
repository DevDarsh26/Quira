import { Badge } from "@/components/ui/badge";
import { Terminal, Zap, Puzzle, GitPullRequest, Layers, Code2 } from "lucide-react";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Documentation | Quira - Fast RAG Framework",
  description: "Learn how to install, configure, and use Quira's advanced RAG capabilities including Speculative Retrieval, Context Tetris, and Provider Abstractions for zero-latency AI.",
  keywords: ["RAG Documentation", "Fast RAG", "Retrieval Augmented Generation", "Python RAG Tutorial", "Speculative Retrieval", "Context Tetris", "Quira Framework"],
  alternates: {
    canonical: "/docs",
  },
};

export default function DocsPage() {
  return (
    <div className="flex flex-col pb-32">
      {/* Header */}
      <div className="mb-16">
        <Badge variant="outline" className="mb-6 border-primary/20 bg-primary/5 text-primary text-xs py-1 px-3">Version 0.2.0</Badge>
        <h1 className="text-4xl md:text-5xl font-bold tracking-tighter mb-6 text-foreground">
          Quira Documentation
        </h1>
        <p className="text-xl text-muted-foreground leading-relaxed max-w-2xl">
          The high-performance Retrieval Augmented Generation framework built from the ground up for token efficiency and zero perceived latency.
        </p>
      </div>

      <hr className="border-border/40 mb-16" />

      {/* --- INSTALLATION --- */}
      <section id="installation" className="scroll-mt-32 mb-24">
        <h2 className="text-2xl font-semibold tracking-tight flex items-center gap-3 mb-6">
          <Terminal className="w-5 h-5 text-muted-foreground" />
          Installation
        </h2>
        <p className="text-muted-foreground mb-6 leading-relaxed">
          Quira is distributed via PyPI. We highly recommend installing the <code>[all]</code> variant, which automatically pulls in the official client libraries for our supported vector databases and LLM providers.
        </p>
        
        <div className="rounded-xl overflow-hidden border border-border/60 bg-[#0a0a0a] shadow-xl mb-6">
          <div className="flex items-center px-4 py-2 bg-white/[0.02] border-b border-white/5">
            <span className="text-xs font-medium text-zinc-500 font-mono">Terminal</span>
          </div>
          <div className="p-5 font-mono text-sm">
            <span className="text-zinc-500 mr-4">$</span>
            <span className="text-zinc-300">pip install </span>
            <span className="text-green-400">&quot;quira[all]&quot;</span>
          </div>
        </div>

        <p className="text-sm text-muted-foreground pl-4 border-l-2 border-border/60">
          If you prefer a lightweight installation and want to manage dependencies yourself, use <code className="bg-muted px-1.5 py-0.5 rounded text-foreground">pip install quira</code>.
        </p>
      </section>

      {/* --- SPECULATIVE RETRIEVAL --- */}
      <section id="speculative-retrieval" className="scroll-mt-32 mb-24">
        <h2 className="text-2xl font-semibold tracking-tight flex items-center gap-3 mb-6">
          <Zap className="w-5 h-5 text-blue-500" />
          Speculative Retrieval
        </h2>
        <div className="prose prose-zinc dark:prose-invert max-w-none">
          <p className="text-muted-foreground leading-relaxed">
            Standard RAG pipelines suffer from high latency because retrieval happens sequentially <em>after</em> the user submits their query. Network calls to vector databases (like Pinecone or Qdrant) can take anywhere from 200ms to over 500ms.
          </p>
          <div className="my-8 p-6 rounded-xl bg-blue-500/5 border border-blue-500/20">
            <h4 className="text-blue-500 font-medium mb-2 flex items-center gap-2">
              <span className="relative flex h-2 w-2"><span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span><span className="relative inline-flex rounded-full h-2 w-2 bg-blue-500"></span></span>
              How it works
            </h4>
            <p className="text-sm text-muted-foreground m-0">
              Quira tracks keyboard typing speeds in your UI. It implements advanced debounce logic and <strong>speculatively searches the database while the user is still typing</strong>. By the time the user presses &quot;Enter&quot;, the relevant chunks are already loaded in local memory, reducing perceived latency to absolutely zero.
            </p>
          </div>
        </div>
      </section>

      {/* --- CONTEXT TETRIS --- */}
      <section id="context-tetris" className="scroll-mt-32 mb-24">
        <h2 className="text-2xl font-semibold tracking-tight flex items-center gap-3 mb-6">
          <Puzzle className="w-5 h-5 text-purple-500" />
          Context Tetris
        </h2>
        <p className="text-muted-foreground leading-relaxed mb-8">
          Language models have strict context window limits. Instead of blindly passing the top-K retrieved chunks (which often leads to repetitive or irrelevant context), Quira employs a dynamic scoring algorithm. It intelligently packs the most valuable chunks into your remaining token budget based on four strict dimensions.
        </p>
        
        <div className="grid sm:grid-cols-2 gap-4">
          <div className="p-5 rounded-xl border border-border/50 bg-background hover:border-purple-500/30 transition-colors">
            <h3 className="font-semibold mb-2">1. Relevance</h3>
            <p className="text-sm text-muted-foreground">Standard cosine similarity between the embedded query and the document chunks.</p>
          </div>
          <div className="p-5 rounded-xl border border-border/50 bg-background hover:border-purple-500/30 transition-colors">
            <h3 className="font-semibold mb-2">2. Recency</h3>
            <p className="text-sm text-muted-foreground">A temporal decay function. Newer chunks in the conversation history are penalized less than older chunks.</p>
          </div>
          <div className="p-5 rounded-xl border border-border/50 bg-background hover:border-purple-500/30 transition-colors">
            <h3 className="font-semibold mb-2">3. Density</h3>
            <p className="text-sm text-muted-foreground">Chunks with a high concentration of specific keywords related to the query receive a significant point boost.</p>
          </div>
          <div className="p-5 rounded-xl border border-border/50 bg-background hover:border-purple-500/30 transition-colors">
            <h3 className="font-semibold mb-2">4. Uniqueness</h3>
            <p className="text-sm text-muted-foreground">Semantically identical chunks are heavily penalized, preventing the LLM from reading the same information twice.</p>
          </div>
        </div>
      </section>

      {/* --- DIFFERENTIAL CONTEXT --- */}
      <section id="differential-context" className="scroll-mt-32 mb-24">
        <h2 className="text-2xl font-semibold tracking-tight flex items-center gap-3 mb-6">
          <GitPullRequest className="w-5 h-5 text-green-500" />
          Differential Context
        </h2>
        <p className="text-muted-foreground leading-relaxed">
          Quira maintains an internal conversational state. During a continuous session, the model already &quot;knows&quot; what it read in previous turns. Instead of fetching the entire knowledge base again, Quira computes a semantic delta and only fetches <strong>new information</strong> that hasn&apos;t been discussed yet. This drastically cuts down on redundant database hits and LLM token usage.
        </p>
      </section>

      {/* --- PROVIDER ABSTRACTION --- */}
      <section id="provider-abstraction" className="scroll-mt-32 mb-24">
        <h2 className="text-2xl font-semibold tracking-tight flex items-center gap-3 mb-6">
          <Layers className="w-5 h-5 text-orange-500" />
          Provider Abstraction
        </h2>
        <p className="text-muted-foreground leading-relaxed mb-6">
          Write your pipeline once, deploy it anywhere. Quira features a robust abstraction layer that allows you to swap your entire infrastructure (Vector Stores, Caches, and LLMs) simply by changing a string. No refactoring required.
        </p>

        <div className="rounded-xl overflow-hidden border border-border/60 bg-[#0a0a0a] shadow-xl">
          <div className="flex items-center px-4 py-3 bg-white/[0.02] border-b border-white/5 gap-2">
            <div className="w-2.5 h-2.5 rounded-full bg-zinc-700 hover:bg-red-500 transition-colors" />
            <div className="w-2.5 h-2.5 rounded-full bg-zinc-700 hover:bg-yellow-500 transition-colors" />
            <div className="w-2.5 h-2.5 rounded-full bg-zinc-700 hover:bg-green-500 transition-colors" />
            <span className="ml-3 text-xs font-medium text-zinc-500 font-mono">pipeline.py</span>
          </div>
          <div className="p-6 overflow-x-auto text-sm font-mono leading-relaxed text-zinc-300">
            <pre><code><span className="text-pink-400">from</span> quira <span className="text-pink-400">import</span> quiraPipeline{"\n\n"}
<span className="text-zinc-500"># Instantly swap providers without changing your business logic</span>{"\n"}
pipeline = quiraPipeline({"\n"}
    vector_store=<span className="text-green-400">&quot;pinecone&quot;</span>,        <span className="text-zinc-500"># Or: qdrant, chroma, weaviate</span>{"\n"}
    cache=<span className="text-green-400">&quot;redis&quot;</span>,                 <span className="text-zinc-500"># Or: memory, disk</span>{"\n"}
    llm=<span className="text-green-400">&quot;anthropic/claude-3-opus&quot;</span>  <span className="text-zinc-500"># Or: openai, groq, ollama</span>{"\n"}
){"\n"}</code></pre>
          </div>
        </div>
      </section>

      {/* --- INTEGRATIONS --- */}
      <section id="integrations" className="scroll-mt-32">
        <h2 className="text-2xl font-semibold tracking-tight flex items-center gap-3 mb-6">
          <Code2 className="w-5 h-5 text-indigo-500" />
          Integrations
        </h2>
        <p className="text-muted-foreground leading-relaxed mb-8">
          Quira is designed to be a drop-in upgrade for the frameworks you already use. We provide native wrappers for both LangChain and LlamaIndex.
        </p>
        
        <div className="space-y-6">
          <div className="rounded-xl border border-border/50 bg-background/30 p-6">
            <h3 className="font-semibold mb-4 flex items-center gap-2">
              LangChain Retriever
            </h3>
            <div className="rounded-lg overflow-hidden border border-border/60 bg-[#0a0a0a]">
              <div className="p-4 text-xs font-mono leading-relaxed text-zinc-300 overflow-x-auto">
                <pre><code><span className="text-pink-400">from</span> quira.integrations <span className="text-pink-400">import</span> QuiraRetriever{"\n\n"}
retriever = QuiraRetriever(pipeline=pipeline){"\n"}
docs = retriever.invoke(<span className="text-green-400">&quot;What is speculative retrieval?&quot;</span>)</code></pre>
              </div>
            </div>
          </div>

          <div className="rounded-xl border border-border/50 bg-background/30 p-6">
            <h3 className="font-semibold mb-4 flex items-center gap-2">
              LlamaIndex Query Engine
            </h3>
            <div className="rounded-lg overflow-hidden border border-border/60 bg-[#0a0a0a]">
              <div className="p-4 text-xs font-mono leading-relaxed text-zinc-300 overflow-x-auto">
                <pre><code><span className="text-pink-400">from</span> quira.integrations <span className="text-pink-400">import</span> QuiraQueryEngine{"\n\n"}
engine = QuiraQueryEngine(pipeline=pipeline){"\n"}
response = engine.query(<span className="text-green-400">&quot;What is context tetris?&quot;</span>)</code></pre>
              </div>
            </div>
          </div>
        </div>
      </section>

    </div>
  );
}
