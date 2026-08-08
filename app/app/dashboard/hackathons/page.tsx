export const runtime = "edge";
import { createClient } from "@/lib/supabase/server";
import { redirect } from "next/navigation";
import HackathonsClient from "../_components/HackathonsClient";

export const dynamic = "force-dynamic";

export default async function HackathonsPage() {
  const supabase = await createClient();
  const {
    data: { user },
  } = await supabase.auth.getUser();
  if (!user) redirect("/auth/login");

  return <HackathonsClient userId={user.id} userEmail={user.email ?? ""} />;
}
