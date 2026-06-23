import { Badge } from "@/components/ui/badge";
import { Terminal, Zap, Puzzle, GitPullRequest, Layers, Code2 } from "lucide-react";
import type { Metadata } from "next";
import { CopyButton } from "@/components/CopyButton";
import { AnimatedSection } from "@/components/AnimatedSection";

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
      <AnimatedSection direction="up" delay={0.1} className="mb-16">
        <Badge variant="outline" className="mb-6 border-primary/20 bg-primary/5 text-primary text-xs py-1 px-3">Version 0.2.0</Badge>
        <h1 className="text-4xl md:text-5xl font-bold tracking-tighter mb-6 text-foreground">
          Quira Documentation
        </h1>
        <p className="text-xl text-muted-foreground leading-relaxed max-w-2xl">
          The high-performance Retrieval Augmented Generation framework built from the ground up for token efficiency and zero perceived latency.
        </p>
      </AnimatedSection>

      <hr className="border-border/40 mb-16" />

      {/* --- INSTALLATION --- */}
      <AnimatedSection direction="up" delay={0.2} id="installation" className="scroll-mt-32 mb-24">
        <h2 className="text-2xl font-semibold tracking-tight flex items-center gap-3 mb-6">
          <Terminal className="w-5 h-5 text-muted-foreground" />
          Installation
        </h2>
        <p className="text-muted-foreground mb-6 leading-relaxed">
          Quira is distributed via PyPI. We highly recommend installing the <code className="bg-white/10 px-1 rounded text-white">all</code> variant, which automatically pulls in the official client libraries for our supported vector databases and LLM providers.
        </p>
        
        <div className="rounded-xl overflow-hidden border border-white/10 bg-[#0a0a0a] shadow-xl mb-6">
          <div className="flex items-center justify-between px-4 py-2.5 bg-white/[0.03] border-b border-white/[0.06]">
            <span className="text-xs font-medium text-zinc-500 font-mono">Terminal</span>
            <CopyButton text={'pip install "quira[all]"'} />
          </div>
          <div className="p-5 font-mono text-sm">
            <span className="text-zinc-500 mr-4">$</span>
            <span className="text-zinc-300">pip install </span>
            <span className="text-emerald-400">&quot;quira[all]&quot;</span>
          </div>
        </div>

        <p className="text-sm text-muted-foreground pl-4 border-l-2 border-border/60">
          If you prefer a lightweight installation and want to manage dependencies yourself, use <code className="bg-white/10 px-1.5 py-0.5 rounded text-white">pip install quira</code>.
        </p>
      </AnimatedSection>

      {/* --- SPECULATIVE RETRIEVAL --- */}
      <AnimatedSection direction="up" delay={0.3} id="speculative-retrieval" className="scroll-mt-32 mb-24">
        <h2 className="text-2xl font-semibold tracking-tight flex items-center gap-3 mb-6">
          <div className="w-8 h-8 rounded-lg bg-blue-500/20 flex items-center justify-center text-blue-500 border border-blue-500/30">
            <Zap className="w-4 h-4" />
          </div>
          Speculative Retrieval
        </h2>
        <div className="prose prose-zinc dark:prose-invert max-w-none">
          <p className="text-muted-foreground leading-relaxed">
            Standard RAG pipelines suffer from high latency because retrieval happens sequentially <em>after</em> the user submits their query. Network calls to vector databases (like Pinecone or Qdrant) can take anywhere from 200ms to over 500ms.
          </p>
          <div className="my-8 p-6 rounded-xl bg-gradient-to-br from-blue-500/10 to-blue-500/5 border border-blue-500/20 backdrop-blur-sm">
            <h4 className="text-blue-400 font-medium mb-3 flex items-center gap-2 text-lg">
              <span className="relative flex h-2 w-2"><span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span><span className="relative inline-flex rounded-full h-2 w-2 bg-blue-500"></span></span>
              How it works
            </h4>
            <p className="text-[15px] text-zinc-300 m-0 leading-relaxed">
              Quira tracks keyboard typing speeds in your UI. It implements advanced debounce logic and <strong className="text-white font-semibold">speculatively searches the database while the user is still typing</strong>. By the time the user presses &quot;Enter&quot;, the relevant chunks are already loaded in local memory, reducing perceived latency to absolutely zero.
            </p>
          </div>
        </div>
      </AnimatedSection>

      {/* --- CONTEXT TETRIS --- */}
      <AnimatedSection direction="up" delay={0.4} id="context-tetris" className="scroll-mt-32 mb-24">
        <h2 className="text-2xl font-semibold tracking-tight flex items-center gap-3 mb-6">
          <div className="w-8 h-8 rounded-lg bg-purple-500/20 flex items-center justify-center text-purple-500 border border-purple-500/30">
            <Puzzle className="w-4 h-4" />
          </div>
          Context Tetris
        </h2>
        <p className="text-muted-foreground leading-relaxed mb-8">
          Language models have strict context window limits. Instead of blindly passing the top-K retrieved chunks (which often leads to repetitive or irrelevant context), Quira employs a dynamic scoring algorithm. It intelligently packs the most valuable chunks into your remaining token budget based on four strict dimensions.
        </p>
        
        <div className="grid sm:grid-cols-2 gap-5">
          <div className="p-6 rounded-xl border border-white/10 bg-white/[0.02] hover:bg-white/[0.04] hover:border-purple-500/40 transition-all duration-300">
            <h3 className="font-semibold mb-2 text-white">1. Relevance</h3>
            <p className="text-sm text-zinc-400">Standard cosine similarity between the embedded query and the document chunks.</p>
          </div>
          <div className="p-6 rounded-xl border border-white/10 bg-white/[0.02] hover:bg-white/[0.04] hover:border-purple-500/40 transition-all duration-300">
            <h3 className="font-semibold mb-2 text-white">2. Recency</h3>
            <p className="text-sm text-zinc-400">A temporal decay function. Newer chunks in the conversation history are penalized less than older chunks.</p>
          </div>
          <div className="p-6 rounded-xl border border-white/10 bg-white/[0.02] hover:bg-white/[0.04] hover:border-purple-500/40 transition-all duration-300">
            <h3 className="font-semibold mb-2 text-white">3. Density</h3>
            <p className="text-sm text-zinc-400">Chunks with a high concentration of specific keywords related to the query receive a significant point boost.</p>
          </div>
          <div className="p-6 rounded-xl border border-white/10 bg-white/[0.02] hover:bg-white/[0.04] hover:border-purple-500/40 transition-all duration-300">
            <h3 className="font-semibold mb-2 text-white">4. Uniqueness</h3>
            <p className="text-sm text-zinc-400">Semantically identical chunks are heavily penalized, preventing the LLM from reading the same information twice.</p>
          </div>
        </div>
      </AnimatedSection>

      {/* --- DIFFERENTIAL CONTEXT --- */}
      <AnimatedSection direction="up" delay={0.5} id="differential-context" className="scroll-mt-32 mb-24">
        <h2 className="text-2xl font-semibold tracking-tight flex items-center gap-3 mb-6">
          <div className="w-8 h-8 rounded-lg bg-green-500/20 flex items-center justify-center text-green-500 border border-green-500/30">
            <GitPullRequest className="w-4 h-4" />
          </div>
          Differential Context
        </h2>
        <p className="text-muted-foreground leading-relaxed">
          Quira maintains an internal conversational state. During a continuous session, the model already &quot;knows&quot; what it read in previous turns. Instead of fetching the entire knowledge base again, Quira computes a semantic delta and only fetches <strong className="text-white font-semibold">new information</strong> that hasn&apos;t been discussed yet. This drastically cuts down on redundant database hits and LLM token usage.
        </p>
      </AnimatedSection>

      {/* --- PROVIDER ABSTRACTION --- */}
      <AnimatedSection direction="up" delay={0.6} id="provider-abstraction" className="scroll-mt-32 mb-24">
        <h2 className="text-2xl font-semibold tracking-tight flex items-center gap-3 mb-6">
          <div className="w-8 h-8 rounded-lg bg-orange-500/20 flex items-center justify-center text-orange-500 border border-orange-500/30">
            <Layers className="w-4 h-4" />
          </div>
          Provider Abstraction
        </h2>
        <p className="text-muted-foreground leading-relaxed mb-6">
          Write your pipeline once, deploy it anywhere. Quira features a robust abstraction layer that allows you to swap your entire infrastructure (Vector Stores, Caches, and LLMs) simply by changing a string. No refactoring required.
        </p>

        <div className="rounded-xl overflow-hidden border border-white/10 bg-[#0a0a0a] shadow-xl group">
          <div className="flex items-center justify-between px-4 py-2.5 bg-white/[0.03] border-b border-white/[0.06]">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-[#ff5f57]" />
              <div className="w-3 h-3 rounded-full bg-[#febc2e]" />
              <div className="w-3 h-3 rounded-full bg-[#28c840]" />
              <span className="ml-3 text-xs font-medium text-zinc-500 font-mono">pipeline.py</span>
            </div>
            <div className="opacity-0 group-hover:opacity-100 transition-opacity">
              <CopyButton text={'from quira import quiraPipeline\n\n# Instantly swap providers without changing your business logic\npipeline = quiraPipeline(\n    vector_store="pinecone",        # Or: qdrant, chroma, weaviate\n    cache="redis",                 # Or: memory, disk\n    llm="anthropic/claude-3-opus"  # Or: openai, groq, ollama\n)'} />
            </div>
          </div>
          <div className="p-6 overflow-x-auto text-sm font-mono leading-relaxed text-zinc-300">
<pre><code><span className="text-violet-400">from</span> quira <span className="text-violet-400">import</span> quiraPipeline{"\n\n"}
<span className="text-zinc-600"># Instantly swap providers without changing your business logic</span>{"\n"}
pipeline = quiraPipeline({"\n"}
    vector_store=<span className="text-emerald-400">&quot;pinecone&quot;</span>,        <span className="text-zinc-600"># Or: qdrant, chroma, weaviate</span>{"\n"}
    cache=<span className="text-emerald-400">&quot;redis&quot;</span>,                 <span className="text-zinc-600"># Or: memory, disk</span>{"\n"}
    llm=<span className="text-emerald-400">&quot;anthropic/claude-3-opus&quot;</span>  <span className="text-zinc-600"># Or: openai, groq, ollama</span>{"\n"}
){"\n"}</code></pre>
          </div>
        </div>
      </AnimatedSection>

      {/* --- RESILIENCE & FALLBACKS --- */}
      <AnimatedSection direction="up" delay={0.7} id="resilience" className="scroll-mt-32 mb-24">
        <h2 className="text-2xl font-semibold tracking-tight flex items-center gap-3 mb-6">
          <div className="w-8 h-8 rounded-lg bg-red-500/20 flex items-center justify-center text-red-500 border border-red-500/30">
            <svg className="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
          </div>
          Resilience &amp; Fallbacks
        </h2>
        <p className="text-muted-foreground leading-relaxed mb-6">
          Quira is built for production reliability. It features a robust <strong className="text-white font-semibold">Exception Hierarchy</strong> (<code className="bg-white/10 px-1 rounded text-white">QuiraError</code>) and transparent <strong className="text-white font-semibold">Retry &amp; Fallback Logic</strong>. All LLM and Vector Store network calls automatically retry up to 3 times with exponential backoff.
        </p>

        <div className="rounded-xl overflow-hidden border border-white/10 bg-[#0a0a0a] shadow-xl group">
          <div className="flex items-center justify-between px-4 py-2.5 bg-white/[0.03] border-b border-white/[0.06]">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-[#ff5f57]" />
              <div className="w-3 h-3 rounded-full bg-[#febc2e]" />
              <div className="w-3 h-3 rounded-full bg-[#28c840]" />
              <span className="ml-3 text-xs font-medium text-zinc-500 font-mono">fallbacks.py</span>
            </div>
            <div className="opacity-0 group-hover:opacity-100 transition-opacity">
              <CopyButton text={'# Seamlessly failover to a backup provider if the primary goes down\npipeline = quiraPipeline(\n    llm="anthropic/claude-3-opus",\n    fallback_llm="openai/gpt-4o",\n    vector_store="pinecone",\n    fallback_vector_store="qdrant"\n)'} />
            </div>
          </div>
          <div className="p-6 overflow-x-auto text-[13px] font-mono leading-[1.7] text-zinc-300">
<pre><code><span className="text-zinc-600"># Seamlessly failover to a backup provider if the primary goes down</span>{"\n"}
pipeline = quiraPipeline({"\n"}
    llm=<span className="text-emerald-400">&quot;anthropic/claude-3-opus&quot;</span>,{"\n"}
    fallback_llm=<span className="text-emerald-400">&quot;openai/gpt-4o&quot;</span>,{"\n"}
    vector_store=<span className="text-emerald-400">&quot;pinecone&quot;</span>,{"\n"}
    fallback_vector_store=<span className="text-emerald-400">&quot;qdrant&quot;</span>{"\n"}
){"\n"}</code></pre>
          </div>
        </div>
      </AnimatedSection>

      {/* --- INTEGRATIONS --- */}
      <AnimatedSection direction="up" delay={0.8} id="integrations" className="scroll-mt-32">
        <h2 className="text-2xl font-semibold tracking-tight flex items-center gap-3 mb-6">
          <div className="w-8 h-8 rounded-lg bg-indigo-500/20 flex items-center justify-center text-indigo-400 border border-indigo-500/30">
            <Code2 className="w-4 h-4" />
          </div>
          Integrations
        </h2>
        <p className="text-muted-foreground leading-relaxed mb-8">
          Quira is designed to be a drop-in upgrade for the frameworks you already use. We provide native wrappers for both LangChain and LlamaIndex.
        </p>
        
        <div className="space-y-6">
          <div className="rounded-xl border border-white/10 bg-white/[0.02] p-6 hover:border-indigo-500/30 transition-all duration-300">
            <h3 className="font-semibold mb-4 flex items-center gap-2 text-white">
              LangChain Retriever
            </h3>
            <div className="rounded-lg overflow-hidden border border-white/10 bg-[#0a0a0a] group relative">
              <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity z-10">
                <CopyButton text={'from quira.integrations import QuiraRetriever\n\nretriever = QuiraRetriever(pipeline=pipeline)\ndocs = retriever.invoke("What is speculative retrieval?")'} />
              </div>
              <div className="p-5 text-[13px] font-mono leading-[1.7] text-zinc-300 overflow-x-auto">
<pre><code><span className="text-violet-400">from</span> quira.integrations <span className="text-violet-400">import</span> QuiraRetriever{"\n\n"}
retriever = QuiraRetriever(pipeline=pipeline){"\n"}
docs = retriever.invoke(<span className="text-emerald-400">&quot;What is speculative retrieval?&quot;</span>)</code></pre>
              </div>
            </div>
          </div>

          <div className="rounded-xl border border-white/10 bg-white/[0.02] p-6 hover:border-indigo-500/30 transition-all duration-300">
            <h3 className="font-semibold mb-4 flex items-center gap-2 text-white">
              LlamaIndex Query Engine
            </h3>
            <div className="rounded-lg overflow-hidden border border-white/10 bg-[#0a0a0a] group relative">
              <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity z-10">
                <CopyButton text={'from quira.integrations import QuiraQueryEngine\n\nengine = QuiraQueryEngine(pipeline=pipeline)\nresponse = engine.query("What is context tetris?")'} />
              </div>
              <div className="p-5 text-[13px] font-mono leading-[1.7] text-zinc-300 overflow-x-auto">
<pre><code><span className="text-violet-400">from</span> quira.integrations <span className="text-violet-400">import</span> QuiraQueryEngine{"\n\n"}
engine = QuiraQueryEngine(pipeline=pipeline){"\n"}
response = engine.query(<span className="text-emerald-400">&quot;What is context tetris?&quot;</span>)</code></pre>
              </div>
            </div>
          </div>
        </div>
      </AnimatedSection>

    </div>
  );
}
