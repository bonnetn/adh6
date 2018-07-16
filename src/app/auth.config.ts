import { AuthConfig } from 'angular-oauth2-oidc';

export const authConfig: AuthConfig = {
  loginUrl: 'https://adh6.minet.net/oauth/authorize',
  logoutUrl: 'https://adh6.minet.net/oauth/logout',
  redirectUri: 'https://adh6.minet.net',
  clientId: 'H4XcptJlYAWAqyxTJxybMXfi',
  scope: 'profile',
  oidc: false,
}
