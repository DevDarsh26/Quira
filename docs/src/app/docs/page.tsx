import { Badge } from "@/components/ui/badge";
import { Terminal, Zap, Puzzle, GitPullRequest, Layers, Code2 } from "lucide-react";
import type { Metadata } from "next";
import { CopyButton } from "@/components/CopyButton";
import { AnimatedSection } from "@/components/AnimatedSection";
import { InstallTabs } from "@/components/InstallTabs";

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
      <AnimatedSection direction="none" className="mb-12">
        <div className="flex items-center text-sm font-medium text-zinc-500 mb-4">
          <span>Docs</span>
          <span className="mx-2">/</span>
          <span className="text-zinc-900 dark:text-zinc-100">Getting Started</span>
        </div>
        <h1 className="text-3xl md:text-4xl font-semibold tracking-tight mb-4 text-zinc-900 dark:text-white">
          Quira Framework
        </h1>
        <p className="text-lg text-zinc-600 dark:text-zinc-400 leading-relaxed max-w-2xl">
          The high-performance Retrieval Augmented Generation framework built from the ground up for token efficiency and zero perceived latency.
        </p>
      </AnimatedSection>

      <hr className="border-zinc-200 dark:border-white/10 mb-12" />

      {/* --- INSTALLATION --- */}
      <AnimatedSection direction="none" id="installation" className="scroll-mt-32 mb-20">
        <h2 className="text-2xl font-semibold tracking-tight mb-4 text-zinc-900 dark:text-white">
          Installation
        </h2>
        <p className="text-zinc-600 dark:text-zinc-400 mb-6 leading-relaxed">
          Quira is distributed via PyPI. We highly recommend installing the <code className="bg-zinc-100 dark:bg-white/10 px-1.5 py-0.5 rounded text-zinc-800 dark:text-zinc-200 font-mono text-[13px]">all</code> variant, which automatically pulls in the official client libraries for our supported vector databases and LLM providers.
        </p>
        
        <InstallTabs />

        <p className="text-[14px] text-zinc-500 dark:text-zinc-400 pl-4 border-l-2 border-zinc-200 dark:border-white/20">
          If you prefer a lightweight installation and want to manage dependencies yourself, use <code className="bg-zinc-100 dark:bg-white/10 px-1.5 py-0.5 rounded text-zinc-800 dark:text-zinc-200 font-mono">pip install quira</code>.
        </p>
      </AnimatedSection>

      {/* --- SPECULATIVE RETRIEVAL --- */}
      <AnimatedSection direction="none" id="speculative-retrieval" className="scroll-mt-32 mb-20">
        <h2 className="text-2xl font-semibold tracking-tight mb-4 text-zinc-900 dark:text-white">
          Speculative Retrieval
        </h2>
        <div className="prose prose-zinc dark:prose-invert max-w-none">
          <p className="text-zinc-600 dark:text-zinc-400 leading-relaxed">
            Standard RAG pipelines suffer from high latency because retrieval happens sequentially <em>after</em> the user submits their query. Network calls to vector databases (like Pinecone or Qdrant) can take anywhere from 200ms to over 500ms.
          </p>
          <div className="my-8 p-6 rounded-lg bg-zinc-50 dark:bg-white/[0.02] border border-zinc-200 dark:border-white/10">
            <h4 className="font-semibold mb-2 text-zinc-900 dark:text-white text-[15px]">
              How it works
            </h4>
            <div className="text-[14px] text-zinc-600 dark:text-zinc-400 m-0 leading-relaxed">
              Quira tracks keyboard typing speeds in your UI. It implements advanced debounce logic and <strong className="text-zinc-900 dark:text-white font-medium">speculatively searches the database while the user is still typing</strong>. By the time the user presses &quot;Enter&quot;, the relevant chunks are already loaded in local memory, reducing perceived latency to absolutely zero.
            </div>
          </div>
        </div>
      </AnimatedSection>

      {/* --- CONTEXT TETRIS --- */}
      <AnimatedSection direction="none" id="context-tetris" className="scroll-mt-32 mb-20">
        <h2 className="text-2xl font-semibold tracking-tight mb-4 text-zinc-900 dark:text-white">
          Context Tetris
        </h2>
        <p className="text-zinc-600 dark:text-zinc-400 leading-relaxed mb-6">
          Language models have strict context window limits. Instead of blindly passing the top-K retrieved chunks (which often leads to repetitive or irrelevant context), Quira employs a dynamic scoring algorithm. It intelligently packs the most valuable chunks into your remaining token budget based on four strict dimensions.
        </p>
        
        <div className="grid sm:grid-cols-2 gap-4">
          <div className="p-5 rounded-lg border border-zinc-200 dark:border-white/10 bg-white dark:bg-[#0a0a0a]">
            <h3 className="font-medium mb-1.5 text-zinc-900 dark:text-white text-[15px]">1. Relevance</h3>
            <p className="text-[14px] text-zinc-500 dark:text-zinc-400">Standard cosine similarity between the embedded query and the document chunks.</p>
          </div>
          <div className="p-5 rounded-lg border border-zinc-200 dark:border-white/10 bg-white dark:bg-[#0a0a0a]">
            <h3 className="font-medium mb-1.5 text-zinc-900 dark:text-white text-[15px]">2. Recency</h3>
            <p className="text-[14px] text-zinc-500 dark:text-zinc-400">Decay function applied to document creation dates to favor newer information.</p>
          </div>
          <div className="p-5 rounded-lg border border-zinc-200 dark:border-white/10 bg-white dark:bg-[#0a0a0a]">
            <h3 className="font-medium mb-1.5 text-zinc-900 dark:text-white text-[15px]">3. Diversity</h3>
            <p className="text-[14px] text-zinc-500 dark:text-zinc-400">Penalizes chunks that are too semantically similar to each other using MMR.</p>
          </div>
          <div className="p-5 rounded-lg border border-zinc-200 dark:border-white/10 bg-white dark:bg-[#0a0a0a]">
            <h3 className="font-medium mb-1.5 text-zinc-900 dark:text-white text-[15px]">4. Density</h3>
            <p className="text-[14px] text-zinc-500 dark:text-zinc-400">Extracts keyword density to prioritize factual information over filler text.</p>
          </div>
        </div>
      </AnimatedSection>

      {/* --- DIFFERENTIAL CONTEXT --- */}
      <AnimatedSection direction="none" id="differential-context" className="scroll-mt-32 mb-20">
        <h2 className="text-2xl font-semibold tracking-tight mb-4 text-zinc-900 dark:text-white">
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
      <AnimatedSection direction="none" id="provider-abstraction" className="scroll-mt-32 mb-20">
        <h2 className="text-2xl font-semibold tracking-tight mb-4 text-zinc-900 dark:text-white">
          Provider Abstraction
        </h2>
        <p className="text-zinc-600 dark:text-zinc-400 leading-relaxed mb-6">
          Quira exposes unified classes like <code className="bg-zinc-100 dark:bg-white/10 px-1.5 py-0.5 rounded text-zinc-800 dark:text-zinc-200 font-mono text-[13px]">BaseVectorStore</code> and <code className="bg-zinc-100 dark:bg-white/10 px-1.5 py-0.5 rounded text-zinc-800 dark:text-zinc-200 font-mono text-[13px]">BaseLLMProvider</code>. When writing your RAG application, you program against these interfaces. Swapping from Qdrant to Pinecone, or OpenAI to Anthropic, is literally a one-line config change.
        </p>

        <div className="rounded-lg overflow-hidden border border-zinc-200 dark:border-white/10 bg-white dark:bg-[#0a0a0a]">
          <div className="flex px-4 border-b border-zinc-200 dark:border-white/[0.06] bg-zinc-50 dark:bg-white/[0.02]">
            <div className="px-4 py-2.5 text-[13px] font-medium border-b-2 border-zinc-900 dark:border-white text-zinc-900 dark:text-white -mb-[1px]">pipeline.py</div>
          </div>
          <div className="p-5 font-mono text-[13px] leading-relaxed bg-zinc-900 dark:bg-transparent overflow-x-auto text-zinc-300">
            <span className="text-[#c678dd]">pipeline</span> = <span className="text-[#61afef]">quiraPipeline</span>(<br/>
            <span>    vector_store=</span><span className="text-[#98c379]">&quot;qdrant&quot;</span>,  <span className="text-zinc-500 italic"># or &quot;pinecone&quot;, &quot;weaviate&quot;</span><br/>
            <span>    llm=</span><span className="text-[#98c379]">&quot;anthropic/claude-3-opus&quot;</span>, <span className="text-zinc-500 italic"># or &quot;openai/gpt-4o&quot;</span><br/>
            <span>    cache=</span><span className="text-[#98c379]">&quot;redis&quot;</span><br/>
            )
          </div>
        </div>
      </AnimatedSection>

      {/* --- INTEGRATIONS --- */}
      <AnimatedSection direction="none" id="integrations" className="scroll-mt-32">
        <h2 className="text-2xl font-semibold tracking-tight mb-4 text-zinc-900 dark:text-white">
          Integrations
        </h2>
        <div className="prose prose-zinc dark:prose-invert max-w-none">
          <p className="text-zinc-600 dark:text-zinc-400 leading-relaxed mb-6">
            We don&apos;t want to reinvent the wheel. If you have an existing application built on <strong>LangChain</strong> or <strong>LlamaIndex</strong>, you can use Quira seamlessly as a high-performance retrieval step.
          </p>

          <h3 className="text-lg font-semibold text-zinc-900 dark:text-white mt-8 mb-4">LangChain Compatible Retriever</h3>
          <p className="text-zinc-600 dark:text-zinc-400 text-sm mb-4">Quira provides a LangChain-compatible retriever class that conforms to the BaseRetriever interface.</p>
          <div className="rounded-lg overflow-hidden border border-zinc-200 dark:border-white/10 bg-white dark:bg-[#0a0a0a] mt-4">
            <div className="flex px-4 border-b border-zinc-200 dark:border-white/[0.06] bg-zinc-50 dark:bg-white/[0.02]">
              <div className="px-4 py-2.5 text-[13px] font-medium border-b-2 border-zinc-900 dark:border-white text-zinc-900 dark:text-white -mb-[1px]">retriever.py</div>
            </div>
            <div className="p-5 font-mono text-[13px] leading-relaxed bg-zinc-900 dark:bg-transparent overflow-x-auto text-zinc-300">
              <span className="text-[#c678dd]">from</span> quira.integrations <span className="text-[#c678dd]">import</span> QuiraRetriever<br/><br/>
              retriever = <span className="text-[#61afef]">QuiraRetriever</span>(pipeline=pipeline)<br/>
              docs = retriever.<span className="text-[#61afef]">invoke</span>(<span className="text-[#98c379]">&quot;How does context tetris work?&quot;</span>)
            </div>
          </div>
        </div>
      </AnimatedSection>
    </div>
  );
}
