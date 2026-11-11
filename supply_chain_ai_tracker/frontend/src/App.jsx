import React, { useEffect, useState } from 'react';
import LiveTransitMap from './components/LiveTransitMap';
import ExtractedDataGrid from './components/ExtractedDataGrid';
import { fetchShipments, fetchEntities, uploadDocument } from './api';

function App() {
  const [shipments, setShipments] = useState([]);
  const [entities, setEntities] = useState([]);

  useEffect(() => {
    // Initial load
    fetchShipments().then(setShipments).catch(console.error);
    fetchEntities().then(setEntities).catch(console.error);
  }, []);

  const handleUpload = async (e) => {
    e.preventDefault();
    const text = e.target.elements.text.value;
    if (!text) return;
    const res = await uploadDocument({ text });
    if (res.status === 'success') {
      setEntities((prev) => [...prev, res.entity]);
    }
    e.target.reset();
  };

  return (
    <div className="min-h-screen p-4 bg-gray-900 text-white">
      <h1 className="text-3xl font-bold mb-4 text-center">GenAI Supply Chain Tracker</h1>
      <section className="mb-8">
        <LiveTransitMap shipments={shipments} />
      </section>
      <section className="mb-8">
        <h2 className="text-2xl mb-2">Extracted Document Entities</h2>
        <form onSubmit={handleUpload} className="mb-4">
          <textarea name="text" rows={3} className="w-full p-2 rounded" placeholder="Paste unstructured logistics text..." required></textarea>
          <button type="submit" className="mt-2 px-4 py-2 bg-blue-600 rounded hover:bg-blue-500">Upload & Extract</button>
        </form>
        <ExtractedDataGrid entities={entities} />
      </section>
    </div>
  );
}

export default App;
