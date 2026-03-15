import ThemeToggle from "@/components/ui/ThemeToggle";

type Props = {
  title: string;
  subtitle?: string;
};

export default function Topbar({ title, subtitle }: Props) {
  return (
    <div className="flex items-start justify-between border-b bg-white px-6 py-4 dark:border-slate-700 dark:bg-slate-900">
      <div>
        <h2 className="text-2xl font-semibold text-slate-900 dark:text-slate-100">{title}</h2>
        {subtitle ? (
          <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">{subtitle}</p>
        ) : null}
      </div>

      <ThemeToggle />
    </div>
  );
}