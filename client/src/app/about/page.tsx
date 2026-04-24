import Link from "next/link";
import Navbar from "@/components/Navbar";
import { ArrowRight, Shield, Cpu, Activity } from "lucide-react";

export default function About() {
  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      
      <main className="flex-1 bg-[color:var(--background)]">
        {/* Hero Section */}
        <section className="w-full py-20 lg:py-32">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <h1 className="text-4xl font-extrabold tracking-tight sm:text-5xl md:text-6xl mb-6">
              Pioneering <span className="text-[color:var(--primary)]">Cognitive Science.</span>
            </h1>
            <p className="mx-auto max-w-3xl text-[color:var(--muted-foreground)] md:text-xl leading-relaxed mb-10">
              At NeuroMind, we bridge the gap between longitudinal behavioral data and advanced machine learning to predict, mitigate, and manage stress before it escalates into burnout.
            </p>
          </div>
        </section>

        {/* Mission Segment */}
        <section className="w-full py-16 bg-[color:var(--secondary)] border-y border-[color:var(--border)]">
          <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
             <div className="flex flex-col md:flex-row gap-12 items-center">
                <div className="md:w-1/2 space-y-6">
                   <h2 className="text-3xl font-bold">Our Mission</h2>
                   <p className="text-[color:var(--muted-foreground)] leading-relaxed">
                     Traditional psychological assessments rely on outdated, isolated survey methods. Our mission is to integrate continuous, non-invasive behavioral telemetry—sleep algorithms, physical activity coefficients, and academic pressure mappings—into a cohesive neural network model capable of generating real-time risk profiles.
                   </p>
                </div>
                <div className="md:w-1/2 grid grid-cols-1 gap-6">
                   <div className="p-6 bg-[color:var(--background)] rounded-2xl shadow-sm border border-[color:var(--border)] flex items-start space-x-4">
                      <Cpu className="h-6 w-6 text-[color:var(--primary)] flex-shrink-0 mt-1" />
                      <div>
                         <h4 className="font-bold">Algorithmic Precision</h4>
                         <p className="text-sm text-[color:var(--muted-foreground)] mt-1">Utilizing advanced gradient boosting and structured pipeline inferences.</p>
                      </div>
                   </div>
                   <div className="p-6 bg-[color:var(--background)] rounded-2xl shadow-sm border border-[color:var(--border)] flex items-start space-x-4">
                      <Shield className="h-6 w-6 text-[color:var(--primary)] flex-shrink-0 mt-1" />
                      <div>
                         <h4 className="font-bold">Ethical Data Practices</h4>
                         <p className="text-sm text-[color:var(--muted-foreground)] mt-1">Ensuring clinical-grade anonymization for all dynamic lifestyle metadata.</p>
                      </div>
                   </div>
                </div>
             </div>
          </div>
        </section>

        {/* CTA */}
        <section className="w-full py-24 text-center">
          <div className="max-w-3xl mx-auto px-4">
             <h2 className="text-3xl font-bold mb-6">Ready to integrate NeuroMind?</h2>
             <p className="text-[color:var(--muted-foreground)] mb-8">Deploy our state-of-the-art telemetry models directly to your student body or workforce ecosystem.</p>
             <div className="space-x-4">
               <Link
                 href="/contact"
                 className="inline-flex h-11 items-center justify-center rounded-md bg-[color:var(--primary)] px-8 text-sm font-medium text-[color:var(--primary-foreground)] hover:opacity-90 transition-colors"
               >
                 Contact Integration Team <ArrowRight className="ml-2 h-4 w-4" />
               </Link>
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
