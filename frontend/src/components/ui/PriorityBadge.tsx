import clsx from "clsx";

type Props = {
  value: string;
};

export default function PriorityBadge({ value }: Props) {
  return (
    <span
      className={clsx(
        "inline-flex rounded-full px-3 py-1 text-xs font-semibold capitalize",
        value === "low" && "bg-slate-200 text-slate-700",
        value === "medium" && "bg-blue-100 text-blue-700",
        value === "high" && "bg-orange-100 text-orange-700",
        value === "critical" && "bg-red-100 text-red-700"
      )}
    >
      {value}
    </span>
  );
}