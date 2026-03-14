import Link from "next/link";

export default function HomePage() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-100 p-6">
      <div className="w-full max-w-md rounded-2xl border bg-white p-8 shadow-sm">
        <h1 className="text-3xl font-bold text-slate-900">SysDesk Helpdesk</h1>
        <p className="mt-2 text-sm text-slate-500">
          Multi-tenant helpdesk platform for MSP support teams.
        </p>

        <div className="mt-6 space-y-3">
          <Link
            href="/login"
            className="block rounded-lg bg-slate-900 px-4 py-3 text-center text-white"
          >
            Go to Login
          </Link>
          <Link
            href="/agent/dashboard"
            className="block rounded-lg border px-4 py-3 text-center text-slate-700"
          >
            Open Dashboard
          </Link>
        </div>
      </div>
    </main>
  );
}