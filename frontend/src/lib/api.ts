const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8067/api/v1";

class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = "ApiError";
  }
}

async function fetchJson<T>(url: string, options?: RequestInit): Promise<T> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 5000); // 5s timeout

  try {
    const res = await fetch(`${API_BASE}${url}`, {
      headers: { "Content-Type": "application/json", ...options?.headers },
      ...options,
      signal: controller.signal,
    });

    if (!res.ok) {
      const err = await res.text();
      throw new ApiError(res.status, err || res.statusText);
    }

    if (res.status === 204) return undefined as T;
    return res.json();
  } catch (e: any) {
    if (e.name === "AbortError") {
      throw new ApiError(0, "Backend request timed out. Is the backend running on port 8067?");
    }
    throw e;
  } finally {
    clearTimeout(timeout);
  }
}

export interface Project {
  id: string;
  title: string;
  script_text: string;
  status: "draft" | "storyboard" | "rendering" | "done";
  video_url: string | null;
  duration: number | null;
  template: string;
  voice_profile_id: string | null;
  character_id: string | null;
  created_at: string;
  updated_at: string;
}

export interface ProjectCreate {
  title: string;
  script_text: string;
  template?: string;
  voice_profile_id?: string | null;
  character_id?: string | null;
}

export interface ProjectUpdate {
  title?: string;
  script_text?: string;
  status?: string;
  template?: string;
}

export interface Scene {
  id: string;
  project_id: string;
  scene_number: number;
  narration_text: string;
  visual_prompt: string;
  duration_seconds: number;
  status: "pending" | "generating" | "done" | "error";
  video_clip_url: string | null;
  scene_metadata: Record<string, unknown>;
  created_at: string;
  updated_at: string;
}

export const api = {
  projects: {
    list: (): Promise<Project[]> => fetchJson("/projects"),
    get: (id: string): Promise<Project> => fetchJson(`/projects/${id}`),
    create: (data: ProjectCreate): Promise<Project> =>
      fetchJson("/projects", { method: "POST", body: JSON.stringify(data) }),
    update: (id: string, data: ProjectUpdate): Promise<Project> =>
      fetchJson(`/projects/${id}`, { method: "PUT", body: JSON.stringify(data) }),
    remove: (id: string): Promise<void> =>
      fetchJson(`/projects/${id}`, { method: "DELETE" }),
  },
  scenes: {
    listByProject: (projectId: string): Promise<Scene[]> =>
      fetchJson(`/projects/${projectId}/scenes`),
    get: (id: string): Promise<Scene> => fetchJson(`/scenes/${id}`),
    update: (id: string, data: Partial<Scene>): Promise<Scene> =>
      fetchJson(`/scenes/${id}`, { method: "PUT", body: JSON.stringify(data) }),
    remove: (id: string): Promise<void> =>
      fetchJson(`/scenes/${id}`, { method: "DELETE" }),
  },
  health: (): Promise<{ status: string }> =>
    fetch(`${API_BASE.replace("/api/v1", "")}/health`).then((r) => r.json()),
};
