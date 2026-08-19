import { ReactNode } from "react";
import { ScrollSpySidebar } from "@/components/ScrollSpySidebar";
import { DocsSidebar } from "@/components/DocsSidebar";

export default function DocsLayout({ children }: { children: ReactNode }) {
  return (
    <div className="max-w-[1300px] mx-auto px-4 sm:px-6 flex-1 flex flex-col lg:flex-row gap-10 py-12 relative w-full">
      <div className="absolute inset-0 bg-grid opacity-30 pointer-events-none" />
      
      {/* Left Navigation Sidebar */}
      <DocsSidebar />
      
      {/* Main Content Area */}
      <main className="flex-1 min-w-0 max-w-3xl relative z-10 w-full">
        {children}
      </main>

      {/* Right Scroll Spy (On this page) */}
      <div className="hidden xl:block w-56 shrink-0 relative z-10">
        <ScrollSpySidebar />
      </div>
    </div>
  );
}
