/**
 * Common frontend types for navigation, themes, and UI states.
 */

export type Theme = "light" | "dark";

export interface NavItem {
  label: string;
  href: string;
  badge?: string;
  isExternal?: boolean;
}

export interface BreakpointState {
  isMobile: boolean;
  isTablet: boolean;
  isDesktop: boolean;
  isWide: boolean;
}
