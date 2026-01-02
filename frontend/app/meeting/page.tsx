'use client';

import { useEffect, useMemo, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Navbar } from '@/components/navbar';
import { Mic, MicOff, Phone, Users, MessageSquare } from 'lucide-react';
import axios from 'axios';

interface Transcript {
  id: string;
  speaker_name: string;
  transcript_text: string;
  created_at: string;
}

interface AudioFile {
  id: string;
  file_path: string;
  file_size?: number;
  duration_seconds?: number;
  format?: string;
}

export default function MeetingRoom() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const meetingId = useMemo(() => {
    const param = searchParams.get('id');
    if (param) return param;
    if (typeof window !== 'undefined') {
      const parts = window.location.pathname.split('/');
      return parts[parts.length - 1] || null;
    }
    return null;
  }, [searchParams]);
  const [meeting, setMeeting] = useState<any>(null);
  const [transcripts, setTranscripts] = useState<Transcript[]>([]);
  const [audioFiles, setAudioFiles] = useState<AudioFile[]>([]);
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState('');
  const [isMicOn, setIsMicOn] = useState(false);
  const [participants, setParticipants] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
  const user = typeof window !== 'undefined' ? JSON.parse(localStorage.getItem('user') || 'null') : null;

  useEffect(() => {
    if (!meetingId || !token) {
      router.push('/dashboard');
      return;
    }

    fetchMeetingDetails();
    const interval = setInterval(fetchMeetingDetails, 2000);
    return () => clearInterval(interval);
  }, [meetingId, token, router]);

  const fetchMeetingDetails = async () => {
    try {
      const response = await axios.get(
        `${process.env.NEXT_PUBLIC_API_URL}/api/meetings/${meetingId}`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setMeeting(response.data);
      setAudioFiles(response.data.audio_files || []);

      const transcriptResponse = await axios.get(
        `${process.env.NEXT_PUBLIC_API_URL}/api/meetings/${meetingId}/transcripts`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setTranscripts(transcriptResponse.data);
    } catch (error) {
      console.error('Failed to fetch meeting:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleEndMeeting = async () => {
    try {
      await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/api/meetings/${meetingId}/end`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      );
      router.push(`/summary/${meetingId}`);
    } catch (error) {
      console.error('Failed to end meeting:', error);
    }
  };

  const handleUploadAudio = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) return;
    const file = e.target.files[0];
    setUploading(true);
    setUploadError('');
    try {
      const formData = new FormData();
      formData.append('file', file);
      await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/api/audio/upload?meeting_id=${meetingId}&user_id=${user?.id}`,
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'multipart/form-data',
          },
        }
      );
      await fetchMeetingDetails();
    } catch (err: any) {
      setUploadError(err.response?.data?.detail || 'Upload failed');
    } finally {
      setUploading(false);
      e.target.value = '';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center">
        <div className="text-white text-xl">Loading meeting...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      <Navbar />

      <div className="max-w-6xl mx-auto p-4 sm:p-6 lg:p-8">
        <div className="grid lg:grid-cols-3 gap-6">
          {/* Main Video Area */}
          <div className="lg:col-span-2">
            <Card className="bg-slate-700/50 border-slate-600 aspect-video flex items-center justify-center mb-6">
              <div className="text-center">
                <Mic className="w-16 h-16 text-slate-400 mx-auto mb-4" />
                <p className="text-slate-400">Audio Meeting in Progress</p>
              </div>
            </Card>

            {/* Transcripts */}
            <Card className="bg-slate-700/50 border-slate-600 p-6">
              <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                <MessageSquare className="w-5 h-5" />
                Live Transcript
              </h3>
              <div className="space-y-3 max-h-96 overflow-y-auto">
                {transcripts.length === 0 ? (
                  <p className="text-slate-400">Waiting for transcription...</p>
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

            {/* Audio Files */}
            <Card className="bg-slate-700/50 border-slate-600 p-6 mt-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-white">Meeting Audio</h3>
                <div>
                  <input
                    type="file"
                    accept="audio/*"
                    onChange={handleUploadAudio}
                    disabled={uploading}
                    className="text-slate-300"
                  />
                </div>
              </div>
              {uploadError && (
                <div className="text-red-400 text-sm mb-3">Upload failed: {uploadError}</div>
              )}
              {audioFiles.length === 0 ? (
                <p className="text-slate-400">No audio uploaded yet.</p>
              ) : (
                <div className="space-y-4">
                  {audioFiles.map((file) => (
                    <div key={file.id} className="bg-slate-800/50 p-3 rounded">
                      <p className="text-sm text-slate-300 mb-2">
                        {file.file_path.split('/').pop()} • {file.format || 'audio'}
                      </p>
                      <audio
                        controls
                        className="w-full"
                        src={`${process.env.NEXT_PUBLIC_API_URL}${file.file_path}`}
                      />
                    </div>
                  ))}
                </div>
              )}
            </Card>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Meeting Info */}
            <Card className="bg-slate-700/50 border-slate-600 p-6">
              <h2 className="text-xl font-semibold text-white mb-4">{meeting?.meeting_title}</h2>
              <div className="space-y-3 text-sm text-slate-300">
                <div className="flex items-center gap-2">
                  <Users className="w-4 h-4" />
                  <span>{meeting?.participants_count || 0} participants</span>
                </div>
                <div className="text-xs text-slate-400">
                  Status: <span className="text-blue-400">{meeting?.status}</span>
                </div>
              </div>
            </Card>

            {/* Controls */}
            <Card className="bg-slate-700/50 border-slate-600 p-6">
              <div className="space-y-3">
                <Button
                  onClick={() => setIsMicOn(!isMicOn)}
                  className={`w-full flex items-center justify-center gap-2 ${
                    isMicOn
                      ? 'bg-red-600 hover:bg-red-700'
                      : 'bg-green-600 hover:bg-green-700'
                  }`}
                >
                  {isMicOn ? (
                    <>
                      <MicOff className="w-4 h-4" />
                      Mute
                    </>
                  ) : (
                    <>
                      <Mic className="w-4 h-4" />
                      Unmute
                    </>
                  )}
                </Button>
                <Button
                  onClick={handleEndMeeting}
                  className="w-full bg-red-600 hover:bg-red-700 flex items-center justify-center gap-2"
                >
                  <Phone className="w-4 h-4" />
                  End Meeting
                </Button>
              </div>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
