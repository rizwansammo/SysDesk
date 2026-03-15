"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import clsx from "clsx";
import { useEffect, useState } from "react";
import { fetchMe, logout } from "@/lib/services";
import type { CurrentUser } from "@/lib/types";

export default function Sidebar() {
  const pathname = usePathname();
  const [user, setUser] = useState<CurrentUser | null>(null);

  useEffect(() => {
    fetchMe().then(setUser).catch(() => {});
  }, []);

  const isAgent =
    user?.role.code === "agent" || user?.role.code === "super_admin";

  const items = isAgent
    ? [
        { href: "/agent/dashboard", label: "Dashboard" },
        { href: "/agent/tickets", label: "Tickets" },
        { href: "/portal/tickets/new", label: "Create Ticket" },
      ]
    : [
        { href: "/customer/dashboard", label: "Dashboard" },
        { href: "/customer/tickets", label: "My Tickets" },
        { href: "/customer/new-ticket", label: "Create Ticket" },
      ];

  return (
    <aside className="w-64 border-r bg-white p-4">
      <div className="mb-6">
        <h1 className="text-xl font-bold text-slate-900">SysDesk Helpdesk</h1>
        <p className="text-sm text-slate-500">
          {isAgent ? "Support Workspace" : "Customer Portal"}
        </p>
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

      <div className="mt-8 border-t pt-4">
        <button
          onClick={() => {
            logout();
            window.location.href = "/login";
          }}
          className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm text-slate-700 hover:bg-slate-100"
        >
          Logout
        </button>
      </div>
    </aside>
  );
}