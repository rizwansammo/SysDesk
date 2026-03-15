"use client";

import { useEffect, useMemo, useState } from "react";
import Sidebar from "@/components/layout/Sidebar";
import Topbar from "@/components/layout/Topbar";
import MetricCard from "@/components/ui/MetricCard";
import TicketTable from "@/components/tickets/TicketTable";
import { fetchMyTickets } from "@/lib/services";
import type { Ticket } from "@/lib/types";

export default function CustomerDashboardPage() {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchMyTickets()
      .then(setTickets)
      .catch(() => setError("Failed to load your tickets"));
  }, []);

  const stats = useMemo(() => {
    return {
      open: tickets.filter((t) => t.status === "open").length,
      pending: tickets.filter((t) => t.status === "pending").length,
      resolved: tickets.filter((t) => t.status === "resolved").length,
    };
  }, [tickets]);

  return (
    <div className="flex min-h-screen bg-slate-100">
      <Sidebar />

      <div className="flex-1">
        <Topbar
          title="Customer Dashboard"
          subtitle="Track your support requests and create new tickets."
        />

        <main className="space-y-6 p-6">
          {error ? <p className="text-red-600">{error}</p> : null}

          <div className="grid gap-4 md:grid-cols-3">
            <MetricCard title="Open Tickets" value={stats.open} />
            <MetricCard title="Pending Tickets" value={stats.pending} />
            <MetricCard title="Resolved Tickets" value={stats.resolved} />
          </div>

          <div>
            <h3 className="mb-3 text-lg font-semibold text-slate-900">My Recent Tickets</h3>
            <TicketTable tickets={tickets} basePath="/customer/tickets" />
          </div>
        </main>
      </div>
    </div>
  );
}