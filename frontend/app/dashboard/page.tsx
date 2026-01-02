'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Navbar } from '@/components/navbar';
import { Plus, Calendar, Users, Clock, FileText, MessageSquare } from 'lucide-react';
import axios from 'axios';

interface Meeting {
  id: string;
  meeting_title: string;
  status: string;
  created_at: string;
  ended_at?: string;
  participants_count?: number;
}

export default function Dashboard() {
  const router = useRouter();
  const [meetings, setMeetings] = useState<Meeting[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [meetingTitle, setMeetingTitle] = useState('');
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('user');

    if (!token) {
      router.push('/auth');
      return;
    }

    if (userData) {
      setUser(JSON.parse(userData));
      fetchMeetings(JSON.parse(userData).id, token);
    }
  }, [router]);

  const fetchMeetings = async (userId: string, token: string) => {
    try {
      const response = await axios.get(
        `${process.env.NEXT_PUBLIC_API_URL}/api/meetings/user/${userId}`,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );
      setMeetings(response.data);
    } catch (error) {
      console.error('Failed to fetch meetings:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateMeeting = async () => {
    if (!meetingTitle.trim()) return;

    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/api/meetings/create`,
        { meeting_title: meetingTitle, max_participants: 20 },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      setMeetings([response.data, ...meetings]);
      setMeetingTitle('');
      setShowCreateModal(false);
      router.push(`/meeting/${response.data.id}`);
    } catch (error) {
      console.error('Failed to create meeting:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      <Navbar />

      <div className="max-w-6xl mx-auto p-4 sm:p-6 lg:p-8">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-4xl font-bold text-white">Dashboard</h1>
            <p className="text-slate-400 mt-2">Welcome back, {user?.name}</p>
          </div>
          <Button
            onClick={() => setShowCreateModal(true)}
            className="bg-blue-600 hover:bg-blue-700 flex items-center gap-2"
          >
            <Plus className="w-4 h-4" />
            New Meeting
          </Button>
        </div>

        {/* Create Meeting Modal */}
        {showCreateModal && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
            <Card className="w-full max-w-md bg-slate-800 border-slate-700">
              <div className="p-6">
                <h2 className="text-2xl font-bold text-white mb-4">Create New Meeting</h2>
                <Input
                  type="text"
                  placeholder="Meeting Title"
                  value={meetingTitle}
                  onChange={(e) => setMeetingTitle(e.target.value)}
                  className="bg-slate-700 border-slate-600 text-white mb-4"
                />
                <div className="flex gap-2">
                  <Button
                    onClick={handleCreateMeeting}
                    className="flex-1 bg-blue-600 hover:bg-blue-700"
                  >
                    Create
                  </Button>
                  <Button
                    onClick={() => setShowCreateModal(false)}
                    variant="outline"
                    className="flex-1 border-slate-600 text-white hover:bg-slate-700"
                  >
                    Cancel
                  </Button>
                </div>
              </div>
            </Card>
          </div>
        )}

        {/* Meetings Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {loading ? (
            <div className="col-span-full text-center text-slate-400 py-12">
              Loading meetings...
            </div>
          ) : meetings.length === 0 ? (
            <div className="col-span-full text-center text-slate-400 py-12">
              <p className="mb-4">No meetings yet. Create one to get started!</p>
            </div>
          ) : (
            meetings.map((meeting) => (
              <Card
                key={meeting.id}
                className="bg-slate-700/50 border-slate-600 hover:border-blue-500 transition"
              >
                <div className="p-6 space-y-4">
                  <h3 className="text-lg font-semibold text-white">
                    {meeting.meeting_title}
                  </h3>
                  <div className="space-y-2 text-sm text-slate-300">
                    <div className="flex items-center gap-2">
                      <Calendar className="w-4 h-4" />
                      {new Date(meeting.created_at).toLocaleDateString()}
                    </div>
                    <div className="flex items-center gap-2">
                      <Clock className="w-4 h-4" />
                      {meeting.status}
                    </div>
                    <div className="flex items-center gap-2">
                      <Users className="w-4 h-4" />
                      {meeting.participants_count ?? 0} participants
                    </div>
                  </div>
                  <div className="flex flex-col gap-2">
                    <Button
                      onClick={() => router.push(`/meeting?id=${meeting.id}`)}
                      className="w-full bg-blue-600 hover:bg-blue-700 flex items-center gap-2 justify-center"
                    >
                      <MessageSquare className="w-4 h-4" />
                      Open Meeting
                    </Button>
                    <Button
                      onClick={() => router.push(`/summary?id=${meeting.id}`)}
                      variant="outline"
                      className="w-full border-slate-600 text-white hover:bg-slate-700 flex items-center gap-2 justify-center"
                    >
                      <FileText className="w-4 h-4" />
                      View Summary & Transcript
                    </Button>
                  </div>
                </div>
              </Card>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
