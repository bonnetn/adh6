import { AuthConfig } from 'angular-oauth2-oidc';

export const authConfig: AuthConfig = {
  loginUrl: 'http://zteeed.fr:50000/oauth/authorize',
  redirectUri: 'http://zteeed.fr:55555',
  clientId: 'iEj5ZZivEYvKxHKuc4d6EQcC',
  scope: 'profile',
  requireHttps: false,
  oidc: false,
}
