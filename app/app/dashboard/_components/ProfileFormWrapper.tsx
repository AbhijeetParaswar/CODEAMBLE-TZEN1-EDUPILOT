"use client";

import { useEffect, useState } from "react";
import { getProfile, type StudentProfile } from "@/lib/api/api";
import ProfileForm from "./ProfileForm";

function ProfileSkeleton() {
  return (
    <div className="flex flex-col gap-6 max-w-2xl animate-pulse">
      <div>
        <div className="w-40 h-6 bg-gray-200 dark:bg-white/10 rounded mb-2" />
        <div className="w-72 h-3 bg-gray-200 dark:bg-white/10 rounded" />
      </div>
      {[...Array(3)].map((_, i) => (
        <div
          key={i}
          className="border border-black/10 dark:border-white/8 p-5 flex flex-col gap-4"
        >
          <div className="w-32 h-4 bg-gray-200 dark:bg-white/10 rounded" />
          <div className="grid grid-cols-2 gap-4">
            {[...Array(4)].map((_, j) => (
              <div key={j} className="flex flex-col gap-1">
                <div className="w-20 h-3 bg-gray-200 dark:bg-white/10 rounded" />
                <div className="w-full h-9 bg-gray-200 dark:bg-white/10 rounded" />
              </div>
            ))}
          </div>
        </div>
      ))}
      <div className="w-28 h-9 bg-gray-200 dark:bg-white/10 rounded" />
    </div>
  );
}

export default function ProfileFormWrapper({
  userId,
  userEmail,
}: {
  userId: string;
  userEmail: string;
}) {
  const [profile, setProfile] = useState<StudentProfile | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getProfile(userId, userEmail)
      .then((data) => setProfile(data))
      .catch(() => setProfile(null))
      .finally(() => setLoading(false));
  }, [userId, userEmail]);

  if (loading) return <ProfileSkeleton />;

  return (
    <ProfileForm initial={profile} userId={userId} userEmail={userEmail} />
  );
}
