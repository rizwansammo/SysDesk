import type { TicketSLA } from "@/lib/types";

type Props = {
  sla?: TicketSLA;
};

export default function TicketSLA({ sla }: Props) {
  return (
    <div className="rounded-xl border bg-white p-4 shadow-sm">
      <h3 className="mb-4 text-lg font-semibold text-slate-900">SLA</h3>

      {!sla ? (
        <p className="text-sm text-slate-500">No SLA data available.</p>
      ) : (
        <div className="space-y-3 text-sm text-slate-700">
          <div>
            <p className="text-slate-500">Policy</p>
            <p className="font-medium text-slate-900">{sla.policy_name || "No policy"}</p>
          </div>

          <div>
            <p className="text-slate-500">First Response Deadline</p>
            <p className="font-medium text-slate-900">
              {sla.first_response_deadline
                ? new Date(sla.first_response_deadline).toLocaleString()
                : "N/A"}
            </p>
          </div>

          <div>
            <p className="text-slate-500">Resolution Deadline</p>
            <p className="font-medium text-slate-900">
              {sla.resolution_deadline
                ? new Date(sla.resolution_deadline).toLocaleString()
                : "N/A"}
            </p>
          </div>

          <div>
            <p className="text-slate-500">First Response Breached</p>
            <p className={sla.first_response_breached ? "font-medium text-red-600" : "font-medium text-green-600"}>
              {sla.first_response_breached ? "Yes" : "No"}
            </p>
          </div>

          <div>
            <p className="text-slate-500">Resolution Breached</p>
            <p className={sla.resolution_breached ? "font-medium text-red-600" : "font-medium text-green-600"}>
              {sla.resolution_breached ? "Yes" : "No"}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}