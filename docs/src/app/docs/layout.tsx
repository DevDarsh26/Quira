import { ReactNode } from "react";
import { ScrollSpySidebar } from "@/components/ScrollSpySidebar";

export default function DocsLayout({ children }: { children: ReactNode }) {
  return (
    <div className="container mx-auto px-6 flex-1 flex flex-col md:flex-row gap-16 py-16">
      
      {/* Scroll Spy Navigation */}
      <ScrollSpySidebar />
      
      {/* Main Content Area */}
      <main className="flex-1 min-w-0 max-w-4xl">
        {children}
      </main>
    </div>
  );
}
