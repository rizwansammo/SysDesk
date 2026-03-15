"use client";

import { useCallback, useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Sidebar from "@/components/layout/Sidebar";
import Topbar from "@/components/layout/Topbar";
import StatusBadge from "@/components/ui/StatusBadge";
import PriorityBadge from "@/components/ui/PriorityBadge";
import TicketThread from "@/components/tickets/TicketThread";
import TicketHistoryList from "@/components/tickets/TicketHistoryList";
import TicketSLA from "@/components/tickets/TicketSLA";
import TicketActionPanel from "@/components/tickets/TicketActionPanel";
import { fetchMe, fetchTicketDetail } from "@/lib/services";
import type { CurrentUser, TicketDetail } from "@/lib/types";

export default function AgentTicketDetailPage() {
  const params = useParams();
  const id = params?.id ? String(params.id) : "";

  const [ticket, setTicket] = useState<TicketDetail | null>(null);
  const [currentUser, setCurrentUser] = useState<CurrentUser | null>(null);
  const [error, setError] = useState("");

  const loadTicket = useCallback(async () => {
    if (!id) return;

    try {
      const data = await fetchTicketDetail(id);
      setTicket(data);
      setError("");
    } catch {
      setError("Failed to load ticket detail");
    }
  }, [id]);

  useEffect(() => {
    fetchMe().then(setCurrentUser).catch(() => {});
    loadTicket();
  }, [loadTicket]);

  const isAgent =
    currentUser?.role.code === "agent" || currentUser?.role.code === "super_admin";

  return (
    <div className="flex min-h-screen bg-slate-100">
      <Sidebar />

      <div className="flex-1">
        <Topbar title="Ticket Detail" subtitle="View conversation, history, SLA, and actions." />

        <main className="p-6">
          {error ? <p className="mb-4 text-red-600">{error}</p> : null}

          {!ticket ? (
            <p className="text-slate-500">Loading ticket...</p>
          ) : (
            <div className="grid gap-6 xl:grid-cols-3">
              <div className="space-y-6 xl:col-span-2">
                <div className="rounded-xl border bg-white p-5 shadow-sm">
                  <div className="mb-4 flex flex-wrap items-center gap-3">
                    <h1 className="text-2xl font-bold text-slate-900">{ticket.subject}</h1>
                    <StatusBadge value={ticket.status} />
                    <PriorityBadge value={ticket.priority} />
                  </div>

                  <div className="grid gap-4 text-sm md:grid-cols-2">
                    <div>
                      <p className="text-slate-500">Ticket Number</p>
                      <p className="font-medium text-slate-900">{ticket.ticket_number}</p>
                    </div>
                    <div>
                      <p className="text-slate-500">Organization</p>
                      <p className="font-medium text-slate-900">{ticket.organization_name}</p>
                    </div>
                    <div>
                      <p className="text-slate-500">Created By</p>
                      <p className="font-medium text-slate-900">{ticket.created_by_name}</p>
                    </div>
                    <div>
                      <p className="text-slate-500">Assigned Agent</p>
                      <p className="font-medium text-slate-900">
                        {ticket.assigned_agent_name || "Unassigned"}
                      </p>
                    </div>
                    <div>
                      <p className="text-slate-500">Category</p>
                      <p className="font-medium text-slate-900">{ticket.category || "N/A"}</p>
                    </div>
                    <div>
                      <p className="text-slate-500">Source</p>
                      <p className="font-medium capitalize text-slate-900">{ticket.source}</p>
                    </div>
                  </div>

                  <div className="mt-5">
                    <p className="mb-2 text-sm text-slate-500">Description</p>
                    <div className="whitespace-pre-wrap rounded-lg bg-slate-50 p-4 text-sm text-slate-800">
                      {ticket.description}
                    </div>
                  </div>
                </div>

                <div>
                  <h2 className="mb-3 text-lg font-semibold text-slate-900">Conversation</h2>
                  <TicketThread replies={ticket.replies} />
                </div>
              </div>

              <div className="space-y-6">
                {isAgent ? <TicketActionPanel ticket={ticket} onRefresh={loadTicket} /> : null}

                <div className="rounded-xl border bg-white p-4 shadow-sm">
                  <h3 className="mb-4 text-lg font-semibold text-slate-900">Metadata</h3>

                  <div className="space-y-3 text-sm">
                    <div>
                      <p className="text-slate-500">Created At</p>
                      <p className="font-medium text-slate-900">
                        {new Date(ticket.created_at).toLocaleString()}
                      </p>
                    </div>
                    <div>
                      <p className="text-slate-500">Updated At</p>
                      <p className="font-medium text-slate-900">
                        {new Date(ticket.updated_at).toLocaleString()}
                      </p>
                    </div>
                    <div>
                      <p className="text-slate-500">First Response At</p>
                      <p className="font-medium text-slate-900">
                        {ticket.first_response_at
                          ? new Date(ticket.first_response_at).toLocaleString()
                          : "Not yet"}
                      </p>
                    </div>
                    <div>
                      <p className="text-slate-500">Resolved At</p>
                      <p className="font-medium text-slate-900">
                        {ticket.resolved_at ? new Date(ticket.resolved_at).toLocaleString() : "Not resolved"}
                      </p>
                    </div>
                    <div>
                      <p className="text-slate-500">Closed At</p>
                      <p className="font-medium text-slate-900">
                        {ticket.closed_at ? new Date(ticket.closed_at).toLocaleString() : "Not closed"}
                      </p>
                    </div>
                  </div>
                </div>

                <TicketSLA sla={ticket.sla} />
                <TicketHistoryList history={ticket.history} />
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}