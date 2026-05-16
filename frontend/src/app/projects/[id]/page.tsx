"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { api, Project, Scene } from "@/lib/api";
import { ArrowLeft, Play, Trash, Wand2 } from "lucide-react";

const statusColors: Record<string, string> = {
  draft: "bg-yellow-100 text-yellow-800",
  storyboard: "bg-blue-100 text-blue-800",
  rendering: "bg-purple-100 text-purple-800 animate-pulse",
  done: "bg-green-100 text-green-800",
};

export default function ProjectDetailPage() {
  const params = useParams();
  const router = useRouter();
  const projectId = params.id as string;

  const [project, setProject] = useState<Project | null>(null);
  const [scenes, setScenes] = useState<Scene[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function load() {
      try {
        const [p, s] = await Promise.all([
          api.projects.get(projectId),
          api.scenes.listByProject(projectId),
        ]);
        setProject(p);
        setScenes(s);
      } catch {
        setError("Failed to load project. Make sure the backend is running.");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [projectId]);

  const handleDelete = async () => {
    if (!confirm("Are you sure you want to delete this project?")) return;
    try {
      await api.projects.remove(projectId);
      router.push("/projects");
    } catch {
      setError("Failed to delete project.");
    }
  };

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        Loading...
      </div>
    );
  }

  if (!project) {
    return (
      <div className="flex min-h-screen flex-col items-center justify-center gap-4">
        <h1 className="text-2xl font-bold">Project not found</h1>
        <Link href="/projects">
          <Button>Back to Projects</Button>
        </Link>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b bg-card">
        <div className="mx-auto flex h-16 max-w-5xl items-center justify-between px-4">
          <div className="flex items-center gap-4">
            <Link href="/projects">
              <ArrowLeft className="h-5 w-5 text-muted-foreground" />
            </Link>
            <div>
              <h1 className="text-lg font-semibold">{project.title}</h1>
              <p className="text-xs text-muted-foreground">{project.template}</p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Badge className={statusColors[project.status] || ""}>{project.status}</Badge>
            <Button variant="outline" size="sm" onClick={handleDelete}>
              <Trash className="mr-1 h-4 w-4" />
              Delete
            </Button>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-5xl px-4 py-6">
        {error && <p className="mb-4 text-sm text-destructive">{error}</p>}

        <Tabs defaultValue="scenes">
          <TabsList>
            <TabsTrigger value="scenes">Scenes</TabsTrigger>
            <TabsTrigger value="script">Script</TabsTrigger>
            <TabsTrigger value="render">Render</TabsTrigger>
          </TabsList>

          <TabsContent value="scenes" className="mt-4 space-y-4">
            {scenes.length === 0 ? (
              <Card className="border-dashed">
                <CardContent className="py-8 text-center">
                  <p className="text-muted-foreground">No scenes yet.</p>
                </CardContent>
              </Card>
            ) : (
              scenes.map((scene) => (
                <SceneCard key={scene.id} scene={scene} />
              ))
            )}

            <div className="flex gap-2">
              <Button>
                <Wand2 className="mr-2 h-4 w-4" />
                Generate Storyboard
              </Button>
              <Button variant="secondary">
                <Play className="mr-2 h-4 w-4" />
                Render Video
              </Button>
            </div>
          </TabsContent>

          <TabsContent value="script" className="mt-4">
            <Card>
              <CardHeader>
                <CardTitle>Original Script</CardTitle>
                <CardDescription>
                  This is the script you provided. Scenes were auto-generated from paragraph breaks.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <pre className="whitespace-pre-wrap rounded-md bg-muted p-4 text-sm">
                  {project.script_text}
                </pre>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="render" className="mt-4">
            <Card className="border-dashed">
              <CardContent className="py-12 text-center">
                <Play className="mx-auto mb-4 h-12 w-12 text-muted-foreground" />
                <h3 className="text-lg font-medium">Ready to Render</h3>
                <p className="mt-2 text-sm text-muted-foreground">
                  When you're happy with the scenes, render your final video.
                </p>
                <Button className="mt-4">
                  <Play className="mr-2 h-4 w-4" />
                  Start Render
                </Button>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  );
}

function SceneCard({ scene }: { scene: Scene }) {
  const sceneStatusColors: Record<string, string> = {
    pending: "bg-gray-100 text-gray-800",
    generating: "bg-blue-100 text-blue-800 animate-pulse",
    done: "bg-green-100 text-green-800",
    error: "bg-red-100 text-red-800",
  };

  return (
    <Card>
      <CardHeader className="pb-2">
        <div className="flex items-center justify-between">
          <CardTitle className="text-base">Scene {scene.scene_number}</CardTitle>
          <Badge className={sceneStatusColors[scene.status] || ""}>{scene.status}</Badge>
        </div>
        <CardDescription className="line-clamp-3 text-sm">
          {scene.narration_text}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <p className="text-xs text-muted-foreground">
          Duration: {scene.duration_seconds}s · Visual prompt: {scene.visual_prompt || "None"}
        </p>
      </CardContent>
    </Card>
  );
}
