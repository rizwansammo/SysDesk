type Props = {
  title: string;
  subtitle?: string;
};

export default function Topbar({ title, subtitle }: Props) {
  return (
    <div className="border-b bg-white px-6 py-4">
      <h2 className="text-2xl font-semibold text-slate-900">{title}</h2>
      {subtitle ? <p className="mt-1 text-sm text-slate-500">{subtitle}</p> : null}
    </div>
  );
}