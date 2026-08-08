import Link from "next/link";
import {
  GraduationCap,
  MessageSquare,
  FileText,
  Briefcase,
  ArrowRight,
} from "lucide-react";

const actions = [
  {
    href: "/dashboard/scholarships",
    label: "Search scholarships",
    icon: <GraduationCap size={15} />,
  },
  {
    href: "/dashboard/chat",
    label: "Chat with AI",
    icon: <MessageSquare size={15} />,
  },
  {
    href: "/dashboard/documents",
    label: "Upload document",
    icon: <FileText size={15} />,
  },
  {
    href: "/dashboard/internships",
    label: "Find internships",
    icon: <Briefcase size={15} />,
  },
];

export default function QuickActions() {
  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 transition-all duration-500">
      {actions.map((action) => (
        <Link
          key={action.href}
          href={action.href}
          className="flex items-center justify-between gap-2 px-4 py-3 border border-black/10 dark:border-white/8 bg-white dark:bg-[#161822] hover:border-[#0C65D2]/40 hover:bg-[#0C65D2]/4 dark:hover:bg-[#0C65D2]/8 transition-all duration-500 group"
        >
          <div className="flex items-center gap-2 font-mono text-[12px] text-gray-600 dark:text-[#6B7280] group-hover:text-[#0C65D2] transition-all duration-500">
            <span className="text-[#0C65D2]">{action.icon}</span>
            {action.label}
          </div>
          <ArrowRight
            size={13}
            className="text-gray-300 dark:text-white/20 group-hover:text-[#0C65D2] transition-colors duration-500"
          />
        </Link>
      ))}
    </div>
  );
}
