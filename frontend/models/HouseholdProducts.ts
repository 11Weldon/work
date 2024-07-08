/* tslint:disable */
/* eslint-disable */
/**
 * Your API Title
 * This is a very cool project
 *
 * The version of the OpenAPI document: 1.0.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */

import { mapValues } from '../runtime';
/**
 * 
 * @export
 * @interface HouseholdProducts
 */
export interface HouseholdProducts {
    /**
     * 
     * @type {number}
     * @memberof HouseholdProducts
     */
    householdId: number;
    /**
     * 
     * @type {Array<number>}
     * @memberof HouseholdProducts
     */
    productIds: Array<number>;
}

/**
 * Check if a given object implements the HouseholdProducts interface.
 */
export function instanceOfHouseholdProducts(value: object): value is HouseholdProducts {
    if (!('householdId' in value) || value['householdId'] === undefined) return false;
    if (!('productIds' in value) || value['productIds'] === undefined) return false;
    return true;
}

export function HouseholdProductsFromJSON(json: any): HouseholdProducts {
    return HouseholdProductsFromJSONTyped(json, false);
}

export function HouseholdProductsFromJSONTyped(json: any, ignoreDiscriminator: boolean): HouseholdProducts {
    if (json == null) {
        return json;
    }
    return {
        
        'householdId': json['householdId'],
        'productIds': json['productIds'],
    };
}

export function HouseholdProductsToJSON(value?: HouseholdProducts | null): any {
    if (value == null) {
        return value;
    }
    return {
        
        'householdId': value['householdId'],
        'productIds': value['productIds'],
    };
}

