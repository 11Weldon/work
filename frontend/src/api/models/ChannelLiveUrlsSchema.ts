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
 * @interface ChannelLiveUrlsSchema
 */
export interface ChannelLiveUrlsSchema {
    /**
     * 
     * @type {number}
     * @memberof ChannelLiveUrlsSchema
     */
    channelId: number;
    /**
     * 
     * @type {Array<{ [key: string]: string; }>}
     * @memberof ChannelLiveUrlsSchema
     */
    channelUrls?: Array<{ [key: string]: string; }> | null;
}

/**
 * Check if a given object implements the ChannelLiveUrlsSchema interface.
 */
export function instanceOfChannelLiveUrlsSchema(value: object): value is ChannelLiveUrlsSchema {
    if (!('channelId' in value) || value['channelId'] === undefined) return false;
    return true;
}

export function ChannelLiveUrlsSchemaFromJSON(json: any): ChannelLiveUrlsSchema {
    return ChannelLiveUrlsSchemaFromJSONTyped(json, false);
}

export function ChannelLiveUrlsSchemaFromJSONTyped(json: any, ignoreDiscriminator: boolean): ChannelLiveUrlsSchema {
    if (json == null) {
        return json;
    }
    return {
        
        'channelId': json['channelId'],
        'channelUrls': json['channelUrls'] == null ? undefined : json['channelUrls'],
    };
}

export function ChannelLiveUrlsSchemaToJSON(value?: ChannelLiveUrlsSchema | null): any {
    if (value == null) {
        return value;
    }
    return {
        
        'channelId': value['channelId'],
        'channelUrls': value['channelUrls'],
    };
}

