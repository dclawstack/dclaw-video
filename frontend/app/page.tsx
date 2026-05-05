import Link from "next/link";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-6 p-24">
      <h1 className="text-4xl font-bold tracking-tight">DClaw Video</h1>
      <p className="text-muted-foreground">AI Video Director & Editor</p>
      <div className="flex gap-4">
        <Link
          href="/projects"
          className="inline-flex h-10 items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90"
        >
          View Projects
        </Link>
        <Link
          href="/projects/new"
          className="inline-flex h-10 items-center justify-center rounded-md border border-input bg-background px-4 py-2 text-sm font-medium hover:bg-accent hover:text-accent-foreground"
        >
          New Project
        </Link>
      </div>
    </main>
  );
}
