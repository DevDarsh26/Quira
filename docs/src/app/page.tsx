import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Terminal, Zap, Layers, Puzzle, GitPullRequest, ArrowRight } from "lucide-react";
import Link from "next/link";
import fs from "fs";
import path from "path";

export default async function Home() {
  // Read version dynamically from pyproject.toml
  let version = "0.x.x";
  try {
    const tomlPath = path.join(process.cwd(), "../pyproject.toml");
    const tomlContent = fs.readFileSync(tomlPath, "utf8");
    const match = tomlContent.match(/version\s*=\s*"([^"]+)"/);
    if (match && match[1]) version = match[1];
  } catch (_) {
    console.error("Could not read pyproject.toml version");
  }

  return (
    <div className="flex flex-col items-center justify-start w-full">
      
      {/* HERO SECTION */}
      <section className="w-full max-w-6xl mx-auto px-6 py-24 md:py-32 flex flex-col items-center text-center gap-8 relative overflow-hidden">
        {/* Subtle background glow */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[400px] bg-primary/20 blur-[120px] rounded-full pointer-events-none -z-10" />
        
        <Badge variant="outline" className="px-4 py-1.5 text-sm rounded-full border-primary/30 bg-primary/5 text-primary">
          v{version} is now live on PyPI
        </Badge>
        
        <h1 className="text-5xl md:text-7xl font-extrabold tracking-tighter max-w-4xl bg-clip-text text-transparent bg-linear-to-br from-foreground via-foreground/90 to-muted-foreground">
          Faster, Smarter RAG for the Modern AI Stack
        </h1>
        
        <p className="text-lg md:text-xl text-muted-foreground max-w-2xl leading-relaxed">
          Quira optimizes Retrieval Augmented Generation using <strong>Speculative Retrieval</strong> and <strong>Context Tetris</strong> to deliver blazing fast context packing and unmatched token efficiency.
        </p>
        
        <div className="flex flex-col sm:flex-row gap-4 mt-4 w-full sm:w-auto">
          <Link href="/docs">
            <Button size="lg" className="rounded-full px-8 gap-2 text-base h-12">
              Get Started <ArrowRight className="w-4 h-4" />
            </Button>
          </Link>
          <a href="https://github.com/DevDarsh26/Quira" target="_blank" rel="noreferrer">
            <Button size="lg" variant="outline" className="rounded-full px-8 gap-2 text-base h-12 w-full sm:w-auto">
              View on GitHub
            </Button>
          </a>
        </div>
      </section>

      {/* FEATURES SECTION */}
      <section id="features" className="w-full bg-muted/30 border-y border-border/40 py-24">
        <div className="max-w-6xl mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold tracking-tight mb-4">Re-thinking Retrieval</h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">We ripped out the slow parts of standard RAG and replaced them with hyper-optimized algorithms.</p>
          </div>
          
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <Card className="bg-background/50 border-border/50 shadow-sm backdrop-blur transition-all hover:bg-background">
              <CardHeader>
                <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center mb-4 text-primary">
                  <Zap className="w-5 h-5" />
                </div>
                <CardTitle>Speculative Retrieval</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-base leading-relaxed">
                  Fetches vectors in the background while the user is still typing, eliminating perceived retrieval latency completely.
                </CardDescription>
              </CardContent>
            </Card>

            <Card className="bg-background/50 border-border/50 shadow-sm backdrop-blur transition-all hover:bg-background">
              <CardHeader>
                <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center mb-4 text-primary">
                  <Puzzle className="w-5 h-5" />
                </div>
                <CardTitle>Context Tetris</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-base leading-relaxed">
                  Packs context intelligently by scoring relevance, recency, density, and uniqueness to maximize your token budget.
                </CardDescription>
              </CardContent>
            </Card>

            <Card className="bg-background/50 border-border/50 shadow-sm backdrop-blur transition-all hover:bg-background">
              <CardHeader>
                <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center mb-4 text-primary">
                  <GitPullRequest className="w-5 h-5" />
                </div>
                <CardTitle>Differential Context</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-base leading-relaxed">
                  Maintains conversational state and only retrieves new &quot;delta&quot; chunks, significantly reducing redundant database hits.
                </CardDescription>
              </CardContent>
            </Card>
            
            <Card className="md:col-span-2 lg:col-span-3 bg-background/50 border-border/50 shadow-sm backdrop-blur mt-4">
              <CardHeader className="flex flex-row items-center gap-4 pb-4">
                <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center text-primary shrink-0">
                  <Layers className="w-5 h-5" />
                </div>
                <div>
                  <CardTitle>Provider Abstraction Layer</CardTitle>
                  <CardDescription className="mt-1">Write once, deploy anywhere.</CardDescription>
                </div>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground mb-4">
                  Seamlessly switch between Vector Stores, Cache Backends, and LLM Providers simply by changing a string. Quira supports everything from Qdrant and Redis to OpenAI, Groq, and Pinecone out of the box.
                </p>
                <div className="flex flex-wrap gap-2">
                  <Badge variant="secondary">Qdrant</Badge>
                  <Badge variant="secondary">Pinecone</Badge>
                  <Badge variant="secondary">Chroma</Badge>
                  <Badge variant="secondary">Weaviate</Badge>
                  <Badge variant="secondary">Redis</Badge>
                  <Badge variant="secondary">OpenAI</Badge>
                  <Badge variant="secondary">Anthropic</Badge>
                  <Badge variant="secondary">Groq</Badge>
                  <Badge variant="secondary">Ollama</Badge>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* QUICKSTART SECTION */}
      <section id="quickstart" className="w-full max-w-6xl mx-auto px-6 py-24">
        <div className="flex flex-col lg:flex-row items-center gap-12">
          <div className="lg:w-1/3 space-y-6">
            <h2 className="text-3xl font-bold tracking-tight">Zero-Friction Setup</h2>
            <p className="text-muted-foreground text-lg leading-relaxed">
              Quira is designed to be ridiculously easy to integrate. Install the package, define your providers, and you have a production-ready RAG pipeline.
            </p>
            <div className="p-4 rounded-xl bg-muted font-mono text-sm border border-border/50 flex items-center gap-3">
              <Terminal className="w-4 h-4 text-muted-foreground" />
              <span className="text-foreground">pip install &quot;quira[litellm,qdrant]&quot;</span>
            </div>
            <p className="text-sm text-muted-foreground">
              Supports LangChain and LlamaIndex natively via `QuiraRetriever` and `QuiraQueryEngine`.
            </p>
          </div>
          
          <div className="lg:w-2/3 w-full">
            <div className="rounded-xl overflow-hidden border border-border/40 shadow-2xl bg-[#0d0d0d]">
              <div className="flex items-center px-4 py-3 bg-white/5 border-b border-white/5 gap-2">
                <div className="w-3 h-3 rounded-full bg-red-500/80" />
                <div className="w-3 h-3 rounded-full bg-yellow-500/80" />
                <div className="w-3 h-3 rounded-full bg-green-500/80" />
                <span className="ml-2 text-xs font-medium text-muted-foreground font-mono">main.py</span>
              </div>
              <div className="p-4 sm:p-6 font-mono text-xs sm:text-sm text-zinc-300 leading-relaxed overflow-x-auto"><pre><code><span className="text-zinc-500"># 1. Install via pip</span>{"\n"}
<span className="text-zinc-300">pip install </span><span className="text-green-400">&quot;quira[litellm,qdrant]&quot;</span>{"\n\n"}
<span className="text-zinc-500"># 2. Setup your pipeline</span>{"\n"}
<span className="text-zinc-300">from quira import quiraPipeline, UserSession</span>{"\n"}
<span className="text-zinc-300">from quira.integrations import QuiraRetriever</span>{"\n\n"}
pipeline = quiraPipeline({"\n"}
    vector_store=<span className="text-green-400">&quot;qdrant&quot;</span>,{"\n"}
    cache=<span className="text-green-400">&quot;redis&quot;</span>,{"\n"}
    llm=<span className="text-green-400">&quot;openai/gpt-4o&quot;</span>{"\n"}
){"\n\n"}
<span className="text-zinc-500"># 100% LangChain compatible</span>{"\n"}
retriever = QuiraRetriever(pipeline=pipeline){"\n"}
docs = retriever.invoke(<span className="text-green-400">&quot;What is Context Tetris?&quot;</span>){"\n\n"}
<span className="text-zinc-500"># 3. Process a query (handles Tetris + Generation internally)</span>{"\n"}
session = UserSession(<span className="text-green-400">&quot;user_123&quot;</span>){"\n"}
<span className="text-zinc-500"># Use stream_sync for real-time output, or sync for a single block</span>{"\n"}
answer = pipeline.process_submission_sync(session, <span className="text-green-400">&quot;What is quantum mechanics?&quot;</span>){"\n\n"}
<span className="text-blue-400">print</span>(answer)</code></pre>
              </div>
            </div>
          </div>
        </div>
      </section>
      
    </div>
  );
}
