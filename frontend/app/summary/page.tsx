'use client';

import { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Navbar } from '@/components/navbar';
import { Download, Loader, CheckCircle } from 'lucide-react';
import axios from 'axios';

interface Summary {
  id: string;
  summary_text: string;
  action_items: string[];
  keywords: string[];
  generated_at: string;
  meeting_id?: string;
}

interface Transcript {
  id: string;
  speaker_name: string;
  transcript_text: string;
  created_at: string;
}

export default function SummaryPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const meetingId = searchParams.get('id');
  const [summary, setSummary] = useState<Summary | null>(null);
  const [transcripts, setTranscripts] = useState<Transcript[]>([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;

  useEffect(() => {
    if (!meetingId || !token) {
      router.push('/dashboard');
      return;
    }

    fetchSummary();
  }, [meetingId, token, router]);

  const fetchSummary = async () => {
    try {
      const response = await axios.get(
        `${process.env.NEXT_PUBLIC_API_URL}/api/ai/summary/${meetingId}`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setSummary(response.data);

      const transcriptResponse = await axios.get(
        `${process.env.NEXT_PUBLIC_API_URL}/api/meetings/${meetingId}/transcripts`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setTranscripts(transcriptResponse.data);
    } catch (error) {
      console.error('Failed to fetch summary:', error);
      // Try to generate summary if not found
      generateSummary();
    } finally {
      setLoading(false);
    }
  };

  const generateSummary = async () => {
    setGenerating(true);
    try {
      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/api/ai/summarize`,
        { meeting_id: meetingId },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setSummary(response.data);

      const transcriptResponse = await axios.get(
        `${process.env.NEXT_PUBLIC_API_URL}/api/meetings/${meetingId}/transcripts`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setTranscripts(transcriptResponse.data);
    } catch (error) {
      console.error('Failed to generate summary:', error);
    } finally {
      setGenerating(false);
    }
  };

  const handleDownloadPDF = () => {
    // Placeholder for PDF download functionality
    alert('PDF download feature coming soon!');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center">
        <div className="text-white text-xl">Loading summary...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      <Navbar />

      <div className="max-w-4xl mx-auto p-4 sm:p-6 lg:p-8">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-4xl font-bold text-white">Meeting Summary</h1>
          <Button
            onClick={handleDownloadPDF}
            className="bg-blue-600 hover:bg-blue-700 flex items-center gap-2"
          >
            <Download className="w-4 h-4" />
            Download PDF
          </Button>
        </div>

        {generating && (
          <Card className="bg-blue-900/20 border-blue-700 p-4 mb-6 flex items-center gap-2">
            <Loader className="w-5 h-5 text-blue-400 animate-spin" />
            <span className="text-blue-400">Generating AI summary...</span>
          </Card>
        )}

        {summary ? (
          <div className="space-y-6">
            {/* Summary */}
            <Card className="bg-slate-700/50 border-slate-600 p-6">
              <h2 className="text-2xl font-semibold text-white mb-4">Summary</h2>
              <p className="text-slate-300 leading-relaxed">{summary.summary_text}</p>
            </Card>

            {/* Transcripts */}
            <Card className="bg-slate-700/50 border-slate-600 p-6">
              <h3 className="text-xl font-semibold text-white mb-4">Transcripts</h3>
              <div className="space-y-3 max-h-80 overflow-y-auto">
                {transcripts.length === 0 ? (
                  <p className="text-slate-400">No transcripts available.</p>
                ) : (
                  transcripts.map((t) => (
                    <div key={t.id} className="bg-slate-800/50 p-3 rounded">
                      <p className="text-sm font-medium text-blue-400">{t.speaker_name}</p>
                      <p className="text-slate-300">{t.transcript_text}</p>
                    </div>
                  ))
                )}
              </div>
            </Card>

            {/* Action Items */}
            {summary.action_items && summary.action_items.length > 0 && (
              <Card className="bg-slate-700/50 border-slate-600 p-6">
                <h3 className="text-xl font-semibold text-white mb-4 flex items-center gap-2">
                  <CheckCircle className="w-5 h-5 text-green-400" />
                  Action Items
                </h3>
                <ul className="space-y-2">
                  {summary.action_items.map((item, i) => (
                    <li key={i} className="flex items-start gap-3 text-slate-300">
                      <span className="text-green-400 mt-1">•</span>
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </Card>
            )}

            {/* Keywords */}
            {summary.keywords && summary.keywords.length > 0 && (
              <Card className="bg-slate-700/50 border-slate-600 p-6">
                <h3 className="text-xl font-semibold text-white mb-4">Key Topics</h3>
                <div className="flex flex-wrap gap-2">
                  {summary.keywords.map((keyword, i) => (
                    <span
                      key={i}
                      className="bg-blue-600/20 border border-blue-500 text-blue-300 px-3 py-1 rounded-full text-sm"
                    >
                      {keyword}
                    </span>
                  ))}
                </div>
              </Card>
            )}

            {/* Back Button */}
            <Button
              onClick={() => router.push('/dashboard')}
              variant="outline"
              className="w-full border-slate-600 text-white hover:bg-slate-700"
            >
              Back to Dashboard
            </Button>
          </div>
        ) : (
          <Card className="bg-slate-700/50 border-slate-600 p-12 text-center">
            <p className="text-slate-400 mb-4">No summary available yet.</p>
            <Button
              onClick={generateSummary}
              disabled={generating}
              className="bg-blue-600 hover:bg-blue-700"
            >
              {generating ? 'Generating...' : 'Generate Summary'}
            </Button>
          </Card>
        )}
      </div>
    </div>
  );
}
