import type { TicketReply } from "@/lib/types";

type Props = {
  replies: TicketReply[];
};

export default function TicketThread({ replies }: Props) {
  return (
    <div className="space-y-4">
      {replies.length === 0 ? (
        <div className="rounded-xl border bg-white p-4 text-sm text-slate-500 shadow-sm">
          No replies yet.
        </div>
      ) : (
        replies.map((reply) => (
          <div key={reply.id} className="rounded-xl border bg-white p-4 shadow-sm">
            <div className="mb-2 flex items-center justify-between gap-4">
              <div>
                <p className="font-semibold text-slate-900">{reply.author_name}</p>
                <p className="text-xs text-slate-500">{reply.author_email}</p>
              </div>
              <div className="text-right">
                <p className="text-xs text-slate-500">
                  {new Date(reply.created_at).toLocaleString()}
                </p>
                <p className="mt-1 text-xs font-medium text-slate-600">
                  {reply.is_internal ? "Internal Note" : "Public Reply"}
                </p>
              </div>
            </div>

            <div className="whitespace-pre-wrap text-sm text-slate-800">{reply.body}</div>
          </div>
        ))
      )}
    </div>
  );
}