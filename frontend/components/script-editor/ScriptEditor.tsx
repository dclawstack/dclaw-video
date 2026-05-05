"use client";

import { useState } from "react";

interface ScriptEditorProps {
  initialValue?: string;
  onChange?: (value: string) => void;
}

export default function ScriptEditor({ initialValue = "", onChange }: ScriptEditorProps) {
  const [value, setValue] = useState(initialValue);

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setValue(e.target.value);
    onChange?.(e.target.value);
  };

  const sceneCount = value.split("\n\n").filter((p) => p.trim()).length;

  return (
    <div className="space-y-2">
      <textarea
        className="flex min-h-[300px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm leading-relaxed"
        value={value}
        onChange={handleChange}
        placeholder="Write your script. Separate scenes with blank lines."
      />
      <div className="flex justify-between text-xs text-muted-foreground">
        <span>{value.length} characters</span>
        <span>{sceneCount} scene{sceneCount === 1 ? "" : "s"} detected</span>
      </div>
    </div>
  );
}
