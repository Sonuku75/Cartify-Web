"use client";

import React, { useEffect, useState } from "react";
import { Container } from "@/components/layout/Container";
import { Button } from "@/components/common/Button";
import { Badge } from "@/components/common/Badge";
import { Modal } from "@/components/common/Modal";
import { ProductCard } from "@/components/product/ProductCard";
import { ProductCardSkeleton } from "@/components/product/ProductCardSkeleton";
import { CheckoutSummary } from "@/components/checkout/CheckoutSummary";
import { AccountNav } from "@/components/account/AccountNav";
import { checkApiHealth } from "@/lib/api-client";
import { HealthResponse } from "@/types/api";
import { Sparkles, Activity, ShieldCheck, Smartphone, Monitor } from "lucide-react";

export default function HomePage() {
  const [healthStatus, setHealthStatus] = useState<HealthResponse | null>(null);
  const [healthLoading, setHealthLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);

  useEffect(() => {
    let isMounted = true;
    checkApiHealth()
      .then((data) => {
        if (isMounted) {
          setHealthStatus(data);
          setHealthLoading(false);
        }
      })
      .catch(() => {
        if (isMounted) {
          setHealthStatus(null);
          setHealthLoading(false);
        }
      });
    return () => {
      isMounted = false;
    };
  }, []);

  return (
    <div className="w-full py-10 sm:py-14 space-y-16 animate-fade-in">
      {/* Hero / Architecture Banner */}
      <Container>
        <div className="relative overflow-hidden rounded-3xl border border-neutral-200/80 dark:border-neutral-800 bg-gradient-to-b from-white to-neutral-50/50 dark:from-neutral-900 dark:to-neutral-950 p-6 sm:p-10 lg:p-12 shadow-sm">
          <div className="flex flex-wrap items-center gap-2">
            <Badge variant="brand">Module 1.5 Active</Badge>
            <Badge variant="success">Next.js 15 &middot; React 19</Badge>
            <Badge variant="default">Tailwind CSS &middot; Dark Mode</Badge>
          </div>

          <h1 className="mt-5 text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight text-neutral-900 dark:text-white max-w-2xl leading-tight">
            Next.js Responsive Storefront Foundation
          </h1>
          <p className="mt-4 text-base sm:text-lg text-neutral-600 dark:text-neutral-400 max-w-2xl">
            Clean mobile-first architecture engineered for high-performance fashion retail. Supporting viewports from 320px to 1920px+ with zero horizontal overflow.
          </p>

          <div className="mt-8 flex flex-wrap items-center gap-4">
            <Button variant="primary" onClick={() => setModalOpen(true)}>
              <Sparkles className="w-4 h-4 mr-2" />
              Preview Foundation Modal
            </Button>
            <Button
              variant="outline"
              onClick={() => {
                const el = document.getElementById("responsive-grid");
                el?.scrollIntoView({ behavior: "smooth" });
              }}
            >
              Explore Components
            </Button>
          </div>
        </div>
      </Container>

      {/* Backend API Connection & Status Card */}
      <Container>
        <div className="rounded-2xl border border-neutral-200/80 dark:border-neutral-800 bg-white dark:bg-neutral-900 p-6 shadow-sm">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 rounded-xl bg-brand-50 dark:bg-brand-950 flex items-center justify-center text-brand-600 dark:text-brand-400">
                <Activity className="w-5 h-5" />
              </div>
              <div>
                <h2 className="text-base font-bold text-neutral-900 dark:text-white">
                  Centralized Backend API Integration
                </h2>
                <p className="text-xs text-neutral-500">
                  Target: Django REST API &middot; /api/health/ &middot; /api/v1/
                </p>
              </div>
            </div>

            <div className="flex items-center space-x-3">
              {healthLoading ? (
                <div className="flex items-center space-x-2 text-xs text-neutral-500">
                  <div className="w-2 h-2 rounded-full bg-amber-500 animate-ping" />
                  <span>Checking API Health...</span>
                </div>
              ) : healthStatus ? (
                <Badge variant="success">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 mr-1.5 inline-block" />
                  API {healthStatus.status.toUpperCase()} ({healthStatus.service})
                </Badge>
              ) : (
                <Badge variant="warning">
                  <span className="w-1.5 h-1.5 rounded-full bg-amber-500 mr-1.5 inline-block" />
                  API Standby (Start Django server to connect)
                </Badge>
              )}
            </div>
          </div>
        </div>
      </Container>

      {/* Responsive Viewport & Device Support Section */}
      <Container id="responsive-grid">
        <div className="space-y-6">
          <div>
            <h2 className="text-xl font-bold tracking-tight text-neutral-900 dark:text-white">
              Multi-Device & Responsive Foundation
            </h2>
            <p className="text-sm text-neutral-500">
              Validated on Mobile (320px, 375px, 390px, 430px), Tablet (768px), and Desktop (1024px, 1440px, 1920px+).
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="p-5 rounded-xl border border-neutral-200/80 dark:border-neutral-800 bg-white dark:bg-neutral-900 space-y-2">
              <div className="flex items-center space-x-2 text-neutral-900 dark:text-white font-semibold text-sm">
                <Smartphone className="w-4 h-4 text-brand-600" />
                <span>Mobile (320px–430px)</span>
              </div>
              <p className="text-xs text-neutral-500">
                Touch-friendly hit targets (≥44px), off-canvas sliding navigation, zero horizontal scroll.
              </p>
            </div>

            <div className="p-5 rounded-xl border border-neutral-200/80 dark:border-neutral-800 bg-white dark:bg-neutral-900 space-y-2">
              <div className="flex items-center space-x-2 text-neutral-900 dark:text-white font-semibold text-sm">
                <Monitor className="w-4 h-4 text-brand-600" />
                <span>Tablet (768px–1023px)</span>
              </div>
              <p className="text-xs text-neutral-500">
                Adaptive column reflow, intermediate layouts, seamless orientation switching.
              </p>
            </div>

            <div className="p-5 rounded-xl border border-neutral-200/80 dark:border-neutral-800 bg-white dark:bg-neutral-900 space-y-2">
              <div className="flex items-center space-x-2 text-neutral-900 dark:text-white font-semibold text-sm">
                <Monitor className="w-4 h-4 text-brand-600" />
                <span>Desktop (1024px–1440px)</span>
              </div>
              <p className="text-xs text-neutral-500">
                Full horizontal navigation, multi-column catalogs, interactive micro-animations.
              </p>
            </div>

            <div className="p-5 rounded-xl border border-neutral-200/80 dark:border-neutral-800 bg-white dark:bg-neutral-900 space-y-2">
              <div className="flex items-center space-x-2 text-neutral-900 dark:text-white font-semibold text-sm">
                <ShieldCheck className="w-4 h-4 text-brand-600" />
                <span>Ultrawide (1920px+)</span>
              </div>
              <p className="text-xs text-neutral-500">
                Constrained maximum readable container width (max-w-7xl) centered with consistent margins.
              </p>
            </div>
          </div>
        </div>
      </Container>

      {/* Component Foundation Previews (Product, Cart, Checkout, Account) */}
      <Container>
        <div className="space-y-6">
          <div>
            <h2 className="text-xl font-bold tracking-tight text-neutral-900 dark:text-white">
              Domain Component Architecture Previews
            </h2>
            <p className="text-sm text-neutral-500">
              Standardized modular foundations for products, checkout, and customer account areas.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Product Card & Skeleton */}
            <div className="space-y-4">
              <h3 className="text-sm font-semibold text-neutral-700 dark:text-neutral-300">
                Product Card & Hover Animation
              </h3>
              <ProductCard
                title="Structured Wool Blazer"
                category="Outerwear"
                price="$245.00"
                isNew
              />
            </div>

            <div className="space-y-4">
              <h3 className="text-sm font-semibold text-neutral-700 dark:text-neutral-300">
                Loading Skeleton Foundation
              </h3>
              <ProductCardSkeleton />
            </div>

            {/* Checkout & Account Foundation */}
            <div className="space-y-6">
              <div>
                <h3 className="text-sm font-semibold text-neutral-700 dark:text-neutral-300 mb-3">
                  Account Navigation
                </h3>
                <AccountNav />
              </div>

              <div>
                <h3 className="text-sm font-semibold text-neutral-700 dark:text-neutral-300 mb-3">
                  Checkout Summary
                </h3>
                <CheckoutSummary />
              </div>
            </div>
          </div>
        </div>
      </Container>

      {/* Interactive Modal Example */}
      <Modal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        title="Cartify Architecture Foundation"
      >
        <div className="space-y-4 text-sm text-neutral-600 dark:text-neutral-300">
          <p>
            This modal demonstrates the accessible dialog primitive with backdrop blur, keyboard escape listener, and smooth CSS animation.
          </p>
          <div className="rounded-lg bg-neutral-100 dark:bg-neutral-800 p-4 font-mono text-xs text-neutral-800 dark:text-neutral-200">
            components/common/Modal.tsx &middot; Accessible Dialog Primitive
          </div>
          <div className="flex justify-end pt-4">
            <Button variant="primary" onClick={() => setModalOpen(false)}>
              Got it
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  );
}
