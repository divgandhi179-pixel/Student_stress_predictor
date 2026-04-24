"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Activity, LogOut, LayoutDashboard, UserCircle, KeyRound } from "lucide-react";

export default function Navbar() {
  const pathname = usePathname();
  const isDashboard = pathname.startsWith("/dashboard");

  return (
    <nav className="border-b bg-[color:var(--background)] sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            <Link href="/" className="flex flex-shrink-0 items-center gap-2">
              <Activity className="h-6 w-6 text-[color:var(--primary)]" />
              <span className="font-bold text-lg tracking-tight">NeuroMind.</span>
            </Link>
            {isDashboard && (
              <div className="hidden sm:ml-8 sm:flex sm:space-x-8">
                <Link
                  href="/dashboard"
                  className={`${
                    pathname === "/dashboard"
                      ? "border-[color:var(--primary)] text-[color:var(--foreground)]"
                      : "border-transparent text-[color:var(--muted-foreground)] hover:border-[color:var(--border)] hover:text-[color:var(--foreground)]"
                  } inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors`}
                >
                  <LayoutDashboard className="h-4 w-4 mr-2" />
                  Telemetry
                </Link>
                <Link
                  href="/dashboard/profile"
                  className={`${
                    pathname === "/dashboard/profile"
                      ? "border-[color:var(--primary)] text-[color:var(--foreground)]"
                      : "border-transparent text-[color:var(--muted-foreground)] hover:border-[color:var(--border)] hover:text-[color:var(--foreground)]"
                  } inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium transition-colors`}
                >
                   <UserCircle className="h-4 w-4 mr-2" />
                  Profile Configuration
                </Link>
              </div>
            )}
          </div>
          <div className="flex items-center space-x-4">
             {isDashboard ? (
                <button
                  onClick={() => {
                     localStorage.removeItem("token");
                     window.location.href = "/login";
                  }}
                  className="inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors hover:bg-[color:var(--secondary)] h-9 px-4 py-2"
                >
                  <LogOut className="h-4 w-4 mr-2" />
                  Disconnect
                </button>
             ) : (
                <Link
                  href="/login"
                  className="inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors bg-[color:var(--primary)] text-[color:var(--primary-foreground)] hover:opacity-90 h-9 px-4 py-2 shadow-sm"
                >
                  <KeyRound className="h-4 w-4 mr-2" />
                  Portal Access
                </Link>
             )}
          </div>
        </div>
      </div>
    </nav>
  );
}
