import { createClient } from "@/lib/supabase/server";
import { redirect } from "next/navigation";
import InternshipsClient from "../_components/InternshipsClient";

export const dynamic = "force-dynamic";

export default async function InternshipsPage() {
  const supabase = await createClient();
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) redirect("/auth/login");

  return (
    <InternshipsClient
      userId={user.id}
      userEmail={user.email ?? ""}
    />
  );
}
