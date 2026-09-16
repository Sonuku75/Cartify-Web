import React from "react";
import { cn } from "@/lib/utils";

interface SpinnerProps {
  size?: "sm" | "md" | "lg";
  className?: string;
}

export function Spinner({ size = "md", className }: SpinnerProps) {
  const sizes = {
    sm: "w-4 h-4 border-2",
    md: "w-6 h-6 border-2",
    lg: "w-8 h-8 border-3",
  };

  return (
    <div
      role="status"
      aria-label="Loading"
      className={cn(
        "rounded-full border-neutral-300 dark:border-neutral-700 border-t-neutral-900 dark:border-t-white animate-spin",
        sizes[size],
        className
      )}
    />
  );
}
