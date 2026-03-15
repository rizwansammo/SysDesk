type Props = {
  title: string;
  value: string | number;
};

export default function MetricCard({ title, value }: Props) {
  return (
    <div className="rounded-xl border bg-white p-5 shadow-sm dark:border-slate-700 dark:bg-slate-900">
      <p className="text-sm text-slate-500 dark:text-slate-400">{title}</p>
      <p className="mt-2 text-3xl font-bold text-slate-900 dark:text-slate-100">{value}</p>
    </div>
  );
}