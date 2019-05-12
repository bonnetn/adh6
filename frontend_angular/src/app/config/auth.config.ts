import {AuthConfig} from 'angular-oauth2-oidc';

export const authConfig: AuthConfig = {
  loginUrl: 'https://cas.minet.net/oauth2.0/authorize',
  logoutUrl: 'https://cas.minet.net/logout',
  redirectUri: 'https://adh6.minet.net',
  clientId: 'adh6',
  scope: 'profile',
  oidc: false,
};
