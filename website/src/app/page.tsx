export default function HomePage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-6 text-center">
      <div className="max-w-xl rounded-2xl border border-neutral-200 bg-white p-8 shadow-sm">
        <span className="inline-flex items-center rounded-full bg-emerald-50 px-3 py-1 text-xs font-semibold text-emerald-700">
          Module 1.1 Active
        </span>
        <h1 className="mt-4 text-3xl font-bold tracking-tight text-neutral-900">
          Cartify Storefront
        </h1>
        <p className="mt-2 text-sm text-neutral-600">
          Next.js App Router, TypeScript, and Tailwind CSS foundation initialized.
        </p>
        <div className="mt-6 border-t border-neutral-100 pt-6">
          <p className="text-xs text-neutral-500">
            Connected Architecture: Unified REST API &middot; PostgreSQL &middot; Redis &middot; Celery
          </p>
        </div>
      </div>
    </main>
  );
}
