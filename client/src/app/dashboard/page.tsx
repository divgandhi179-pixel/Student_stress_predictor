"use client";

import { useState } from "react";
import { ActivitySquare, Loader2, TrendingUp, AlertTriangle, CheckCircle2 } from "lucide-react";

export default function DashboardTelemetry() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  
  const [metrics, setMetrics] = useState({
    sleep_hours: 7,
    study_hours: 4,
    mood: 3,
    physical_activity: 1,
    social_interaction: 2
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const token = localStorage.getItem("token");
      const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:5000";
      const res = await fetch(`${API_URL}/api/predict`, {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(metrics),
      });
      
      const data = await res.json();
      if (!res.ok) throw new Error(data.message);
      
      setResult(data);
    } catch (err: any) {
      alert("Telemetry transmission failure: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
      
      <div className="bg-[color:var(--card)] p-8 rounded-2xl shadow-sm border border-[color:var(--border)]">
        <div className="mb-6 flex items-center gap-3">
           <ActivitySquare className="h-6 w-6 text-[color:var(--primary)]" />
           <h2 className="text-xl font-bold tracking-tight">Telemetry Input Matrix</h2>
        </div>
        
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium mb-2">REM Sleep Cycle (Hours)</label>
              <input type="number" step="0.5" required className="w-full px-3 py-2 border rounded-md bg-[color:var(--input)]" value={metrics.sleep_hours} onChange={e => setMetrics({...metrics, sleep_hours: parseFloat(e.target.value)})} />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Cognitive Load (Study Hrs)</label>
              <input type="number" step="0.5" required className="w-full px-3 py-2 border rounded-md bg-[color:var(--input)]" value={metrics.study_hours} onChange={e => setMetrics({...metrics, study_hours: parseFloat(e.target.value)})} />
            </div>
          </div>
          
          <div>
            <label className="block text-sm font-medium mb-2">Self-Reported Baseline Mood (1-5) : <span className="text-[color:var(--primary)] font-bold">{metrics.mood}</span></label>
            <input type="range" min="1" max="5" required className="w-full cursor-pointer accent-[color:var(--primary)]" value={metrics.mood} onChange={e => setMetrics({...metrics, mood: parseInt(e.target.value)})} />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium mb-2">Physical Kinematics (Hrs)</label>
              <input type="number" step="0.5" required className="w-full px-3 py-2 border rounded-md bg-[color:var(--input)]" value={metrics.physical_activity} onChange={e => setMetrics({...metrics, physical_activity: parseFloat(e.target.value)})} />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">Social Interaction / Screen (Hrs)</label>
              <input type="number" step="0.5" required className="w-full px-3 py-2 border rounded-md bg-[color:var(--input)]" value={metrics.social_interaction} onChange={e => setMetrics({...metrics, social_interaction: parseFloat(e.target.value)})} />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full flex justify-center items-center py-3 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-[color:var(--primary)] hover:opacity-90 transition-all disabled:opacity-50"
          >
            {loading ? <Loader2 className="h-5 w-5 animate-spin" /> : "Execute Predictive Algorithm"}
          </button>
        </form>
      </div>

      <div className="bg-[color:var(--card)] p-8 rounded-2xl shadow-sm border border-[color:var(--border)] flex flex-col justify-center items-center text-center">
        {result ? (
           <div className="w-full animate-in fade-in slide-in-from-bottom-4 duration-500">
              <h3 className="text-lg font-medium text-[color:var(--muted-foreground)] uppercase tracking-widest mb-2">Calculated Stress Quotient</h3>
              
              <div className="flex items-end justify-center gap-1 mb-8">
                <span className={`text-6xl font-extrabold ${result.score > 70 ? 'text-red-500' : (result.score > 40 ? 'text-amber-500' : 'text-emerald-500')}`}>
                   {result.score}
                </span>
                <span className="text-xl text-[color:var(--muted-foreground)] mb-1">/100</span>
              </div>
              
              <div className="w-full bg-[color:var(--secondary)] rounded-full h-3 mb-8 overflow-hidden">
                <div 
                   className={`h-3 transition-all duration-1000 ease-out rounded-full ${result.score > 70 ? 'bg-red-500' : (result.score > 40 ? 'bg-amber-500' : 'bg-emerald-500')}`}
                   style={{ width: `${result.score}%` }}
                ></div>
              </div>
              
              <div className="bg-[color:var(--secondary)] p-6 rounded-xl border border-[color:var(--border)] text-left">
                 <h4 className="font-semibold text-[color:var(--foreground)] flex items-center mb-3">
                   {result.score > 70 ? <AlertTriangle className="h-4 w-4 mr-2 text-red-500"/> : <CheckCircle2 className="h-4 w-4 mr-2 text-emerald-500"/>}
                   Diagnostic Analysis
                 </h4>
                 <ul className="space-y-2">
                    {result.feedback.map((f: string, i: number) => (
                       <li key={i} className="text-sm text-[color:var(--muted-foreground)] flex items-start">
                          <span className="text-[color:var(--primary)] mr-2 mt-0.5">•</span>
                          {f}
                       </li>
                    ))}
                 </ul>
              </div>
           </div>
        ) : (
           <div className="text-[color:var(--muted-foreground)] flex flex-col items-center opacity-50">
              <TrendingUp className="h-16 w-16 mb-4" />
              <p>Awaiting telemetry inputs to compute structural stress vector.</p>
           </div>
        )}
      </div>

    </div>
  );
}
