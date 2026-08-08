import { getDashboardStats, getProfile } from "@/lib/api/api";
import { AlertCircle } from "lucide-react";
import { GraduationCap, Briefcase, FileText, TrendingUp } from "lucide-react";
import Link from "next/link";

export default async function StatsSection({
  userId,
  email,
}: {
  userId: string;
  email: string;
}) {
  const [stats, profile] = await Promise.all([
    getDashboardStats(userId, email).catch(() => ({
      scholarships_matched: 0,
      internships_available: 0,
      documents_uploaded: 0,
      applications_tracked: 0,
      readiness_score: 0,
    })),
    getProfile(userId, email).catch(() => null),
  ]);

  const profileComplete = !!(
    profile?.college &&
    profile?.stream &&
    profile?.year_of_study
  );

  return (
    <>
      {!profileComplete && (
        <div className="flex items-center justify-between gap-4 px-5 py-4 border border-yellow-500/30 bg-yellow-500/8 dark:bg-yellow-500/10 transition-all duration-500">
          <div className="flex items-center gap-3">
            <AlertCircle size={16} className="text-yellow-500 shrink-0" />
            <p className="font-mono text-sm text-yellow-700 dark:text-yellow-400">
              Complete your profile to get personalized scholarship matches.
            </p>
          </div>
          <Link
            href="/dashboard/profile"
            className="font-mono text-[12px] text-yellow-600 dark:text-yellow-400 border border-yellow-500/30 px-3 py-1.5 hover:bg-yellow-500/10 shrink-0 transition-all duration-500"
          >
            Complete profile →
          </Link>
        </div>
      )}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 transition-all duration-500">
        {[
          {
            label: "Scholarships matched",
            value: String(stats.scholarships_matched),
            icon: <GraduationCap size={16} />,
            color: "text-[#0C65D2]",
          },
          {
            label: "Internships available",
            value: String(stats.internships_available),
            icon: <Briefcase size={16} />,
            color: "text-green-500",
          },
          {
            label: "Documents uploaded",
            value: String(stats.documents_uploaded),
            icon: <FileText size={16} />,
            color: "text-purple-500",
          },
          {
            label: "Applications tracked",
            value: String(stats.applications_tracked),
            icon: <TrendingUp size={16} />,
            color: "text-orange-500",
          },
        ].map((stat) => (
          <div
            key={stat.label}
            className="border border-black/10 dark:border-white/8 bg-gray-50 dark:bg-[#0F1117] p-4 transition-all duration-500"
          >
            <div className={`mb-2 ${stat.color}`}>{stat.icon}</div>
            <p className={`font-syne text-2xl font-extrabold ${stat.color}`}>
              {stat.value}
            </p>
            <p className="font-mono text-[11px] text-gray-400 dark:text-[#6B7280] mt-0.5">
              {stat.label}
            </p>
          </div>
        ))}
      </div>
    </>
  );
}
