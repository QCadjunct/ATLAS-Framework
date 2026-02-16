import { useState } from "react";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Search } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface DocSection {
  id: string;
  title: string;
  content: string;
  tags: string[];
}

const docSections: DocSection[] = [
  {
    id: "prerequisites",
    title: "Prerequisites",
    content: "Before deploying, ensure you have Git installed, a GitHub account, and Node.js/Python environment set up.",
    tags: ["setup", "requirements", "git"]
  },
  {
    id: "github-pages",
    title: "GitHub Pages Deployment",
    content: "GitHub Pages is the recommended free hosting option. It supports custom domains and automatic SSL.",
    tags: ["github", "free", "hosting"]
  },
  {
    id: "custom-domain",
    title: "Custom Domain Setup",
    content: "Configure DNS records (A records and CNAME) to point your custom domain to your deployment.",
    tags: ["dns", "domain", "ssl"]
  },
  {
    id: "ssl-https",
    title: "SSL/HTTPS Configuration",
    content: "Most platforms provide automatic SSL certificates. Ensure 'Enforce HTTPS' is enabled in settings.",
    tags: ["security", "https", "ssl"]
  }
];

export function SearchableDocs() {
  const [searchQuery, setSearchQuery] = useState("");

  const filteredDocs = docSections.filter(doc => 
    doc.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    doc.content.toLowerCase().includes(searchQuery.toLowerCase()) ||
    doc.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  return (
    <div className="space-y-6">
      <div className="relative">
        <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
        <Input
          placeholder="Search documentation..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="pl-10"
        />
      </div>

      <ScrollArea className="h-[400px] rounded-md border p-4">
        <div className="space-y-4">
          {filteredDocs.map((doc) => (
            <Card key={doc.id}>
              <CardHeader>
                <CardTitle className="text-lg">{doc.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-muted-foreground">{doc.content}</p>
                <div className="flex gap-2 mt-2">
                  {doc.tags.map(tag => (
                    <span key={tag} className="text-xs bg-muted px-2 py-1 rounded-full text-muted-foreground">
                      #{tag}
                    </span>
                  ))}
                </div>
              </CardContent>
            </Card>
          ))}
          {filteredDocs.length === 0 && (
            <div className="text-center text-muted-foreground py-8">
              No results found for "{searchQuery}"
            </div>
          )}
        </div>
      </ScrollArea>
    </div>
  );
}
