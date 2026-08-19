"use client";

import * as React from "react";
import { motion, useInView } from "framer-motion";

export function ArchitectureDiagram() {
  const ref = React.useRef(null);
  const isInView = useInView(ref, { once: true, margin: "-100px" });

  const containerVariant = {
    hidden: { opacity: 0 },
    visible: { 
      opacity: 1, 
      transition: { 
        staggerChildren: 0.2,
        delayChildren: 0.1
      }
    }
  };

  const itemVariant = {
    hidden: { y: 20, opacity: 0 },
    visible: { y: 0, opacity: 1, transition: { duration: 0.4 } }
  };

  const lineVariant = {
    hidden: { pathLength: 0, opacity: 0 },
    visible: { pathLength: 1, opacity: 0.3, transition: { duration: 0.8 } }
  };
  
  const pulseVariant = {
    hidden: { opacity: 0, scale: 0 },
    visible: { 
      opacity: [0, 1, 0], 
      scale: [0.8, 1, 0.8], 
      transition: { repeat: Infinity, duration: 2 } 
    }
  };

  return (
    <div ref={ref} className="w-full max-w-4xl mx-auto py-10 overflow-x-auto">
      <div className="min-w-[600px] h-[300px] relative mx-auto flex items-center justify-between px-10">
        
        {/* Background SVG connections */}
        <svg className="absolute inset-0 w-full h-full pointer-events-none" style={{ zIndex: 0 }}>
          <motion.path
            d="M 120 150 L 300 150"
            stroke="currentColor"
            strokeWidth="2"
            strokeDasharray="4 4"
            fill="none"
            className="text-zinc-400 dark:text-zinc-600"
            variants={lineVariant}
            initial="hidden"
            animate={isInView ? "visible" : "hidden"}
          />
          <motion.path
            d="M 450 150 L 630 150"
            stroke="currentColor"
            strokeWidth="2"
            strokeDasharray="4 4"
            fill="none"
            className="text-zinc-400 dark:text-zinc-600"
            variants={lineVariant}
            initial="hidden"
            animate={isInView ? "visible" : "hidden"}
          />
          
          {/* Animated data packets */}
          {isInView && (
            <>
              <motion.circle r="3" fill="#10b981" className="dark:fill-[#34d399]"
                initial={{ x: 120, y: 150, opacity: 0 }}
                animate={{ x: 300, y: 150, opacity: [0, 1, 0] }}
                transition={{ repeat: Infinity, duration: 1.5, delay: 0.5 }}
              />
              <motion.circle r="3" fill="#10b981" className="dark:fill-[#34d399]"
                initial={{ x: 120, y: 150, opacity: 0 }}
                animate={{ x: 300, y: 150, opacity: [0, 1, 0] }}
                transition={{ repeat: Infinity, duration: 1.5, delay: 1.25 }}
              />
              
              {/* Context Tetris to LLM */}
              <motion.rect width="10" height="10" rx="2" fill="#3b82f6" className="dark:fill-[#60a5fa]"
                initial={{ x: 450, y: 145, opacity: 0 }}
                animate={{ x: 630, y: 145, opacity: [0, 1, 0] }}
                transition={{ repeat: Infinity, duration: 1.5, delay: 1 }}
              />
            </>
          )}
        </svg>

        <motion.div 
          className="relative z-10 flex w-full justify-between items-center"
          variants={containerVariant}
          initial="hidden"
          animate={isInView ? "visible" : "hidden"}
        >
          {/* Node 1: User / App */}
          <motion.div variants={itemVariant} className="flex flex-col items-center">
            <div className="w-20 h-20 rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-white/10 shadow-lg flex items-center justify-center relative">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-zinc-600 dark:text-zinc-400"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
            </div>
            <span className="mt-3 text-xs font-semibold uppercase tracking-wider text-zinc-500">Query</span>
          </motion.div>

          {/* Node 2: Quira Engine */}
          <motion.div variants={itemVariant} className="flex flex-col items-center relative">
            <motion.div variants={pulseVariant} className="absolute inset-0 -m-4 rounded-3xl border border-emerald-500/30 bg-emerald-500/5 pointer-events-none" />
            <div className="w-40 h-28 rounded-xl bg-white dark:bg-zinc-900 border border-emerald-500/30 dark:border-emerald-500/20 shadow-[0_0_30px_-5px_rgba(16,185,129,0.2)] flex flex-col items-center justify-center relative overflow-hidden">
              <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-emerald-400 to-emerald-600" />
              <div className="font-bold text-lg text-zinc-900 dark:text-white mb-1">Quira Pipeline</div>
              <div className="flex gap-2 mt-2">
                <div className="px-2 py-1 rounded bg-zinc-100 dark:bg-zinc-800 text-[9px] font-mono text-zinc-500">Speculative</div>
                <div className="px-2 py-1 rounded bg-zinc-100 dark:bg-zinc-800 text-[9px] font-mono text-zinc-500">Tetris</div>
              </div>
            </div>
            <span className="mt-3 text-xs font-semibold uppercase tracking-wider text-emerald-600 dark:text-emerald-500">Processing</span>
          </motion.div>

          {/* Node 3: LLM */}
          <motion.div variants={itemVariant} className="flex flex-col items-center">
            <div className="w-20 h-20 rounded-xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-white/10 shadow-lg flex items-center justify-center relative">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-zinc-600 dark:text-zinc-400"><path d="M12 2v20"></path><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>
            </div>
            <span className="mt-3 text-xs font-semibold uppercase tracking-wider text-zinc-500">LLM</span>
          </motion.div>

        </motion.div>
      </div>
    </div>
  );
}
