import type { Metadata } from 'next';
import type { ReactNode } from 'react';
import { Providers } from './providers';
import './globals.css';

export const metadata: Metadata = {
  title: 'EchoBrief AI - Meeting Transcription & Summarization',
  description: 'AI-powered audio meeting platform with real-time transcription and intelligent summaries',
  keywords: ['meetings', 'transcription', 'AI', 'summarization', 'audio'],
  authors: [{ name: 'EchoBrief Team' }],
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://echobriefai.com',
    title: 'EchoBrief AI',
    description: 'AI-powered audio meeting platform',
  },
};

export default function RootLayout({
  children,
}: {
  children: ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </head>
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
