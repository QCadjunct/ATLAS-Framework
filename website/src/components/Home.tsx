import { Button } from "@/components/ui/button";
import { DeploymentWizard } from "@/components/DeploymentWizard";
import { SearchableDocs } from "@/components/SearchableDocs";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Rocket, BookOpen, Terminal } from "lucide-react";

export default function Home() {
  return (
    <div className="min-h-screen bg-background text-foreground flex flex-col">
      <header className="border-b bg-card/50 backdrop-blur-sm sticky top-0 z-10">
        <div className="container mx-auto py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Rocket className="w-6 h-6 text-primary" />
            <h1 className="text-xl font-bold tracking-tight">ATLAS Deployment Guide</h1>
          </div>
          <nav className="flex gap-4">
            <Button variant="ghost" size="sm">Documentation</Button>
            <Button variant="ghost" size="sm">GitHub</Button>
          </nav>
        </div>
      </header>

      <main className="flex-1 container mx-auto py-8 px-4">
        <div className="max-w-4xl mx-auto space-y-8">
          <div className="text-center space-y-4 mb-12">
            <h2 className="text-4xl font-extrabold tracking-tight lg:text-5xl">
              Deploy Your Knowledge Graph <span className="text-primary">In Minutes</span>
            </h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Interactive guide to deploying the ATLAS Framework. Choose your platform, follow the steps, and go live.
            </p>
            <div className="flex justify-center gap-4 pt-4">
              <Button size="lg" className="gap-2">
                <Rocket className="w-4 h-4" /> Start Deployment
              </Button>
              <Button size="lg" variant="outline" className="gap-2">
                <BookOpen className="w-4 h-4" /> Read Docs
              </Button>
            </div>
          </div>

          <Tabs defaultValue="wizard" className="w-full">
            <TabsList className="grid w-full grid-cols-2 mb-8">
              <TabsTrigger value="wizard" className="gap-2">
                <Terminal className="w-4 h-4" /> Interactive Wizard
              </TabsTrigger>
              <TabsTrigger value="docs" className="gap-2">
                <BookOpen className="w-4 h-4" /> Searchable Docs
              </TabsTrigger>
            </TabsList>
            
            <TabsContent value="wizard" className="space-y-4">
              <DeploymentWizard />
            </TabsContent>
            
            <TabsContent value="docs" className="space-y-4">
              <SearchableDocs />
            </TabsContent>
          </Tabs>
        </div>
      </main>

      <footer className="border-t py-8 mt-12 bg-muted/20">
        <div className="container mx-auto text-center text-muted-foreground text-sm">
          <p>© 2026 ATLAS Framework. Open Source & Community Driven.</p>
        </div>
      </footer>
    </div>
  );
}
