/**
 * 分页Hook
 * 统一管理分页状态和逻辑
 */
import { useState, useCallback } from 'react';

export interface PaginationState {
  page: number;
  pageSize: number;
  total: number;
  totalPages: number;
}

export interface UsePaginationReturn {
  pagination: PaginationState;
  setPagination: (pagination: Partial<PaginationState>) => void;
  setPage: (page: number) => void;
  setPageSize: (pageSize: number) => void;
  setTotal: (total: number) => void;
  reset: () => void;
  getAntdPagination: () => {
    current: number;
    pageSize: number;
    total: number;
    showSizeChanger: boolean;
    showQuickJumper: boolean;
    showTotal: (total: number) => string;
    onChange: (page: number, pageSize: number) => void;
  };
}

const DEFAULT_PAGE_SIZE = 10;

export function usePagination(
  initialPageSize: number = DEFAULT_PAGE_SIZE
): UsePaginationReturn {
  const [pagination, setPaginationState] = useState<PaginationState>({
    page: 1,
    pageSize: initialPageSize,
    total: 0,
    totalPages: 0,
  });

  const setPagination = useCallback((newPagination: Partial<PaginationState>) => {
    setPaginationState((prev) => {
      const updated = { ...prev, ...newPagination };
      // 自动计算总页数
      if ('total' in newPagination || 'pageSize' in newPagination) {
        updated.totalPages = Math.ceil(updated.total / updated.pageSize);
      }
      return updated;
    });
  }, []);

  const setPage = useCallback((page: number) => {
    setPagination({ page });
  }, [setPagination]);

  const setPageSize = useCallback((pageSize: number) => {
    setPagination({ pageSize, page: 1 }); // 改变页大小时重置到第一页
  }, [setPagination]);

  const setTotal = useCallback((total: number) => {
    setPagination({ total });
  }, [setPagination]);

  const reset = useCallback(() => {
    setPaginationState({
      page: 1,
      pageSize: initialPageSize,
      total: 0,
      totalPages: 0,
    });
  }, [initialPageSize]);

  const getAntdPagination = useCallback(() => {
    return {
      current: pagination.page,
      pageSize: pagination.pageSize,
      total: pagination.total,
      showSizeChanger: true,
      showQuickJumper: true,
      showTotal: (total: number) => `共 ${total} 条`,
      onChange: (page: number, pageSize: number) => {
        setPagination({ page, pageSize });
      },
    };
  }, [pagination, setPagination]);

  return {
    pagination,
    setPagination,
    setPage,
    setPageSize,
    setTotal,
    reset,
    getAntdPagination,
  };
}
