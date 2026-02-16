import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import { Platform, platforms, PlatformId } from "@/lib/platforms";
import { Check } from "lucide-react";

interface PlatformSelectorProps {
  selectedPlatform: PlatformId | null;
  onSelect: (platformId: PlatformId) => void;
}

export function PlatformSelector({ selectedPlatform, onSelect }: PlatformSelectorProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {platforms.map((platform) => (
        <Card 
          key={platform.id}
          className={cn(
            "cursor-pointer transition-all duration-200 hover:border-primary/50 hover:shadow-md relative overflow-hidden group",
            selectedPlatform === platform.id ? "border-primary ring-1 ring-primary bg-primary/5" : "border-border"
          )}
          onClick={() => onSelect(platform.id)}
        >
          {selectedPlatform === platform.id && (
            <div className="absolute top-3 right-3 bg-primary text-primary-foreground rounded-full p-1">
              <Check className="w-3 h-3" />
            </div>
          )}
          
          <CardHeader className="pb-2">
            <div className="flex justify-between items-start">
              <div className="flex items-center gap-3">
                <div className={cn(
                  "p-2 rounded-md transition-colors",
                  selectedPlatform === platform.id ? "bg-primary text-primary-foreground" : "bg-muted text-muted-foreground group-hover:text-primary"
                )}>
                  <platform.icon className="w-5 h-5" />
                </div>
                <div>
                  <CardTitle className="text-lg">{platform.name}</CardTitle>
                  <div className="flex gap-2 mt-1">
                    <Badge variant="secondary" className="text-xs font-normal">
                      {platform.difficulty}
                    </Badge>
                    <Badge variant="outline" className="text-xs font-normal">
                      {platform.cost}
                    </Badge>
                  </div>
                </div>
              </div>
            </div>
          </CardHeader>
          
          <CardContent>
            <CardDescription className="mb-4">
              {platform.description}
            </CardDescription>
            
            <div className="flex flex-wrap gap-2">
              {platform.features.slice(0, 3).map((feature) => (
                <span key={feature} className="text-xs text-muted-foreground bg-muted/50 px-2 py-1 rounded-sm">
                  {feature}
                </span>
              ))}
            </div>
          </CardContent>
          
          {platform.recommended && (
            <div className="absolute top-0 right-0 bg-primary text-primary-foreground text-[10px] px-2 py-0.5 rounded-bl-md font-medium">
              Recommended
            </div>
          )}
        </Card>
      ))}
    </div>
  );
}
