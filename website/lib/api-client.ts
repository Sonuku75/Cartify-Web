import { API_BASE_URL, API_HEALTH_URL } from "@/constants/config";
import { ApiResponse, ApiErrorResponse, HealthResponse } from "@/types/api";

export class ApiError extends Error {
  public status: number;
  public errors: Record<string, string[] | string>;

  constructor(status: number, message: string, errors: Record<string, string[] | string> = {}) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.errors = errors;
  }
}

interface RequestOptions extends RequestInit {
  params?: Record<string, string | number | boolean>;
}

async function request<T>(endpoint: string, options: RequestOptions = {}): Promise<ApiResponse<T>> {
  const { params, headers, ...customConfig } = options;

  let url = endpoint.startsWith("http") ? endpoint : `${API_BASE_URL}${endpoint}`;

  if (params) {
    const searchParams = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        searchParams.append(key, String(value));
      }
    });
    const queryString = searchParams.toString();
    if (queryString) {
      url += (url.includes("?") ? "&" : "?") + queryString;
    }
  }

  const defaultHeaders: HeadersInit = {
    "Content-Type": "application/json",
    Accept: "application/json",
  };

  const config: RequestInit = {
    method: "GET",
    headers: { ...defaultHeaders, ...headers },
    ...customConfig,
  };

  try {
    const response = await fetch(url, config);
    const data = await response.json();

    if (!response.ok) {
      const errorData = data as ApiErrorResponse;
      throw new ApiError(
        response.status,
        errorData.message || "An unexpected API error occurred",
        errorData.errors || {}
      );
    }

    return data as ApiResponse<T>;
  } catch (err: unknown) {
    if (err instanceof ApiError) {
      throw err;
    }
    const message = err instanceof Error ? err.message : "Network error. Please verify backend connectivity.";
    throw new ApiError(500, message);
  }
}

export const apiClient = {
  get: <T>(endpoint: string, options?: RequestOptions) =>
    request<T>(endpoint, { ...options, method: "GET" }),

  post: <T>(endpoint: string, body?: unknown, options?: RequestOptions) =>
    request<T>(endpoint, {
      ...options,
      method: "POST",
      body: body ? JSON.stringify(body) : undefined,
    }),

  put: <T>(endpoint: string, body?: unknown, options?: RequestOptions) =>
    request<T>(endpoint, {
      ...options,
      method: "PUT",
      body: body ? JSON.stringify(body) : undefined,
    }),

  patch: <T>(endpoint: string, body?: unknown, options?: RequestOptions) =>
    request<T>(endpoint, {
      ...options,
      method: "PATCH",
      body: body ? JSON.stringify(body) : undefined,
    }),

  delete: <T>(endpoint: string, options?: RequestOptions) =>
    request<T>(endpoint, { ...options, method: "DELETE" }),
};

export async function checkApiHealth(): Promise<HealthResponse> {
  const response = await fetch(API_HEALTH_URL, {
    method: "GET",
    headers: { Accept: "application/json" },
  });
  if (!response.ok) {
    throw new Error(`Health check failed with status ${response.status}`);
  }
  return response.json();
}
