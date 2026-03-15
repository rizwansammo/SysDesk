"use client";

import { useState } from "react";
import { addTicketReply } from "@/lib/services";

type Props = {
  ticketId: number;
  onRefresh: () => Promise<void>;
};

export default function CustomerReplyPanel({ ticketId, onRefresh }: Props) {
  const [body, setBody] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  async function handleReply() {
    if (!body.trim()) return;

    setLoading(true);
    setMessage("");

    try {
      await addTicketReply(ticketId, body, false);
      setBody("");
      await onRefresh();
      setMessage("Reply sent successfully.");
    } catch {
      setMessage("Failed to send reply.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="rounded-xl border bg-white p-4 shadow-sm">
      <h3 className="mb-3 text-lg font-semibold text-slate-900">Reply to Ticket</h3>

      <textarea
        className="min-h-[140px] w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-slate-900"
        value={body}
        onChange={(e) => setBody(e.target.value)}
        placeholder="Write your reply..."
      />

      <button
        onClick={handleReply}
        disabled={loading}
        className="mt-3 rounded-lg bg-slate-900 px-4 py-2 text-white disabled:opacity-60"
      >
        {loading ? "Sending..." : "Send Reply"}
      </button>

      {message ? <p className="mt-3 text-sm text-slate-600">{message}</p> : null}
    </div>
  );
}