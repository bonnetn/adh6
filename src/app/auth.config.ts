import { AuthConfig } from 'angular-oauth2-oidc';

export const authConfig: AuthConfig = {
  loginUrl: 'http://192.168.103.175:50000/oauth/authorize',
  redirectUri: 'http://192.168.103.175',
  clientId: 'jgE8tWMNou0chC1lvL4ecO5c',
  scope: 'profile',
  requireHttps: false,
  oidc: false,
}
