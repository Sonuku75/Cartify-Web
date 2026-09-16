"use client";

import React, { useState } from "react";
import Link from "next/link";
import { Menu } from "lucide-react";
import { Container } from "./Container";
import { Navbar } from "@/components/navigation/Navbar";
import { MobileNav } from "@/components/navigation/MobileNav";
import { ThemeToggle } from "./ThemeToggle";
import { CartBadge } from "@/components/cart/CartBadge";
import { CartDrawer } from "@/components/cart/CartDrawer";
import { SITE_CONFIG } from "@/constants/config";

export function Header() {
  const [mobileNavOpen, setMobileNavOpen] = useState(false);
  const [cartOpen, setCartOpen] = useState(false);

  return (
    <header className="sticky top-0 z-40 w-full border-b border-neutral-200/80 dark:border-neutral-800/80 bg-white/85 dark:bg-neutral-900/85 backdrop-blur-md transition-colors">
      <Container className="flex h-16 items-center justify-between">
        {/* Left: Brand Logo & Desktop Nav */}
        <div className="flex items-center space-x-8">
          <Link
            href="/"
            className="text-xl font-bold tracking-tight text-neutral-900 dark:text-white transition-opacity hover:opacity-90"
          >
            {SITE_CONFIG.name}
          </Link>
          <Navbar />
        </div>

        {/* Right: Actions */}
        <div className="flex items-center space-x-2 sm:space-x-3">
          <ThemeToggle />
          <CartBadge count={0} onClick={() => setCartOpen(true)} />

          {/* Mobile Menu Button */}
          <button
            onClick={() => setMobileNavOpen(true)}
            className="md:hidden p-2 rounded-lg text-neutral-600 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-800 transition-colors"
            aria-label="Open mobile menu"
          >
            <Menu className="w-5 h-5" />
          </button>
        </div>
      </Container>

      {/* Drawers */}
      <MobileNav isOpen={mobileNavOpen} onClose={() => setMobileNavOpen(false)} />
      <CartDrawer isOpen={cartOpen} onClose={() => setCartOpen(false)} />
    </header>
  );
}
