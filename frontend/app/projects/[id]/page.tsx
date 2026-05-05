"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";

interface Scene {
  id: string;
  scene_number: number;
  narration_text: string;
  visual_prompt: string;
  duration_seconds: number;
  status: string;
}

interface Project {
  id: string;
  title: string;
  status: string;
}

export default function ProjectDetailPage() {
  const { id } = useParams();
  const [project, setProject] = useState<Project | null>(null);
  const [scenes, setScenes] = useState<Scene[]>([]);

  useEffect(() => {
    if (!id) return;
    fetch(`/api/v1/projects/${id}`)
      .then((r) => r.json())
      .then(setProject)
      .catch(() => setProject(null));
    fetch(`/api/v1/projects/${id}/scenes`)
      .then((r) => r.json())
      .then(setScenes)
      .catch(() => setScenes([]));
  }, [id]);

  const generateStoryboard = async () => {
    await fetch(`/api/v1/projects/${id}/storyboard`, { method: "POST" });
    alert("Storyboard generation queued!");
  };

  const renderProject = async () => {
    await fetch(`/api/v1/projects/${id}/render`, { method: "POST" });
    alert("Render queued! Check status.");
  };

  if (!project) return <div className="p-8">Loading...</div>;

  return (
    <main className="container mx-auto py-8 px-4">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">{project.title}</h1>
        <div className="flex gap-2">
          <button
            onClick={generateStoryboard}
            className="inline-flex h-10 items-center justify-center rounded-md border border-input bg-background px-4 py-2 text-sm font-medium hover:bg-accent"
          >
            Generate Storyboard
          </button>
          <button
            onClick={renderProject}
            className="inline-flex h-10 items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90"
          >
            Render Video
          </button>
        </div>
      </div>
      <div className="space-y-4">
        {scenes.map((scene) => (
          <div key={scene.id} className="rounded-lg border bg-card p-4">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-semibold">Scene {scene.scene_number}</span>
              <span className="text-xs px-2 py-1 rounded-full bg-muted">{scene.status}</span>
            </div>
            <p className="text-sm text-muted-foreground mb-2">{scene.narration_text}</p>
            <p className="text-xs text-muted-foreground">Duration: {scene.duration_seconds}s</p>
          </div>
        ))}
        {scenes.length === 0 && (
          <div className="text-center text-muted-foreground py-12">No scenes yet.</div>
        )}
      </div>
      <div className="mt-8">
        <Link href="/projects" className="text-sm text-muted-foreground hover:underline">
          ← Back to projects
        </Link>
      </div>
    </main>
  );
}
