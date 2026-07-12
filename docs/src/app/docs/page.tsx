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
        <Badge variant="outline" className="mb-6 border-zinc-900 dark:border-white/20 bg-zinc-100 dark:bg-white/5 text-zinc-800 dark:text-white text-xs py-1 px-3">Version 0.3.4</Badge>
        <h1 className="text-4xl md:text-5xl font-bold tracking-tighter mb-6 text-zinc-900 dark:text-white">
          Quira Documentation
        </h1>
        <p className="text-xl text-zinc-600 dark:text-zinc-400 leading-relaxed max-w-2xl">
          The high-performance Retrieval Augmented Generation framework built from the ground up for token efficiency and zero perceived latency.
        </p>
      </AnimatedSection>

      <hr className="border-zinc-200 dark:border-white/10 mb-16" />

      {/* --- INSTALLATION --- */}
      <AnimatedSection direction="up" delay={0.2} id="installation" className="scroll-mt-32 mb-24">
        <h2 className="text-2xl font-semibold tracking-tight flex items-center gap-3 mb-6 text-zinc-900 dark:text-white">
          <Terminal className="w-5 h-5 text-zinc-500 dark:text-zinc-400" />
          Installation
        </h2>
        <p className="text-zinc-600 dark:text-zinc-400 mb-6 leading-relaxed">
          Quira is distributed via PyPI. We highly recommend installing the <code className="bg-zinc-100 dark:bg-white/10 px-1 rounded text-zinc-800 dark:text-white font-mono text-sm">all</code> variant, which automatically pulls in the official client libraries for our supported vector databases and LLM providers.
        </p>
        
        <div className="rounded-xl overflow-hidden border border-zinc-200 dark:border-white/10 bg-white dark:bg-[#0a0a0a] shadow-xl mb-6">
          <div className="flex items-center justify-between px-4 py-2.5 bg-zinc-50 dark:bg-white/[0.03] border-b border-zinc-200 dark:border-white/[0.06]">
            <span className="text-xs font-medium text-zinc-500 font-mono">Terminal</span>
            <CopyButton text={'pip install "quira[all]"'} />
          </div>
          <div className="p-5 font-mono text-sm bg-zinc-900 dark:bg-transparent">
            <span className="text-zinc-500 mr-4">$</span>
            <span className="text-zinc-300">pip install </span>
            <span className="text-emerald-400">&quot;quira[all]&quot;</span>
          </div>
        </div>

        <p className="text-sm text-zinc-500 dark:text-zinc-400 pl-4 border-l-2 border-zinc-200 dark:border-white/20">
          If you prefer a lightweight installation and want to manage dependencies yourself, use <code className="bg-zinc-100 dark:bg-white/10 px-1.5 py-0.5 rounded text-zinc-800 dark:text-white font-mono">pip install quira</code>.
        </p>
      </AnimatedSection>

      {/* --- SPECULATIVE RETRIEVAL --- */}
      <AnimatedSection direction="up" delay={0.3} id="speculative-retrieval" className="scroll-mt-32 mb-24">
        <h2 className="text-2xl font-semibold tracking-tight flex items-center gap-3 mb-6 text-zinc-900 dark:text-white">
          <div className="w-8 h-8 rounded-lg bg-blue-100 dark:bg-blue-500/20 flex items-center justify-center text-blue-600 dark:text-blue-500 border border-blue-200 dark:border-blue-500/30">
            <Zap className="w-4 h-4" />
          </div>
          Speculative Retrieval
        </h2>
        <div className="prose prose-zinc dark:prose-invert max-w-none">
          <p className="text-zinc-600 dark:text-zinc-400 leading-relaxed">
            Standard RAG pipelines suffer from high latency because retrieval happens sequentially <em>after</em> the user submits their query. Network calls to vector databases (like Pinecone or Qdrant) can take anywhere from 200ms to over 500ms.
          </p>
          <div className="my-8 p-6 rounded-xl bg-blue-50 dark:bg-gradient-to-br dark:from-blue-500/10 dark:to-blue-500/5 border border-blue-200 dark:border-blue-500/20 backdrop-blur-sm">
            <h4 className="text-blue-700 dark:text-blue-400 font-medium mb-3 flex items-center gap-2 text-lg">
              <span className="relative flex h-2 w-2"><span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span><span className="relative inline-flex rounded-full h-2 w-2 bg-blue-500"></span></span>
              How it works
            </h4>
            <div className="text-[15px] text-zinc-700 dark:text-zinc-300 m-0 leading-relaxed">
              Quira tracks keyboard typing speeds in your UI. It implements advanced debounce logic and <strong className="text-zinc-900 dark:text-white font-semibold">speculatively searches the database while the user is still typing</strong>. By the time the user presses &quot;Enter&quot;, the relevant chunks are already loaded in local memory, reducing perceived latency to absolutely zero.
            </div>
          </div>
        </div>
      </AnimatedSection>

      {/* --- CONTEXT TETRIS --- */}
      <AnimatedSection direction="up" delay={0.4} id="context-tetris" className="scroll-mt-32 mb-24">
        <h2 className="text-2xl font-semibold tracking-tight flex items-center gap-3 mb-6 text-zinc-900 dark:text-white">
          <div className="w-8 h-8 rounded-lg bg-purple-100 dark:bg-purple-500/20 flex items-center justify-center text-purple-600 dark:text-purple-500 border border-purple-200 dark:border-purple-500/30">
            <Puzzle className="w-4 h-4" />
          </div>
          Context Tetris
        </h2>
        <p className="text-zinc-600 dark:text-zinc-400 leading-relaxed mb-8">
          Language models have strict context window limits. Instead of blindly passing the top-K retrieved chunks (which often leads to repetitive or irrelevant context), Quira employs a dynamic scoring algorithm. It intelligently packs the most valuable chunks into your remaining token budget based on four strict dimensions.
        </p>
        
        <div className="grid sm:grid-cols-2 gap-5">
          <div className="p-6 rounded-xl border border-zinc-200 dark:border-white/10 bg-white dark:bg-white/[0.02] hover:border-purple-300 dark:hover:border-purple-500/40 transition-all duration-300 shadow-sm dark:shadow-none">
            <h3 className="font-semibold mb-2 text-zinc-900 dark:text-white">1. Relevance</h3>
            <p className="text-sm text-zinc-600 dark:text-zinc-400">Standard cosine similarity between the embedded query and the document chunks.</p>
          </div>
          <div className="p-6 rounded-xl border border-zinc-200 dark:border-white/10 bg-white dark:bg-white/[0.02] hover:border-purple-300 dark:hover:border-purple-500/40 transition-all duration-300 shadow-sm dark:shadow-none">
            <h3 className="font-semibold mb-2 text-zinc-900 dark:text-white">2. Recency</h3>
            <p className="text-sm text-zinc-600 dark:text-zinc-400">Decay function applied to document creation dates to favor newer information.</p>
          </div>
          <div className="p-6 rounded-xl border border-zinc-200 dark:border-white/10 bg-white dark:bg-white/[0.02] hover:border-purple-300 dark:hover:border-purple-500/40 transition-all duration-300 shadow-sm dark:shadow-none">
            <h3 className="font-semibold mb-2 text-zinc-900 dark:text-white">3. Diversity</h3>
            <p className="text-sm text-zinc-600 dark:text-zinc-400">Penalizes chunks that are too semantically similar to each other using MMR.</p>
          </div>
          <div className="p-6 rounded-xl border border-zinc-200 dark:border-white/10 bg-white dark:bg-white/[0.02] hover:border-purple-300 dark:hover:border-purple-500/40 transition-all duration-300 shadow-sm dark:shadow-none">
            <h3 className="font-semibold mb-2 text-zinc-900 dark:text-white">4. Density</h3>
            <p className="text-sm text-zinc-600 dark:text-zinc-400">Extracts keyword density to prioritize factual information over filler text.</p>
          </div>
        </div>
      </AnimatedSection>

      {/* --- DIFFERENTIAL CONTEXT --- */}
      <AnimatedSection direction="up" delay={0.5} id="differential-context" className="scroll-mt-32 mb-24">
        <h2 className="text-2xl font-semibold tracking-tight flex items-center gap-3 mb-6 text-zinc-900 dark:text-white">
          <div className="w-8 h-8 rounded-lg bg-emerald-100 dark:bg-emerald-500/20 flex items-center justify-center text-emerald-600 dark:text-emerald-500 border border-emerald-200 dark:border-emerald-500/30">
            <GitPullRequest className="w-4 h-4" />
          </div>
          Differential Context
        </h2>
        <div className="prose prose-zinc dark:prose-invert max-w-none">
          <p className="text-zinc-600 dark:text-zinc-400 leading-relaxed">
            In a multi-turn chat session, standard frameworks continuously append the entire conversation history along with newly retrieved chunks to the prompt. This causes the token count to explode exponentially.
          </p>
          <p className="text-zinc-600 dark:text-zinc-400 leading-relaxed mt-4">
            Quira uses <strong>Differential Context</strong>. We maintain the state of the conversation on the server and only send the <em>delta</em> — the exact difference between the last state and the new state — to the LLM. 
          </p>
        </div>
      </AnimatedSection>

      {/* --- PROVIDER ABSTRACTION --- */}
      <AnimatedSection direction="up" delay={0.6} id="provider-abstraction" className="scroll-mt-32 mb-24">
        <h2 className="text-2xl font-semibold tracking-tight flex items-center gap-3 mb-6 text-zinc-900 dark:text-white">
          <div className="w-8 h-8 rounded-lg bg-orange-100 dark:bg-orange-500/20 flex items-center justify-center text-orange-600 dark:text-orange-500 border border-orange-200 dark:border-orange-500/30">
            <Layers className="w-4 h-4" />
          </div>
          Provider Abstraction
        </h2>
        <p className="text-zinc-600 dark:text-zinc-400 leading-relaxed mb-6">
          Quira exposes unified classes like <code className="bg-zinc-100 dark:bg-white/10 px-1 rounded text-zinc-800 dark:text-white font-mono text-sm">BaseVectorStore</code> and <code className="bg-zinc-100 dark:bg-white/10 px-1 rounded text-zinc-800 dark:text-white font-mono text-sm">BaseLLMProvider</code>. When writing your RAG application, you program against these interfaces. Swapping from Qdrant to Pinecone, or OpenAI to Anthropic, is literally a one-line config change.
        </p>

        <div className="rounded-xl overflow-hidden border border-zinc-200 dark:border-white/10 bg-white dark:bg-[#0a0a0a] shadow-xl">
          <div className="flex items-center justify-between px-4 py-2.5 bg-zinc-50 dark:bg-white/[0.03] border-b border-zinc-200 dark:border-white/[0.06]">
            <span className="text-xs font-medium text-zinc-500 font-mono">pipeline.py</span>
          </div>
          <div className="p-5 font-mono text-[13px] leading-relaxed bg-zinc-900 dark:bg-transparent overflow-x-auto">
            <span className="text-pink-400">pipeline</span> <span className="text-zinc-400">=</span> <span className="text-blue-400">quiraPipeline</span><span className="text-zinc-300">(</span><br/>
            <span className="text-zinc-300">    vector_store=</span><span className="text-green-400">&quot;qdrant&quot;</span><span className="text-zinc-300">,  </span><span className="text-zinc-500 italic"># or &quot;pinecone&quot;, &quot;weaviate&quot;</span><br/>
            <span className="text-zinc-300">    llm=</span><span className="text-green-400">&quot;anthropic/claude-3-opus&quot;</span><span className="text-zinc-300">, </span><span className="text-zinc-500 italic"># or &quot;openai/gpt-4o&quot;</span><br/>
            <span className="text-zinc-300">    cache=</span><span className="text-green-400">&quot;redis&quot;</span><br/>
            <span className="text-zinc-300">)</span>
          </div>
        </div>
      </AnimatedSection>

      {/* --- INTEGRATIONS --- */}
      <AnimatedSection direction="up" delay={0.7} id="integrations" className="scroll-mt-32">
        <h2 className="text-2xl font-semibold tracking-tight flex items-center gap-3 mb-6 text-zinc-900 dark:text-white">
          <div className="w-8 h-8 rounded-lg bg-pink-100 dark:bg-pink-500/20 flex items-center justify-center text-pink-600 dark:text-pink-500 border border-pink-200 dark:border-pink-500/30">
            <Code2 className="w-4 h-4" />
          </div>
          Integrations
        </h2>
        <div className="prose prose-zinc dark:prose-invert max-w-none">
          <p className="text-zinc-600 dark:text-zinc-400 leading-relaxed mb-6">
            We don&apos;t want to reinvent the wheel. If you have an existing application built on <strong>LangChain</strong> or <strong>LlamaIndex</strong>, you can use Quira seamlessly as a high-performance retrieval step.
          </p>

          <h3 className="text-lg font-semibold text-zinc-900 dark:text-white mt-8 mb-4">LangChain Compatible Retriever</h3>
          <p className="text-zinc-600 dark:text-zinc-400 text-sm mb-4">Quira provides a LangChain-compatible retriever class that conforms to the BaseRetriever interface.</p>
          <div className="rounded-xl overflow-hidden border border-zinc-200 dark:border-white/10 bg-white dark:bg-[#0a0a0a] shadow-xl">
            <div className="p-5 font-mono text-[13px] leading-relaxed bg-zinc-900 dark:bg-transparent overflow-x-auto">
              <span className="text-pink-400">from</span> <span className="text-zinc-300">quira.integrations</span> <span className="text-pink-400">import</span> <span className="text-zinc-300">QuiraRetriever</span><br/><br/>
              <span className="text-zinc-300">retriever = </span><span className="text-blue-400">QuiraRetriever</span><span className="text-zinc-300">(pipeline=pipeline)</span><br/>
              <span className="text-zinc-300">docs = retriever.</span><span className="text-blue-400">invoke</span><span className="text-zinc-300">(</span><span className="text-green-400">&quot;How does context tetris work?&quot;</span><span className="text-zinc-300">)</span>
            </div>
          </div>
        </div>
      </AnimatedSection>
    </div>
  );
}
