export type FilterValues = Record<string, unknown>;

export const getFilterText = (values: FilterValues, key: string): string => {
  const value = values[key];
  return typeof value === 'string' ? value.trim().toLowerCase() : '';
};

export const getFilterValue = (values: FilterValues, key: string): string | undefined => {
  const value = values[key];
  return typeof value === 'string' && value !== '' ? value : undefined;
};
