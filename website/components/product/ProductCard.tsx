import React from "react";
import { Badge } from "@/components/common/Badge";

interface ProductCardProps {
  title: string;
  category: string;
  price: string;
  isNew?: boolean;
}

export function ProductCard({ title, category, price, isNew }: ProductCardProps) {
  return (
    <div className="group flex flex-col rounded-xl overflow-hidden bg-white dark:bg-neutral-900 border border-neutral-200/80 dark:border-neutral-800 transition-all duration-300 hover:shadow-lg">
      {/* Product Image Area with Hover Zoom */}
      <div className="relative aspect-[3/4] bg-neutral-100 dark:bg-neutral-800 overflow-hidden flex items-center justify-center">
        <div className="text-neutral-400 dark:text-neutral-600 text-xs uppercase tracking-wider font-semibold group-hover:scale-105 transition-transform duration-300">
          Preview Image
        </div>
        {isNew ? (
          <div className="absolute top-3 left-3">
            <Badge variant="brand">New</Badge>
          </div>
        ) : null}
      </div>

      {/* Details */}
      <div className="p-4 flex flex-col space-y-1">
        <span className="text-xs text-neutral-500 uppercase tracking-wider">
          {category}
        </span>
        <h3 className="text-sm font-semibold text-neutral-900 dark:text-white truncate">
          {title}
        </h3>
        <p className="text-sm font-bold text-neutral-900 dark:text-white pt-1">
          {price}
        </p>
      </div>
    </div>
  );
}
