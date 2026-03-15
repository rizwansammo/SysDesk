import type { TicketHistory } from "@/lib/types";

type Props = {
  history: TicketHistory[];
};

export default function TicketHistoryList({ history }: Props) {
  return (
    <div className="rounded-xl border bg-white p-4 shadow-sm">
      <h3 className="mb-4 text-lg font-semibold text-slate-900">Ticket History</h3>

      <div className="space-y-3">
        {history.length === 0 ? (
          <p className="text-sm text-slate-500">No history available.</p>
        ) : (
          history.map((item) => (
            <div key={item.id} className="border-b border-slate-100 pb-3 last:border-b-0">
              <p className="text-sm font-medium text-slate-900">{item.message || item.event_type}</p>
              <p className="mt-1 text-xs text-slate-500">
                {item.actor_name || "System"} • {new Date(item.created_at).toLocaleString()}
              </p>
            </div>
          ))
        )}
      </div>
    </div>
  );
}