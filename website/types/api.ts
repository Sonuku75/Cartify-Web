/**
 * API response and error types adhering to Cartify backend contracts.
 */

export interface ApiResponse<T = any> {
  success: boolean;
  message: string;
  data: T;
}

export interface ApiErrorResponse {
  success: false;
  message: string;
  errors: Record<string, string[] | string>;
}

export interface PaginatedData<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export type PaginatedApiResponse<T> = ApiResponse<PaginatedData<T>>;

export interface HealthResponse {
  status: string;
  service: string;
}
