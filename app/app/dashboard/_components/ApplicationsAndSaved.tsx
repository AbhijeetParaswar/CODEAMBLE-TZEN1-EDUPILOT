import { getApplications } from "@/lib/api/api";
import Link from "next/link";
import {
  GraduationCap,
  BookmarkCheck,
  MessageSquare,
  ChevronRight,
  Inbox,
} from "lucide-react";

function EmptyState({
  message,
  action,
}: {
  message: string;
  action?: { label: string; href: string };
}) {
  return (
    <div className="flex flex-col items-center justify-center py-10 px-5 gap-3 transition-all duration-500">
      <Inbox size={22} className="text-gray-300 dark:text-white/20 transition-all duration-500" />
      <p className="font-mono text-[12px] text-gray-400 dark:text-[#6B7280] text-center transition-all duration-500">
        {message}
      </p>
      {action && (
        <Link
          href={action.href}
          className="font-mono text-[12px] text-[#0C65D2] hover:underline"
        >
          {action.label} →
        </Link>
      )}
    </div>
  );
}

interface AppData {
  id: string;
  opportunity?: { title: string };
  state: string;
  progress_pct: number;
  saved: boolean;
  created_at: string;
}

export default async function ApplicationsAndSaved({
  userId,
  email,
}: {
  userId: string;
  email: string;
}) {
  const appsData = await getApplications(userId, email).catch(
    () => [] as AppData[],
  );

  const applications = appsData.slice(0, 5).map((a: AppData) => ({
    id: a.id,
    title: a.opportunity?.title ?? "Application",
    status: a.state.replace(/_/g, " "),
    pct: a.progress_pct,
  }));

  const saved = appsData
    .filter((a: AppData) => a.saved)
    .slice(0, 5)
    .map((a: AppData) => ({
      id: a.id,
      title: a.opportunity?.title ?? "Saved",
      type: "scholarship",
      saved: new Date(a.created_at).toLocaleDateString(),
    }));

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 transition-all duration-500">
      <div className="border border-black/10 dark:border-white/8 bg-gray-50 dark:bg-[#0F1117] transition-all duration-500">
        <div className="px-5 py-4 border-b border-black/10 dark:border-white/8">
          <p className="font-syne font-bold text-gray-900 dark:text-[#F0F4FF] text-sm transition-all duration-500">
            Application Progress
          </p>
          <p className="font-mono text-[11px] text-gray-400 dark:text-[#6B7280] transition-all duration-500">
            Track your active applications
          </p>
        </div>
        {applications.length === 0 ? (
          <EmptyState
            message="No applications tracked yet. Start applying to scholarships and internships to track them here."
            action={{
              label: "Browse scholarships",
              href: "/dashboard/scholarships",
            }}
          />
        ) : (
          <div className="flex flex-col gap-4 p-5">
            {applications.map((app) => (
              <div key={app.id}>
                <div className="flex items-center justify-between mb-1.5">
                  <p className="font-mono text-[12px] text-gray-900 dark:text-[#F0F4FF] truncate transition-all duration-500">
                    {app.title}
                  </p>
                  <span
                    className={`font-mono text-[10px] shrink-0 ml-2 ${
                      app.pct === 100
                        ? "text-green-500"
                        : app.pct < 50
                          ? "text-yellow-500"
                          : "text-[#0C65D2]"
                    }`}
                  >
                    {app.status}
                  </span>
                </div>
                <div className="w-full h-1.5 bg-black/8 dark:bg-white/8 rounded-full overflow-hidde transition-all duration-500">
                  <div
                    className={`h-full rounded-full transition-all duration-500 ${app.pct === 100 ? "bg-green-500" : "bg-[#0C65D2]"}`}
                    style={{ width: `${app.pct}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
      <div className="border border-black/10 dark:border-white/8 bg-gray-50 dark:bg-[#0F1117] transition-all duration-500">
        <div className="flex items-center justify-between px-5 py-4 border-b border-black/10 dark:border-white/8 transition-all duration-500">
          <div>
            <p className="font-syne font-bold text-gray-900 dark:text-[#F0F4FF] text-sm transition-all duration-500">
              Recent AI Chats
            </p>
            <p className="font-mono text-[11px] text-gray-400 dark:text-[#6B7280] transition-all duration-500">
              Your last conversations
            </p>
          </div>
          <Link
            href="/dashboard/chat"
            className="font-mono text-[11px] text-[#0C65D2] hover:underline flex items-center gap-1 transition-all duration-500"
          >
            Open <ChevronRight size={12} />
          </Link>
        </div>
        <EmptyState
          message="AI Chat coming in Phase 2. Use Scholarship Agent for now."
          action={{
            label: "Browse scholarships",
            href: "/dashboard/scholarships",
          }}
        />
      </div>
      <div className="border border-black/10 dark:border-white/8 bg-gray-50 dark:bg-[#0F1117] transition-all duration-500">
        <div className="flex items-center justify-between px-5 py-4 border-b border-black/10 dark:border-white/8 transition-all duration-500">
          <div>
            <p className="font-syne font-bold text-gray-900 dark:text-[#F0F4FF] text-sm transition-all duration-500">
              Saved Opportunities
            </p>
            <p className="font-mono text-[11px] text-gray-400 dark:text-[#6B7280] transition-all duration-500">
              Your bookmarked items
            </p>
          </div>
          <BookmarkCheck
            size={14}
            className="text-gray-400 dark:text-[#6B7280]"
          />
        </div>
        {saved.length === 0 ? (
          <EmptyState
            message="No saved opportunities yet. Browse scholarships and internships and bookmark ones you're interested in."
            action={{
              label: "Browse scholarships",
              href: "/dashboard/scholarships",
            }}
          />
        ) : (
          <div className="flex flex-col">
            {saved.map((s, i) => (
              <div
                key={s.id}
                className={`flex items-center gap-3 px-5 py-3.5 ${i !== saved.length - 1 ? "border-b border-black/10 dark:border-white/8" : ""} hover:bg-white dark:hover:bg-[#161822] transition-colors duration-500 cursor-pointer group`}
              >
                <div className="w-7 h-7 flex items-center justify-center shrink-0 bg-[#0C65D2]/10 border border-[#0C65D2]/20 text-[#0C65D2]">
                  <GraduationCap size={13} />
                </div>
                <div className="min-w-0 flex-1">
                  <p className="font-mono text-[12px] text-gray-900 dark:text-[#F0F4FF] truncate">
                    {s.title}
                  </p>
                  <p className="font-mono text-[10px] text-gray-400 dark:text-[#6B7280]">
                    Saved {s.saved}
                  </p>
                </div>
                <ChevronRight
                  size={13}
                  className="text-gray-300 dark:text-white/20 group-hover:text-[#0C65D2] shrink-0 transition-colors duration-500"
                />
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
