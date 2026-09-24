const API=import.meta.env.VITE_API_URL || 'http://localhost:8000';
export type Job={id:string;status:string;progress:number;current_step:string;error?:string;pages?:string[];pdf_url?:string};
export async function createTopic(payload:object){const r=await fetch(`${API}/api/generate/topic`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});if(!r.ok)throw new Error('Could not start generation.');return r.json() as Promise<Job>}
export async function getJob(id:string){const r=await fetch(`${API}/api/generation/${id}`);if(!r.ok)throw new Error('Could not retrieve generation.');return r.json() as Promise<Job>}
export {API};
