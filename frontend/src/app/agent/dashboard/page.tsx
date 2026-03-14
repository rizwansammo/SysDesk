"use client";

import { useEffect, useState } from "react";
import Sidebar from "@/components/layout/Sidebar";
import Topbar from "@/components/layout/Topbar";
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
    <div className="flex min-h-screen bg-slate-100">
      <Sidebar />

      <div className="flex-1">
        <Topbar
          title="Agent Dashboard"
          subtitle="Overview of tickets, SLAs, and workload."
        />

        <main className="p-6">
          {error ? <p className="mb-4 text-red-600">{error}</p> : null}

          {!data ? (
            <p className="text-slate-500">Loading dashboard...</p>
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

              <div className="rounded-xl border bg-white p-5 shadow-sm">
                <h3 className="text-lg font-semibold text-slate-900">Tickets by Status</h3>
                <div className="mt-4 space-y-2">
                  {data.tickets_by_status.map((item) => (
                    <div
                      key={item.status}
                      className="flex items-center justify-between rounded-lg border px-4 py-3"
                    >
                      <span className="capitalize text-slate-700">{item.status}</span>
                      <span className="font-semibold text-slate-900">{item.count}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}