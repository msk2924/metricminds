export type ChartType = "bar" | "line" | "area" | "pie";
export interface Analysis { explanation: string; chart: { type: ChartType; title: string; x_key: string | null; series: string[]; data: Record<string, string | number>[] }; table: { columns: string[]; rows: Record<string, string | number>[] } }
const baseUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
export async function askMetricMind(message: string): Promise<Analysis> { const response = await fetch(`${baseUrl}/api/chat`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ message }) }); if (!response.ok) { const data = await response.json().catch(() => ({})); throw new Error(data.detail ?? "Analysis request failed"); } return response.json(); }
