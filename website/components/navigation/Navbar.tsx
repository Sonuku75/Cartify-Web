import React from "react";
import Link from "next/link";
import { MAIN_NAV_ITEMS } from "@/constants/config";
import { cn } from "@/lib/utils";

export function Navbar({ className }: { className?: string }) {
  return (
    <nav className={cn("hidden md:flex items-center space-x-6", className)} aria-label="Main Navigation">
      {MAIN_NAV_ITEMS.map((item) => (
        <Link
          key={item.label}
          href={item.href}
          className="text-sm font-medium text-neutral-600 hover:text-neutral-900 dark:text-neutral-400 dark:hover:text-white transition-colors py-1"
        >
          {item.label}
        </Link>
      ))}
    </nav>
  );
}
