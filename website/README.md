# Cartify Website (Frontend)

This directory contains the responsive web application for Cartify, built with Next.js App Router, TypeScript, and Tailwind CSS.

---

## Technology Stack

- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **API Communication**: REST API client connecting to `/api/v1/`

---

## Directory Structure

```
website/
├── src/
│   └── app/            # App Router routes, layouts, and global styles
│       ├── layout.tsx  # Root layout
│       ├── page.tsx    # Foundation landing page
│       └── globals.css # Global CSS & Tailwind directives
├── package.json        # Dependencies & scripts
├── tsconfig.json       # TypeScript configuration
├── next.config.ts      # Next.js configuration
├── tailwind.config.ts  # Tailwind CSS configuration
├── postcss.config.mjs  # PostCSS configuration
├── .env.example        # Environment variable template
└── .gitignore          # Website-specific gitignore
```

---

## Available Scripts (Reference)

- `npm run dev`: Starts local Next.js development server at `http://localhost:3000`
- `npm run build`: Compiles production build
- `npm run start`: Starts production server
- `npm run lint`: Executes ESLint checks
