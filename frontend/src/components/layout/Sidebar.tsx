"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import clsx from "clsx";

const items = [
  { href: "/agent/dashboard", label: "Dashboard" },
  { href: "/agent/tickets", label: "Tickets" },
  { href: "/portal/tickets/new", label: "Create Ticket" },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 border-r bg-white p-4">
      <div className="mb-6">
        <h1 className="text-xl font-bold text-slate-900">SysDesk Helpdesk</h1>
        <p className="text-sm text-slate-500">Support Workspace</p>
      </div>

      <nav className="space-y-2">
        {items.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className={clsx(
              "block rounded-lg px-3 py-2 text-sm font-medium transition",
              pathname === item.href
                ? "bg-slate-900 text-white"
                : "text-slate-700 hover:bg-slate-100"
            )}
          >
            {item.label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}