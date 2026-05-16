"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Film, Plus } from "lucide-react";
import { api, Project } from "@/lib/api";

const statusColors: Record<string, string> = {
  draft: "bg-yellow-100 text-yellow-800",
  storyboard: "bg-blue-100 text-blue-800",
  rendering: "bg-purple-100 text-purple-800 animate-pulse",
  done: "bg-green-100 text-green-800",
};

export default function ProjectsPage() {
  const [projects, setProjects] = useState<Project[] | null>(null);

  useEffect(() => {
    api.projects.list().then(setProjects).catch(() => setProjects([]));
  }, []);

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b bg-card">
        <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4">
          <Link href="/" className="flex items-center gap-2 text-lg font-semibold">
            <Film className="h-5 w-5 text-primary" />
            DClaw Video
          </Link>
          <Link href="/projects/new">
            <Button size="sm">
              <Plus className="mr-1 h-4 w-4" />
              New Project
            </Button>
          </Link>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-4 py-8">
        <h1 className="mb-6 text-3xl font-bold tracking-tight">Projects</h1>

        {projects === null ? (
          <p className="text-muted-foreground">Loading...</p>
        ) : projects.length === 0 ? (
          <Card className="border-dashed">
            <CardHeader>
              <CardTitle>No projects yet</CardTitle>
              <CardDescription>
                Create your first AI video project to get started.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Link href="/projects/new">
                <Button>
                  <Plus className="mr-1 h-4 w-4" />
                  Create Project
                </Button>
              </Link>
            </CardContent>
          </Card>
        ) : (
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {projects.map((project) => (
              <Link key={project.id} href={`/projects/${project.id}`}>
                <Card className="cursor-pointer transition-shadow hover:shadow-md">
                  <CardHeader className="pb-2">
                    <div className="flex items-center justify-between">
                      <CardTitle className="text-lg">{project.title}</CardTitle>
                      <Badge className={statusColors[project.status] || ""}>
                        {project.status}
                      </Badge>
                    </div>
                    <CardDescription className="line-clamp-2">
                      {project.script_text}
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <p className="text-xs text-muted-foreground">
                      Template: {project.template} · {" "}
                      {new Date(project.created_at).toLocaleDateString()}
                    </p>
                  </CardContent>
                </Card>
              </Link>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
