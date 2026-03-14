"use client";

import { useEffect, useState } from "react";
import Sidebar from "@/components/layout/Sidebar";
import Topbar from "@/components/layout/Topbar";
import TicketTable from "@/components/tickets/TicketTable";
import { fetchTickets } from "@/lib/services";
import type { Ticket } from "@/lib/types";

export default function AgentTicketsPage() {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchTickets()
      .then(setTickets)
      .catch(() => setError("Failed to load tickets"));
  }, []);

  return (
    <div className="flex min-h-screen bg-slate-100">
      <Sidebar />

      <div className="flex-1">
        <Topbar title="Tickets" subtitle="Manage all support tickets." />

        <main className="p-6">
          {error ? <p className="mb-4 text-red-600">{error}</p> : null}
          <TicketTable tickets={tickets} />
        </main>
      </div>
    </div>
  );
}