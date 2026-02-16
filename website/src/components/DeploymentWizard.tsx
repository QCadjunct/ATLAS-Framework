import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { CheckCircle2, Copy, ExternalLink, Github, Globe, Server, Terminal } from "lucide-react";
import { toast } from "sonner";

interface Platform {
  id: string;
  name: string;
  icon: React.ReactNode;
  description: string;
  steps: Step[];
}

interface Step {
  title: string;
  description: string;
  code?: string;
  link?: string;
}

const platforms: Platform[] = [
  {
    id: "github-pages",
    name: "GitHub Pages",
    icon: <Github className="w-6 h-6" />,
    description: "Free hosting for static sites directly from your GitHub repository.",
    steps: [
      {
        title: "Enable GitHub Pages",
        description: "Go to your repository Settings > Pages. Select 'main' branch and '/docs' folder (or root if using a custom build action).",
        link: "https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site"
      },
      {
        title: "Configure Build Action",
        description: "Create a .github/workflows/deploy.yml file with the following content:",
        code: `name: Deploy to GitHub Pages
on:
  push:
    branches: ["main"]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npm run build
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: \${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./dist`
      },
      {
        title: "Verify Deployment",
        description: "Wait for the action to complete. Your site will be live at https://<username>.github.io/<repo-name>."
      }
    ]
  },
  {
    id: "netlify",
    name: "Netlify",
    icon: <Globe className="w-6 h-6" />,
    description: "Fast global CDN with continuous deployment from Git.",
    steps: [
      {
        title: "Connect Repository",
        description: "Log in to Netlify and click 'Add new site' > 'Import an existing project'. Select GitHub and choose your repository."
      },
      {
        title: "Configure Build Settings",
        description: "Set Build command to 'npm run build' and Publish directory to 'dist'.",
        code: "Build command: npm run build\nPublish directory: dist"
      },
      {
        title: "Deploy",
        description: "Click 'Deploy site'. Netlify will automatically build and deploy your site on every push to main."
      }
    ]
  },
  {
    id: "vercel",
    name: "Vercel",
    icon: <Server className="w-6 h-6" />,
    description: "Develop. Preview. Ship. Best for Next.js and static sites.",
    steps: [
      {
        title: "Import Project",
        description: "Go to Vercel Dashboard > Add New > Project. Import your Git repository."
      },
      {
        title: "Framework Preset",
        description: "Vercel should automatically detect Vite. If not, select 'Vite' from the Framework Preset dropdown."
      },
      {
        title: "Environment Variables",
        description: "Add any necessary environment variables (e.g., API keys) in the project settings."
      },
      {
        title: "Deploy",
        description: "Click Deploy. Your site will be live in seconds with a vercel.app domain."
      }
    ]
  },
  {
    id: "docker",
    name: "Docker",
    icon: <Terminal className="w-6 h-6" />,
    description: "Containerize your application for consistent deployment anywhere.",
    steps: [
      {
        title: "Create Dockerfile",
        description: "Ensure a Dockerfile exists in your project root:",
        code: `FROM node:20-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]`
      },
      {
        title: "Build Image",
        description: "Run the following command to build your Docker image:",
        code: "docker build -t atlas-deployment-guide ."
      },
      {
        title: "Run Container",
        description: "Start the container on port 8080:",
        code: "docker run -d -p 8080:80 atlas-deployment-guide"
      }
    ]
  }
];

