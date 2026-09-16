import React from 'react';
import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';

import { Button } from '@/components/common/Button';
import { Badge } from '@/components/common/Badge';
import { Skeleton } from '@/components/common/Skeleton';
import { ProductCard } from '@/components/product/ProductCard';
import { CartBadge } from '@/components/cart/CartBadge';
import { Container } from '@/components/layout/Container';
import { Header } from '@/components/layout/Header';
import { Footer } from '@/components/layout/Footer';
import { ThemeProvider } from '@/components/layout/ThemeProvider';
import { ThemeToggle } from '@/components/layout/ThemeToggle';

describe('Common UI Primitives', () => {
  it('renders Button with primary variant by default', () => {
    render(<Button>Shop Now</Button>);
    const btn = screen.getByRole('button', { name: /shop now/i });
    expect(btn).toBeInTheDocument();
  });

  it('renders Button in loading state with disabled attribute', () => {
    render(<Button isLoading>Processing</Button>);
    const btn = screen.getByRole('button');
    expect(btn).toBeDisabled();
    expect(btn).toHaveAttribute('aria-busy', 'true');
  });

  it('renders Badge with custom variants', () => {
    render(<Badge variant="success">New Arrival</Badge>);
    const badge = screen.getByText('New Arrival');
    expect(badge).toBeInTheDocument();
  });

  it('renders Skeleton with pulsing animation class', () => {
    const { container } = render(<Skeleton className="w-20 h-4" />);
    const skeleton = container.firstChild as HTMLElement;
    expect(skeleton.className).toContain('animate-pulse');
  });
});

describe('Product & Cart Components', () => {
  it('renders ProductCard with title, price, category and tag', () => {
    render(
      <ProductCard
        title="Silk Slip Evening Dress"
        price="$189.99"
        category="Women / Dresses"
        isNew
      />
    );

    expect(screen.getByText('Silk Slip Evening Dress')).toBeInTheDocument();
    expect(screen.getByText('Women / Dresses')).toBeInTheDocument();
    expect(screen.getByText('$189.99')).toBeInTheDocument();
    expect(screen.getByText('New')).toBeInTheDocument();
  });

  it('renders CartBadge with item count', () => {
    render(<CartBadge count={3} />);
    const btn = screen.getByRole('button', { name: /shopping cart with 3 items/i });
    expect(btn).toBeInTheDocument();
    expect(screen.getByText('3')).toBeInTheDocument();
  });
});

describe('Layout & Responsive Behavior', () => {
  it('renders Container constrained to max width', () => {
    const { container } = render(
      <Container>
        <span>Content</span>
      </Container>
    );
    expect(container.firstChild).toHaveClass('max-w-7xl');
    expect(screen.getByText('Content')).toBeInTheDocument();
  });

  it('renders Header brand and navigation elements', () => {
    render(
      <ThemeProvider>
        <Header />
      </ThemeProvider>
    );
    expect(screen.getByText('Cartify')).toBeInTheDocument();
    expect(screen.getByRole('banner')).toBeInTheDocument();
  });

  it('renders Footer with copyright and platform links', () => {
    render(<Footer />);
    expect(screen.getByRole('contentinfo')).toBeInTheDocument();
    expect(screen.getByText(/All rights reserved/i)).toBeInTheDocument();
  });
});

describe('Theme System Integration', () => {
  beforeEach(() => {
    localStorage.clear();
    document.documentElement.classList.remove('dark');
  });

  afterEach(() => {
    localStorage.clear();
    document.documentElement.classList.remove('dark');
  });

  it('toggles theme when ThemeToggle button is clicked', () => {
    render(
      <ThemeProvider>
        <ThemeToggle />
      </ThemeProvider>
    );

    const toggleBtn = screen.getByRole('button', { name: /switch to dark mode/i });
    expect(toggleBtn).toBeInTheDocument();

    // Click to switch to dark theme
    fireEvent.click(toggleBtn);
    expect(document.documentElement.classList.contains('dark')).toBe(true);
    expect(localStorage.getItem('cartify-theme-preference')).toBe('dark');

    // Click again to switch back to light theme
    fireEvent.click(toggleBtn);
    expect(document.documentElement.classList.contains('dark')).toBe(false);
    expect(localStorage.getItem('cartify-theme-preference')).toBe('light');
  });
});
