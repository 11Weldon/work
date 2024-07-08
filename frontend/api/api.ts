import {DefaultApi} from './apis';
import {Configuration} from '../runtime'

const apiClient = new DefaultApi(new Configuration({ basePath: 'http://localhost:8000' }));

