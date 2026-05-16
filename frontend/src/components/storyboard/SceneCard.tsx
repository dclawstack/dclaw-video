"use client";

interface SceneCardProps {
  sceneNumber: number;
  narration: string;
  visualPrompt: string;
  status: string;
  onEdit?: () => void;
  onRegenerate?: () => void;
}

export default function SceneCard({
  sceneNumber,
  narration,
  visualPrompt,
  status,
  onEdit,
  onRegenerate,
}: SceneCardProps) {
  return (
    <div className="rounded-lg border bg-card p-4 space-y-3">
      <div className="flex items-center justify-between">
        <span className="text-sm font-semibold">Scene {sceneNumber}</span>
        <span className="text-xs px-2 py-1 rounded-full bg-muted uppercase">{status}</span>
      </div>
      <div className="grid grid-cols-4 gap-2">
        {[1, 2, 3, 4].map((f) => (
          <div key={f} className="aspect-video bg-muted rounded" />
        ))}
      </div>
      <p className="text-sm text-muted-foreground line-clamp-3">{narration}</p>
      <p className="text-xs text-muted-foreground line-clamp-2">Prompt: {visualPrompt || "—"}</p>
      <div className="flex gap-2">
        <button
          onClick={onEdit}
          className="inline-flex h-8 items-center justify-center rounded-md border border-input px-3 text-xs font-medium hover:bg-accent"
        >
          Edit
        </button>
        <button
          onClick={onRegenerate}
          className="inline-flex h-8 items-center justify-center rounded-md border border-input px-3 text-xs font-medium hover:bg-accent"
        >
          Regenerate
        </button>
      </div>
    </div>
  );
}
