"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function NewProjectPage() {
  const router = useRouter();
  const [title, setTitle] = useState("");
  const [script, setScript] = useState("");
  const [template, setTemplate] = useState("youtube_explainer");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    const res = await fetch("/api/v1/projects", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title, script_text: script, template }),
    });
    const data = await res.json();
    setLoading(false);
    if (res.ok) {
      router.push(`/projects/${data.id}`);
    }
  };

  return (
    <main className="container mx-auto py-8 px-4 max-w-3xl">
      <h1 className="text-2xl font-bold mb-6">New Project</h1>
      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="space-y-2">
          <label className="text-sm font-medium">Title</label>
          <input
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="My Explainer Video"
            required
          />
        </div>
        <div className="space-y-2">
          <label className="text-sm font-medium">Template</label>
          <select
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
            value={template}
            onChange={(e) => setTemplate(e.target.value)}
          >
            <option value="youtube_explainer">YouTube Explainer</option>
            <option value="product_demo">Product Demo</option>
            <option value="social_reel">Social Reel</option>
          </select>
        </div>
        <div className="space-y-2">
          <label className="text-sm font-medium">Script</label>
          <textarea
            className="flex min-h-[200px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
            value={script}
            onChange={(e) => setScript(e.target.value)}
            placeholder="Paste your script here. Separate scenes with blank lines."
            required
          />
          <p className="text-xs text-muted-foreground">
            Scenes are auto-detected from paragraph breaks.
          </p>
        </div>
        <button
          type="submit"
          disabled={loading}
          className="inline-flex h-10 items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:bg-primary/90 disabled:opacity-50"
        >
          {loading ? "Creating..." : "Create Project"}
        </button>
      </form>
    </main>
  );
}
