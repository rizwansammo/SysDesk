"use client";

import { useEffect, useState } from "react";
import type { AgentUser, TicketDetail } from "@/lib/types";
import {
  addTicketReply,
  assignTicket,
  changeTicketPriority,
  changeTicketStatus,
  fetchAgents,
} from "@/lib/services";

type Props = {
  ticket: TicketDetail;
  onRefresh: () => Promise<void>;
};

export default function TicketActionPanel({ ticket, onRefresh }: Props) {
  const [agents, setAgents] = useState<AgentUser[]>([]);
  const [assignedAgentId, setAssignedAgentId] = useState<string>(
    ticket.assigned_agent ? String(ticket.assigned_agent) : ""
  );
  const [status, setStatus] = useState(ticket.status);
  const [priority, setPriority] = useState(ticket.priority);
  const [replyBody, setReplyBody] = useState("");
  const [internalBody, setInternalBody] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetchAgents().then(setAgents).catch(() => {});
  }, []);

  useEffect(() => {
    setAssignedAgentId(ticket.assigned_agent ? String(ticket.assigned_agent) : "");
    setStatus(ticket.status);
    setPriority(ticket.priority);
  }, [ticket]);

  async function handleAssign() {
    setLoading(true);
    setMessage("");
    try {
      await assignTicket(ticket.id, assignedAgentId ? Number(assignedAgentId) : null);
      await onRefresh();
      setMessage("Ticket assignment updated.");
    } catch {
      setMessage("Failed to update assignment.");
    } finally {
      setLoading(false);
    }
  }

  async function handleStatus() {
    setLoading(true);
    setMessage("");
    try {
      await changeTicketStatus(ticket.id, status);
      await onRefresh();
      setMessage("Ticket status updated.");
    } catch {
      setMessage("Failed to update status.");
    } finally {
      setLoading(false);
    }
  }

  async function handlePriority() {
    setLoading(true);
    setMessage("");
    try {
      await changeTicketPriority(ticket.id, priority);
      await onRefresh();
      setMessage("Ticket priority updated.");
    } catch {
      setMessage("Failed to update priority.");
    } finally {
      setLoading(false);
    }
  }

  async function handlePublicReply() {
    if (!replyBody.trim()) return;
    setLoading(true);
    setMessage("");
    try {
      await addTicketReply(ticket.id, replyBody, false);
      setReplyBody("");
      await onRefresh();
      setMessage("Public reply added.");
    } catch {
      setMessage("Failed to add public reply.");
    } finally {
      setLoading(false);
    }
  }

  async function handleInternalNote() {
    if (!internalBody.trim()) return;
    setLoading(true);
    setMessage("");
    try {
      await addTicketReply(ticket.id, internalBody, true);
      setInternalBody("");
      await onRefresh();
      setMessage("Internal note added.");
    } catch {
      setMessage("Failed to add internal note.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-6">
      <div className="rounded-xl border bg-white p-4 shadow-sm">
        <h3 className="mb-4 text-lg font-semibold text-slate-900">Actions</h3>

        <div className="space-y-4">
          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">
              Assign Agent
            </label>
            <div className="flex gap-2">
              <select
                className="flex-1 rounded-lg border border-slate-300 bg-white px-3 py-2 text-slate-900"
                value={assignedAgentId}
                onChange={(e) => setAssignedAgentId(e.target.value)}
              >
                <option value="">Unassigned</option>
                {agents.map((agent) => (
                  <option key={agent.id} value={agent.id}>
                    {agent.full_name || agent.email}
                  </option>
                ))}
              </select>
              <button
                onClick={handleAssign}
                disabled={loading}
                className="rounded-lg bg-slate-900 px-4 py-2 text-white disabled:opacity-60"
              >
                Save
              </button>
            </div>
          </div>

          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Status</label>
            <div className="flex gap-2">
              <select
                className="flex-1 rounded-lg border border-slate-300 bg-white px-3 py-2 text-slate-900"
                value={status}
                onChange={(e) => setStatus(e.target.value)}
              >
                <option value="open">Open</option>
                <option value="pending">Pending</option>
                <option value="resolved">Resolved</option>
                <option value="closed">Closed</option>
              </select>
              <button
                onClick={handleStatus}
                disabled={loading}
                className="rounded-lg bg-slate-900 px-4 py-2 text-white disabled:opacity-60"
              >
                Save
              </button>
            </div>
          </div>

          <div>
            <label className="mb-1 block text-sm font-medium text-slate-700">Priority</label>
            <div className="flex gap-2">
              <select
                className="flex-1 rounded-lg border border-slate-300 bg-white px-3 py-2 text-slate-900"
                value={priority}
                onChange={(e) => setPriority(e.target.value)}
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="critical">Critical</option>
              </select>
              <button
                onClick={handlePriority}
                disabled={loading}
                className="rounded-lg bg-slate-900 px-4 py-2 text-white disabled:opacity-60"
              >
                Save
              </button>
            </div>
          </div>
        </div>

        {message ? <p className="mt-4 text-sm text-slate-600">{message}</p> : null}
      </div>

      <div className="rounded-xl border bg-white p-4 shadow-sm">
        <h3 className="mb-3 text-lg font-semibold text-slate-900">Public Reply</h3>
        <textarea
          className="min-h-[120px] w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-slate-900"
          value={replyBody}
          onChange={(e) => setReplyBody(e.target.value)}
          placeholder="Write a public reply to the customer..."
        />
        <button
          onClick={handlePublicReply}
          disabled={loading}
          className="mt-3 rounded-lg bg-slate-900 px-4 py-2 text-white disabled:opacity-60"
        >
          Send Reply
        </button>
      </div>

      <div className="rounded-xl border bg-white p-4 shadow-sm">
        <h3 className="mb-3 text-lg font-semibold text-slate-900">Internal Note</h3>
        <textarea
          className="min-h-[120px] w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-slate-900"
          value={internalBody}
          onChange={(e) => setInternalBody(e.target.value)}
          placeholder="Write an internal note for agents only..."
        />
        <button
          onClick={handleInternalNote}
          disabled={loading}
          className="mt-3 rounded-lg bg-slate-900 px-4 py-2 text-white disabled:opacity-60"
        >
          Add Note
        </button>
      </div>
    </div>
  );
}