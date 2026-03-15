"use client";

import { useEffect, useState } from "react";
import Sidebar from "@/components/layout/Sidebar";
import Topbar from "@/components/layout/Topbar";
import Footer from "@/components/layout/Footer";
import MetricCard from "@/components/ui/MetricCard";
import { fetchDashboard } from "@/lib/services";
import type { DashboardReport } from "@/lib/types";

export default function AgentDashboardPage() {
  const [data, setData] = useState<DashboardReport | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchDashboard()
      .then(setData)
      .catch(() => setError("Failed to load dashboard"));
  }, []);

  return (
    <div className="flex min-h-screen bg-slate-100 dark:bg-slate-950">
      <Sidebar />

      <div className="flex flex-1 flex-col">
        <Topbar
          title="Agent Dashboard"
          subtitle="Overview of tickets, SLAs, and workload."
        />

        <main className="flex-1 p-6">
          {error ? <p className="mb-4 text-red-600">{error}</p> : null}

          {!data ? (
            <p className="text-slate-500 dark:text-slate-400">Loading dashboard...</p>
          ) : (
            <div className="space-y-6">
              <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
                <MetricCard title="Open Tickets" value={data.open_tickets_count} />
                <MetricCard title="Pending Tickets" value={data.pending_tickets_count} />
                <MetricCard title="Resolved Tickets" value={data.resolved_tickets_count} />
                <MetricCard title="SLA Breached" value={data.sla_breached_count} />
              </div>

              <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-2">
                <MetricCard
                  title="Avg First Response (mins)"
                  value={data.avg_first_response_minutes ?? "N/A"}
                />
                <MetricCard
                  title="Avg Resolution (mins)"
                  value={data.avg_resolution_minutes ?? "N/A"}
                />
              </div>

              <div className="rounded-xl border bg-white p-5 shadow-sm dark:border-slate-700 dark:bg-slate-900">
                <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100">
                  Tickets by Status
                </h3>
                <div className="mt-4 space-y-2">
                  {data.tickets_by_status.map((item) => (
                    <div
                      key={item.status}
                      className="flex items-center justify-between rounded-lg border px-4 py-3 dark:border-slate-700"
                    >
                      <span className="capitalize text-slate-700 dark:text-slate-200">
                        {item.status}
                      </span>
                      <span className="font-semibold text-slate-900 dark:text-slate-100">
                        {item.count}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </main>

        <Footer />
      </div>
    </div>
  );
}