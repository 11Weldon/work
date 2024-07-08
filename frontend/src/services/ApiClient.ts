import axios, { AxiosInstance, AxiosRequestConfig } from 'axios';
import { DefaultApi } from './/frontend/api/apis';


export class ApiClient {
  private axiosInstance: AxiosInstance;

  constructor(baseURL: string) {
    this.axiosInstance = axios.create({
      baseURL,
    });
  }

  private async request<T>(config: AxiosRequestConfig): Promise<T> {
    try {
      const response = await this.axiosInstance.request<T>(config);
      return response.data;
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  async createChannel(channelSchema: any): Promise<any> {
    const api = new DefaultApi(this.axiosInstance);
    const requestParams = {
      channelSchema,
    };
    return await api.createChannelOpFacadeChnMgmtCreateChannelPost(requestParams);
  }

}
