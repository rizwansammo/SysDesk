"use client";

import Sidebar from "@/components/layout/Sidebar";
import Topbar from "@/components/layout/Topbar";

export default function CustomerDashboardPage() {
  return (
    <div className="flex min-h-screen bg-slate-100">
      <Sidebar />

      <div className="flex-1">
        <Topbar
          title="Customer Portal"
          subtitle="View your support tickets and create new ones."
        />

        <main className="p-6">
          <div className="rounded-xl border bg-white p-6 shadow-sm">
            <h2 className="text-xl font-semibold text-slate-900">
              Welcome to SysDesk Support
            </h2>

            <p className="mt-2 text-slate-600">
              You can create support tickets and track responses from the support team.
            </p>
          </div>
        </main>
      </div>
    </div>
  );
}