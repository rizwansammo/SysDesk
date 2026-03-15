import { api, setAuthToken } from "./api";
import { clearTokens, getAccessToken, setTokens } from "./auth";
import type {
  CurrentUser,
  DashboardReport,
  LoginResponse,
  Ticket,
  TicketDetail,
} from "./types";

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
  const token = getAccessToken();
  setAuthToken(token);

  const response = await api.get<CurrentUser>("/auth/me/");
  return response.data;
}

export async function fetchDashboard(): Promise<DashboardReport> {
  const token = getAccessToken();
  setAuthToken(token);

  const response = await api.get<DashboardReport>("/reports/dashboard/");
  return response.data;
}

export async function fetchTickets(): Promise<Ticket[]> {
  const token = getAccessToken();
  setAuthToken(token);

  const response = await api.get<Ticket[]>("/tickets/");
  return response.data;
}

export async function fetchTicketDetail(ticketId: string | number): Promise<TicketDetail> {
  const token = getAccessToken();
  setAuthToken(token);

  const response = await api.get<TicketDetail>(`/tickets/${ticketId}/`);
  return response.data;
}

export function logout() {
  clearTokens();
  setAuthToken(null);
}