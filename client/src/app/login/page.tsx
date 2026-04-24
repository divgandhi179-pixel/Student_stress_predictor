"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { Activity, ArrowRight, Loader2 } from "lucide-react";

export default function Login() {
  const router = useRouter();
  const [isLogin, setIsLogin] = useState(true);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  
  const [formData, setFormData] = useState({ username: "", password: "" });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    
    try {
      const endpoint = isLogin ? "/api/auth/login" : "/api/auth/register";
      const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:5000";
      const res = await fetch(`${API_URL}${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      
      const data = await res.json();
      
      if (!res.ok) {
        throw new Error(data.message || "Failed to authenticate");
      }
      
      if (isLogin) {
        localStorage.setItem("token", data.token);
        router.push("/dashboard");
      } else {
        setIsLogin(true);
        setError("Registration successful! Please log in.");
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[color:var(--secondary)] py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8 bg-[color:var(--background)] p-10 rounded-2xl shadow-sm border border-[color:var(--border)]">
        
        <div className="flex flex-col items-center">
           <Link href="/" className="flex items-center gap-2 mb-8">
              <Activity className="h-8 w-8 text-[color:var(--primary)]" />
              <span className="font-extrabold text-2xl tracking-tight">NeuroMind.</span>
           </Link>
          <h2 className="text-center text-2xl font-bold tracking-tight">
            {isLogin ? "Authenticate to Portal" : "Establish New Credentials"}
          </h2>
          <p className="mt-2 text-center text-sm text-[color:var(--muted-foreground)]">
            Enterprise cognitive telemetry system.
          </p>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          {error && (
            <div className={`p-4 rounded-md text-sm font-medium ${error.includes("successful") ? 'bg-green-500/10 text-green-500' : 'bg-red-500/10 text-red-500'}`}>
              {error}
            </div>
          )}
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-[color:var(--foreground)] mb-1">
                Identification String 
              </label>
              <input
                type="text"
                required
                className="appearance-none relative block w-full px-3 py-2 border border-[color:var(--border)] bg-[color:var(--input)] placeholder-[color:var(--muted-foreground)] rounded-md focus:outline-none focus:ring-2 focus:ring-[color:var(--primary)] focus:border-transparent sm:text-sm transition-all"
                placeholder="root_user_01"
                value={formData.username}
                onChange={(e) => setFormData({...formData, username: e.target.value})}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-[color:var(--foreground)] mb-1">
                Authorization Key
              </label>
              <input
                type="password"
                required
                className="appearance-none relative block w-full px-3 py-2 border border-[color:var(--border)] bg-[color:var(--input)] placeholder-[color:var(--muted-foreground)] rounded-md focus:outline-none focus:ring-2 focus:ring-[color:var(--primary)] focus:border-transparent sm:text-sm transition-all"
                placeholder="••••••••"
                value={formData.password}
                onChange={(e) => setFormData({...formData, password: e.target.value})}
              />
            </div>
          </div>

          <div>
            <button
              type="submit"
              disabled={loading}
              className="group relative w-full flex justify-center py-2.5 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-[color:var(--primary)] hover:opacity-90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[color:var(--primary)] transition-all disabled:opacity-50"
            >
              {loading ? <Loader2 className="h-5 w-5 animate-spin" /> : (isLogin ? "Verify Access" : "Initialize Matrix")}
            </button>
          </div>
        </form>
        
        <div className="text-center mt-4">
           <button 
             onClick={() => { setIsLogin(!isLogin); setError(""); }}
             className="text-sm font-medium text-[color:var(--muted-foreground)] hover:text-[color:var(--foreground)] transition-colors"
           >
             {isLogin ? "Request new credentials architecture? Initialize here." : "Existing matrix vector? Authenticate here."}
           </button>
        </div>

      </div>
    </div>
  );
}
