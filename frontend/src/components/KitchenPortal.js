import React, { useEffect, useState } from 'react';
import { api } from '../services/api';

export default function KitchenPortal({ user }) {
  const [orders, setOrders] = useState([]);

  const load = () => {
    api.get('/orders/').then(setOrders);
  };

  useEffect(() => {
    load();
    const interval = setInterval(load, 5000);
    return () => clearInterval(interval);
  }, []);

  const nextStatus = (o) => {
    const seq = ['pending', 'accepted', 'preparing', 'ready', 'served', 'closed'];
    const idx = seq.indexOf(o.status);
    const next = seq[Math.min(seq.length - 1, idx + 1)];
    api.post(`/orders/${o.id}/status/`, {status: next}).then(load);
  };

  const activeOrders = orders.filter(o => !['closed', 'served'].includes(o.status));

  return (
    <div className="card">
      <div className="card-header">
        <h2 className="card-title">Kitchen - Active Orders ({activeOrders.length})</h2>
        <button onClick={load} className="btn btn-ghost btn-sm">Refresh</button>
      </div>
      <table>
        <thead>
          <tr>
            <th>Order #</th>
            <th>Guest</th>
            <th>Table</th>
            <th>Status</th>
            <th>Items</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {activeOrders.map(o => (
            <tr key={o.id}>
              <td><strong>#{o.id}</strong></td>
              <td>{o.guest_name}</td>
              <td>{o.table_number}</td>
              <td>
                <span className={`status-badge status-${o.status}`}>
                  {o.status}
                </span>
              </td>
              <td>
                {o.items.map(it => (
                  <div key={it.id}>{it.quantity}x {it.menu_item.name}</div>
                ))}
              </td>
              <td>
                {o.status !== 'served' && (
                  <button onClick={() => nextStatus(o)} className="btn btn-success btn-sm">
                    Advance
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {activeOrders.length === 0 && (
        <div style={{textAlign: 'center', padding: '40px', color: 'var(--text-secondary)'}}>
          No active orders
        </div>
      )}
    </div>
  );
}