export function DeploymentWizard() {
  const [selectedPlatform, setSelectedPlatform] = useState<string>("github-pages");
  const [completedSteps, setCompletedSteps] = useState<Record<string, boolean[]>>({});

  const handleCopy = (text: string) => {
    navigator.clipboard.writeText(text);
    toast.success("Code copied to clipboard");
  };

  const toggleStep = (platformId: string, stepIndex: number) => {
    setCompletedSteps(prev => {
      const platformSteps = prev[platformId] || [];
      const newSteps = [...platformSteps];
      newSteps[stepIndex] = !newSteps[stepIndex];
      return { ...prev, [platformId]: newSteps };
    });
  };

  const currentPlatform = platforms.find(p => p.id === selectedPlatform);

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      <div className="md:col-span-1 space-y-4">
        <h3 className="text-lg font-semibold mb-4">Select Platform</h3>
        {platforms.map(platform => (
          <Card 
            key={platform.id}
            className={`cursor-pointer transition-all hover:border-primary ${selectedPlatform === platform.id ? 'border-primary bg-primary/5' : ''}`}
            onClick={() => setSelectedPlatform(platform.id)}
          >
            <CardHeader className="flex flex-row items-center gap-4 p-4">
              <div className={`p-2 rounded-full ${selectedPlatform === platform.id ? 'bg-primary text-primary-foreground' : 'bg-muted'}`}>
                {platform.icon}
              </div>
              <div>
                <CardTitle className="text-base">{platform.name}</CardTitle>
                <CardDescription className="text-xs line-clamp-1">{platform.description}</CardDescription>
              </div>
            </CardHeader>
          </Card>
        ))}
      </div>

      <div className="md:col-span-2">
        {currentPlatform && (
          <Card className="h-full flex flex-col">
            <CardHeader>
              <div className="flex items-center gap-3 mb-2">
                {currentPlatform.icon}
                <CardTitle>{currentPlatform.name} Deployment Guide</CardTitle>
              </div>
              <CardDescription>{currentPlatform.description}</CardDescription>
            </CardHeader>
            <CardContent className="flex-1 space-y-6">
              {currentPlatform.steps.map((step, index) => (
                <div key={index} className="relative pl-8 pb-6 border-l last:border-0 border-muted-foreground/20">
                  <div 
                    className={`absolute left-[-12px] top-0 w-6 h-6 rounded-full border-2 flex items-center justify-center bg-background cursor-pointer transition-colors ${
                      completedSteps[currentPlatform.id]?.[index] 
                        ? 'border-primary bg-primary text-primary-foreground' 
                        : 'border-muted-foreground/30 text-muted-foreground'
                    }`}
                    onClick={() => toggleStep(currentPlatform.id, index)}
                  >
                    {completedSteps[currentPlatform.id]?.[index] ? <CheckCircle2 className="w-4 h-4" /> : <span className="text-xs font-bold">{index + 1}</span>}
                  </div>
                  
                  <div className="space-y-2">
                    <h4 className="font-medium text-lg flex items-center gap-2">
                      {step.title}
                      {step.link && (
                        <a href={step.link} target="_blank" rel="noopener noreferrer" className="text-muted-foreground hover:text-primary">
                          <ExternalLink className="w-4 h-4" />
                        </a>
                      )}
                    </h4>
                    <p className="text-muted-foreground text-sm">{step.description}</p>
                    
                    {step.code && (
                      <div className="relative mt-3 group">
                        <pre className="bg-muted/50 p-4 rounded-md overflow-x-auto text-sm font-mono border border-border">
                          {step.code}
                        </pre>
                        <Button
                          size="icon"
                          variant="ghost"
                          className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity h-8 w-8"
                          onClick={() => handleCopy(step.code!)}
                        >
                          <Copy className="w-4 h-4" />
                        </Button>
                      </div>
                    )}
                  </div>
                </div>
              ))}
            </CardContent>
            <CardFooter className="bg-muted/10 border-t p-4 flex justify-between items-center">
              <div className="text-sm text-muted-foreground">
                Step {completedSteps[currentPlatform.id]?.filter(Boolean).length || 0} of {currentPlatform.steps.length} completed
              </div>
              <Button 
                variant={completedSteps[currentPlatform.id]?.filter(Boolean).length === currentPlatform.steps.length ? "default" : "secondary"}
                disabled={completedSteps[currentPlatform.id]?.filter(Boolean).length !== currentPlatform.steps.length}
              >
                {completedSteps[currentPlatform.id]?.filter(Boolean).length === currentPlatform.steps.length ? "Deployment Ready!" : "Complete All Steps"}
              </Button>
            </CardFooter>
          </Card>
        )}
      </div>
    </div>
  );
}
