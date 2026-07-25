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
    <aside className="w-full">
      <div className="md:sticky md:top-24">
        <h4 className="font-medium mb-4 text-[13px] uppercase tracking-wider text-zinc-900 dark:text-zinc-100">On this page</h4>
        <div className="flex flex-col gap-1.5 text-[13px] border-l border-zinc-200 dark:border-white/10 overflow-x-auto pb-2 md:pb-0 [&::-webkit-scrollbar]:hidden [-ms-overflow-style:none] [scrollbar-width:none]">
          {SECTIONS.map((section) => (
            <Link
              key={section.id}
              href={`#${section.id}`}
              className={cn(
                "px-3 py-1 transition-all border-l-2 -ml-[1px]",
                activeId === section.id
                  ? "text-zinc-900 dark:text-white border-zinc-900 dark:border-white font-medium"
                  : "text-zinc-500 dark:text-zinc-400 border-transparent hover:text-zinc-900 dark:hover:text-white hover:border-zinc-300 dark:hover:border-white/20"
              )}
            >
              {section.label}
            </Link>
          ))}
        </div>
      </div>
    </aside>
  );
}
