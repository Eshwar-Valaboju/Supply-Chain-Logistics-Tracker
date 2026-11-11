import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
});

export const fetchShipments = async () => {
  const resp = await api.get('/api/shipments/');
  return resp.data;
};

export const fetchEntities = async () => {
  const resp = await api.get('/api/documents/entities');
  return resp.data;
};

export const uploadDocument = async (payload) => {
  const resp = await api.post('/api/documents/upload', payload);
  return resp.data;
};
