"use client";

import * as React from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronDown } from "lucide-react";
import { AnimatedSection } from "@/components/AnimatedSection";

const faqs = [
  {
    question: "Do I need to migrate my vector database?",
    answer: "No. Quira works out-of-the-box with your existing vector databases (Qdrant, Pinecone, Chroma, etc.). It acts as a lightweight wrapper that orchestrates the Speculative Retrieval layer on top of your current infrastructure."
  },
  {
    question: "Is Quira compatible with LangChain and LlamaIndex?",
    answer: "Yes, Quira provides native abstractions for both LangChain and LlamaIndex. You can drop in our QuiraRetriever directly into your existing chains without rewriting your application logic."
  },
  {
    question: "How exactly does Context Tetris reduce token usage?",
    answer: "Instead of indiscriminately feeding chunks into the LLM context window, Context Tetris analyzes chunk boundaries, overlaps, and semantic relevance, packing only the exact context required to answer the query. This drastically reduces the noise-to-signal ratio, saving up to 40% on token costs."
  },
  {
    question: "Is Quira open-source?",
    answer: "Yes, Quira is 100% open-source and MIT-licensed. We believe the future of RAG infrastructure should be transparent and accessible to all developers."
  }
];

export function FAQSection() {
  const [openIndex, setOpenIndex] = React.useState<number | null>(0);

  return (
    <section className="w-full max-w-3xl mx-auto py-24 px-4 sm:px-6">
      <AnimatedSection direction="up" delay={0.1}>
        <div className="text-center mb-12">
          <h2 className="text-2xl md:text-3xl font-bold text-zinc-900 dark:text-white mb-4 tracking-tight">Frequently Asked Questions</h2>
          <p className="text-sm text-zinc-500 max-w-xl mx-auto">Everything you need to know about the product and billing.</p>
        </div>
      </AnimatedSection>

      <div className="space-y-4">
        {faqs.map((faq, index) => {
          const isOpen = openIndex === index;
          return (
            <AnimatedSection key={index} direction="up" delay={0.2 + index * 0.1}>
              <div 
                className={`border rounded-xl transition-colors duration-200 overflow-hidden ${
                  isOpen 
                    ? "bg-white dark:bg-zinc-900/60 border-zinc-200 dark:border-white/10" 
                    : "bg-transparent border-transparent hover:bg-zinc-50 dark:hover:bg-zinc-900/40"
                }`}
              >
                <button
                  onClick={() => setOpenIndex(isOpen ? null : index)}
                  className="flex items-center justify-between w-full p-5 text-left focus:outline-none"
                >
                  <span className="font-medium text-[15px] text-zinc-900 dark:text-zinc-100">{faq.question}</span>
                  <motion.div
                    animate={{ rotate: isOpen ? 180 : 0 }}
                    transition={{ duration: 0.2, ease: "easeInOut" }}
                    className="text-zinc-400"
                  >
                    <ChevronDown className="w-5 h-5" />
                  </motion.div>
                </button>
                <AnimatePresence initial={false}>
                  {isOpen && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: "auto", opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      transition={{ duration: 0.3, ease: "easeInOut" }}
                    >
                      <div className="px-5 pb-5 pt-1 text-[14px] leading-relaxed text-zinc-500 dark:text-zinc-400">
                        {faq.answer}
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            </AnimatedSection>
          );
        })}
      </div>
    </section>
  );
}
