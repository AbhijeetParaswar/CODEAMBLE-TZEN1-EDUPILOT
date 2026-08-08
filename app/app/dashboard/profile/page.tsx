export const runtime = "edge";
import { createClient } from "@/lib/supabase/server";
import { redirect } from "next/navigation";
import ProfileFormWrapper from "../_components/ProfileFormWrapper";

export default async function ProfilePage() {
  const supabase = await createClient();
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) redirect("/auth/login");

  return <ProfileFormWrapper userId={user.id} userEmail={user.email ?? ""} />;
}