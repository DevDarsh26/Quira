import Link from "next/link";
import { ArrowRight, ChevronRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import pkg from "../../package.json";
import { AnimatedSection } from "@/components/AnimatedSection";
import { CopyButton } from "@/components/CopyButton";
import { TerminalTypewriter } from "@/components/TerminalTypewriter";
import { ArchitectureDiagram } from "@/components/ArchitectureDiagram";
import { BenchmarksSection } from "@/components/BenchmarksSection";
import { FAQSection } from "@/components/FAQSection";

/* ── Syntax-highlighted code as raw HTML to avoid JSX escaping issues ── */
const codeHTML = `<span class="line"><span class="kw">from</span> quira <span class="kw">import</span> quiraPipeline, UserSession</span>
<span class="line"><span class="kw">from</span> quira.integrations <span class="kw">import</span> QuiraRetriever</span>
<span class="line"></span>
<span class="line">pipeline = quiraPipeline(</span>
<span class="line">    vector_store=<span class="str">&quot;qdrant&quot;</span>,</span>
<span class="line">    cache=<span class="str">&quot;redis&quot;</span>,</span>
<span class="line">    llm=<span class="str">&quot;openai/gpt-4o&quot;</span></span>
<span class="line">)</span>
<span class="line"></span>
<span class="line"><span class="cmt"># 100% LangChain compatible</span></span>
<span class="line">retriever = QuiraRetriever(pipeline=pipeline)</span>
<span class="line">docs = retriever.invoke(<span class="str">&quot;What is Context Tetris?&quot;</span>)</span>
<span class="line"></span>
<span class="line"><span class="cmt"># Full pipeline with streaming</span></span>
<span class="line">session = UserSession(<span class="str">&quot;user_123&quot;</span>)</span>
<span class="line"><span class="kw">async for</span> chunk <span class="kw">in</span> pipeline.process_submission_stream(</span>
<span class="line">    session, <span class="str">&quot;What is quantum mechanics?&quot;</span></span>
<span class="line">):</span>
<span class="line">    <span class="fn">print</span>(chunk, end=<span class="str">&quot;&quot;</span>, flush=<span class="const">True</span>)</span>`;

const codeSnippetRaw = `from quira import quiraPipeline, UserSession
from quira.integrations import QuiraRetriever

pipeline = quiraPipeline(
    vector_store="qdrant",
    cache="redis",
    llm="openai/gpt-4o"
)

# 100% LangChain compatible
retriever = QuiraRetriever(pipeline=pipeline)
docs = retriever.invoke("What is Context Tetris?")

# Full pipeline with streaming
session = UserSession("user_123")
async for chunk in pipeline.process_submission_stream(
    session, "What is quantum mechanics?"
):
    print(chunk, end="", flush=True)`;

const installCmd = `pip install "quira[litellm,qdrant]"`;

export default async function Home() {
  const version = pkg.version || "0.x.x";

  return (
    <div className="flex flex-col items-center w-full relative">

      {/* ── Background ── */}
      <div className="absolute inset-0 bg-grid -z-10 pointer-events-none" />

      {/* ══════════════════════════════════════════════════════════════
          HERO SECTION
      ══════════════════════════════════════════════════════════════ */}
      <section className="w-full max-w-[1100px] mx-auto px-4 sm:px-6 pt-14 pb-14 md:pt-24 md:pb-20 flex flex-col items-center text-center">

        {/* Version badge */}
        <AnimatedSection direction="up" delay={0}>
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-zinc-100 dark:bg-white/5 border border-zinc-200 dark:border-white/10 mb-8 cursor-default hover:bg-zinc-200 dark:hover:bg-white/10 transition-colors">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
            <span className="text-xs font-mono text-zinc-600 dark:text-zinc-300">v{version} is now available</span>
          </div>
        </AnimatedSection>

        {/* Headline */}
        <AnimatedSection direction="up" delay={0.08}>
          <h1 className="text-[2rem] sm:text-[2.75rem] md:text-[3.75rem] lg:text-[4.5rem] font-extrabold tracking-[-0.035em] leading-[1.08] max-w-3xl">
            <span className="text-zinc-900 dark:text-white">Build RAG that</span>
            <br />
            <span className="text-transparent bg-clip-text bg-linear-to-r from-zinc-500 to-zinc-900 dark:from-zinc-400 dark:to-zinc-600">
              actually performs.
            </span>
          </h1>
        </AnimatedSection>

        {/* Subheadline */}
        <AnimatedSection direction="up" delay={0.16}>
          <p className="mt-4 text-sm sm:text-[15px] md:text-base text-zinc-600 dark:text-zinc-500 max-w-xl leading-relaxed px-2 sm:px-0">
            A Python framework for retrieval-augmented generation.
            Speculative Retrieval eliminates latency. Context Tetris maximizes every token.
          </p>
        </AnimatedSection>

        {/* CTAs */}
        <AnimatedSection direction="up" delay={0.24}>
          <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 mt-8 w-full sm:w-auto">
            <Link href="/docs" className="w-full sm:w-auto">
              <Button
                size="lg"
                className="rounded-lg px-6 gap-2 text-[13px] h-10 font-semibold bg-zinc-900 text-white dark:bg-white dark:text-black hover:bg-zinc-800 dark:hover:bg-zinc-200 transition-all w-full"
              >
                Get Started <ArrowRight className="w-3.5 h-3.5" />
              </Button>
            </Link>
            <div className="flex items-center gap-2.5 h-10 bg-zinc-100 dark:bg-zinc-900/80 border border-zinc-200 dark:border-white/8 rounded-lg px-4 font-mono text-[13px] text-zinc-600 dark:text-zinc-400 w-full sm:w-auto overflow-hidden">
              <span className="text-zinc-400 dark:text-zinc-600 select-none shrink-0">$</span>
              <span className="text-zinc-700 dark:text-zinc-300 truncate">{installCmd}</span>
              <div className="shrink-0"><CopyButton text={installCmd} /></div>
            </div>
          </div>
        </AnimatedSection>

        {/* Metrics */}
        <AnimatedSection direction="up" delay={0.32}>
          <div className="grid grid-cols-3 gap-4 sm:gap-8 mt-12 pt-8 border-t border-zinc-200 dark:border-white/6 w-full max-w-sm sm:max-w-md">
            {[
              { value: "85%", label: "Lower latency" },
              { value: "2.6×", label: "Denser context" },
              { value: "40%", label: "Fewer tokens" },
            ].map((stat) => (
              <div key={stat.label} className="text-center">
                <div className="text-xl sm:text-2xl font-bold tracking-tight text-zinc-900 dark:text-white">{stat.value}</div>
                <div className="text-[10px] text-zinc-500 dark:text-zinc-600 mt-0.5 uppercase tracking-[0.12em] font-medium">{stat.label}</div>
              </div>
            ))}
          </div>
        </AnimatedSection>

      </section>

      {/* ══════════════════════════════════════════════════════════════
          FEATURES — Bento Grid
      ══════════════════════════════════════════════════════════════ */}
      <section id="features" className="w-full max-w-[1100px] mx-auto px-4 sm:px-6 py-14 md:py-20">

        <AnimatedSection direction="up" delay={0}>
          <div className="mb-10 text-center sm:text-left">
            <h2 className="text-2xl md:text-3xl font-bold text-zinc-900 dark:text-white mb-2 tracking-tight">Rethinking Retrieval</h2>
            <p className="text-[15px] text-zinc-500 max-w-lg">We stripped away the abstractions that make traditional RAG slow and token-hungry.</p>
          </div>
        </AnimatedSection>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-4 auto-rows-auto">

          {/* ── Speculative Retrieval (wide) ── */}
          <AnimatedSection direction="up" delay={0.06} className="sm:col-span-2 lg:col-span-4">
            <div className="group h-full rounded-2xl bg-white dark:bg-zinc-900/60 border border-zinc-200 dark:border-white/6 p-8 md:p-10 flex flex-col justify-between relative overflow-hidden transition-all duration-300 hover:border-zinc-300 dark:hover:border-white/12 hover:shadow-md dark:hover:bg-zinc-900/80">
              <div className="absolute -top-24 -right-24 w-64 h-64 rounded-full bg-emerald-500/10 dark:bg-white/3 blur-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
              <div className="relative z-10">
                <div className="w-12 h-12 rounded-xl bg-zinc-100 dark:bg-white/6 border border-zinc-200 dark:border-white/8 flex items-center justify-center mb-8">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-6 h-6 text-zinc-700 dark:text-zinc-300"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" strokeLinecap="round" strokeLinejoin="round"/></svg>
                </div>
                <h3 className="text-xl font-bold text-zinc-900 dark:text-white mb-3">Speculative Retrieval</h3>
                <p className="text-[15px] text-zinc-600 dark:text-zinc-400 leading-relaxed max-w-md">
                  Why wait for the LLM to finish thinking? Quira predicts the required context
                  and pre-fetches it asynchronously. By the time the LLM needs it, the data is already there.
                </p>
              </div>
            </div>
          </AnimatedSection>

          {/* ── Context Tetris ── */}
          <AnimatedSection direction="up" delay={0.12} className="sm:col-span-1 lg:col-span-2">
            <div className="group h-full rounded-2xl bg-white dark:bg-zinc-900/60 border border-zinc-200 dark:border-white/6 p-8 flex flex-col justify-between relative overflow-hidden transition-all duration-300 hover:border-zinc-300 dark:hover:border-white/12 hover:shadow-md dark:hover:bg-zinc-900/80">
              <div>
                <div className="w-10 h-10 rounded-xl bg-zinc-100 dark:bg-white/6 border border-zinc-200 dark:border-white/8 flex items-center justify-center mb-7">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-5 h-5 text-zinc-700 dark:text-zinc-300"><rect x="3" y="3" width="18" height="18" rx="2" ry="2" strokeLinecap="round" strokeLinejoin="round"/><line x1="3" y1="9" x2="21" y2="9" strokeLinecap="round" strokeLinejoin="round"/><line x1="9" y1="21" x2="9" y2="9" strokeLinecap="round" strokeLinejoin="round"/></svg>
                </div>
                <h3 className="text-lg font-bold text-zinc-900 dark:text-white mb-2">Context Tetris</h3>
                <p className="text-sm text-zinc-600 dark:text-zinc-400 leading-relaxed">
                  Packs context chunks with algorithmic precision. Achieves 2.6× higher information density.
                </p>
              </div>
            </div>
          </AnimatedSection>

          {/* ── Differential Context ── */}
          <AnimatedSection direction="up" delay={0.18} className="sm:col-span-1 lg:col-span-2">
            <div className="group h-full rounded-2xl bg-white dark:bg-zinc-900/60 border border-zinc-200 dark:border-white/6 p-8 flex flex-col justify-between relative overflow-hidden transition-all duration-300 hover:border-zinc-300 dark:hover:border-white/12 hover:shadow-md dark:hover:bg-zinc-900/80">
              <div>
                <div className="w-10 h-10 rounded-xl bg-zinc-100 dark:bg-white/6 border border-zinc-200 dark:border-white/8 flex items-center justify-center mb-7">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-5 h-5 text-zinc-700 dark:text-zinc-300"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" strokeLinecap="round" strokeLinejoin="round"/><polyline points="7.5 4.21 12 6.81 16.5 4.21" strokeLinecap="round" strokeLinejoin="round"/><polyline points="7.5 19.79 7.5 14.6 3 12" strokeLinecap="round" strokeLinejoin="round"/><polyline points="21 12 16.5 14.6 16.5 19.79" strokeLinecap="round" strokeLinejoin="round"/><polyline points="3.27 6.96 12 12.01 20.73 6.96" strokeLinecap="round" strokeLinejoin="round"/><line x1="12" y1="22.08" x2="12" y2="12" strokeLinecap="round" strokeLinejoin="round"/></svg>
                </div>
                <h3 className="text-lg font-bold text-zinc-900 dark:text-white mb-2">Differential States</h3>
                <p className="text-sm text-zinc-600 dark:text-zinc-400 leading-relaxed">
                  Only sends the delta of context updates to the LLM, slashing token costs by 40%.
                </p>
              </div>
            </div>
          </AnimatedSection>

          {/* ── Provider Abstraction (wide) ── */}
          <AnimatedSection direction="up" delay={0.24} className="sm:col-span-2 lg:col-span-4">
            <div className="group h-full rounded-2xl bg-white dark:bg-zinc-900/60 border border-zinc-200 dark:border-white/6 p-8 md:p-10 flex flex-col justify-between relative overflow-hidden transition-all duration-300 hover:border-zinc-300 dark:hover:border-white/12 hover:shadow-md dark:hover:bg-zinc-900/80">
              <div className="flex flex-col md:flex-row md:items-start gap-8">
                <div className="md:max-w-xs shrink-0">
                  <div className="w-10 h-10 rounded-xl bg-zinc-100 dark:bg-white/6 border border-zinc-200 dark:border-white/8 flex items-center justify-center mb-6">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-5 h-5 text-zinc-700 dark:text-zinc-300"><rect x="2" y="7" width="20" height="14" rx="2" ry="2" strokeLinecap="round" strokeLinejoin="round"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16" strokeLinecap="round" strokeLinejoin="round"/></svg>
                  </div>
                  <h3 className="text-lg font-bold text-zinc-900 dark:text-white mb-2">Provider Agnostic</h3>
                  <p className="text-sm text-zinc-600 dark:text-zinc-400 leading-relaxed">
                    Write code once. Swap out vector DBs, embedding models, and LLMs by changing a single string in your pipeline config.
                  </p>
                </div>
                <div className="flex-1 flex flex-wrap gap-2 mt-4 md:mt-0 items-center justify-center bg-zinc-50/50 dark:bg-black/20 rounded-xl p-4 md:p-6 border border-zinc-100 dark:border-white/5">
                  {[
                    { name: "Qdrant" },
                    { name: "Pinecone" },
                    { name: "Weaviate" },
                    { name: "Chroma" },
                    { name: "Redis" },
                    { name: "OpenAI" },
                    { name: "Anthropic" },
                    { name: "Ollama" },
                  ].map(p => (
                    <span 
                      key={p.name}
                      className="px-3 py-1.5 rounded-lg bg-zinc-100 dark:bg-white/4 border border-zinc-200 dark:border-white/6 text-xs font-medium text-zinc-600 dark:text-zinc-400 transition-colors hover:text-zinc-900 dark:hover:text-zinc-200 hover:border-zinc-300 dark:hover:border-white/12 cursor-default select-none"
                    >
                      {p.name}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </AnimatedSection>

        </div>

        {/* ── Architecture Flow ── */}
        <AnimatedSection direction="up" delay={0.3}>
          <div className="mt-24 mb-10 text-center">
            <h2 className="text-xl md:text-2xl font-bold text-zinc-900 dark:text-white mb-3 tracking-tight">How Quira Works</h2>
            <p className="text-[13px] md:text-sm text-zinc-500 max-w-xl mx-auto">
              A streamlined, high-performance RAG pipeline designed from the ground up for minimal latency.
            </p>
          </div>
          <ArchitectureDiagram />
        </AnimatedSection>
        
        {/* ── Benchmarks ── */}
        <AnimatedSection direction="up" delay={0.4}>
          <div className="mt-24 mb-10 text-center">
            <h2 className="text-xl md:text-2xl font-bold text-zinc-900 dark:text-white mb-3 tracking-tight">Performance at Scale</h2>
            <p className="text-[13px] md:text-sm text-zinc-500 max-w-xl mx-auto">
              Real-world metrics demonstrating the impact of Speculative Retrieval and Context Tetris.
            </p>
          </div>
          <BenchmarksSection />
        </AnimatedSection>

      </section>

      {/* ══════════════════════════════════════════════════════════════
          QUICKSTART — Code Showcase
      ══════════════════════════════════════════════════════════════ */}
      <section id="quickstart" className="w-full max-w-[1100px] mx-auto px-4 sm:px-6 py-14 md:py-20">
        <div className="flex flex-col lg:flex-row gap-10 lg:gap-20 items-start">

          {/* Left — Text */}
          <AnimatedSection direction="left" delay={0.06} className="lg:w-5/12 w-full lg:sticky lg:top-28">
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-zinc-500 mb-3">Quickstart</p>
            <h2 className="text-3xl md:text-4xl font-bold tracking-tight text-zinc-900 dark:text-white mb-6">
              Production-ready in minutes
            </h2>
            <p className="text-zinc-600 dark:text-zinc-400 text-base leading-relaxed mb-8">
              Initialize a pipeline, pick your providers, and integrate directly
              with LangChain or LlamaIndex. No boilerplate, no configuration hell.
            </p>
            <ul className="space-y-3 mb-10">
              {["pip install quira", "Drop-in LangChain retriever", "Automated vector packing", "Streaming first-class citizen"].map((item, i) => (
                <li key={i} className="flex items-center gap-3 text-sm text-zinc-700 dark:text-zinc-300">
                  <div className="w-5 h-5 rounded-full bg-emerald-100 dark:bg-white/10 flex items-center justify-center text-emerald-600 dark:text-white">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" className="w-3 h-3"><path d="M20 6L9 17l-5-5" strokeLinecap="round" strokeLinejoin="round"/></svg>
                  </div>
                  {item}
                </li>
              ))}
            </ul>
          </AnimatedSection>

          {/* Right — Code Editor */}
          <AnimatedSection direction="right" delay={0.12} className="lg:w-7/12 w-full">
            <div className="rounded-xl overflow-hidden border border-zinc-200 dark:border-white/8 bg-white dark:bg-[#0a0a0a] shadow-2xl shadow-zinc-200 dark:shadow-black/60 relative group max-w-full">
              {/* Title bar */}
              <div className="flex items-center px-4 py-3 bg-zinc-50 dark:bg-white/3 border-b border-zinc-200 dark:border-white/6">
                <div className="flex gap-[7px]">
                  <div className="w-[11px] h-[11px] rounded-full bg-[#ff5f56]" />
                  <div className="w-[11px] h-[11px] rounded-full bg-[#ffbd2e]" />
                  <div className="w-[11px] h-[11px] rounded-full bg-[#27c93f]" />
                </div>
                <div className="flex-1 text-center text-xs font-mono text-zinc-500 dark:text-zinc-600">main.py</div>
                <div className="opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                  <CopyButton text={codeSnippetRaw} />
                </div>
              </div>
              {/* Code content */}
              <style>{`
                .code-block .kw  { color: #c678dd; }
                .code-block .str { color: #98c379; }
                .code-block .cmt { color: #5c6370; font-style: italic; }
                .code-block .fn  { color: #61afef; }
                .code-block .const { color: #d19a66; }
              `}</style>
              <div className="p-4 sm:p-6 overflow-x-auto max-w-full dark:bg-transparent bg-zinc-900 rounded-b-xl">
                <TerminalTypewriter htmlContent={codeHTML} />
              </div>
            </div>
          </AnimatedSection>

        </div>
      </section>

      {/* ══════════════════════════════════════════════════════════════
          FAQ SECTION
      ══════════════════════════════════════════════════════════════ */}
      <FAQSection />

      {/* ══════════════════════════════════════════════════════════════
          CTA — Bottom
      ══════════════════════════════════════════════════════════════ */}
      <section className="w-full max-w-[1100px] mx-auto px-4 sm:px-6 py-14 md:py-20">
        <AnimatedSection direction="up" delay={0.06}>
          <div className="rounded-2xl border border-zinc-200 dark:border-white/6 bg-white dark:bg-zinc-900/40 shadow-sm dark:shadow-none p-10 md:p-14 text-center relative overflow-hidden">
            <div className="absolute inset-0 bg-grid opacity-10 dark:opacity-30 pointer-events-none" />
            <div className="relative z-10">
              <h2 className="text-3xl md:text-4xl font-bold tracking-tight text-zinc-900 dark:text-white mb-4">
                Ready to ship faster?
              </h2>
              <p className="text-zinc-600 dark:text-zinc-400 text-base max-w-lg mx-auto mb-8">
                Quira is open-source, MIT-licensed, and designed for teams that
                care about performance. Start building today.
              </p>
              <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-center gap-3 w-full sm:w-auto">
                <Link href="/docs" className="w-full sm:w-auto">
                  <Button
                    size="lg"
                    className="rounded-lg px-8 gap-2 text-sm h-11 font-semibold bg-zinc-900 text-white dark:bg-white dark:text-black hover:bg-zinc-800 dark:hover:bg-zinc-200 transition-all w-full"
                  >
                    Read the Docs <ArrowRight className="w-4 h-4" />
                  </Button>
                </Link>
                <a href="https://github.com/DevDarsh26/Quira" target="_blank" rel="noreferrer" className="w-full sm:w-auto">
                  <Button
                    size="lg"
                    variant="outline"
                    className="rounded-lg px-8 gap-2 text-sm h-11 font-semibold border-zinc-200 dark:border-white/10 hover:border-zinc-300 dark:hover:border-white/20 hover:bg-zinc-50 dark:hover:bg-white/5 transition-all w-full"
                  >
                    <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round"><path d="M15 22v-4a4.8 4.8 0 0 0-1-3.03c3.15-.38 6.5-1.4 6.5-7.17a5.1 5.1 0 0 0-1.4-3.5 4.6 4.6 0 0 0-.1-3.4s-1.1-.35-3.5 1.3a11.5 11.5 0 0 0-6 0C6.1 2.5 5 2.85 5 2.85a4.6 4.6 0 0 0-.1 3.4 5.1 5.1 0 0 0-1.4 3.5c0 5.77 3.35 6.79 6.5 7.17A4.8 4.8 0 0 0 9 18v4" /></svg>
                    Star on GitHub
                  </Button>
                </a>
              </div>
            </div>
          </div>
        </AnimatedSection>
      </section>

    </div>
  );
}
