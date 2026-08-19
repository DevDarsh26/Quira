"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";

const NAV_ITEMS = [
  {
    title: "Getting Started",
    links: [
      { href: "/docs#installation", label: "Installation" },
    ],
  },
  {
    title: "Core Concepts",
    links: [
      { href: "/docs#speculative-retrieval", label: "Speculative Retrieval" },
      { href: "/docs#context-tetris", label: "Context Tetris" },
      { href: "/docs#differential-context", label: "Differential Context" },
    ],
  },
  {
    title: "Architecture",
    links: [
      { href: "/docs#provider-abstraction", label: "Provider Abstraction" },
      { href: "/docs#integrations", label: "Integrations" },
    ],
  },
];

export function DocsSidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-full md:w-64 shrink-0 mb-8 md:mb-0 md:pr-6 md:border-r border-zinc-200 dark:border-white/5 h-full relative z-10 hidden lg:block">
      <div className="md:sticky md:top-24 space-y-8">
        {NAV_ITEMS.map((section) => (
          <div key={section.title}>
            <h4 className="font-medium mb-3 text-sm text-zinc-900 dark:text-zinc-100">
              {section.title}
            </h4>
            <div className="flex flex-col gap-2 border-l border-zinc-200 dark:border-white/10 ml-1">
              {section.links.map((link) => {
                const isActive = false;
                return (
                  <Link
                    key={link.href}
                    href={link.href}
                    className={cn(
                      "pl-4 py-1 text-[13px] transition-colors border-l-2 -ml-[1px]",
                      isActive
                        ? "text-zinc-900 dark:text-white border-zinc-900 dark:border-white font-medium"
                        : "text-zinc-500 dark:text-zinc-400 border-transparent hover:text-zinc-900 dark:hover:text-white hover:border-zinc-300 dark:hover:border-white/20"
                    )}
                  >
                    {link.label}
                  </Link>
                );
              })}
            </div>
          </div>
        ))}
      </div>
    </aside>
  );
}
