import React from "react";
import { Skeleton } from "@/components/common/Skeleton";

export function ProductCardSkeleton() {
  return (
    <div className="flex flex-col space-y-3">
      {/* Product Image Placeholder */}
      <Skeleton className="w-full aspect-[3/4] rounded-xl" />
      {/* Category Tag */}
      <Skeleton className="w-16 h-3 rounded" />
      {/* Title */}
      <Skeleton className="w-3/4 h-4 rounded" />
      {/* Price */}
      <Skeleton className="w-20 h-4 rounded" />
    </div>
  );
}
