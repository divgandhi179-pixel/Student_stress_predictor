import Link from "next/link";
import Navbar from "@/components/Navbar";
import { ArrowRight, BrainCircuit, ActivitySquare, ShieldCheck } from "lucide-react";

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      
      <main className="flex-1">
        <section className="w-full py-24 lg:py-32 xl:py-48 bg-[color:var(--background)]">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex flex-col items-center space-y-8 text-center">
              <div className="space-y-4 max-w-3xl">
                <h1 className="text-4xl font-extrabold tracking-tight sm:text-5xl md:text-6xl lg:text-7xl">
                  Enterprise-Grade <br/>
                  <span className="text-[color:var(--primary)]">Cognitive Telemetry.</span>
                </h1>
                <p className="mx-auto max-w-[700px] text-[color:var(--muted-foreground)] md:text-xl leading-relaxed">
                  Advanced predictive analytics processing granular behavioral logs to forecast and mitigate psychological stress mechanisms before clinical manifestation.
                </p>
              </div>
              <div className="space-x-4">
                <Link
                  href="/login"
                  className="inline-flex h-11 items-center justify-center rounded-md bg-[color:var(--primary)] px-8 text-sm font-medium text-[color:var(--primary-foreground)] shadow transition-colors hover:opacity-90"
                >
                  Access Platform <ArrowRight className="ml-2 h-4 w-4" />
                </Link>
                <Link
                  href="/about"
                  className="inline-flex h-11 items-center justify-center rounded-md border text-sm font-medium transition-colors hover:bg-[color:var(--secondary)] px-8"
                >
                  View Documentation
                </Link>
              </div>
            </div>
          </div>
        </section>

        <section className="w-full py-20 bg-[color:var(--secondary)] border-y border-[color:var(--border)]">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
             <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
                <div className="flex flex-col items-center space-y-4 text-center">
                   <div className="p-4 bg-[color:var(--background)] rounded-2xl shadow-sm border border-[color:var(--border)]">
                      <BrainCircuit className="h-8 w-8 text-[color:var(--primary)]" />
                   </div>
                   <h3 className="text-xl font-bold">Predictive AI Inference</h3>
                   <p className="text-[color:var(--muted-foreground)] leading-relaxed">Utilizing extreme gradient boosting architectures targeting static demographic and longitudinal volatile variables.</p>
                </div>
                <div className="flex flex-col items-center space-y-4 text-center">
                   <div className="p-4 bg-[color:var(--background)] rounded-2xl shadow-sm border border-[color:var(--border)]">
                      <ActivitySquare className="h-8 w-8 text-[color:var(--primary)]" />
                   </div>
                   <h3 className="text-xl font-bold">Continuous Monitoring</h3>
                   <p className="text-[color:var(--muted-foreground)] leading-relaxed">Pivoting away from reactive isolated surveys in favor of systemic daily multi-dimensional behavioral logging arrays.</p>
                </div>
                <div className="flex flex-col items-center space-y-4 text-center">
                   <div className="p-4 bg-[color:var(--background)] rounded-2xl shadow-sm border border-[color:var(--border)]">
                      <ShieldCheck className="h-8 w-8 text-[color:var(--primary)]" />
                   </div>
                   <h3 className="text-xl font-bold">Absolute Data Privacy</h3>
                   <p className="text-[color:var(--muted-foreground)] leading-relaxed">Full anonymization and rigid JWT session authorization securing highly sensitive medical trajectory information.</p>
                </div>
             </div>
          </div>
        </section>
      </main>
      
      <footer className="w-full py-6 border-t bg-[color:var(--background)] mt-auto">
        <div className="max-w-7xl mx-auto px-4 flex justify-between items-center text-sm text-[color:var(--muted-foreground)]">
           <p>© 2026 NeuroMind Architecture. All rights reserved.</p>
           <div className="space-x-4">
              <Link href="/privacy" className="hover:underline">Privacy Architecture</Link>
              <Link href="/contact" className="hover:underline">Systems Support</Link>
           </div>
        </div>
      </footer>
    </div>
  );
}
