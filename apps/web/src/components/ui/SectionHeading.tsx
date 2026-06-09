export function SectionHeading({ title, hint }: { title: string; hint?: string }) {
  return (
    <div className="mb-5">
      <h2 className="text-2xl font-bold tracking-tight text-white">{title}</h2>
      {hint && <p className="mt-1.5 text-[0.9375rem] font-normal text-white/[0.92]">{hint}</p>}
    </div>
  );
}