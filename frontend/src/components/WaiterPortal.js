import React, { useEffect, useState } from 'react';
import { api } from '../services/api';

export default function WaiterPortal({ user }) {
  const [menu, setMenu] = useState([]);
  const [categories, setCategories] = useState([]);
  const [orderItems, setOrderItems] = useState([]);
  const [guest, setGuest] = useState('');
  const [table, setTable] = useState('');
  const [created, setCreated] = useState(null);

  useEffect(() => {
    Promise.all([api.get('/menu/'), api.get('/menu/categories/')])
      .then(([menuData, catData]) => {
        setMenu(menuData);
        setCategories(catData);
      });
  }, []);

  const addItem = (item) => {
    const exists = orderItems.find(i => i.menu_item.id === item.id);
    if (exists) {
      setOrderItems(orderItems.map(i => i.menu_item.id === item.id ? {...i, quantity: i.quantity + 1} : i));
    } else {
      setOrderItems([...orderItems, {menu_item: item, menu_item_id: item.id, quantity: 1, unit_price: item.price}]);
    }
  };

  const increaseQuantity = (itemId) => {
    setOrderItems(orderItems.map(i => i.menu_item.id === itemId ? {...i, quantity: i.quantity + 1} : i));
  };

  const decreaseQuantity = (itemId) => {
    setOrderItems(orderItems.map(i => {
      if (i.menu_item.id === itemId) {
        return i.quantity > 1 ? {...i, quantity: i.quantity - 1} : i;
      }
      return i;
    }));
  };

  const removeItem = (itemId) => {
    setOrderItems(orderItems.filter(i => i.menu_item.id !== itemId));
  };

  const submit = async () => {
    // Validation
    if (!guest.trim()) {
      alert('Please enter guest name');
      return;
    }
    if (!table.trim()) {
      alert('Please enter table number');
      return;
    }
    if (orderItems.length === 0) {
      alert('Please add at least one item to the order');
      return;
    }

    try {
      const payload = {guest_name: guest, table_number: table, items: orderItems.map(i => ({menu_item_id: i.menu_item_id, quantity: i.quantity}))};
      const data = await api.post('/orders/', payload);
      setCreated(data);
      setOrderItems([]);
      setGuest('');
      setTable('');
      setTimeout(() => setCreated(null), 5000);
    } catch (error) {
      alert('Failed to create order: ' + (error.message || 'Unknown error'));
    }
  };

  const total = orderItems.reduce((sum, item) => sum + parseFloat(item.unit_price) * item.quantity, 0);

  const groupByCategory = () => {
    const grouped = {};
    categories.forEach(cat => {
      grouped[cat.id] = {...cat, items: menu.filter(item => item.category.id === cat.id)};
    });
    return Object.values(grouped);
  };

  return (
    <div>
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Create New Order</h2>
        </div>
        <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '16px'}}>
          <input className="form-input" placeholder="Guest Name" value={guest} onChange={e => setGuest(e.target.value)} />
          <input className="form-input" placeholder="Table Number" value={table} onChange={e => setTable(e.target.value)} />
        </div>

        {orderItems.length > 0 && (
          <div className="order-summary">
            <h3>Current Order</h3>
            {orderItems.map(item => (
              <div key={item.menu_item.id} style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '12px 0', borderBottom: '1px solid var(--border)'}}>
                <div style={{flex: 1}}>
                  <strong>{item.menu_item.name}</strong>
                  <div className="text-muted">₹{item.unit_price} each</div>
                </div>
                <div style={{display: 'flex', alignItems: 'center', gap: '12px'}}>
                  <div style={{display: 'flex', alignItems: 'center', gap: '8px'}}>
                    <button onClick={() => decreaseQuantity(item.menu_item.id)} className="btn-icon" title="Decrease">−</button>
                    <span style={{minWidth: '24px', textAlign: 'center', fontWeight: '600'}}>{item.quantity}</span>
                    <button onClick={() => increaseQuantity(item.menu_item.id)} className="btn-icon" title="Increase">+</button>
                  </div>
                  <div style={{minWidth: '80px', textAlign: 'right', fontWeight: '600'}}>₹{(parseFloat(item.unit_price) * item.quantity).toFixed(2)}</div>
                  <button onClick={() => removeItem(item.menu_item.id)} className="btn-icon btn-danger" title="Remove item">×</button>
                </div>
              </div>
            ))}
            <div className="order-total">
              <span>Total:</span>
              <span>₹{total.toFixed(2)}</span>
            </div>
            <button onClick={submit} className="btn btn-primary" style={{width: '100%', marginTop: '16px'}}>Submit Order</button>
          </div>
        )}

        {created && <div style={{marginTop: '16px', padding: '12px', background: '#dcfce7', borderRadius: '8px'}}>✓ Order #{created.id} created!</div>}
      </div>

      <div className="menu-categories">
        {groupByCategory().map(category => (
          <div key={category.id} className="category-section">
            <div className="category-header">
              <h2 className="category-name">{category.name}</h2>
              <p className="category-description">{category.description}</p>
            </div>
            <div className="menu-grid">
              {category.items.map(item => (
                <div key={item.id} className="menu-item-card" onClick={() => addItem(item)}>
                  <div className="menu-item-header">
                    <h3 className="menu-item-name">{item.name}</h3>
                    <span className="menu-item-price">₹{item.price}</span>
                  </div>
                  <p className="menu-item-description">{item.description}</p>
                  <div className="menu-item-badges">
                    {item.is_vegetarian && <span className="badge badge-veg">🌱 Veg</span>}
                    {item.spice_level && <span className="badge badge-spicy">🌶️ {item.spice_level}</span>}
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
