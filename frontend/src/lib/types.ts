export type RoleCode = "super_admin" | "agent" | "end_user" | "vip_user";

export interface Role {
  id: number;
  code: RoleCode;
  name: string;
}

export interface CurrentUser {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  full_name: string;
  phone: string;
  job_title: string;
  is_active: boolean;
  is_staff: boolean;
  is_superuser: boolean;
  organization: number | null;
  organization_name?: string;
  role: Role;
  created_at: string;
  updated_at: string;
}

export interface LoginResponse {
  refresh: string;
  access: string;
}

export interface TicketSLA {
  policy_id: number | null;
  policy_name: string | null;
  priority: string;
  first_response_deadline: string | null;
  resolution_deadline: string | null;
  first_response_breached: boolean;
  resolution_breached: boolean;
}

export interface Ticket {
  id: number;
  ticket_number: string;
  organization: number;
  organization_name: string;
  created_by: number;
  created_by_name: string;
  assigned_agent: number | null;
  assigned_agent_name?: string;
  subject: string;
  description: string;
  status: "open" | "pending" | "resolved" | "closed";
  priority: "low" | "medium" | "high" | "critical";
  category: string;
  source: "portal" | "email" | "api";
  created_at: string;
  updated_at: string;
  sla?: TicketSLA;
}

export interface DashboardReport {
  tickets_by_status: { status: string; count: number }[];
  tickets_by_organization: {
    organization_id: number;
    organization_name: string;
    count: number;
  }[];
  tickets_by_priority: { priority: string; count: number }[];
  agent_workload: {
    agent_id: number;
    agent_name: string;
    agent_email: string;
    open_count: number;
    pending_count: number;
    resolved_count: number;
    closed_count: number;
    total_count: number;
  }[];
  avg_first_response_minutes: number | null;
  avg_resolution_minutes: number | null;
  sla_breached_count: number;
  open_tickets_count: number;
  pending_tickets_count: number;
  resolved_tickets_count: number;
  closed_tickets_count: number;
}