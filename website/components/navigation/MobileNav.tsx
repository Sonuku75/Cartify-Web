"use client";

import React, { useEffect } from "react";
import Link from "next/link";
import { X } from "lucide-react";
import { MAIN_NAV_ITEMS, SITE_CONFIG } from "@/constants/config";

interface MobileNavProps {
  isOpen: boolean;
  onClose: () => void;
}

export function MobileNav({ isOpen, onClose }: MobileNavProps) {
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
    <div className="fixed inset-0 z-50 md:hidden flex">
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black/60 backdrop-blur-sm transition-opacity animate-fade-in"
        onClick={onClose}
        aria-hidden="true"
      />

      {/* Drawer */}
      <div className="relative z-10 w-4/5 max-w-xs h-full bg-white dark:bg-neutral-900 shadow-2xl p-6 flex flex-col justify-between animate-slide-up">
        <div>
          <div className="flex items-center justify-between pb-6 border-b border-neutral-100 dark:border-neutral-800">
            <span className="text-xl font-bold tracking-tight text-neutral-900 dark:text-white">
              {SITE_CONFIG.name}
            </span>
            <button
              onClick={onClose}
              className="p-2 rounded-lg text-neutral-500 hover:text-neutral-900 dark:hover:text-white hover:bg-neutral-100 dark:hover:bg-neutral-800"
              aria-label="Close menu"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          <nav className="mt-6 flex flex-col space-y-4" aria-label="Mobile Navigation">
            {MAIN_NAV_ITEMS.map((item) => (
              <Link
                key={item.label}
                href={item.href}
                onClick={onClose}
                className="text-base font-medium text-neutral-800 dark:text-neutral-200 hover:text-brand-600 dark:hover:text-brand-400 py-2 border-b border-neutral-50 dark:border-neutral-800/60"
              >
                {item.label}
              </Link>
            ))}
          </nav>
        </div>

        <div className="pt-6 border-t border-neutral-100 dark:border-neutral-800 text-xs text-neutral-500">
          Cartify Fashion &middot; Responsive Mobile Foundation
        </div>
      </div>
    </div>
  );
}
