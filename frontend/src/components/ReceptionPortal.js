import React, { useEffect, useState } from 'react';
import { api } from '../services/api';

export default function ReceptionPortal({ user }) {
  const [orders, setOrders] = useState([]);
  const [stats, setStats] = useState(null);
  const [billPreview, setBillPreview] = useState(null);
  const [showTables, setShowTables] = useState(false);

  const load = () => {
    Promise.all([
      api.get('/orders/'),
      api.get('/tables/stats/')
    ]).then(([ordersData, statsData]) => {
      setOrders(ordersData);
      setStats(statsData);
    });
  };

  useEffect(() => {
    load();
    const interval = setInterval(load, 5000);
    return () => clearInterval(interval);
  }, []);

  const changeStatus = (id, status) => {
    api.post(`/orders/${id}/status/`, {status}).then(load);
  };

  const previewBill = async (id) => {
    try {
      const data = await api.get(`/orders/${id}/bill/`);
      setBillPreview(data);
    } catch (error) {
      alert('Failed to generate bill preview');
    }
  };

  const closeBillPreview = () => {
    setBillPreview(null);
  };

  const printBill = () => {
    if (!billPreview) return;
    
    // Create a new window for printing
    const printWindow = window.open('', '_blank');
    printWindow.document.write(`
      <html>
        <head>
          <title>Invoice - Order #${billPreview.order.id}</title>
          <style>
            body { font-family: Arial, sans-serif; padding: 40px; }
            h1 { color: #d97706; }
            .line { margin: 10px 0; }
            .total { font-weight: bold; font-size: 18px; margin-top: 20px; }
          </style>
        </head>
        <body>
          ${billPreview.bill_text.split('\\n').map(line => `<div class="line">${line}</div>`).join('')}
          <script>window.print(); window.close();</script>
        </body>
      </html>
    `);
    printWindow.document.close();
  };

  const sendEmail = async (id) => {
    const email = prompt('Customer email:');
    if (!email) return;
    try {
      await api.post(`/orders/${id}/bill/`, {email});
      alert('Bill sent to ' + email);
    } catch (error) {
      alert('Email failed. Using console email backend - check Django console.');
    }
  };

  return (
    <div>
      {/* Statistics Dashboard */}
      {stats && (
        <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px', marginBottom: '24px'}}>
          <div className="stat-card">
            <div className="stat-value">{stats.total_tables_occupied}</div>
            <div className="stat-label">Tables Occupied</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{stats.active_orders}</div>
            <div className="stat-label">Active Orders</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{stats.closed_orders}</div>
            <div className="stat-label">Closed Orders</div>
          </div>
          <div className="stat-card">
            <div className="stat-value">{stats.total_orders}</div>
            <div className="stat-label">Total Orders</div>
          </div>
        </div>
      )}

      {/* Table View Toggle */}
      <div style={{marginBottom: '16px'}}>
        <button onClick={() => setShowTables(!showTables)} className="btn btn-ghost btn-sm">
          {showTables ? 'Show Orders' : 'Show Table View'}
        </button>
      </div>

      {/* Table View */}
      {showTables && stats && (
        <div className="card" style={{marginBottom: '24px'}}>
          <div className="card-header">
            <h2 className="card-title">Table Overview</h2>
          </div>
          <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))', gap: '16px', padding: '16px'}}>
            {Object.keys(stats.occupied_tables).length === 0 ? (
              <p style={{gridColumn: '1/-1', textAlign: 'center', color: 'var(--text-secondary)'}}>No tables occupied</p>
            ) : (
              Object.entries(stats.occupied_tables).map(([table, tableOrders]) => (
                <div key={table} className="table-card">
                  <div className="table-header">Table {table}</div>
                  <div className="table-info">
                    {tableOrders.map(order => (
                      <div key={order.id} style={{padding: '8px 0', borderBottom: '1px solid var(--border)'}}>
                        <div><strong>Order #{order.id}</strong></div>
                        <div style={{fontSize: '14px', color: 'var(--text-secondary)'}}>{order.guest_name}</div>
                        <div><span className={`status-badge status-${order.status}`}>{order.status}</span></div>
                        <div style={{fontWeight: '600', marginTop: '4px'}}>₹{order.total}</div>
                      </div>
                    ))}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      )}

      {/* Orders Table */}
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Reception - All Orders ({orders.length})</h2>
          <button onClick={load} className="btn btn-ghost btn-sm">Refresh</button>
        </div>
        <table>
          <thead>
            <tr>
              <th>Order #</th>
              <th>Guest</th>
              <th>Table</th>
              <th>Waiter</th>
              <th>Status</th>
              <th>Total</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {orders.map(o => (
              <tr key={o.id}>
                <td><strong>#{o.id}</strong></td>
                <td>{o.guest_name}</td>
                <td>{o.table_number}</td>
                <td>{o.waiter?.username || '-'}</td>
                <td>
                  <span className={`status-badge status-${o.status}`}>
                    {o.status}
                  </span>
                </td>
                <td>₹{o.total}</td>
                <td>
                  <div style={{display: 'flex', gap: '8px'}}>
                    {o.status === 'pending' && (
                      <button onClick={() => changeStatus(o.id, 'accepted')} className="btn btn-success btn-sm">Accept</button>
                    )}
                    {o.status !== 'closed' && (
                      <>
                        <button onClick={() => previewBill(o.id)} className="btn btn-secondary btn-sm">Preview Bill</button>
                        <button onClick={() => sendEmail(o.id)} className="btn btn-ghost btn-sm">Email</button>
                      </>
                    )}
                    {o.status === 'served' && (
                      <button onClick={() => changeStatus(o.id, 'closed')} className="btn btn-primary btn-sm">Close</button>
                    )}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Bill Preview Modal */}
      {billPreview && (
        <div className="modal-overlay" onClick={closeBillPreview}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Invoice Preview - Order #{billPreview.order.id}</h2>
              <button onClick={closeBillPreview} className="btn-close">×</button>
            </div>
            <div className="modal-body">
              <div className="bill-preview">
                <h3 style={{color: 'var(--primary)', marginBottom: '16px'}}>Order #{billPreview.order.id}</h3>
                <div style={{marginBottom: '8px'}}><strong>Guest:</strong> {billPreview.order.guest_name}</div>
                <div style={{marginBottom: '16px'}}><strong>Table:</strong> {billPreview.order.table_number}</div>
                <h4 style={{marginBottom: '12px'}}>Items:</h4>
                {billPreview.order.items.map((item, idx) => (
                  <div key={idx} style={{display: 'flex', justifyContent: 'space-between', padding: '8px 0', borderBottom: '1px solid var(--border)'}}>
                    <div>
                      <strong>{item.quantity} × {item.menu_item.name}</strong>
                      <div style={{fontSize: '14px', color: 'var(--text-secondary)'}}>@₹{item.unit_price}</div>
                    </div>
                    <div style={{fontWeight: '600'}}>₹{(parseFloat(item.unit_price) * item.quantity).toFixed(2)}</div>
                  </div>
                ))}
                <div style={{fontSize: '20px', fontWeight: 'bold', marginTop: '16px', padding: '12px 0', borderTop: '2px solid var(--primary)'}}>
                  <span>Total:</span>
                  <span style={{float: 'right'}}>₹{billPreview.order.total}</span>
                </div>
              </div>
            </div>
            <div className="modal-footer">
              <button onClick={printBill} className="btn btn-primary">Print Bill</button>
              <button onClick={() => sendEmail(billPreview.order.id)} className="btn btn-secondary">Send Email</button>
              <button onClick={closeBillPreview} className="btn btn-ghost">Close</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
