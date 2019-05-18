/**
 * Adherent
 * Adherent api
 *
 * The version of the OpenAPI document: 1.0.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */
/* tslint:disable:no-unused-variable member-ordering */

import { Inject, Injectable, Optional }                      from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams,
         HttpResponse, HttpEvent }                           from '@angular/common/http';
import { CustomHttpUrlEncodingCodec }                        from '../encoder';

import { Observable }                                        from 'rxjs';

import { Port } from '../model/port';

import { BASE_PATH, COLLECTION_FORMATS }                     from '../variables';
import { Configuration }                                     from '../configuration';


@Injectable({
  providedIn: 'root'
})
export class PortService {

    protected basePath = 'http://localhost/api';
    public defaultHeaders = new HttpHeaders();
    public configuration = new Configuration();

    constructor(protected httpClient: HttpClient, @Optional()@Inject(BASE_PATH) basePath: string, @Optional() configuration: Configuration) {

        if (configuration) {
            this.configuration = configuration;
            this.configuration.basePath = configuration.basePath || basePath || this.basePath;

        } else {
            this.configuration.basePath = basePath || this.basePath;
        }
    }

    /**
     * @param consumes string[] mime-types
     * @return true: consumes contains 'multipart/form-data', false: otherwise
     */
    private canConsumeForm(consumes: string[]): boolean {
        const form = 'multipart/form-data';
        for (const consume of consumes) {
            if (form === consume) {
                return true;
            }
        }
        return false;
    }


