import { NavItem } from "@/types/common";

export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api/v1";

export const API_HEALTH_URL =
  process.env.NEXT_PUBLIC_API_HEALTH_URL || "http://localhost:8000/api/health/";

export const SITE_CONFIG = {
  name: "Cartify",
  description: "Modern fashion e-commerce platform.",
  defaultTheme: "light" as const,
  themeStorageKey: "cartify-theme-preference",
};

export const MAIN_NAV_ITEMS: NavItem[] = [
  { label: "New Arrivals", href: "#new-arrivals" },
  { label: "Women", href: "#women" },
  { label: "Men", href: "#men" },
  { label: "Accessories", href: "#accessories" },
];
