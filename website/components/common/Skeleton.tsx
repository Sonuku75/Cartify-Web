import React from "react";
import { cn } from "@/lib/utils";

export type SkeletonProps = React.HTMLAttributes<HTMLDivElement>;

export function Skeleton({ className, ...props }: SkeletonProps) {
  return (
    <div
      className={cn(
        "bg-neutral-200 dark:bg-neutral-800 rounded-md animate-pulse-subtle",
        className
      )}
      {...props}
    />
  );
}
