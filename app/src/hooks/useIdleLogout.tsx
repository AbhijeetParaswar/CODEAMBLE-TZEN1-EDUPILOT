import { useEffect } from "react";
import { createClient } from "@/lib/supabase/client";
import { useRouter, usePathname } from "next/navigation";

const SESSION_KEY = "session-login-time";
const savedRememberMe = localStorage.getItem("remember-me") === "true";
const EXPIRY_MS = savedRememberMe ? 30 * 24 * 60 * 60 * 1000 : 7 * 24 * 60 * 60 * 1000;

export function useSessionExpiry() {
  const router = useRouter();
  const pathName = usePathname();
  const supabase = createClient();

  useEffect(() => {
    const checkExpiry = async () => {
      const {
        data: { session },
      } = await supabase.auth.getSession();

      if (!session) {
        localStorage.removeItem(SESSION_KEY);
        return;
      }

      const loginTime = localStorage.getItem(SESSION_KEY);

      if (!loginTime) {
        localStorage.setItem(SESSION_KEY, Date.now().toString());
        return;
      }

      const elapsed = Date.now() - parseInt(loginTime, 10);

      if (elapsed > EXPIRY_MS) {
        localStorage.removeItem(SESSION_KEY);
        await supabase.auth.signOut();
        router.push("/auth/login");
      }
    };

    checkExpiry();
  }, [pathName]);
}
