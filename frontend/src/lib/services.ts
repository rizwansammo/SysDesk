import { api, setAuthToken } from "./api";
import { clearTokens, getAccessToken, setTokens } from "./auth";
import type {
  AgentUser,
  CurrentUser,
  DashboardReport,
  LoginResponse,
  Ticket,
  TicketDetail,
} from "./types";

function prepareAuth() {
  const token = getAccessToken();
  setAuthToken(token);
}

export async function login(email: string, password: string): Promise<LoginResponse> {
  const response = await api.post<LoginResponse>("/auth/login/", {
    email,
    password,
  });

  setTokens(response.data.access, response.data.refresh);
  setAuthToken(response.data.access);

  return response.data;
}

export async function fetchMe(): Promise<CurrentUser> {
  prepareAuth();
  const response = await api.get<CurrentUser>("/auth/me/");
  return response.data;
}

export async function fetchDashboard(): Promise<DashboardReport> {
  prepareAuth();
  const response = await api.get<DashboardReport>("/reports/dashboard/");
  return response.data;
}

export async function fetchTickets(): Promise<Ticket[]> {
  prepareAuth();
  const response = await api.get<Ticket[]>("/tickets/");
  return response.data;
}

export async function fetchMyTickets(): Promise<Ticket[]> {
  prepareAuth();
  const response = await api.get<Ticket[]>("/tickets/");
  return response.data;
}

export async function fetchTicketDetail(ticketId: string | number): Promise<TicketDetail> {
  prepareAuth();
  const response = await api.get<TicketDetail>(`/tickets/${ticketId}/`);
  return response.data;
}

export async function fetchAgents(): Promise<AgentUser[]> {
  prepareAuth();
  const response = await api.get<AgentUser[]>("/agents/");
  return response.data;
}

export async function assignTicket(ticketId: string | number, assignedAgentId: number | null) {
  prepareAuth();
  const response = await api.post(`/tickets/${ticketId}/assign/`, {
    assigned_agent_id: assignedAgentId,
  });
  return response.data;
}

export async function changeTicketStatus(ticketId: string | number, status: string) {
  prepareAuth();
  const response = await api.post(`/tickets/${ticketId}/change_status/`, {
    status,
  });
  return response.data;
}

export async function changeTicketPriority(ticketId: string | number, priority: string) {
  prepareAuth();
  const response = await api.post(`/tickets/${ticketId}/change_priority/`, {
    priority,
  });
  return response.data;
}

export async function addTicketReply(
  ticketId: string | number,
  body: string,
  isInternal: boolean
) {
  prepareAuth();
  const response = await api.post(`/tickets/${ticketId}/reply/`, {
    body,
    is_internal: isInternal,
  });
  return response.data;
}

export async function createTicket(payload: {
  subject: string;
  description: string;
  category?: string;
  priority?: string;
}) {
  prepareAuth();
  const response = await api.post("/tickets/", payload);
  return response.data;
}

export function logout() {
  clearTokens();
  setAuthToken(null);
}