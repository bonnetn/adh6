import {AuthConfig} from 'angular-oauth2-oidc';

export const authConfig: AuthConfig = {
  loginUrl: '${SSO_AUTHORIZE}',
  logoutUrl: '${SSO_LOGOUT}',
  redirectUri: '${ADH6_URL}',
  clientId: 'adh6',
  scope: 'profile',
  oidc: false,
};
