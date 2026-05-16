import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Film, Zap, Palette, Mic } from "lucide-react";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col">
      <header className="border-b bg-card">
        <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4">
          <Link href="/" className="flex items-center gap-2 text-lg font-semibold">
            <Film className="h-5 w-5 text-primary" />
            DClaw Video
          </Link>
          <Link href="/projects">
            <Button variant="outline" size="sm">Dashboard</Button>
          </Link>
        </div>
      </header>

      <section className="mx-auto flex max-w-6xl flex-1 flex-col items-center justify-center px-4 text-center">
        <div className="mb-8 inline-flex items-center rounded-full bg-primary/10 px-3 py-1 text-sm font-medium text-primary">
          <Zap className="mr-2 h-4 w-4" />
          AI Video Director for Content Teams
        </div>

        <h1 className="mb-4 text-4xl font-extrabold tracking-tight sm:text-6xl">
          Script to video in
          <span className="text-primary"> 3 minutes</span>
        </h1>

        <p className="mb-8 max-w-2xl text-lg text-muted-foreground">
          Write a script. AI breaks it into scenes, generates storyboards, adds voiceover, 
          and renders your final video — no editing skills required.
        </p>

        <div className="mb-12 flex gap-4">
          <Link href="/projects/new">
            <Button size="lg">
              <Zap className="mr-2 h-4 w-4" />
              Create Your First Video
            </Button>
          </Link>
          <Link href="/projects">
            <Button variant="outline" size="lg">View Projects</Button>
          </Link>
        </div>

        <div className="grid w-full max-w-4xl gap-4 sm:grid-cols-3">
          <Card className="text-left">
            <CardHeader className="pb-2">
              <Palette className="mb-2 h-8 w-8 text-primary" />
              <CardTitle className="text-base">AI Storyboard</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                ComfyUI generates visual storyboards for each scene automatically.
              </p>
            </CardContent>
          </Card>

          <Card className="text-left">
            <CardHeader className="pb-2">
              <Mic className="mb-2 h-8 w-8 text-primary" />
              <CardTitle className="text-base">Auto Voiceover</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Kokoro TTS creates natural narration for every scene in your video.
              </p>
            </CardContent>
          </Card>

          <Card className="text-left">
            <CardHeader className="pb-2">
              <Film className="mb-2 h-8 w-8 text-primary" />
              <CardTitle className="text-base">One-Click Render</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Assemble scenes, audio, and captions into a final publishable video.
              </p>
            </CardContent>
          </Card>
        </div>
      </section>
    </main>
  );
}
