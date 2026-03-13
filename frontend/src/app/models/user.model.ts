export interface User {
  id: number;
  username: string;
  email: string;
  bio?: string;
  avatar_url?: string;
}

export interface AuthToken {
  access_token: string;
  token_type: string;
}

export interface UserCreate {
  username: string;
  email: string;
  password: string;
}