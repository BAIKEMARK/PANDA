export interface FileInfo {
  id: string;
  org_id?: string;
  filename: string;
  stored_filename: string;
  file_path: string;
  file_type?: string;
  file_size?: number;
  mime_type?: string;
  category: string;
  resource_type?: string;
  resource_id?: string;
  uploaded_by: string;
  description?: string;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface FileListResponse {
  files: FileInfo[];
  total: number;
  skip: number;
  limit: number;
}

export interface FileUploadResponse {
  file: FileInfo;
  url: string;
}
