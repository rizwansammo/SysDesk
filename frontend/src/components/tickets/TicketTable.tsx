import type { Ticket } from "@/lib/types";

type Props = {
  tickets: Ticket[];
};

export default function TicketTable({ tickets }: Props) {
  return (
    <div className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">
      <table className="min-w-full text-sm text-slate-900">
        <thead className="bg-slate-50 text-slate-700">
          <tr>
            <th className="px-4 py-3 text-left font-medium">Ticket #</th>
            <th className="px-4 py-3 text-left font-medium">Subject</th>
            <th className="px-4 py-3 text-left font-medium">Organization</th>
            <th className="px-4 py-3 text-left font-medium">Status</th>
            <th className="px-4 py-3 text-left font-medium">Priority</th>
            <th className="px-4 py-3 text-left font-medium">Assigned</th>
          </tr>
        </thead>
        <tbody className="bg-white text-slate-900">
          {tickets.map((ticket) => (
            <tr key={ticket.id} className="border-t border-slate-200">
              <td className="px-4 py-3">{ticket.ticket_number}</td>
              <td className="px-4 py-3">{ticket.subject}</td>
              <td className="px-4 py-3">{ticket.organization_name}</td>
              <td className="px-4 py-3 capitalize">{ticket.status}</td>
              <td className="px-4 py-3 capitalize">{ticket.priority}</td>
              <td className="px-4 py-3">{ticket.assigned_agent_name || "Unassigned"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}