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
import type { HouseholdSchema } from './HouseholdSchema';
import {
    HouseholdSchemaFromJSON,
    HouseholdSchemaFromJSONTyped,
    HouseholdSchemaToJSON,
} from './HouseholdSchema';
import type { UserSchema } from './UserSchema';
import {
    UserSchemaFromJSON,
    UserSchemaFromJSONTyped,
    UserSchemaToJSON,
} from './UserSchema';

/**
 * 
 * @export
 * @interface BodyCreateHouseholdExtOpFacadeHoushMgmtCreateHouseholdExtPost
 */
export interface BodyCreateHouseholdExtOpFacadeHoushMgmtCreateHouseholdExtPost {
    /**
     * 
     * @type {HouseholdSchema}
     * @memberof BodyCreateHouseholdExtOpFacadeHoushMgmtCreateHouseholdExtPost
     */
    householdData: HouseholdSchema;
    /**
     * 
     * @type {UserSchema}
     * @memberof BodyCreateHouseholdExtOpFacadeHoushMgmtCreateHouseholdExtPost
     */
    userData: UserSchema;
}

/**
 * Check if a given object implements the BodyCreateHouseholdExtOpFacadeHoushMgmtCreateHouseholdExtPost interface.
 */
export function instanceOfBodyCreateHouseholdExtOpFacadeHoushMgmtCreateHouseholdExtPost(value: object): value is BodyCreateHouseholdExtOpFacadeHoushMgmtCreateHouseholdExtPost {
    if (!('householdData' in value) || value['householdData'] === undefined) return false;
    if (!('userData' in value) || value['userData'] === undefined) return false;
    return true;
}

export function BodyCreateHouseholdExtOpFacadeHoushMgmtCreateHouseholdExtPostFromJSON(json: any): BodyCreateHouseholdExtOpFacadeHoushMgmtCreateHouseholdExtPost {
    return BodyCreateHouseholdExtOpFacadeHoushMgmtCreateHouseholdExtPostFromJSONTyped(json, false);
}

export function BodyCreateHouseholdExtOpFacadeHoushMgmtCreateHouseholdExtPostFromJSONTyped(json: any, ignoreDiscriminator: boolean): BodyCreateHouseholdExtOpFacadeHoushMgmtCreateHouseholdExtPost {
    if (json == null) {
        return json;
    }
    return {
        
        'householdData': HouseholdSchemaFromJSON(json['household_data']),
        'userData': UserSchemaFromJSON(json['user_data']),
    };
}

export function BodyCreateHouseholdExtOpFacadeHoushMgmtCreateHouseholdExtPostToJSON(value?: BodyCreateHouseholdExtOpFacadeHoushMgmtCreateHouseholdExtPost | null): any {
    if (value == null) {
        return value;
    }
    return {
        
        'household_data': HouseholdSchemaToJSON(value['householdData']),
        'user_data': UserSchemaToJSON(value['userData']),
    };
}

