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
    <aside className="w-full md:w-64 shrink-0 hidden md:block">
      <div className="sticky top-24 space-y-6">
        <div>
          <h4 className="font-semibold mb-4 text-foreground tracking-tight text-sm uppercase text-muted-foreground">On this page</h4>
          <div className="flex flex-col gap-2.5 text-sm border-l border-border/50">
            {SECTIONS.map((section) => (
              <Link
                key={section.id}
                href={`#${section.id}`}
                className={cn(
                  "pl-4 py-0.5 transition-all relative border-l-[3px] -ml-[2px]",
                  activeId === section.id
                    ? "text-primary font-medium border-primary"
                    : "text-muted-foreground border-transparent hover:text-foreground hover:border-muted-foreground/50"
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
