import React from "react";
import Link from "next/link";
import { User, Package, Heart, Settings } from "lucide-react";

export function AccountNav() {
  const items = [
    { label: "Profile", icon: User, href: "#profile" },
    { label: "Orders", icon: Package, href: "#orders" },
    { label: "Wishlist", icon: Heart, href: "#wishlist" },
    { label: "Settings", icon: Settings, href: "#settings" },
  ];

  return (
    <nav className="flex flex-col space-y-1 p-2 rounded-xl border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-900" aria-label="Account Navigation">
      {items.map((item) => {
        const Icon = item.icon;
        return (
          <Link
            key={item.label}
            href={item.href}
            className="flex items-center space-x-3 px-3 py-2 rounded-lg text-sm font-medium text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-800 transition-colors"
          >
            <Icon className="w-4 h-4 text-neutral-500" />
            <span>{item.label}</span>
          </Link>
        );
      })}
    </nav>
  );
}
