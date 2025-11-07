import { Card, CardContent } from "@/components/ui/card";
import { LucideIcon } from "lucide-react";

interface KPICardProps {
  title: string;
  value: string | number;
  icon: LucideIcon;
  variant?: "default" | "success" | "warning" | "primary";
}

export const KPICard = ({ title, value, icon: Icon, variant = "default" }: KPICardProps) => {
  const variantStyles = {
    default: "bg-card",
    success: "bg-success/10 border-success/20",
    warning: "bg-warning/10 border-warning/20",
    primary: "bg-primary/10 border-primary/20",
  };

  const iconStyles = {
    default: "text-muted-foreground",
    success: "text-success",
    warning: "text-warning",
    primary: "text-primary",
  };

  return (
    <Card className={variantStyles[variant]}>
      <CardContent className="flex items-center justify-between p-6">
        <div className="space-y-1">
          <p className="text-sm font-medium text-muted-foreground">{title}</p>
          <p className="text-3xl font-bold text-foreground">{value}</p>
        </div>
        <Icon className={`h-10 w-10 ${iconStyles[variant]}`} />
      </CardContent>
    </Card>
  );
};
