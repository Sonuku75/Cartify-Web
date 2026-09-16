import React from "react";
import { Container } from "./Container";
import { SITE_CONFIG } from "@/constants/config";

export function Footer() {
  return (
    <footer className="w-full border-t border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-950 transition-colors py-12 mt-auto">
      <Container className="flex flex-col sm:flex-row items-center justify-between gap-6 text-center sm:text-left">
        <div>
          <span className="text-base font-bold text-neutral-900 dark:text-white">
            {SITE_CONFIG.name}
          </span>
          <p className="mt-1 text-xs text-neutral-500 max-w-sm">
            Modern fashion e-commerce platform. Mobile-first responsive architecture supporting web, iOS, and Android.
          </p>
        </div>

        <div className="flex flex-col sm:items-end text-xs text-neutral-400 space-y-1">
          <span>Shared Backend: Django REST API &middot; PostgreSQL</span>
          <span>&copy; {new Date().getFullYear()} Cartify. All rights reserved.</span>
        </div>
      </Container>
    </footer>
  );
}
