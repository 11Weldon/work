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
 * @interface ServicesList
 */
export interface ServicesList {
    /**
     * 
     * @type {string}
     * @memberof ServicesList
     */
    targetType: string;
    /**
     * 
     * @type {number}
     * @memberof ServicesList
     */
    targetId: number;
    /**
     * 
     * @type {string}
     * @memberof ServicesList
     */
    name: string;
    /**
     * 
     * @type {string}
     * @memberof ServicesList
     */
    type: string;
    /**
     * 
     * @type {number}
     * @memberof ServicesList
     */
    seqNum: number;
    /**
     * 
     * @type {boolean}
     * @memberof ServicesList
     */
    inheritable: boolean;
    /**
     * 
     * @type {boolean}
     * @memberof ServicesList
     */
    locked: boolean;
    /**
     * 
     * @type {{ [key: string]: string; }}
     * @memberof ServicesList
     */
    title?: { [key: string]: string; } | null;
    /**
     * 
     * @type {{ [key: string]: string; }}
     * @memberof ServicesList
     */
    descr?: { [key: string]: string; } | null;
    /**
     * 
     * @type {Array<string>}
     * @memberof ServicesList
     */
    entryIds?: Array<string> | null;
    /**
     * 
     * @type {Array<number>}
     * @memberof ServicesList
     */
    entryLsns?: Array<number> | null;
}

/**
 * Check if a given object implements the ServicesList interface.
 */
export function instanceOfServicesList(value: object): value is ServicesList {
    if (!('targetType' in value) || value['targetType'] === undefined) return false;
    if (!('targetId' in value) || value['targetId'] === undefined) return false;
    if (!('name' in value) || value['name'] === undefined) return false;
    if (!('type' in value) || value['type'] === undefined) return false;
    if (!('seqNum' in value) || value['seqNum'] === undefined) return false;
    if (!('inheritable' in value) || value['inheritable'] === undefined) return false;
    if (!('locked' in value) || value['locked'] === undefined) return false;
    return true;
}

export function ServicesListFromJSON(json: any): ServicesList {
    return ServicesListFromJSONTyped(json, false);
}

export function ServicesListFromJSONTyped(json: any, ignoreDiscriminator: boolean): ServicesList {
    if (json == null) {
        return json;
    }
    return {
        
        'targetType': json['targetType'],
        'targetId': json['targetId'],
        'name': json['name'],
        'type': json['type'],
        'seqNum': json['seqNum'],
        'inheritable': json['inheritable'],
        'locked': json['locked'],
        'title': json['title'] == null ? undefined : json['title'],
        'descr': json['descr'] == null ? undefined : json['descr'],
        'entryIds': json['entryIds'] == null ? undefined : json['entryIds'],
        'entryLsns': json['entryLsns'] == null ? undefined : json['entryLsns'],
    };
}

export function ServicesListToJSON(value?: ServicesList | null): any {
    if (value == null) {
        return value;
    }
    return {
        
        'targetType': value['targetType'],
        'targetId': value['targetId'],
        'name': value['name'],
        'type': value['type'],
        'seqNum': value['seqNum'],
        'inheritable': value['inheritable'],
        'locked': value['locked'],
        'title': value['title'],
        'descr': value['descr'],
        'entryIds': value['entryIds'],
        'entryLsns': value['entryLsns'],
    };
}

