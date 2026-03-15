import clsx from "clsx";

type Props = {
  value: string;
};

export default function StatusBadge({ value }: Props) {
  return (
    <span
      className={clsx(
        "inline-flex rounded-full px-3 py-1 text-xs font-semibold capitalize",
        value === "open" && "bg-blue-100 text-blue-700",
        value === "pending" && "bg-amber-100 text-amber-700",
        value === "resolved" && "bg-green-100 text-green-700",
        value === "closed" && "bg-slate-200 text-slate-700"
      )}
    >
      {value}
    </span>
  );
}