"use client";

import * as React from "react";
import { motion, useInView } from "framer-motion";

interface TerminalTypewriterProps {
  htmlContent: string;
}

export function TerminalTypewriter({ htmlContent }: TerminalTypewriterProps) {
  const ref = React.useRef(null);
  const isInView = useInView(ref, { once: true, margin: "-50px" });
  
  // Split the HTML content by newlines to animate line-by-line
  const lines = htmlContent.split('\n');

  return (
    <div ref={ref}>
      <motion.pre
        className="code-block text-[11px] sm:text-[13px] leading-[1.8] font-mono text-zinc-300 whitespace-pre"
        initial="hidden"
        animate={isInView ? "visible" : "hidden"}
        variants={{
          visible: {
            transition: {
              staggerChildren: 0.1,
            },
          },
          hidden: {},
        }}
      >
        {lines.map((line, idx) => (
          <motion.div
            key={idx}
            variants={{
              visible: { 
                opacity: 1, 
                filter: "blur(0px)",
                x: 0,
                transition: { duration: 0.2 } 
              },
              hidden: { 
                opacity: 0, 
                filter: "blur(4px)",
                x: -4 
              },
            }}
            dangerouslySetInnerHTML={{ __html: line }}
          />
        ))}
      </motion.pre>
    </div>
  );
}
