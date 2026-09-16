"use client";

import React, { useEffect } from "react";
import { X, ShoppingBag } from "lucide-react";
import { Button } from "@/components/common/Button";

interface CartDrawerProps {
  isOpen: boolean;
  onClose: () => void;
}

export function CartDrawer({ isOpen, onClose }: CartDrawerProps) {
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "unset";
    }
    return () => {
      document.body.style.overflow = "unset";
    };
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex justify-end">
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black/50 backdrop-blur-sm transition-opacity animate-fade-in"
        onClick={onClose}
        aria-hidden="true"
      />

      {/* Slide-over panel */}
      <div className="relative z-10 w-full max-w-md bg-white dark:bg-neutral-900 h-full shadow-2xl p-6 flex flex-col justify-between animate-slide-down">
        <div>
          <div className="flex items-center justify-between pb-4 border-b border-neutral-100 dark:border-neutral-800">
            <div className="flex items-center space-x-2">
              <ShoppingBag className="w-5 h-5 text-neutral-900 dark:text-white" />
              <h2 className="text-lg font-bold text-neutral-900 dark:text-white">
                Your Bag
              </h2>
            </div>
            <button
              onClick={onClose}
              className="p-1 rounded-lg text-neutral-500 hover:text-neutral-900 dark:hover:text-white"
              aria-label="Close cart"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          <div className="mt-12 text-center">
            <div className="mx-auto w-12 h-12 rounded-full bg-neutral-100 dark:bg-neutral-800 flex items-center justify-center text-neutral-400">
              <ShoppingBag className="w-6 h-6" />
            </div>
            <h3 className="mt-4 text-base font-semibold text-neutral-900 dark:text-white">
              Your bag is empty
            </h3>
            <p className="mt-1 text-sm text-neutral-500">
              Cart foundation initialized. Catalog items will be added in upcoming modules.
            </p>
          </div>
        </div>

        <div className="pt-4 border-t border-neutral-100 dark:border-neutral-800">
          <Button variant="outline" className="w-full" onClick={onClose}>
            Continue Shopping
          </Button>
        </div>
      </div>
    </div>
  );
}
