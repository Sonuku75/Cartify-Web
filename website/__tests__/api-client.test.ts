import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { apiClient, checkApiHealth, ApiError } from '@/lib/api-client';

describe('API Client', () => {
  const originalFetch = globalThis.fetch;

  beforeEach(() => {
    globalThis.fetch = vi.fn();
  });

  afterEach(() => {
    globalThis.fetch = originalFetch;
    vi.restoreAllMocks();
  });

  it('performs GET request and returns standardized Cartify envelope', async () => {
    const mockResponse = {
      success: true,
      message: 'Items retrieved',
      data: [{ id: 1, title: 'Item 1' }],
    };

    (globalThis.fetch as any).mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: async () => mockResponse,
    });

    const result = await apiClient.get<any[]>('/items/');
    expect(result.success).toBe(true);
    expect(result.data).toHaveLength(1);
    expect(result.data[0].title).toBe('Item 1');
  });

  it('performs POST request with JSON serialized body', async () => {
    const mockResponse = {
      success: true,
      message: 'Created',
      data: { id: 2, title: 'New Item' },
    };

    (globalThis.fetch as any).mockResolvedValueOnce({
      ok: true,
      status: 201,
      json: async () => mockResponse,
    });

    const body = { title: 'New Item' };
    const result = await apiClient.post<any>('/items/', body);

    expect(globalThis.fetch).toHaveBeenCalledWith(
      expect.stringContaining('/items/'),
      expect.objectContaining({
        method: 'POST',
        body: JSON.stringify(body),
        headers: expect.objectContaining({
          'Content-Type': 'application/json',
        }),
      })
    );
    expect(result.data.title).toBe('New Item');
  });

  it('throws ApiError with standardized details on HTTP 400 failure', async () => {
    const mockError = {
      success: false,
      message: 'Validation failed for one or more fields.',
      errors: {
        email: ['Enter a valid email address.'],
      },
    };

    (globalThis.fetch as any).mockResolvedValueOnce({
      ok: false,
      status: 400,
      json: async () => mockError,
    });

    await expect(apiClient.get('/invalid-endpoint/')).rejects.toThrow(ApiError);
  });

  it('checkApiHealth fetches lightweight health probe', async () => {
    const mockHealth = {
      status: 'ok',
      service: 'cartify-api',
    };

    (globalThis.fetch as any).mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: async () => mockHealth,
    });

    const health = await checkApiHealth();
    expect(health.status).toBe('ok');
    expect(health.service).toBe('cartify-api');
  });
});
