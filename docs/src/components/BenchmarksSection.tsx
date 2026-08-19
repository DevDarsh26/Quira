"use client";

import * as React from "react";
import { motion, useInView } from "framer-motion";

export function BenchmarksSection() {
  const ref = React.useRef(null);
  const isInView = useInView(ref, { once: true, margin: "-50px" });

  const StandardRAGHeight = "85%";
  const QuiraHeight = "15%"; // 85% lower latency

  const StandardTokenHeight = "100%";
  const QuiraTokenHeight = "60%"; // 40% fewer tokens

  return (
    <div ref={ref} className="w-full max-w-3xl mx-auto py-10 px-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-12 md:gap-24">
        
        {/* Latency Benchmark */}
        <div className="flex flex-col items-center">
          <div className="text-sm font-semibold text-zinc-500 uppercase tracking-widest mb-8">Latency</div>
          
          <div className="flex items-end gap-6 h-48 w-full justify-center border-b border-zinc-200 dark:border-white/10 pb-2 relative">
            {/* Standard RAG Bar */}
            <div className="flex flex-col items-center gap-2 w-16">
              <span className="text-xs text-zinc-400 font-mono">1.2s</span>
              <motion.div 
                className="w-full bg-zinc-200 dark:bg-zinc-800 rounded-t-sm"
                initial={{ height: 0 }}
                animate={{ height: isInView ? StandardRAGHeight : 0 }}
                transition={{ duration: 1, ease: "easeOut" }}
              />
              <span className="text-[10px] text-zinc-500 uppercase mt-2">Standard</span>
            </div>
            
            {/* Quira Bar */}
            <div className="flex flex-col items-center gap-2 w-16">
              <span className="text-xs text-emerald-600 dark:text-emerald-400 font-bold font-mono">0.18s</span>
              <motion.div 
                className="w-full bg-emerald-500 dark:bg-emerald-500 rounded-t-sm"
                initial={{ height: 0 }}
                animate={{ height: isInView ? QuiraHeight : 0 }}
                transition={{ duration: 1, ease: "easeOut", delay: 0.2 }}
              />
              <span className="text-[10px] font-bold text-zinc-900 dark:text-white uppercase mt-2">Quira</span>
            </div>
          </div>
          <div className="mt-6 text-center text-sm text-zinc-500">85% reduction in time-to-first-token</div>
        </div>

        {/* Token Usage Benchmark */}
        <div className="flex flex-col items-center">
          <div className="text-sm font-semibold text-zinc-500 uppercase tracking-widest mb-8">Token Usage</div>
          
          <div className="flex items-end gap-6 h-48 w-full justify-center border-b border-zinc-200 dark:border-white/10 pb-2 relative">
            {/* Standard RAG Bar */}
            <div className="flex flex-col items-center gap-2 w-16">
              <span className="text-xs text-zinc-400 font-mono">8k</span>
              <motion.div 
                className="w-full bg-zinc-200 dark:bg-zinc-800 rounded-t-sm"
                initial={{ height: 0 }}
                animate={{ height: isInView ? StandardTokenHeight : 0 }}
                transition={{ duration: 1, ease: "easeOut", delay: 0.4 }}
              />
              <span className="text-[10px] text-zinc-500 uppercase mt-2">Standard</span>
            </div>
            
            {/* Quira Bar */}
            <div className="flex flex-col items-center gap-2 w-16">
              <span className="text-xs text-blue-600 dark:text-blue-400 font-bold font-mono">4.8k</span>
              <motion.div 
                className="w-full bg-blue-500 dark:bg-blue-500 rounded-t-sm"
                initial={{ height: 0 }}
                animate={{ height: isInView ? QuiraTokenHeight : 0 }}
                transition={{ duration: 1, ease: "easeOut", delay: 0.6 }}
              />
              <span className="text-[10px] font-bold text-zinc-900 dark:text-white uppercase mt-2">Quira</span>
            </div>
          </div>
          <div className="mt-6 text-center text-sm text-zinc-500">40% fewer tokens per request</div>
        </div>

      </div>
    </div>
  );
}
