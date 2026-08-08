export const runtime = "edge";
import { createClient } from "@/lib/supabase/server";
import { redirect } from "next/navigation";
import ScholarshipsClient from "../_components/ScholarshipsClient";

export default async function ScholarshipsPage() {
  const supabase = await createClient();
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) redirect("/auth/login");

  return (
    <ScholarshipsClient
      userId={user.id}
      userEmail={user.email ?? ""}
    />
  );
}