"use client";

import { useState } from "react";
import Sidebar from "@/components/layout/Sidebar";
import Topbar from "@/components/layout/Topbar";
import { createTicket } from "@/lib/services";

export default function CustomerNewTicketPage() {
  const [subject, setSubject] = useState("");
  const [description, setDescription] = useState("");
  const [category, setCategory] = useState("");
  const [priority, setPriority] = useState("medium");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit() {
    setMessage("");
    setLoading(true);

    try {
      await createTicket({
        subject,
        description,
        category,
        priority,
      });

      setMessage("Ticket created successfully.");
      setSubject("");
      setDescription("");
      setCategory("");
      setPriority("medium");
    } catch {
      setMessage("Failed to create ticket.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex min-h-screen bg-slate-100">
      <Sidebar />

      <div className="flex-1">
        <Topbar title="Create Ticket" subtitle="Submit a new support request." />

        <main className="p-6">
          <div className="max-w-2xl rounded-xl border bg-white p-6 shadow-sm">
            <div className="space-y-4">
              <div>
                <label className="mb-1 block text-sm font-medium text-slate-700">Subject</label>
                <input
                  className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-slate-900"
                  value={subject}
                  onChange={(e) => setSubject(e.target.value)}
                />
              </div>

              <div>
                <label className="mb-1 block text-sm font-medium text-slate-700">Description</label>
                <textarea
                  className="min-h-[140px] w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-slate-900"
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                />
              </div>

              <div>
                <label className="mb-1 block text-sm font-medium text-slate-700">Category</label>
                <input
                  className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-slate-900"
                  value={category}
                  onChange={(e) => setCategory(e.target.value)}
                />
              </div>

              <div>
                <label className="mb-1 block text-sm font-medium text-slate-700">Priority</label>
                <select
                  className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-slate-900"
                  value={priority}
                  onChange={(e) => setPriority(e.target.value)}
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                  <option value="critical">Critical</option>
                </select>
              </div>

              <button
                onClick={handleSubmit}
                disabled={loading}
                className="rounded-lg bg-slate-900 px-4 py-2 text-white disabled:opacity-60"
              >
                {loading ? "Submitting..." : "Submit Ticket"}
              </button>

              {message ? <p className="text-sm text-slate-600">{message}</p> : null}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}