"use client";

import React from "react";
import { ShoppingBag } from "lucide-react";
import { cn } from "@/lib/utils";

interface CartBadgeProps {
  count?: number;
  onClick?: () => void;
  className?: string;
}

export function CartBadge({ count = 0, onClick, className }: CartBadgeProps) {
  return (
    <button
      onClick={onClick}
      className={cn(
        "relative p-2 rounded-lg text-neutral-600 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-800 transition-colors focus:outline-none focus:ring-2 focus:ring-neutral-400",
        className
      )}
      aria-label={`Shopping cart with ${count} items`}
    >
      <ShoppingBag className="w-5 h-5 transition-transform hover:scale-105" />
      {count > 0 ? (
        <span className="absolute top-1 right-1 flex items-center justify-center min-w-[18px] h-[18px] px-1 text-[10px] font-bold text-white bg-brand-600 rounded-full animate-fade-in">
          {count}
        </span>
      ) : null}
    </button>
  );
}
