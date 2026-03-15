"use client";

import { useEffect, useState } from "react";
import { fetchTickets } from "@/lib/services";
import type { Ticket } from "@/lib/types";
import Sidebar from "@/components/layout/Sidebar";
import Topbar from "@/components/layout/Topbar";
import StatusBadge from "@/components/ui/StatusBadge";
import PriorityBadge from "@/components/ui/PriorityBadge";
import Link from "next/link";

export default function CustomerTicketsPage() {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [error, setError] = useState("");

  async function loadTickets() {
    try {
      const data = await fetchTickets();
      setTickets(data);
    } catch {
      setError("Failed to load tickets");
    }
  }

  useEffect(() => {
    loadTickets();
  }, []);

  return (
    <div className="flex min-h-screen bg-slate-100">
      <Sidebar />

      <div className="flex-1">
        <Topbar
          title="My Tickets"
          subtitle="View and track your support tickets."
        />

        <main className="p-6">
          {error ? <p className="text-red-600">{error}</p> : null}

          <div className="rounded-xl border bg-white shadow-sm">
            <table className="w-full text-sm">
              <thead className="border-b bg-slate-50">
                <tr>
                  <th className="p-3 text-left">Ticket</th>
                  <th className="p-3 text-left">Subject</th>
                  <th className="p-3 text-left">Status</th>
                  <th className="p-3 text-left">Priority</th>
                  <th className="p-3 text-left">Updated</th>
                </tr>
              </thead>

              <tbody>
                {tickets.map((ticket) => (
                  <tr
                    key={ticket.id}
                    className="border-b hover:bg-slate-50"
                  >
                    <td className="p-3">
                      <Link
                        className="text-blue-600 hover:underline"
                        href={`/customer/tickets/${ticket.id}`}
                      >
                        {ticket.ticket_number}
                      </Link>
                    </td>

                    <td className="p-3">{ticket.subject}</td>

                    <td className="p-3">
                      <StatusBadge value={ticket.status} />
                    </td>

                    <td className="p-3">
                      <PriorityBadge value={ticket.priority} />
                    </td>

                    <td className="p-3">
                      {new Date(ticket.updated_at).toLocaleString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </main>
      </div>
    </div>
  );
}