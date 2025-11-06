import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { Home, Package, List, User, LogOut } from "lucide-react";
import { NotificationPopover } from "./NotificationPopover";
import { useAuth } from "@/contexts/AuthContext";
import { Button } from "./ui/button";

export const DashboardLayout = () => {
  const { signOut } = useAuth();
  const navigate = useNavigate();

  const navItems = [
    { title: "Home", url: "/", icon: Home },
    { title: "My Products", url: "/products", icon: Package },
    { title: "My Orders", url: "/orders", icon: List },
    { title: "Profile", url: "/profile", icon: User },
  ];

  const handleSignOut = async () => {
    await signOut();
    navigate("/auth");
  };

  return (
    <div className="flex min-h-screen w-full bg-background">
      {/* Sidebar */}
      <aside className="w-64 border-r border-border bg-card p-6 flex flex-col justify-between min-h-screen">
        <div>
          <div className="mb-8">
            <h1 className="text-2xl font-bold text-foreground">ClickPick</h1>
          </div>
          
          <nav className="space-y-2">
            {navItems.map((item) => (
              <NavLink
                key={item.title}
                to={item.url}
                end
                className={({ isActive }) =>
                  `flex items-center gap-3 rounded-lg px-4 py-3 transition-colors ${
                    isActive
                      ? "bg-primary/10 text-primary font-medium"
                      : "text-muted-foreground hover:bg-muted hover:text-foreground"
                  }`
                }
              >
                <item.icon className="h-5 w-5" />
                <span>{item.title}</span>
              </NavLink>
            ))}
          </nav>
        </div>

        {/* Sign out at bottom */}
        <div className="mt-auto">
          <Button
            variant="ghost"
            onClick={handleSignOut}
            className="flex items-center gap-3 rounded-lg px-4 py-3 w-full text-muted-foreground hover:bg-muted hover:text-foreground transition-colors justify-start"
          >
            <LogOut className="h-5 w-5" />
            <span>Sign Out</span>
          </Button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1">
        <div className="p-8">
          {/* Notification bell in top right */}
          <div className="flex justify-end mb-4">
            <NotificationPopover />
          </div>
          <Outlet />
        </div>
      </main>
    </div>
  );
};
