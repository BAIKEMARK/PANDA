import { isAxiosError } from 'axios';

type ApiErrorPayload = {
  detail?: unknown;
  message?: unknown;
};

const isApiErrorPayload = (value: unknown): value is ApiErrorPayload =>
  typeof value === 'object' && value !== null;

const stringFromPayloadValue = (value: unknown): string | undefined => {
  if (typeof value === 'string') {
    return value;
  }
  return undefined;
};

export const getApiErrorMessage = (error: unknown, fallback = '操作失败'): string => {
  if (isAxiosError(error)) {
    const data = error.response?.data;
    if (isApiErrorPayload(data)) {
      return (
        stringFromPayloadValue(data.detail) ??
        stringFromPayloadValue(data.message) ??
        error.message ??
        fallback
      );
    }
    return error.message || fallback;
  }

  if (error instanceof Error) {
    return error.message;
  }

  return fallback;
};
