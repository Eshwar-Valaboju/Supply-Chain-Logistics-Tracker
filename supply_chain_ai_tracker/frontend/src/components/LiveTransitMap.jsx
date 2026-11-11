import React, { useEffect, useState } from 'react';

function LiveTransitMap({ shipments }) {
  const [updates, setUpdates] = useState([]);

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws/transit');
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        setUpdates((prev) => [...prev, data]);
      } catch (_) {}
    };
    ws.onerror = (e) => console.error('WebSocket error', e);
    return () => ws.close();
  }, []);

  // Merge live updates with initial shipments list (simple concat)
  const allShipments = [...shipments, ...updates];

  return (
    <div className="overflow-x-auto rounded border border-gray-700">
      <h2 className="text-xl font-semibold p-2 bg-gray-800">Live Transit Feed</h2>
      <table className="min-w-full text-sm">
        <thead className="bg-gray-800">
          <tr>
            <th className="p-2 text-left">Shipment ID</th>
            <th className="p-2 text-left">Lat</th>
            <th className="p-2 text-left">Lng</th>
            <th className="p-2 text-left">Status</th>
            <th className="p-2 text-left">Timestamp</th>
          </tr>
        </thead>
        <tbody>
          {allShipments.map((s, i) => (
            <tr key={i} className="border-b border-gray-700">
              <td className="p-2">{s.shipment_id}</td>
              <td className="p-2">{s.lat?.toFixed(3)}</td>
              <td className="p-2">{s.lng?.toFixed(3)}</td>
              <td className="p-2">{s.status}</td>
              <td className="p-2">{new Date(s.timestamp).toLocaleTimeString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default LiveTransitMap;
