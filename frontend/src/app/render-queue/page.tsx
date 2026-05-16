"use client";

import { useEffect, useState } from "react";

interface Job {
  id: string;
  project_id: string;
  progress_percent: number;
  status: string;
  created_at: string;
}

export default function RenderQueuePage() {
  const [jobs, setJobs] = useState<Job[]>([]);

  useEffect(() => {
    // In a real app, fetch from /api/v1/render-jobs or similar
    setJobs([
      {
        id: "job-1",
        project_id: "proj-1",
        progress_percent: 75,
        status: "started",
        created_at: new Date().toISOString(),
      },
    ]);
  }, []);

  return (
    <main className="container mx-auto py-8 px-4">
      <h1 className="text-2xl font-bold mb-6">Render Queue</h1>
      <div className="space-y-4">
        {jobs.map((job) => (
          <div key={job.id} className="rounded-lg border bg-card p-4 space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-sm font-medium">{job.id}</span>
              <span className="text-xs px-2 py-1 rounded-full bg-muted">{job.status}</span>
            </div>
            <div className="w-full bg-muted rounded-full h-2">
              <div
                className="bg-primary h-2 rounded-full transition-all"
                style={{ width: `${job.progress_percent}%` }}
              />
            </div>
            <div className="text-xs text-muted-foreground">
              Project: {job.project_id} · {new Date(job.created_at).toLocaleString()}
            </div>
          </div>
        ))}
        {jobs.length === 0 && (
          <div className="text-center text-muted-foreground py-12">No active renders.</div>
        )}
      </div>
    </main>
  );
}
