"use client";

import { useState } from "react";
import { CopyButton } from "./CopyButton";

type PackageManager = "pip" | "poetry" | "uv";

export function InstallTabs() {
  const [manager, setManager] = useState<PackageManager>("pip");

  const commands = {
    pip: 'pip install "quira[all]"',
    poetry: 'poetry add quira --extras all',
    uv: 'uv pip install "quira[all]"'
  };

  const activeTabClass = "px-4 py-2.5 text-[13px] font-medium border-b-2 border-zinc-900 dark:border-white text-zinc-900 dark:text-white -mb-[1px] cursor-pointer";
  const inactiveTabClass = "px-4 py-2.5 text-[13px] font-medium text-zinc-500 hover:text-zinc-700 dark:hover:text-zinc-300 cursor-pointer transition-colors";

  return (
    <div className="rounded-lg overflow-hidden border border-zinc-200 dark:border-white/10 bg-white dark:bg-[#0a0a0a] mb-6">
      <div className="flex overflow-x-auto whitespace-nowrap px-4 border-b border-zinc-200 dark:border-white/[0.06] bg-zinc-50 dark:bg-white/[0.02] no-scrollbar">
        <div 
          onClick={() => setManager("pip")} 
          className={manager === "pip" ? activeTabClass : inactiveTabClass}
        >
          pip
        </div>
        <div 
          onClick={() => setManager("poetry")} 
          className={manager === "poetry" ? activeTabClass : inactiveTabClass}
        >
          poetry
        </div>
        <div 
          onClick={() => setManager("uv")} 
          className={manager === "uv" ? activeTabClass : inactiveTabClass}
        >
          uv
        </div>
        <div className="ml-auto py-2 flex items-center">
          <CopyButton text={commands[manager]} />
        </div>
      </div>
      <div className="p-5 font-mono text-[13px] bg-zinc-900 dark:bg-transparent text-zinc-300">
        <span className="text-zinc-500 select-none mr-3">$</span>
        {manager === "pip" && <>pip install <span className="text-zinc-100">&quot;quira[all]&quot;</span></>}
        {manager === "poetry" && <>poetry add <span className="text-zinc-100">quira --extras all</span></>}
        {manager === "uv" && <>uv pip install <span className="text-zinc-100">&quot;quira[all]&quot;</span></>}
      </div>
    </div>
  );
}
