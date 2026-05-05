"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

interface Project {
  id: string;
  title: string;
  status: string;
  duration: number | null;
  created_at: string;
}

export default function ProjectsPage() {
  const [projects, setProjects] = useState<Project[]>([]);

  useEffect(() => {
    fetch("/api/v1/projects")
      .then((r) => r.json())
      .then(setProjects)
      .catch(() => setProjects([]));
  }, []);

  return (
    <main className="container mx-auto py-8 px-4">
      <div className="flex items-center justify-between mb-8">
        <h1 className="text-2xl font-bold">Projects</h1>
        <Link
          href="/projects/new"
          className="inline-flex h-10 items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90"
        >
          New Project
        </Link>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {projects.map((p) => (
          <Link key={p.id} href={`/projects/${p.id}`}>
            <div className="rounded-lg border bg-card p-4 hover:shadow-sm transition-shadow">
              <div className="flex items-center justify-between mb-2">
                <h2 className="font-semibold truncate">{p.title}</h2>
                <span className="text-xs px-2 py-1 rounded-full bg-muted">{p.status}</span>
              </div>
              <p className="text-sm text-muted-foreground">
                {p.duration ? `${p.duration}s` : "—"} · {new Date(p.created_at).toLocaleDateString()}
              </p>
            </div>
          </Link>
        ))}
        {projects.length === 0 && (
          <div className="col-span-full text-center text-muted-foreground py-12">
            No projects yet. Create one to get started.
          </div>
        )}
      </div>
    </main>
  );
}
