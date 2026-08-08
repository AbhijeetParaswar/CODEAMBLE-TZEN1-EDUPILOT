import { createClient } from "@/lib/supabase/server";
import { redirect } from "next/navigation";
import ProfileClient from "./ProfileClient";

export default async function ProfilePage() {
  const supabase = await createClient();
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) redirect("/auth/login");

  const { data: profile } = await supabase
    .from("profiles")
    .select("full_name, email, phone, college, stream, year_of_study, cgpa, is_admin")
    .eq("id", user.id)
    .single();

  const { count: documentCount } = await supabase
    .from("documents")
    .select("*", { count: "exact", head: true })
    .eq("user_id", user.id);

  return (
    <ProfileClient
      userId={user.id}
      initialProfile={{
        full_name: profile?.full_name ?? "",
        email: profile?.email ?? user.email ?? "",
        phone: profile?.phone ?? "",
        college: profile?.college ?? "",
        stream: profile?.stream ?? "",
        year_of_study: profile?.year_of_study ?? "",
        cgpa: profile?.cgpa ?? "",
        is_admin: profile?.is_admin ?? false,
      }}
      documentCount={documentCount ?? 0}
    />
  );
}