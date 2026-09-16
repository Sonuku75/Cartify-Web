import React from "react";

export function CheckoutSummary() {
  return (
    <div className="rounded-xl border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-900 p-6 shadow-sm">
      <h3 className="text-base font-bold text-neutral-900 dark:text-white pb-4 border-b border-neutral-100 dark:border-neutral-800">
        Order Summary
      </h3>
      <div className="mt-4 space-y-3 text-sm text-neutral-600 dark:text-neutral-400">
        <div className="flex justify-between">
          <span>Subtotal</span>
          <span>$0.00</span>
        </div>
        <div className="flex justify-between">
          <span>Estimated Shipping</span>
          <span>Free</span>
        </div>
        <div className="flex justify-between font-bold text-neutral-900 dark:text-white pt-3 border-t border-neutral-100 dark:border-neutral-800">
          <span>Total</span>
          <span>$0.00</span>
        </div>
      </div>
      <p className="mt-4 text-xs text-neutral-500 text-center">
        Checkout foundation placeholder. Financial processing will be integrated in Module 6.
      </p>
    </div>
  );
}
