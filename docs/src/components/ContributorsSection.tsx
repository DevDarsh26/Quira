import { AnimatedSection } from "./AnimatedSection";

export function ContributorsSection() {
  // A mix of realistic looking GitHub avatars for demonstration.
  // In a real app, this would be fetched from the GitHub API.
  const avatars = [
    "DevDarsh26"
  ];

  return (
    <section className="w-full max-w-[1100px] mx-auto px-4 sm:px-6 py-14 md:py-24 border-t border-zinc-200 dark:border-white/5">
      <AnimatedSection direction="up" delay={0.1}>
        <div className="flex flex-col items-center text-center">
          <h2 className="text-3xl md:text-4xl font-bold tracking-tight text-zinc-900 dark:text-white mb-4">
            The people behind Quira
          </h2>
          <p className="text-zinc-600 dark:text-zinc-400 text-base max-w-xl mb-12">
            Every developer who has shipped code, docs, or fixes — pulled live from GitHub. Thank you. ♥
          </p>
          
          <div className="flex flex-wrap justify-center gap-3 max-w-3xl">
            {avatars.map((username, i) => (
              <a 
                key={i} 
                href={`https://github.com/${username}`} 
                target="_blank" 
                rel="noreferrer" 
                className="group relative"
              >
                <div className="w-12 h-12 sm:w-14 sm:h-14 rounded-full overflow-hidden border-2 border-white dark:border-[#0a0a0a] ring-2 ring-zinc-100 dark:ring-white/10 hover:ring-zinc-300 dark:hover:ring-white/30 transition-all hover:-translate-y-1 hover:shadow-lg bg-zinc-200 dark:bg-zinc-800">
                  <img 
                    src={`https://github.com/${username}.png?size=100`} 
                    alt={username} 
                    className="w-full h-full object-cover transition-all duration-300"
                    loading="lazy"
                  />
                </div>
              </a>
            ))}
            
            <a 
              href="https://github.com/DevDarsh26/Quira/blob/main/CONTRIBUTING.md" 
              target="_blank" 
              rel="noreferrer" 
              className="group relative"
            >
              <div className="w-12 h-12 sm:w-14 sm:h-14 rounded-full overflow-hidden border-2 border-white dark:border-[#0a0a0a] ring-2 ring-zinc-100 dark:ring-white/10 hover:ring-zinc-300 dark:hover:ring-white/30 transition-all hover:-translate-y-1 hover:shadow-lg bg-zinc-50 dark:bg-zinc-900 flex items-center justify-center text-xs font-medium text-zinc-500">
                + Join
              </div>
            </a>
          </div>
        </div>
      </AnimatedSection>
    </section>
  );
}
