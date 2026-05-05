"use client";

import { useState } from "react";

interface TimelineScene {
  id: string;
  scene_number: number;
  thumbnail_url?: string;
  duration_seconds: number;
}

interface TimelinePreviewProps {
  scenes: TimelineScene[];
}

export default function TimelinePreview({ scenes }: TimelinePreviewProps) {
  const [currentScene, setCurrentScene] = useState(0);
  const totalDuration = scenes.reduce((sum, s) => sum + s.duration_seconds, 0);

  return (
    <div className="space-y-4">
      <div className="aspect-video bg-black rounded-lg flex items-center justify-center text-white">
        <span>Remotion Player Placeholder — Scene {currentScene + 1}</span>
      </div>
      <div className="flex items-center gap-2 overflow-x-auto py-2">
        {scenes.map((scene, idx) => (
          <button
            key={scene.id}
            onClick={() => setCurrentScene(idx)}
            className={`flex-shrink-0 w-24 rounded border p-1 text-left ${
              idx === currentScene ? "border-primary bg-primary/10" : "border-muted"
            }`}
          >
            <div className="aspect-video bg-muted rounded mb-1" />
            <div className="text-[10px] text-muted-foreground">
              {scene.duration_seconds}s
            </div>
          </button>
        ))}
      </div>
      <div className="text-sm text-muted-foreground">
        Total: {totalDuration.toFixed(1)}s
      </div>
    </div>
  );
}
