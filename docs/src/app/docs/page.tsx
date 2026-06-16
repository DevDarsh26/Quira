import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Terminal, Zap, Layers, Puzzle, GitPullRequest, Settings, Code2 } from "lucide-react";
import { Separator } from "@/components/ui/separator";

export default function DocsPage() {
  return (
    <div className="flex flex-col max-w-4xl pb-24">
      {/* Header */}
      <div className="mb-12">
        <Badge variant="secondary" className="mb-4">v0.2.0</Badge>
        <h1 className="text-4xl md:text-5xl font-extrabold tracking-tight mb-4">Quira Documentation</h1>
        <p className="text-xl text-muted-foreground leading-relaxed">
          The high-performance Retrieval Augmented Generation framework built for token efficiency and zero perceived latency.
        </p>
      </div>

      <Separator className="mb-12" />

      {/* --- INSTALLATION --- */}
      <section id="installation" className="mb-16 scroll-mt-24">
        <div className="flex items-center gap-2 mb-6">
          <Terminal className="w-6 h-6 text-primary" />
          <h2 className="text-3xl font-bold tracking-tight">Installation</h2>
        </div>
        <p className="text-lg text-muted-foreground mb-6">
          Quira is available on PyPI. You can install the core package or the full suite of providers.
        </p>
        
        <div className="grid md:grid-cols-2 gap-6">
          <Card className="bg-background shadow-sm">
            <CardHeader>
              <CardTitle className="text-lg">Full Installation (Recommended)</CardTitle>
              <CardDescription>Includes Qdrant, Pinecone, OpenAI, etc.</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="p-4 bg-[#0d0d0d] rounded-lg font-mono text-sm text-green-400 border border-white/10">
                pip install quira[all]
              </div>
            </CardContent>
          </Card>
          
          <Card className="bg-background shadow-sm">
            <CardHeader>
              <CardTitle className="text-lg">Core Only</CardTitle>
              <CardDescription>If you want to bring your own clients.</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="p-4 bg-[#0d0d0d] rounded-lg font-mono text-sm text-green-400 border border-white/10">
                pip install quira
              </div>
            </CardContent>
          </Card>
        </div>
      </section>

      <Separator className="mb-12" />

      {/* --- CORE CONCEPTS --- */}
      <section id="core-concepts" className="mb-16 scroll-mt-24">
        <div className="flex items-center gap-2 mb-6">
          <Settings className="w-6 h-6 text-primary" />
          <h2 className="text-3xl font-bold tracking-tight">Core Concepts</h2>
        </div>
        <p className="text-lg text-muted-foreground mb-8">
          Standard RAG is slow and wastes tokens. We built three core engines to solve this.
        </p>
        
        <div className="grid gap-6">
          <Card className="border-l-4 border-l-blue-500 bg-background/50">
            <CardHeader>
              <div className="flex items-center gap-2">
                <Zap className="w-5 h-5 text-blue-500" />
                <CardTitle>Speculative Retrieval</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="text-muted-foreground leading-relaxed">
              Fetching from vector databases takes time (often 200-500ms). Quira tracks keyboard typing speeds and debounces queries. It speculatively searches the database <strong>while the user is still typing</strong>. By the time they press &quot;Enter&quot;, the context is already loaded in memory.
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-purple-500 bg-background/50">
            <CardHeader>
              <div className="flex items-center gap-2">
                <Puzzle className="w-5 h-5 text-purple-500" />
                <CardTitle>Context Tetris</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="text-muted-foreground leading-relaxed">
              Language models have strict context limits. Instead of blindly passing the top-K chunks, Context Tetris scores chunks across four dimensions:
              <ul className="mt-4 space-y-2 list-disc list-inside marker:text-purple-500">
                <li><strong>Relevance:</strong> Cosine similarity to the query.</li>
                <li><strong>Recency:</strong> Newer chunks in the conversation decay slower.</li>
                <li><strong>Density:</strong> High keyword concentration gets a boost.</li>
                <li><strong>Uniqueness:</strong> Semantically identical chunks are penalized to prevent redundancy.</li>
              </ul>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-green-500 bg-background/50">
            <CardHeader>
              <div className="flex items-center gap-2">
                <GitPullRequest className="w-5 h-5 text-green-500" />
                <CardTitle>Differential Context</CardTitle>
              </div>
            </CardHeader>
            <CardContent className="text-muted-foreground leading-relaxed">
              Maintains an internal state of what the LLM already knows. On subsequent messages in the same session, Quira only fetches the &quot;delta&quot; (new information), avoiding expensive redundant database calls.
            </CardContent>
          </Card>
        </div>
      </section>

      <Separator className="mb-12" />

      {/* --- ARCHITECTURE --- */}
      <section id="provider-abstraction" className="mb-16 scroll-mt-24">
        <div className="flex items-center gap-2 mb-6">
          <Layers className="w-6 h-6 text-primary" />
          <h2 className="text-3xl font-bold tracking-tight">Provider Abstraction</h2>
        </div>
        <p className="text-lg text-muted-foreground mb-6">
          Don&apos;t get locked into a single vector database or LLM. Quira uses a unified abstraction layer. You can switch your entire infrastructure by changing a string.
        </p>

        <div className="rounded-xl overflow-hidden border border-border bg-[#0d0d0d] shadow-lg">
          <div className="flex items-center px-4 py-3 bg-white/5 border-b border-white/5 gap-2">
            <div className="w-3 h-3 rounded-full bg-red-500/80" />
            <div className="w-3 h-3 rounded-full bg-yellow-500/80" />
            <div className="w-3 h-3 rounded-full bg-green-500/80" />
            <span className="ml-2 text-xs font-medium text-muted-foreground font-mono">pipeline.py</span>
          </div>
          <div className="p-6 overflow-x-auto text-sm font-mono leading-relaxed text-zinc-300">
            <pre><code><span className="text-pink-400">from</span> quira <span className="text-pink-400">import</span> quiraPipeline{"\n\n"}
<span className="text-zinc-500"># Swap from Qdrant to Pinecone instantly</span>{"\n"}
pipeline = quiraPipeline({"\n"}
    vector_store=<span className="text-green-400">&quot;pinecone&quot;</span>,{"\n"}
    cache=<span className="text-green-400">&quot;redis&quot;</span>,{"\n"}
    llm=<span className="text-green-400">&quot;anthropic/claude-3-opus&quot;</span>{"\n"}
){"\n"}</code></pre>
          </div>
        </div>
      </section>

      <Separator className="mb-12" />

      {/* --- INTEGRATIONS --- */}
      <section id="integrations" className="mb-16 scroll-mt-24">
        <div className="flex items-center gap-2 mb-6">
          <Code2 className="w-6 h-6 text-primary" />
          <h2 className="text-3xl font-bold tracking-tight">Integrations</h2>
        </div>
        <p className="text-lg text-muted-foreground mb-6">
          Already using LangChain or LlamaIndex? Quira slides right in.
        </p>
        
        <div className="grid md:grid-cols-2 gap-6">
          <Card className="bg-background shadow-sm border-border">
            <CardHeader>
              <CardTitle>LangChain</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="p-4 bg-[#0d0d0d] rounded-lg font-mono text-xs leading-relaxed text-zinc-300 border border-white/10">
                <pre><code><span className="text-pink-400">from</span> quira.integrations <span className="text-pink-400">import</span> QuiraRetriever{"\n\n"}
<span className="text-zinc-500"># Drop-in replacement</span>{"\n"}
retriever = QuiraRetriever(pipeline=pipeline){"\n"}
docs = retriever.invoke(<span className="text-green-400">&quot;query&quot;</span>)</code></pre>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-background shadow-sm border-border">
            <CardHeader>
              <CardTitle>LlamaIndex</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="p-4 bg-[#0d0d0d] rounded-lg font-mono text-xs leading-relaxed text-zinc-300 border border-white/10">
                <pre><code><span className="text-pink-400">from</span> quira.integrations <span className="text-pink-400">import</span> QuiraQueryEngine{"\n\n"}
<span className="text-zinc-500"># Drop-in replacement</span>{"\n"}
engine = QuiraQueryEngine(pipeline=pipeline){"\n"}
res = engine.query(<span className="text-green-400">&quot;query&quot;</span>)</code></pre>
              </div>
            </CardContent>
          </Card>
        </div>
      </section>

    </div>
  );
}
