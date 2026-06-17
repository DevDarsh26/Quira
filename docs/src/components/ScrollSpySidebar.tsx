"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { cn } from "@/lib/utils";

const SECTIONS = [
  { id: "installation", label: "Installation" },
  { id: "speculative-retrieval", label: "Speculative Retrieval" },
  { id: "context-tetris", label: "Context Tetris" },
  { id: "differential-context", label: "Differential Context" },
  { id: "provider-abstraction", label: "Provider Abstraction" },
  { id: "integrations", label: "Integrations" },
];

export function ScrollSpySidebar() {
  const [activeId, setActiveId] = useState("");

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        // We find the intersecting entry that takes up the most screen space
        // or just the first one that is intersecting
        const intersecting = entries.find((entry) => entry.isIntersecting);
        if (intersecting) {
          setActiveId(intersecting.target.id);
        }
      },
      { rootMargin: "-100px 0px -66% 0px" } // trigger when near top
    );

    SECTIONS.forEach((section) => {
      const el = document.getElementById(section.id);
      if (el) observer.observe(el);
    });

    return () => observer.disconnect();
  }, []);

  return (
    <aside className="w-full md:w-64 shrink-0 mb-8 md:mb-0">
      <div className="md:sticky md:top-24 md:space-y-6">
        <div>
          <h4 className="font-semibold mb-3 md:mb-4 text-foreground tracking-tight text-xs md:text-sm uppercase text-muted-foreground hidden md:block">On this page</h4>
          <div className="flex flex-row md:flex-col gap-2 md:gap-2.5 text-sm md:border-l md:border-border/50 overflow-x-auto pb-2 md:pb-0 [&::-webkit-scrollbar]:hidden [-ms-overflow-style:none] [scrollbar-width:none]">
            {SECTIONS.map((section) => (
              <Link
                key={section.id}
                href={`#${section.id}`}
                className={cn(
                  "whitespace-nowrap px-3 py-1.5 md:px-0 md:pl-4 md:py-0.5 transition-all relative md:border-l-[3px] md:-ml-[2px] rounded-full md:rounded-none border border-border/50 md:border-transparent md:border-l-transparent",
                  activeId === section.id
                    ? "text-primary font-medium bg-primary/10 md:bg-transparent md:border-l-primary border-primary/20 md:border-y-transparent md:border-r-transparent"
                    : "text-muted-foreground md:border-l-transparent hover:text-foreground bg-background hover:bg-muted/50 md:bg-transparent md:hover:bg-transparent md:hover:border-l-muted-foreground/50"
                )}
              >
                {section.label}
              </Link>
            ))}
          </div>
        </div>
      </div>
    </aside>
  );
}
