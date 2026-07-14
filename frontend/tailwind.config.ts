import type { Config } from "tailwindcss";
export default { darkMode: ["class"], content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"], theme: { extend: { colors: { surface: "hsl(var(--surface))", border: "hsl(var(--border))" } } }, plugins: [] } satisfies Config;
