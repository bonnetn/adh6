/**
 * Adherent
 * Adherent api
 *
 * OpenAPI spec version: 1.0.0
 * 
 *
 * NOTE: This class is auto generated by the swagger code generator program.
 * https://github.com/swagger-api/swagger-codegen.git
 * Do not edit the class manually.
 *//* tslint:disable:no-unused-variable member-ordering */

import { Inject, Injectable, Optional }                      from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams,
         HttpResponse, HttpEvent }                           from '@angular/common/http';
import { CustomHttpUrlEncodingCodec }                        from '../encoder';

import { Observable }                                        from 'rxjs/Observable';

import { PaymentMethod } from '../model/paymentMethod';
import { PaymentMethodPatchRequest } from '../model/paymentMethodPatchRequest';

import { BASE_PATH, COLLECTION_FORMATS }                     from '../variables';
import { Configuration }                                     from '../configuration';


@Injectable()
export class PaymentMethodService {

    protected basePath = '/api';
    public defaultHeaders = new HttpHeaders();
    public configuration = new Configuration();

    constructor(protected httpClient: HttpClient, @Optional()@Inject(BASE_PATH) basePath: string, @Optional() configuration: Configuration) {
        if (basePath) {
            this.basePath = basePath;
        }
        if (configuration) {
            this.configuration = configuration;
            this.basePath = basePath || configuration.basePath || this.basePath;
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
     * Filter payment methods
     * 
     * @param limit Limit the number of payment methods returned in the result. Default is 100
     * @param offset Skip the first n results
     * @param terms Search terms
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    public paymentMethodGet(limit?: number, offset?: number, terms?: string, observe?: 'body', reportProgress?: boolean): Observable<Array<PaymentMethod>>;
    public paymentMethodGet(limit?: number, offset?: number, terms?: string, observe?: 'response', reportProgress?: boolean): Observable<HttpResponse<Array<PaymentMethod>>>;
    public paymentMethodGet(limit?: number, offset?: number, terms?: string, observe?: 'events', reportProgress?: boolean): Observable<HttpEvent<Array<PaymentMethod>>>;
    public paymentMethodGet(limit?: number, offset?: number, terms?: string, observe: any = 'body', reportProgress: boolean = false ): Observable<any> {




        let queryParameters = new HttpParams({encoder: new CustomHttpUrlEncodingCodec()});
        if (limit !== undefined && limit !== null) {
            queryParameters = queryParameters.set('limit', <any>limit);
        }
        if (offset !== undefined && offset !== null) {
            queryParameters = queryParameters.set('offset', <any>offset);
        }
        if (terms !== undefined && terms !== null) {
            queryParameters = queryParameters.set('terms', <any>terms);
        }

        let headers = this.defaultHeaders;

        // to determine the Accept header
        let httpHeaderAccepts: string[] = [
            'application/json'
        ];
        const httpHeaderAcceptSelected: string | undefined = this.configuration.selectHeaderAccept(httpHeaderAccepts);
        if (httpHeaderAcceptSelected != undefined) {
            headers = headers.set('Accept', httpHeaderAcceptSelected);
        }

        // to determine the Content-Type header
        const consumes: string[] = [
        ];

        return this.httpClient.get<Array<PaymentMethod>>(`${this.basePath}/payment_method/`,
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
     * Retrieve a payment method
     * 
     * @param paymentMethodId 
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    public paymentMethodPaymentMethodIdGet(paymentMethodId: number, observe?: 'body', reportProgress?: boolean): Observable<PaymentMethod>;
    public paymentMethodPaymentMethodIdGet(paymentMethodId: number, observe?: 'response', reportProgress?: boolean): Observable<HttpResponse<PaymentMethod>>;
    public paymentMethodPaymentMethodIdGet(paymentMethodId: number, observe?: 'events', reportProgress?: boolean): Observable<HttpEvent<PaymentMethod>>;
    public paymentMethodPaymentMethodIdGet(paymentMethodId: number, observe: any = 'body', reportProgress: boolean = false ): Observable<any> {

        if (paymentMethodId === null || paymentMethodId === undefined) {
            throw new Error('Required parameter paymentMethodId was null or undefined when calling paymentMethodPaymentMethodIdGet.');
        }

        let headers = this.defaultHeaders;

        // to determine the Accept header
        let httpHeaderAccepts: string[] = [
            'application/json'
        ];
        const httpHeaderAcceptSelected: string | undefined = this.configuration.selectHeaderAccept(httpHeaderAccepts);
        if (httpHeaderAcceptSelected != undefined) {
            headers = headers.set('Accept', httpHeaderAcceptSelected);
        }

        // to determine the Content-Type header
        const consumes: string[] = [
        ];

        return this.httpClient.get<PaymentMethod>(`${this.basePath}/payment_method/${encodeURIComponent(String(paymentMethodId))}`,
            {
                withCredentials: this.configuration.withCredentials,
                headers: headers,
                observe: observe,
                reportProgress: reportProgress
            }
        );
    }

    /**
     * Partially update
     * 
     * @param body New values of the payment method
     * @param paymentMethodId Name of the payment method will be updated
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    public paymentMethodPaymentMethodIdPatch(body: PaymentMethodPatchRequest, paymentMethodId: string, observe?: 'body', reportProgress?: boolean): Observable<any>;
    public paymentMethodPaymentMethodIdPatch(body: PaymentMethodPatchRequest, paymentMethodId: string, observe?: 'response', reportProgress?: boolean): Observable<HttpResponse<any>>;
    public paymentMethodPaymentMethodIdPatch(body: PaymentMethodPatchRequest, paymentMethodId: string, observe?: 'events', reportProgress?: boolean): Observable<HttpEvent<any>>;
    public paymentMethodPaymentMethodIdPatch(body: PaymentMethodPatchRequest, paymentMethodId: string, observe: any = 'body', reportProgress: boolean = false ): Observable<any> {

        if (body === null || body === undefined) {
            throw new Error('Required parameter body was null or undefined when calling paymentMethodPaymentMethodIdPatch.');
        }

        if (paymentMethodId === null || paymentMethodId === undefined) {
            throw new Error('Required parameter paymentMethodId was null or undefined when calling paymentMethodPaymentMethodIdPatch.');
        }

        let headers = this.defaultHeaders;

        // to determine the Accept header
        let httpHeaderAccepts: string[] = [
        ];
        const httpHeaderAcceptSelected: string | undefined = this.configuration.selectHeaderAccept(httpHeaderAccepts);
        if (httpHeaderAcceptSelected != undefined) {
            headers = headers.set('Accept', httpHeaderAcceptSelected);
        }

        // to determine the Content-Type header
        const consumes: string[] = [
            'application/json'
        ];
        const httpContentTypeSelected: string | undefined = this.configuration.selectHeaderContentType(consumes);
        if (httpContentTypeSelected != undefined) {
            headers = headers.set('Content-Type', httpContentTypeSelected);
        }

        return this.httpClient.patch<any>(`${this.basePath}/payment_method/${encodeURIComponent(String(paymentMethodId))}`,
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
     * Create a payment method
     * 
     * @param body Payment method to create
     * @param observe set whether or not to return the data Observable as the body, response or events. defaults to returning the body.
     * @param reportProgress flag to report request and response progress.
     */
    public paymentMethodPost(body: PaymentMethod, observe?: 'body', reportProgress?: boolean): Observable<any>;
    public paymentMethodPost(body: PaymentMethod, observe?: 'response', reportProgress?: boolean): Observable<HttpResponse<any>>;
    public paymentMethodPost(body: PaymentMethod, observe?: 'events', reportProgress?: boolean): Observable<HttpEvent<any>>;
    public paymentMethodPost(body: PaymentMethod, observe: any = 'body', reportProgress: boolean = false ): Observable<any> {

        if (body === null || body === undefined) {
            throw new Error('Required parameter body was null or undefined when calling paymentMethodPost.');
        }

        let headers = this.defaultHeaders;

        // to determine the Accept header
        let httpHeaderAccepts: string[] = [
        ];
        const httpHeaderAcceptSelected: string | undefined = this.configuration.selectHeaderAccept(httpHeaderAccepts);
        if (httpHeaderAcceptSelected != undefined) {
            headers = headers.set('Accept', httpHeaderAcceptSelected);
        }

        // to determine the Content-Type header
        const consumes: string[] = [
            'application/json'
        ];
        const httpContentTypeSelected: string | undefined = this.configuration.selectHeaderContentType(consumes);
        if (httpContentTypeSelected != undefined) {
            headers = headers.set('Content-Type', httpContentTypeSelected);
        }

        return this.httpClient.post<any>(`${this.basePath}/payment_method/`,
            body,
            {
                withCredentials: this.configuration.withCredentials,
                headers: headers,
                observe: observe,
                reportProgress: reportProgress
            }
        );
    }

}
