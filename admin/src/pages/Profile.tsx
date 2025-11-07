import { useAuth } from "@/contexts/AuthContext";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Phone, Mail, User, Shield } from "lucide-react";

const Profile = () => {
  const { user } = useAuth();

  const getInitials = (name: string) => {
    return name
      .split(" ")
      .map((n) => n[0])
      .join("")
      .toUpperCase()
      .slice(0, 2);
  };

  if (!user) {
    return (
      <div className="text-center p-8">
        <p className="text-muted-foreground">Not logged in</p>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-4xl">
      <div>
        <h1 className="text-3xl font-bold text-foreground">Profile</h1>
        <p className="text-muted-foreground">View your account information</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Personal Information</CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Profile Avatar */}
          <div className="flex items-center gap-6">
            <Avatar className="h-24 w-24">
              <AvatarFallback className="text-2xl">
                {getInitials(user.name)}
              </AvatarFallback>
            </Avatar>
          </div>

          {/* User ID */}
          <div className="space-y-2">
            <Label className="flex items-center gap-2 text-muted-foreground">
              <Shield className="h-4 w-4" />
              User ID
            </Label>
            <Input value={user.id} disabled className="bg-muted" />
          </div>

          {/* Name */}
          <div className="space-y-2">
            <Label htmlFor="name" className="flex items-center gap-2">
              <User className="h-4 w-4" />
              Name
            </Label>
            <Input id="name" value={user.name} disabled className="bg-muted" />
          </div>

          {/* Email */}
          <div className="space-y-2">
            <Label htmlFor="email" className="flex items-center gap-2">
              <Mail className="h-4 w-4" />
              Email Address
            </Label>
            <Input id="email" value={user.email} disabled className="bg-muted" />
          </div>

          {/* Phone Number */}
          <div className="space-y-2">
            <Label htmlFor="phone" className="flex items-center gap-2">
              <Phone className="h-4 w-4" />
              Phone Number
            </Label>
            <Input id="phone" value={user.number} disabled className="bg-muted" />
          </div>

          {/* Role */}
          <div className="space-y-2">
            <Label className="flex items-center gap-2 text-muted-foreground">
              <Shield className="h-4 w-4" />
              Role
            </Label>
            <Input value={user.role} disabled className="bg-muted" />
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Profile;
