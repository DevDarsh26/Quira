import { AnimatedSection } from "./AnimatedSection";

const CHANGELOG_ITEMS = [
  {
    version: "v1.0.0",
    date: "July 25, 2026",
    title: "Enterprise Edition & Session Store",
    description: "Added RedisSessionStore for horizontal scaling and native observability with OpenTelemetry and LangSmith.",
  },
  {
    version: "v0.2.2",
    date: "June 22, 2026",
    title: "Streaming Output & Multi-Format Ingestion",
    description: "Added process_submission_stream and extended DocumentIngestor to natively parse .html, .docx, and .md.",
  },
  {
    version: "v0.2.1",
    date: "June 15, 2026",
    title: "Provider Abstraction Layer",
    description: "Initial implementation of PAL supporting Qdrant, Pinecone, Chroma, OpenAI, Anthropic, and Groq.",
  }
];

export function ChangelogSection() {
  return (
    <section className="w-full max-w-[1100px] mx-auto px-4 sm:px-6 py-14 md:py-24 border-t border-zinc-200 dark:border-white/5">
      <div className="flex flex-col lg:flex-row gap-12 lg:gap-24">
        {/* Left column */}
        <AnimatedSection direction="up" delay={0.1} className="lg:w-1/3">
          <div className="lg:sticky lg:top-28">
            <p className="text-xs font-semibold uppercase tracking-[0.2em] text-zinc-500 mb-3">08 — Changelog</p>
            <h2 className="text-3xl md:text-4xl font-bold tracking-tight text-zinc-900 dark:text-white mb-6">
              Shipping, in the open.
            </h2>
            <p className="text-zinc-600 dark:text-zinc-400 text-base leading-relaxed">
              We constantly iterate to make Quira faster, leaner, and more powerful. Here are the latest updates to the framework.
            </p>
          </div>
        </AnimatedSection>
        
        {/* Right column */}
        <div className="lg:w-2/3 flex flex-col gap-10 sm:gap-12 relative">
          {/* Vertical line connecting the timeline items (hidden on mobile) */}
          <div className="absolute left-[15px] top-4 bottom-4 w-px bg-zinc-200 dark:bg-white/10 hidden sm:block" />
          
          {CHANGELOG_ITEMS.map((item, i) => (
            <AnimatedSection key={item.version} direction="up" delay={0.1 + i * 0.1}>
              <div className="flex gap-6 relative">
                {/* Timeline dot */}
                <div className="hidden sm:flex shrink-0 w-8 h-8 rounded-full bg-zinc-50 dark:bg-[#0a0a0a] border-2 border-zinc-200 dark:border-white/20 items-center justify-center z-10 mt-1">
                  <div className="w-2 h-2 rounded-full bg-zinc-400 dark:bg-zinc-600" />
                </div>
                
                {/* Content */}
                <div className="flex-1">
                  <div className="flex flex-wrap items-center gap-3 mb-3">
                    <span className="px-2 py-0.5 rounded bg-zinc-100 dark:bg-white/10 text-xs font-mono font-medium text-zinc-800 dark:text-zinc-200">
                      {item.version}
                    </span>
                    <span className="text-sm text-zinc-500">{item.date}</span>
                  </div>
                  <h3 className="text-xl font-semibold text-zinc-900 dark:text-white mb-3 tracking-tight">
                    {item.title}
                  </h3>
                  <p className="text-zinc-600 dark:text-zinc-400 leading-relaxed text-[15px]">
                    {item.description}
                  </p>
                </div>
              </div>
            </AnimatedSection>
          ))}

          <AnimatedSection direction="up" delay={0.4}>
            <div className="flex gap-6 relative mt-4">
              <div className="hidden sm:block shrink-0 w-8" /> {/* Spacer to align with text */}
              <a 
                href="https://github.com/DevDarsh26/Quira/blob/main/CHANGELOG.md" 
                target="_blank" 
                rel="noreferrer"
                className="inline-flex items-center text-sm font-medium text-zinc-900 dark:text-white hover:opacity-70 transition-opacity"
              >
                View full changelog on GitHub 
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="w-4 h-4 ml-1"><path d="M5 12h14M12 5l7 7-7 7" strokeLinecap="round" strokeLinejoin="round"/></svg>
              </a>
            </div>
          </AnimatedSection>
        </div>
      </div>
    </section>
  );
}
