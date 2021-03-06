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


export interface MembershipRequest { 
    /**
     * Duration in days
     */
    duration: number;
    paymentMethod?: MembershipRequest.PaymentMethodEnum;
}
export namespace MembershipRequest {
    export type PaymentMethodEnum = 'cash' | 'card' | 'bank_cheque';
    export const PaymentMethodEnum = {
        Cash: 'cash' as PaymentMethodEnum,
        Card: 'card' as PaymentMethodEnum,
        BankCheque: 'bank_cheque' as PaymentMethodEnum
    };
}

