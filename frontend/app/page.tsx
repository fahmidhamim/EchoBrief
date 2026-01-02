'use client';

import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Navbar } from '@/components/navbar';
import { Zap, Mic, Brain, BarChart3 } from 'lucide-react';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      <Navbar />
      
      {/* Hero Section */}
      <section className="pt-20 pb-32 px-4 sm:px-6 lg:px-8">
        <div className="max-w-6xl mx-auto text-center">
          <h1 className="text-5xl sm:text-6xl font-bold text-white mb-6 leading-tight">
            AI-Powered Meeting Intelligence
          </h1>
          <p className="text-xl text-slate-300 mb-8 max-w-2xl mx-auto">
            Real-time transcription, intelligent summaries, and actionable insights from every meeting.
          </p>
          <div className="flex gap-4 justify-center flex-wrap">
            <Link href="/auth?mode=signup">
              <Button size="lg" className="bg-blue-600 hover:bg-blue-700">
                Get Started Free
              </Button>
            </Link>
            <Link href="/auth?mode=login">
              <Button size="lg" variant="outline" className="border-slate-400 text-white hover:bg-slate-800">
                Sign In
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-slate-800/50">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl font-bold text-white text-center mb-16">Powerful Features</h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {[
              {
                icon: Mic,
                title: 'Real-time Transcription',
                description: 'Live speech-to-text powered by advanced AI'
              },
              {
                icon: Brain,
                title: 'AI Summaries',
                description: 'Automatic meeting summaries and action items'
              },
              {
                icon: Zap,
                title: 'Instant Insights',
                description: 'Key takeaways and keywords extracted automatically'
              },
              {
                icon: BarChart3,
                title: 'Analytics',
                description: 'Track meetings, participants, and productivity'
              }
            ].map((feature, i) => {
              const Icon = feature.icon;
              return (
                <div key={i} className="bg-slate-700/50 p-6 rounded-lg border border-slate-600 hover:border-blue-500 transition">
                  <Icon className="w-12 h-12 text-blue-400 mb-4" />
                  <h3 className="text-lg font-semibold text-white mb-2">{feature.title}</h3>
                  <p className="text-slate-300">{feature.description}</p>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl font-bold text-white mb-6">Ready to Transform Your Meetings?</h2>
          <p className="text-xl text-slate-300 mb-8">Join thousands of teams using EchoBrief AI to capture and act on meeting insights.</p>
          <Link href="/auth/signup">
            <Button size="lg" className="bg-blue-600 hover:bg-blue-700">
              Start Free Trial
            </Button>
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-700 py-8 px-4 sm:px-6 lg:px-8 bg-slate-900/50">
        <div className="max-w-6xl mx-auto text-center text-slate-400">
          <p>&copy; 2024 EchoBrief AI. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
