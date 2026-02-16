import { Github, Server, Cloud, Box } from "lucide-react";

export type PlatformId = "github" | "netlify" | "vercel" | "docker";

export interface Platform {
  id: PlatformId;
  name: string;
  description: string;
  icon: any;
  features: string[];
  recommended?: boolean;
  difficulty: "Easy" | "Medium" | "Advanced";
  cost: "Free" | "Paid";
}

export const platforms: Platform[] = [
  {
    id: "github",
    name: "GitHub Pages",
    description: "Free hosting directly from your repository. Best for documentation.",
    icon: Github,
    features: ["Automatic SSL", "Custom Domains", "Git Integration", "Free Hosting"],
    recommended: true,
    difficulty: "Easy",
    cost: "Free"
  },
  {
    id: "netlify",
    name: "Netlify",
    description: "Drag-and-drop deployment with powerful CI/CD features.",
    icon: Cloud,
    features: ["Drag & Drop", "Instant Rollbacks", "Form Handling", "Global CDN"],
    difficulty: "Easy",
    cost: "Free"
  },
  {
    id: "vercel",
    name: "Vercel",
    description: "Zero-configuration deployment with edge network performance.",
    icon: Box,
    features: ["Zero Config", "Edge Network", "Preview Deployments", "Fastest"],
    difficulty: "Easy",
    cost: "Free"
  },
  {
    id: "docker",
    name: "Docker / Self-Hosted",
    description: "Full control over your deployment environment.",
    icon: Server,
    features: ["Full Control", "Private Network", "Custom Environment", "Portable"],
    difficulty: "Advanced",
    cost: "Free"
  }
];
