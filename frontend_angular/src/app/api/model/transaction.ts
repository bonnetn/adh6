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


export interface Transaction { 
    attachments?: string;
    dst: number;
    readonly id?: number;
    name: string;
    src: number;
    readonly timestamp?: Date;
    payment_method: string;
    value: number;
}

