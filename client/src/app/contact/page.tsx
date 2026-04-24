import Link from "next/link";
import Navbar from "@/components/Navbar";
import { Mail, MessageSquare, MapPin, Send } from "lucide-react";

export default function Contact() {
  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      
      <main className="flex-1 bg-[color:var(--background)]">
        <section className="w-full py-20 lg:py-32">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            
            <div className="text-center max-w-3xl mx-auto mb-16">
               <h1 className="text-4xl font-extrabold tracking-tight sm:text-5xl mb-6">
                 Establish <span className="text-[color:var(--primary)]">Connection.</span>
               </h1>
               <p className="text-[color:var(--muted-foreground)] md:text-xl leading-relaxed">
                 Whether you are looking to integrate our telemetry endpoint API or require dedicated support for an existing institutional deployment, our engineering team is ready to assist.
               </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-12 items-start max-w-5xl mx-auto">
               
               {/* Contact Information */}
               <div className="space-y-8">
                  <div className="bg-[color:var(--secondary)] p-8 rounded-2xl border border-[color:var(--border)]">
                     <h3 className="text-2xl font-bold mb-6">Corporate Infrastructure</h3>
                     
                     <div className="space-y-6 text-[color:var(--muted-foreground)]">
                        <div className="flex items-start space-x-4">
                           <MapPin className="w-6 h-6 text-[color:var(--primary)] flex-shrink-0" />
                           <div>
                              <p className="font-medium text-[color:var(--foreground)]">NeuroMind Headquarters</p>
                              <p>Silicon Valley, Enterprise Block 4<br/>San Francisco, CA 94107</p>
                           </div>
                        </div>
                        
                        <div className="flex items-start space-x-4">
                           <Mail className="w-6 h-6 text-[color:var(--primary)] flex-shrink-0" />
                           <div>
                              <p className="font-medium text-[color:var(--foreground)]">Systems Support</p>
                              <p>telemetry-support@neuromind.com</p>
                           </div>
                        </div>

                        <div className="flex items-start space-x-4">
                           <MessageSquare className="w-6 h-6 text-[color:var(--primary)] flex-shrink-0" />
                           <div>
                              <p className="font-medium text-[color:var(--foreground)]">Enterprise Integration</p>
                              <p>deployments@neuromind.com</p>
                           </div>
                        </div>
                     </div>
                  </div>
               </div>

               {/* Contact Form */}
               <div className="bg-[color:var(--background)] p-8 rounded-2xl border border-[color:var(--border)] shadow-sm">
                  <h3 className="text-2xl font-bold mb-6">Send Transmission</h3>
                  <form className="space-y-4" onSubmit={(e) => e.preventDefault()}>
                     <div className="space-y-2">
                        <label className="text-sm font-medium">Clearance Name</label>
                        <input 
                           type="text" 
                           placeholder="John Doe" 
                           className="w-full h-11 px-4 rounded-md border border-[color:var(--border)] bg-[color:var(--background)] text-sm focus:outline-none focus:ring-2 focus:ring-[color:var(--primary)]/50 focus:border-[color:var(--primary)] transition-colors"
                        />
                     </div>
                     <div className="space-y-2">
                        <label className="text-sm font-medium">Institutional Email</label>
                        <input 
                           type="email" 
                           placeholder="john@university.edu" 
                           className="w-full h-11 px-4 rounded-md border border-[color:var(--border)] bg-[color:var(--background)] text-sm focus:outline-none focus:ring-2 focus:ring-[color:var(--primary)]/50 focus:border-[color:var(--primary)] transition-colors"
                        />
                     </div>
                     <div className="space-y-2">
                        <label className="text-sm font-medium">Transmission Body</label>
                        <textarea 
                           placeholder="Describe your integration requirements..." 
                           rows={4}
                           className="w-full p-4 rounded-md border border-[color:var(--border)] bg-[color:var(--background)] text-sm focus:outline-none focus:ring-2 focus:ring-[color:var(--primary)]/50 focus:border-[color:var(--primary)] transition-colors resize-none"
                        ></textarea>
                     </div>
                     <button className="w-full h-11 rounded-md bg-[color:var(--primary)] text-[color:var(--primary-foreground)] font-medium text-sm hover:opacity-90 transition-colors flex justify-center items-center">
                        <Send className="w-4 h-4 mr-2" />
                        Transmit Message
                     </button>
                  </form>
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
