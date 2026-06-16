export default function DocsPage() {
  return (
    <article className="prose prose-zinc dark:prose-invert max-w-none pb-24">
      <h1 className="text-4xl font-extrabold tracking-tight mb-2">Quira Documentation</h1>
      <p className="text-xl text-muted-foreground mb-8">
        Learn how to integrate Quira into your modern AI stack to optimize Retrieval Augmented Generation.
      </p>

      {/* --- INTRODUCTION --- */}
      <h2 id="introduction" className="scroll-m-20 border-b pb-2">Introduction</h2>
      <p>
        <strong>Quira</strong> is a high-performance RAG optimization library designed to maximize token efficiency and minimize perceived latency. It achieves this by ripping out the slow parts of standard RAG pipelines and replacing them with highly-optimized, dynamic algorithms like <strong>Context Tetris</strong> and <strong>Speculative Retrieval</strong>.
      </p>

      {/* --- INSTALLATION --- */}
      <h2 id="installation" className="scroll-m-20 border-b pb-2 mt-12">Installation</h2>
      <p>Install Quira with all optional dependencies (including vector providers, caching, and embeddings) via pip:</p>
      <pre><code>pip install quira[all]</code></pre>
      <p>If you only want the core logic and plan to bring your own clients, simply use:</p>
      <pre><code>pip install quira</code></pre>

      {/* --- CORE CONCEPTS --- */}
      <h2 id="speculative-retrieval" className="scroll-m-20 border-b pb-2 mt-12">Speculative Retrieval</h2>
      <p>
        Retrieval latency is a massive bottleneck in conversational AI. Quira solves this by fetching vector contexts in the background <strong>while the user is still typing</strong>.
      </p>
      <ul>
        <li>Uses advanced debounce logic to detect typing speed.</li>
        <li>Searches the vector store speculatively before the user even presses 'Send'.</li>
        <li>Reduces perceived retrieval latency to <strong>zero</strong>.</li>
      </ul>

      <h2 id="context-tetris" className="scroll-m-20 border-b pb-2 mt-12">Context Tetris</h2>
      <p>
        Stop blindly stuffing contexts into your prompt. Context Tetris intelligently packs chunks into your token budget by scoring them across four dynamic dimensions:
      </p>
      <ol>
        <li><strong>Relevance Score:</strong> Semantic similarity to the query.</li>
        <li><strong>Recency Score:</strong> Temporal decay function ensuring newer chunks are prioritized.</li>
        <li><strong>Density Score:</strong> Analyzes keyword concentration inside the chunk.</li>
        <li><strong>Uniqueness Penalty:</strong> Penalizes chunks that are semantically identical to already-selected chunks.</li>
      </ol>

      <h2 id="differential-context" className="scroll-m-20 border-b pb-2 mt-12">Differential Context</h2>
      <p>
        Quira maintains an internal conversational state and a <em>context pool</em>. Instead of retrieving everything from scratch on every turn, it computes a "delta" and only pulls new information that hasn't been discussed yet.
      </p>

      {/* --- ARCHITECTURE --- */}
      <h2 id="provider-abstraction" className="scroll-m-20 border-b pb-2 mt-12">Provider Abstraction</h2>
      <p>
        Write your pipeline once, deploy it anywhere. Quira uses a robust provider abstraction layer that lets you switch infrastructure providers by simply passing a string.
      </p>
      <pre><code>{`from quira import quiraPipeline

pipeline = quiraPipeline(
    vector_store="qdrant",  # Or "pinecone", "chroma", "weaviate"
    cache="memory",         # Or "redis", "disk"
    llm="openai/gpt-4o"     # Or "groq", "anthropic", "ollama"
)`}</code></pre>

      <h2 id="integrations" className="scroll-m-20 border-b pb-2 mt-12">Integrations</h2>
      <p>Quira can be used natively inside your existing frameworks.</p>
      
      <h3>LangChain Integration</h3>
      <p>Use `QuiraRetriever` as a drop-in replacement for any LangChain retriever:</p>
      <pre><code>{`from quira.integrations import QuiraRetriever
from quira import quiraPipeline

pipeline = quiraPipeline(vector_store="qdrant")
retriever = QuiraRetriever(pipeline=pipeline)

# Use it in any LangChain chain
docs = retriever.invoke("What is quantum mechanics?")`}</code></pre>

      <h3>LlamaIndex Integration</h3>
      <p>Use `QuiraQueryEngine` as your primary query engine:</p>
      <pre><code>{`from quira.integrations import QuiraQueryEngine
from quira import quiraPipeline

pipeline = quiraPipeline(vector_store="qdrant")
engine = QuiraQueryEngine(pipeline=pipeline)

response = engine.query("What is quantum mechanics?")`}</code></pre>

    </article>
  );
}
