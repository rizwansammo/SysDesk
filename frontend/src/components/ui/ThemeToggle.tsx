"use client";

import { useEffect, useState } from "react";
import { applyTheme, getStoredTheme, ThemeMode } from "@/lib/theme";

export default function ThemeToggle() {
  const [theme, setTheme] = useState<ThemeMode>("light");

  useEffect(() => {
    const current = getStoredTheme();
    setTheme(current);
    applyTheme(current);
  }, []);

  function toggleTheme() {
    const nextTheme: ThemeMode = theme === "light" ? "dark" : "light";
    setTheme(nextTheme);
    applyTheme(nextTheme);
  }

  return (
    <button
      onClick={toggleTheme}
      className="rounded-lg border px-3 py-2 text-sm text-slate-700 hover:bg-slate-100 dark:text-slate-100 dark:hover:bg-slate-800"
    >
      {theme === "light" ? "Dark Mode" : "Light Mode"}
    </button>
  );
}