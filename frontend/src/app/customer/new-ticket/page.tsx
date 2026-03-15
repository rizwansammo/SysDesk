"use client";

import { useState } from "react";
import { api } from "@/lib/api";
import Sidebar from "@/components/layout/Sidebar";
import Topbar from "@/components/layout/Topbar";

export default function NewTicketPage() {
  const [subject, setSubject] = useState("");
  const [description, setDescription] = useState("");
  const [message, setMessage] = useState("");

  async function submitTicket() {
    try {
      await api.post("/tickets/", {
        subject,
        description,
        priority: "medium",
      });

      setMessage("Ticket created successfully.");
      setSubject("");
      setDescription("");
    } catch {
      setMessage("Failed to create ticket.");
    }
  }

  return (
    <div className="flex min-h-screen bg-slate-100">
      <Sidebar />

      <div className="flex-1">
        <Topbar
          title="Create Ticket"
          subtitle="Submit a support request."
        />

        <main className="p-6">
          <div className="rounded-xl border bg-white p-6 shadow-sm max-w-xl">
            <label className="block text-sm font-medium text-slate-700">
              Subject
            </label>

            <input
              className="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2"
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
            />

            <label className="mt-4 block text-sm font-medium text-slate-700">
              Description
            </label>

            <textarea
              className="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2 min-h-[120px]"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            />

            <button
              onClick={submitTicket}
              className="mt-4 rounded-lg bg-slate-900 px-4 py-2 text-white"
            >
              Submit Ticket
            </button>

            {message && (
              <p className="mt-3 text-sm text-slate-600">{message}</p>
            )}
          </div>
        </main>
      </div>
    </div>
  );
}