    /**
     * Check whether MAB is enable on this port or not.
     * 
     * @param portId 
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    public mabGet(portId: number, observe?: 'body', reportProgress?: boolean): Observable<boolean>;
    public mabGet(portId: number, observe?: 'response', reportProgress?: boolean): Observable<HttpResponse<boolean>>;
    public mabGet(portId: number, observe?: 'events', reportProgress?: boolean): Observable<HttpEvent<boolean>>;
    public mabGet(portId: number, observe: any = 'body', reportProgress: boolean = false ): Observable<any> {
        if (portId === null || portId === undefined) {
            throw new Error('Required parameter portId was null or undefined when calling mabGet.');
        }

        let headers = this.defaultHeaders;

        // to determine the Accept header
        const httpHeaderAccepts: string[] = [
            'application/json'
        ];
        const httpHeaderAcceptSelected: string | undefined = this.configuration.selectHeaderAccept(httpHeaderAccepts);
        if (httpHeaderAcceptSelected !== undefined) {
            headers = headers.set('Accept', httpHeaderAcceptSelected);
        }

        // to determine the Content-Type header
        const consumes: string[] = [
        ];

        return this.httpClient.get<boolean>(`${this.configuration.basePath}/port/${encodeURIComponent(String(portId))}/mab/`,
            {
                withCredentials: this.configuration.withCredentials,
                headers: headers,
                observe: observe,
                reportProgress: reportProgress
            }
        );
    }

    /**
     * Filter ports
     * 
     * @param limit Limit the number of ports returned in the result. Default is 100
     * @param offset Skip the first n results
     * @param switchID Filter only ports from that switch
     * @param roomNumber Filter only ports from that room
     * @param terms Search terms
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    public portGet(limit?: number, offset?: number, switchID?: number, roomNumber?: number, terms?: string, observe?: 'body', reportProgress?: boolean): Observable<Array<Port>>;
    public portGet(limit?: number, offset?: number, switchID?: number, roomNumber?: number, terms?: string, observe?: 'response', reportProgress?: boolean): Observable<HttpResponse<Array<Port>>>;
    public portGet(limit?: number, offset?: number, switchID?: number, roomNumber?: number, terms?: string, observe?: 'events', reportProgress?: boolean): Observable<HttpEvent<Array<Port>>>;
    public portGet(limit?: number, offset?: number, switchID?: number, roomNumber?: number, terms?: string, observe: any = 'body', reportProgress: boolean = false ): Observable<any> {

        let queryParameters = new HttpParams({encoder: new CustomHttpUrlEncodingCodec()});
        if (limit !== undefined && limit !== null) {
            queryParameters = queryParameters.set('limit', <any>limit);
        }
        if (offset !== undefined && offset !== null) {
            queryParameters = queryParameters.set('offset', <any>offset);
        }
        if (switchID !== undefined && switchID !== null) {
            queryParameters = queryParameters.set('switchID', <any>switchID);
        }
        if (roomNumber !== undefined && roomNumber !== null) {
            queryParameters = queryParameters.set('roomNumber', <any>roomNumber);
        }
        if (terms !== undefined && terms !== null) {
            queryParameters = queryParameters.set('terms', <any>terms);
        }

        let headers = this.defaultHeaders;

        // to determine the Accept header
        const httpHeaderAccepts: string[] = [
            'application/json'
        ];
        const httpHeaderAcceptSelected: string | undefined = this.configuration.selectHeaderAccept(httpHeaderAccepts);
        if (httpHeaderAcceptSelected !== undefined) {
            headers = headers.set('Accept', httpHeaderAcceptSelected);
        }

        // to determine the Content-Type header
        const consumes: string[] = [
        ];

        return this.httpClient.get<Array<Port>>(`${this.configuration.basePath}/port/`,
            {
                params: queryParameters,
                withCredentials: this.configuration.withCredentials,
                headers: headers,
                observe: observe,
                reportProgress: reportProgress
            }
        );
    }

    /**
     * Delete a port
     * 
     * @param portId 
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    public portPortIdDelete(portId: number, observe?: 'body', reportProgress?: boolean): Observable<any>;
    public portPortIdDelete(portId: number, observe?: 'response', reportProgress?: boolean): Observable<HttpResponse<any>>;
    public portPortIdDelete(portId: number, observe?: 'events', reportProgress?: boolean): Observable<HttpEvent<any>>;
    public portPortIdDelete(portId: number, observe: any = 'body', reportProgress: boolean = false ): Observable<any> {
        if (portId === null || portId === undefined) {
            throw new Error('Required parameter portId was null or undefined when calling portPortIdDelete.');
        }

        let headers = this.defaultHeaders;

        // to determine the Accept header
        const httpHeaderAccepts: string[] = [
        ];
        const httpHeaderAcceptSelected: string | undefined = this.configuration.selectHeaderAccept(httpHeaderAccepts);
        if (httpHeaderAcceptSelected !== undefined) {
            headers = headers.set('Accept', httpHeaderAcceptSelected);
        }

        // to determine the Content-Type header
        const consumes: string[] = [
        ];

        return this.httpClient.delete<any>(`${this.configuration.basePath}/port/${encodeURIComponent(String(portId))}`,
            {
                withCredentials: this.configuration.withCredentials,
                headers: headers,
                observe: observe,
                reportProgress: reportProgress
            }
        );
    }

    /**
     * Retrieve a port
     * 
     * @param portId 
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    public portPortIdGet(portId: number, observe?: 'body', reportProgress?: boolean): Observable<Port>;
    public portPortIdGet(portId: number, observe?: 'response', reportProgress?: boolean): Observable<HttpResponse<Port>>;
    public portPortIdGet(portId: number, observe?: 'events', reportProgress?: boolean): Observable<HttpEvent<Port>>;
    public portPortIdGet(portId: number, observe: any = 'body', reportProgress: boolean = false ): Observable<any> {
        if (portId === null || portId === undefined) {
            throw new Error('Required parameter portId was null or undefined when calling portPortIdGet.');
        }

        let headers = this.defaultHeaders;

        // to determine the Accept header
        const httpHeaderAccepts: string[] = [
            'application/json'
        ];
        const httpHeaderAcceptSelected: string | undefined = this.configuration.selectHeaderAccept(httpHeaderAccepts);
        if (httpHeaderAcceptSelected !== undefined) {
            headers = headers.set('Accept', httpHeaderAcceptSelected);
        }

        // to determine the Content-Type header
        const consumes: string[] = [
        ];

        return this.httpClient.get<Port>(`${this.configuration.basePath}/port/${encodeURIComponent(String(portId))}`,
            {
                withCredentials: this.configuration.withCredentials,
                headers: headers,
                observe: observe,
                reportProgress: reportProgress
            }
        );
    }

    /**
     * Enable/disable MAB on a port
     * 
     * @param portId 
     * @param body 
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    public portPortIdMabPut(portId: number, body: boolean, observe?: 'body', reportProgress?: boolean): Observable<any>;
    public portPortIdMabPut(portId: number, body: boolean, observe?: 'response', reportProgress?: boolean): Observable<HttpResponse<any>>;
    public portPortIdMabPut(portId: number, body: boolean, observe?: 'events', reportProgress?: boolean): Observable<HttpEvent<any>>;
    public portPortIdMabPut(portId: number, body: boolean, observe: any = 'body', reportProgress: boolean = false ): Observable<any> {
        if (portId === null || portId === undefined) {
            throw new Error('Required parameter portId was null or undefined when calling portPortIdMabPut.');
        }
        if (body === null || body === undefined) {
            throw new Error('Required parameter body was null or undefined when calling portPortIdMabPut.');
        }

        let headers = this.defaultHeaders;

        // to determine the Accept header
        const httpHeaderAccepts: string[] = [
        ];
        const httpHeaderAcceptSelected: string | undefined = this.configuration.selectHeaderAccept(httpHeaderAccepts);
        if (httpHeaderAcceptSelected !== undefined) {
            headers = headers.set('Accept', httpHeaderAcceptSelected);
        }

        // to determine the Content-Type header
        const consumes: string[] = [
            'application/json'
        ];
        const httpContentTypeSelected: string | undefined = this.configuration.selectHeaderContentType(consumes);
        if (httpContentTypeSelected !== undefined) {
            headers = headers.set('Content-Type', httpContentTypeSelected);
        }

        return this.httpClient.put<any>(`${this.configuration.basePath}/port/${encodeURIComponent(String(portId))}/mab/`,
            body,
            {
                withCredentials: this.configuration.withCredentials,
                headers: headers,
                observe: observe,
                reportProgress: reportProgress
            }
        );
    }

    /**
     * Update a port
     * 
     * @param portId 
     * @param port Port to update
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    public portPortIdPut(portId: number, port: Port, observe?: 'body', reportProgress?: boolean): Observable<any>;
    public portPortIdPut(portId: number, port: Port, observe?: 'response', reportProgress?: boolean): Observable<HttpResponse<any>>;
    public portPortIdPut(portId: number, port: Port, observe?: 'events', reportProgress?: boolean): Observable<HttpEvent<any>>;
    public portPortIdPut(portId: number, port: Port, observe: any = 'body', reportProgress: boolean = false ): Observable<any> {
        if (portId === null || portId === undefined) {
            throw new Error('Required parameter portId was null or undefined when calling portPortIdPut.');
        }
        if (port === null || port === undefined) {
            throw new Error('Required parameter port was null or undefined when calling portPortIdPut.');
        }

        let headers = this.defaultHeaders;

        // to determine the Accept header
        const httpHeaderAccepts: string[] = [
        ];
        const httpHeaderAcceptSelected: string | undefined = this.configuration.selectHeaderAccept(httpHeaderAccepts);
        if (httpHeaderAcceptSelected !== undefined) {
            headers = headers.set('Accept', httpHeaderAcceptSelected);
        }

        // to determine the Content-Type header
        const consumes: string[] = [
            'application/json'
        ];
        const httpContentTypeSelected: string | undefined = this.configuration.selectHeaderContentType(consumes);
        if (httpContentTypeSelected !== undefined) {
            headers = headers.set('Content-Type', httpContentTypeSelected);
        }

        return this.httpClient.put<any>(`${this.configuration.basePath}/port/${encodeURIComponent(String(portId))}`,
            port,
            {
                withCredentials: this.configuration.withCredentials,
                headers: headers,
                observe: observe,
                reportProgress: reportProgress
            }
        );
    }

    /**
     * Shutdown/enable a port
     * 
     * @param portId 
     * @param body True to open, False to shutdown
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    public portPortIdStatePut(portId: number, body: boolean, observe?: 'body', reportProgress?: boolean): Observable<any>;
    public portPortIdStatePut(portId: number, body: boolean, observe?: 'response', reportProgress?: boolean): Observable<HttpResponse<any>>;
    public portPortIdStatePut(portId: number, body: boolean, observe?: 'events', reportProgress?: boolean): Observable<HttpEvent<any>>;
    public portPortIdStatePut(portId: number, body: boolean, observe: any = 'body', reportProgress: boolean = false ): Observable<any> {
        if (portId === null || portId === undefined) {
            throw new Error('Required parameter portId was null or undefined when calling portPortIdStatePut.');
        }
        if (body === null || body === undefined) {
            throw new Error('Required parameter body was null or undefined when calling portPortIdStatePut.');
        }

        let headers = this.defaultHeaders;

        // to determine the Accept header
        const httpHeaderAccepts: string[] = [
        ];
        const httpHeaderAcceptSelected: string | undefined = this.configuration.selectHeaderAccept(httpHeaderAccepts);
        if (httpHeaderAcceptSelected !== undefined) {
            headers = headers.set('Accept', httpHeaderAcceptSelected);
        }

        // to determine the Content-Type header
        const consumes: string[] = [
            'application/json'
        ];
        const httpContentTypeSelected: string | undefined = this.configuration.selectHeaderContentType(consumes);
        if (httpContentTypeSelected !== undefined) {
            headers = headers.set('Content-Type', httpContentTypeSelected);
        }

        return this.httpClient.put<any>(`${this.configuration.basePath}/port/${encodeURIComponent(String(portId))}/state/`,
            body,
            {
                withCredentials: this.configuration.withCredentials,
                headers: headers,
                observe: observe,
                reportProgress: reportProgress
            }
        );
    }

    /**
     * Change the VLAN assigned a to port
     * 
     * @param portId 
     * @param body VLAN to assign. Set it to 1 if you want to enable authentication on the port.
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    public portPortIdVlanPut(portId: number, body: number, observe?: 'body', reportProgress?: boolean): Observable<any>;
    public portPortIdVlanPut(portId: number, body: number, observe?: 'response', reportProgress?: boolean): Observable<HttpResponse<any>>;
    public portPortIdVlanPut(portId: number, body: number, observe?: 'events', reportProgress?: boolean): Observable<HttpEvent<any>>;
    public portPortIdVlanPut(portId: number, body: number, observe: any = 'body', reportProgress: boolean = false ): Observable<any> {
        if (portId === null || portId === undefined) {
            throw new Error('Required parameter portId was null or undefined when calling portPortIdVlanPut.');
        }
        if (body === null || body === undefined) {
            throw new Error('Required parameter body was null or undefined when calling portPortIdVlanPut.');
        }

        let headers = this.defaultHeaders;

        // to determine the Accept header
        const httpHeaderAccepts: string[] = [
        ];
        const httpHeaderAcceptSelected: string | undefined = this.configuration.selectHeaderAccept(httpHeaderAccepts);
        if (httpHeaderAcceptSelected !== undefined) {
            headers = headers.set('Accept', httpHeaderAcceptSelected);
        }

        // to determine the Content-Type header
        const consumes: string[] = [
            'application/json'
        ];
        const httpContentTypeSelected: string | undefined = this.configuration.selectHeaderContentType(consumes);
        if (httpContentTypeSelected !== undefined) {
            headers = headers.set('Content-Type', httpContentTypeSelected);
        }

        return this.httpClient.put<any>(`${this.configuration.basePath}/port/${encodeURIComponent(String(portId))}/vlan/`,
            body,
            {
                withCredentials: this.configuration.withCredentials,
                headers: headers,
                observe: observe,
                reportProgress: reportProgress
            }
        );
    }

    /**
     * Create a port
     * 
     * @param port Port to create
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    public portPost(port: Port, observe?: 'body', reportProgress?: boolean): Observable<any>;
    public portPost(port: Port, observe?: 'response', reportProgress?: boolean): Observable<HttpResponse<any>>;
    public portPost(port: Port, observe?: 'events', reportProgress?: boolean): Observable<HttpEvent<any>>;
    public portPost(port: Port, observe: any = 'body', reportProgress: boolean = false ): Observable<any> {
        if (port === null || port === undefined) {
            throw new Error('Required parameter port was null or undefined when calling portPost.');
        }

        let headers = this.defaultHeaders;

        // to determine the Accept header
        const httpHeaderAccepts: string[] = [
        ];
        const httpHeaderAcceptSelected: string | undefined = this.configuration.selectHeaderAccept(httpHeaderAccepts);
        if (httpHeaderAcceptSelected !== undefined) {
            headers = headers.set('Accept', httpHeaderAcceptSelected);
        }

        // to determine the Content-Type header
        const consumes: string[] = [
            'application/json'
        ];
        const httpContentTypeSelected: string | undefined = this.configuration.selectHeaderContentType(consumes);
        if (httpContentTypeSelected !== undefined) {
            headers = headers.set('Content-Type', httpContentTypeSelected);
        }

        return this.httpClient.post<any>(`${this.configuration.basePath}/port/`,
            port,
            {
                withCredentials: this.configuration.withCredentials,
                headers: headers,
                observe: observe,
                reportProgress: reportProgress
            }
        );
    }

    /**
     * Retrieve the status of a port.
     * 
     * @param portId 
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    public stateGet(portId: number, observe?: 'body', reportProgress?: boolean): Observable<boolean>;
    public stateGet(portId: number, observe?: 'response', reportProgress?: boolean): Observable<HttpResponse<boolean>>;
    public stateGet(portId: number, observe?: 'events', reportProgress?: boolean): Observable<HttpEvent<boolean>>;
    public stateGet(portId: number, observe: any = 'body', reportProgress: boolean = false ): Observable<any> {
        if (portId === null || portId === undefined) {
            throw new Error('Required parameter portId was null or undefined when calling stateGet.');
        }

        let headers = this.defaultHeaders;

        // to determine the Accept header
        const httpHeaderAccepts: string[] = [
            'application/json'
        ];
        const httpHeaderAcceptSelected: string | undefined = this.configuration.selectHeaderAccept(httpHeaderAccepts);
        if (httpHeaderAcceptSelected !== undefined) {
            headers = headers.set('Accept', httpHeaderAcceptSelected);
        }

        // to determine the Content-Type header
        const consumes: string[] = [
        ];

        return this.httpClient.get<boolean>(`${this.configuration.basePath}/port/${encodeURIComponent(String(portId))}/state/`,
            {
                withCredentials: this.configuration.withCredentials,
                headers: headers,
                observe: observe,
                reportProgress: reportProgress
            }
        );
    }

    /**
     * Retrieve the VLAN assigned to the port.
     * 
     * @param portId 
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    public vlanGet(portId: number, observe?: 'body', reportProgress?: boolean): Observable<number>;
    public vlanGet(portId: number, observe?: 'response', reportProgress?: boolean): Observable<HttpResponse<number>>;
    public vlanGet(portId: number, observe?: 'events', reportProgress?: boolean): Observable<HttpEvent<number>>;
    public vlanGet(portId: number, observe: any = 'body', reportProgress: boolean = false ): Observable<any> {
        if (portId === null || portId === undefined) {
            throw new Error('Required parameter portId was null or undefined when calling vlanGet.');
        }

        let headers = this.defaultHeaders;

        // to determine the Accept header
        const httpHeaderAccepts: string[] = [
            'application/json'
        ];
        const httpHeaderAcceptSelected: string | undefined = this.configuration.selectHeaderAccept(httpHeaderAccepts);
        if (httpHeaderAcceptSelected !== undefined) {
            headers = headers.set('Accept', httpHeaderAcceptSelected);
        }

        // to determine the Content-Type header
        const consumes: string[] = [
        ];

        return this.httpClient.get<number>(`${this.configuration.basePath}/port/${encodeURIComponent(String(portId))}/vlan/`,
            {
                withCredentials: this.configuration.withCredentials,
                headers: headers,
                observe: observe,
                reportProgress: reportProgress
            }
        );
    }

}