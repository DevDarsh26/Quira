import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Terminal, Zap, Layers, Puzzle, GitPullRequest, ArrowRight, Gauge, Shield, BarChart3 } from "lucide-react";
import Link from "next/link";
import pkg from "../../package.json";
import { AnimatedSection } from "@/components/AnimatedSection";
import { CopyButton } from "@/components/CopyButton";

export default async function Home() {
  const version = pkg.version || "0.x.x";

  const codeSnippet = `from quira import quiraPipeline, UserSession
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

  return (
    <div className="flex flex-col items-center justify-start w-full overflow-x-hidden">
      
      {/* HERO SECTION */}
      <section className="w-full relative">
        {/* Animated gradient orbs */}
        <div className="absolute top-[-200px] left-1/2 -translate-x-1/2 w-[800px] h-[600px] rounded-full bg-violet-600/20 blur-[120px] pointer-events-none animate-pulse" />
        <div className="absolute top-[100px] left-[-200px] w-[500px] h-[500px] rounded-full bg-blue-600/10 blur-[120px] pointer-events-none" />
        <div className="absolute top-[200px] right-[-200px] w-[400px] h-[400px] rounded-full bg-purple-600/10 blur-[120px] pointer-events-none" />
        
        <div className="w-full max-w-6xl mx-auto px-6 py-28 md:py-40 flex flex-col items-center text-center gap-8 relative z-10">
          <AnimatedSection direction="up" delay={0}>
            <Badge variant="outline" className="px-4 py-1.5 text-sm rounded-full border-primary/40 bg-primary/10 text-primary font-medium backdrop-blur-sm">
              🚀 v{version} — Now on PyPI
            </Badge>
          </AnimatedSection>
          
          <AnimatedSection direction="up" delay={0.1}>
            <h1 className="text-5xl md:text-7xl lg:text-8xl font-extrabold tracking-[-0.04em] max-w-5xl leading-[0.9]">
              <span className="bg-clip-text text-transparent bg-gradient-to-b from-white via-white/90 to-white/50">Faster, Smarter</span>
              <br />
              <span className="bg-clip-text text-transparent bg-gradient-to-r from-violet-400 via-blue-400 to-purple-500">RAG Framework</span>
            </h1>
          </AnimatedSection>
          
          <AnimatedSection direction="up" delay={0.2}>
            <p className="text-lg md:text-xl text-zinc-400 max-w-2xl leading-relaxed">
              Quira uses <strong className="text-white font-semibold">Speculative Retrieval</strong> and <strong className="text-white font-semibold">Context Tetris</strong> to deliver blazing fast context packing and unmatched token efficiency.
            </p>
          </AnimatedSection>
          
          <AnimatedSection direction="up" delay={0.3}>
            <div className="flex flex-col sm:flex-row gap-4 mt-2">
              <Link href="/docs">
                <Button size="lg" className="rounded-full px-8 gap-2 text-base h-12 font-semibold shadow-[0_0_30px_-5px] shadow-primary/40 hover:shadow-primary/60 transition-all duration-300 hover:scale-105">
                  Get Started <ArrowRight className="w-4 h-4" />
                </Button>
              </Link>
              <a href="https://github.com/DevDarsh26/Quira" target="_blank" rel="noreferrer">
                <Button size="lg" variant="outline" className="rounded-full px-8 gap-2 text-base h-12 font-semibold border-white/10 hover:border-white/25 hover:bg-white/5 transition-all duration-300 w-full sm:w-auto">
                  <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round"><path d="M15 22v-4a4.8 4.8 0 0 0-1-3.03c3.15-.38 6.5-1.4 6.5-7.17a5.1 5.1 0 0 0-1.4-3.5 4.6 4.6 0 0 0-.1-3.4s-1.1-.35-3.5 1.3a11.5 11.5 0 0 0-6 0C6.1 2.5 5 2.85 5 2.85a4.6 4.6 0 0 0-.1 3.4 5.1 5.1 0 0 0-1.4 3.5c0 5.77 3.35 6.79 6.5 7.17A4.8 4.8 0 0 0 9 18v4"></path></svg>
                  Star on GitHub
                </Button>
              </a>
            </div>
          </AnimatedSection>

          {/* Stats row */}
          <AnimatedSection direction="up" delay={0.4}>
            <div className="flex flex-wrap items-center justify-center gap-8 sm:gap-12 mt-8 text-sm text-zinc-500">
              <div className="flex items-center gap-2">
                <Gauge className="w-4 h-4 text-primary" />
                <span><strong className="text-white">85%</strong> faster latency</span>
              </div>
              <div className="flex items-center gap-2">
                <BarChart3 className="w-4 h-4 text-primary" />
                <span><strong className="text-white">2.6×</strong> denser context</span>
              </div>
              <div className="flex items-center gap-2">
                <Shield className="w-4 h-4 text-primary" />
                <span><strong className="text-white">40%</strong> cheaper tokens</span>
              </div>
            </div>
          </AnimatedSection>
        </div>
      </section>

      {/* FEATURES SECTION */}
      <section id="features" className="w-full border-t border-white/5 py-24 md:py-32 relative">
        <div className="absolute inset-0 bg-gradient-to-b from-transparent via-primary/[0.03] to-transparent pointer-events-none" />
        <div className="max-w-6xl mx-auto px-6 relative z-10">
          <AnimatedSection direction="up" delay={0}>
            <div className="text-center mb-16">
              <p className="text-primary font-semibold text-sm uppercase tracking-widest mb-3">Core Modules</p>
              <h2 className="text-3xl md:text-5xl font-bold tracking-tight mb-4">Re-thinking Retrieval</h2>
              <p className="text-zinc-400 max-w-2xl mx-auto text-lg">We ripped out the slow parts of standard RAG and replaced them with hyper-optimized algorithms.</p>
            </div>
          </AnimatedSection>
          
          <div className="grid md:grid-cols-3 gap-5">
            <AnimatedSection direction="up" delay={0.1} className="h-full">
              <Card className="bg-white/[0.03] border-white/[0.06] backdrop-blur-sm transition-all duration-300 hover:bg-white/[0.06] hover:border-primary/20 hover:shadow-[0_0_40px_-12px] hover:shadow-primary/20 h-full group">
                <CardHeader>
                  <div className="w-11 h-11 rounded-xl bg-gradient-to-br from-primary/20 to-primary/5 flex items-center justify-center mb-4 text-primary border border-primary/10 group-hover:scale-110 transition-transform duration-300">
                    <Zap className="w-5 h-5" />
                  </div>
                  <CardTitle className="text-lg">Speculative Retrieval</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-[15px] leading-relaxed text-zinc-400">
                    Fetches vectors in the background while the user is still typing, eliminating perceived retrieval latency completely.
                  </CardDescription>
                </CardContent>
              </Card>
            </AnimatedSection>

            <AnimatedSection direction="up" delay={0.2} className="h-full">
              <Card className="bg-white/[0.03] border-white/[0.06] backdrop-blur-sm transition-all duration-300 hover:bg-white/[0.06] hover:border-primary/20 hover:shadow-[0_0_40px_-12px] hover:shadow-primary/20 h-full group">
                <CardHeader>
                  <div className="w-11 h-11 rounded-xl bg-gradient-to-br from-primary/20 to-primary/5 flex items-center justify-center mb-4 text-primary border border-primary/10 group-hover:scale-110 transition-transform duration-300">
                    <Puzzle className="w-5 h-5" />
                  </div>
                  <CardTitle className="text-lg">Context Tetris</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-[15px] leading-relaxed text-zinc-400">
                    Packs context intelligently by scoring relevance, recency, density, and uniqueness to maximize your token budget.
                  </CardDescription>
                </CardContent>
              </Card>
            </AnimatedSection>

            <AnimatedSection direction="up" delay={0.3} className="h-full">
              <Card className="bg-white/[0.03] border-white/[0.06] backdrop-blur-sm transition-all duration-300 hover:bg-white/[0.06] hover:border-primary/20 hover:shadow-[0_0_40px_-12px] hover:shadow-primary/20 h-full group">
                <CardHeader>
                  <div className="w-11 h-11 rounded-xl bg-gradient-to-br from-primary/20 to-primary/5 flex items-center justify-center mb-4 text-primary border border-primary/10 group-hover:scale-110 transition-transform duration-300">
                    <GitPullRequest className="w-5 h-5" />
                  </div>
                  <CardTitle className="text-lg">Differential Context</CardTitle>
                </CardHeader>
                <CardContent>
                  <CardDescription className="text-[15px] leading-relaxed text-zinc-400">
                    Maintains conversational state and only retrieves new &quot;delta&quot; chunks, significantly reducing redundant database hits.
                  </CardDescription>
                </CardContent>
              </Card>
            </AnimatedSection>
          </div>
          
          {/* Provider Abstraction */}
          <AnimatedSection direction="up" delay={0.4} className="mt-6">
            <Card className="bg-white/[0.03] border-white/[0.06] backdrop-blur-sm transition-all duration-300 hover:bg-white/[0.06] hover:border-primary/20">
              <CardHeader className="flex flex-row items-center gap-4 pb-4">
                <div className="w-11 h-11 rounded-xl bg-gradient-to-br from-primary/20 to-primary/5 flex items-center justify-center text-primary shrink-0 border border-primary/10">
                  <Layers className="w-5 h-5" />
                </div>
                <div>
                  <CardTitle className="text-lg">Provider Abstraction Layer</CardTitle>
                  <CardDescription className="mt-1">Write once, deploy anywhere.</CardDescription>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-zinc-400 mb-5">
                  Seamlessly switch between Vector Stores, Cache Backends, and LLM Providers simply by changing a string.
                </p>
                <div className="flex flex-wrap gap-2">
                  {["Qdrant", "Pinecone", "Chroma", "Weaviate", "Supabase", "Redis", "OpenAI", "Anthropic", "Groq", "Ollama", "LiteLLM"].map((name) => (
                    <Badge key={name} variant="secondary" className="bg-white/5 border border-white/10 text-zinc-300 hover:bg-primary/10 hover:text-primary hover:border-primary/20 transition-all duration-200 cursor-default">
                      {name}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>
          </AnimatedSection>
        </div>
      </section>

      {/* QUICKSTART SECTION */}
      <section id="quickstart" className="w-full border-t border-white/5 py-24 md:py-32 relative">
        <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-[600px] h-[400px] rounded-full bg-[radial-gradient(ellipse_at_center,oklch(0.5_0.25_270/0.1),transparent_70%)] blur-[80px] pointer-events-none" />
        <div className="max-w-6xl mx-auto px-6 relative z-10">
          <div className="flex flex-col lg:flex-row items-start gap-12 lg:gap-16">
            <AnimatedSection direction="left" delay={0.1} className="lg:w-5/12 space-y-6 lg:sticky lg:top-28">
              <p className="text-primary font-semibold text-sm uppercase tracking-widest">Get Started</p>
              <h2 className="text-3xl md:text-4xl font-bold tracking-tight">Zero-Friction Setup</h2>
              <p className="text-zinc-400 text-lg leading-relaxed">
                Install the package, define your providers, and you have a production-ready RAG pipeline in under 10 lines of code.
              </p>
              
              {/* Install command */}
              <div className="rounded-xl bg-[#0a0a0a] border border-white/[0.08] overflow-hidden">
                <div className="flex items-center justify-between px-4 py-2.5 bg-white/[0.03] border-b border-white/[0.06]">
                  <div className="flex items-center gap-2 text-zinc-500 text-xs font-mono">
                    <Terminal className="w-3.5 h-3.5" />
                    terminal
                  </div>
                  <CopyButton text={installCmd} />
                </div>
                <div className="p-4 font-mono text-sm">
                  <span className="text-zinc-500">$ </span>
                  <span className="text-emerald-400">{installCmd}</span>
                </div>
              </div>

              <p className="text-sm text-zinc-500">
                Supports <strong className="text-zinc-300">LangChain</strong> and <strong className="text-zinc-300">LlamaIndex</strong> natively.
              </p>
            </AnimatedSection>
            
            {/* Code snippet */}
            <AnimatedSection direction="right" delay={0.3} className="lg:w-7/12 w-full">
              <div className="rounded-xl overflow-hidden border border-white/[0.08] shadow-2xl shadow-black/50 bg-[#0a0a0a]">
                <div className="flex items-center justify-between px-4 py-2.5 bg-white/[0.03] border-b border-white/[0.06]">
                  <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full bg-[#ff5f57]" />
                    <div className="w-3 h-3 rounded-full bg-[#febc2e]" />
                    <div className="w-3 h-3 rounded-full bg-[#28c840]" />
                    <span className="ml-3 text-xs text-zinc-500 font-mono">main.py</span>
                  </div>
                  <CopyButton text={codeSnippet} />
                </div>
                <div className="p-5 font-mono text-[13px] leading-[1.7] text-zinc-300 overflow-x-auto">
<pre><code><span className="text-violet-400">from</span> quira <span className="text-violet-400">import</span> quiraPipeline, UserSession{"\n"}
<span className="text-violet-400">from</span> quira.integrations <span className="text-violet-400">import</span> QuiraRetriever{"\n"}
{"\n"}
pipeline = quiraPipeline({"\n"}
    vector_store=<span className="text-emerald-400">&quot;qdrant&quot;</span>,{"\n"}
    cache=<span className="text-emerald-400">&quot;redis&quot;</span>,{"\n"}
    llm=<span className="text-emerald-400">&quot;openai/gpt-4o&quot;</span>{"\n"}
){"\n"}
{"\n"}
<span className="text-zinc-600"># 100% LangChain compatible</span>{"\n"}
retriever = QuiraRetriever(pipeline=pipeline){"\n"}
docs = retriever.invoke(<span className="text-emerald-400">&quot;What is Context Tetris?&quot;</span>){"\n"}
{"\n"}
<span className="text-zinc-600"># Full pipeline with streaming</span>{"\n"}
session = UserSession(<span className="text-emerald-400">&quot;user_123&quot;</span>){"\n"}
<span className="text-violet-400">async for</span> chunk <span className="text-violet-400">in</span> pipeline.process_submission_stream({"\n"}
    session, <span className="text-emerald-400">&quot;What is quantum mechanics?&quot;</span>{"\n"}
):{"\n"}
    <span className="text-sky-400">print</span>(chunk, end=<span className="text-emerald-400">&quot;&quot;</span>, flush=<span className="text-orange-400">True</span>)</code></pre>
                </div>
              </div>
            </AnimatedSection>
          </div>
        </div>
      </section>
      
    </div>
  );
}
