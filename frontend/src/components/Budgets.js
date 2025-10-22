import React, { useState, useEffect } from 'react';
import axios from 'axios';
import toast from 'react-hot-toast';
import { useCurrency } from '../contexts/CurrencyContext';
import { Plus, Edit, Trash2, Target, AlertTriangle } from 'lucide-react';

const Budgets = () => {
  const { formatAmount } = useCurrency();
  const [budgets, setBudgets] = useState([]);
  const [loading, setLoading] = useState(***REMOVED***);
  const [showModal, setShowModal] = useState(false);
  const [editingBudget, setEditingBudget] = useState(null);

  const [formData, setFormData] = useState({
    month: new Date().getMonth() + 1,
    year: new Date().getFullYear(),
    amount: '',
    category: 'General'
  });

  const categories = ['General', 'Food', 'Transportation', 'Entertainment', 'Shopping', 'Bills', 'Healthcare'];

  useEffect(() => {
    fetchBudgets();
  }, []);

  const fetchBudgets = async () => {
    try {
      const response = await axios.get('/budgets');
      setBudgets(response.data);
    } catch (error) {
      toast.error('Failed to fetch budgets');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      if (editingBudget) {
        await axios.put(`/budgets/${editingBudget.id}`, formData);
        toast.success('Budget updated successfully');
      } else {
        await axios.post('/budgets', formData);
        toast.success('Budget created successfully');
      }
      
      setShowModal(false);
      setEditingBudget(null);
      setFormData({
        month: new Date().getMonth() + 1,
        year: new Date().getFullYear(),
        amount: '',
        category: 'General'
      });
      fetchBudgets();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to save budget');
    }
  };

  const handleEdit = (budget) => {
    setEditingBudget(budget);
    setFormData({
      month: budget.month,
      year: budget.year,
      amount: budget.amount.toString(),
      category: budget.category
    });
    setShowModal(***REMOVED***);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this budget?')) {
      try {
        await axios.delete(`/budgets/${id}`);
        toast.success('Budget deleted successfully');
        fetchBudgets();
      } catch (error) {
        toast.error('Failed to delete budget');
      }
    }
  };

  const getMonthName = (month) => {
    return new Date(2024, month - 1).toLocaleString('default', { month: 'long' });
  };

  if (loading) {
    return <div className="loading">Loading budgets...</div>;
  }

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <div>
          <h1 style={{ fontSize: '2rem', fontWeight: '700', color: '#2d3748', marginBottom: '0.5rem' }}>
            Budgets
          </h1>
          <p style={{ color: '#718096' }}>Set and manage your monthly budgets</p>
        </div>
        
        <button
          onClick={() => setShowModal(***REMOVED***)}
          className="btn btn-primary"
        >
          <Plus size={16} style={{ marginRight: '0.5rem' }} />
          Add Budget
        </button>
      </div>

      {/* Budget Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.5rem', marginBottom: '2rem' }}>
        {budgets.map((budget) => (
          <div key={budget.id} className="card">
            <div className="card-body">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                <div>
                  <h3 style={{ fontSize: '1.25rem', fontWeight: '600', color: '#2d3748' }}>
                    {getMonthName(budget.month)} {budget.year}
                  </h3>
                  <p style={{ color: '#718096', fontSize: '0.875rem' }}>
                    {budget.category} Budget
                  </p>
                </div>
                <div style={{ display: 'flex', gap: '0.5rem' }}>
                  <button
                    onClick={() => handleEdit(budget)}
                    className="btn btn-secondary"
                    style={{ padding: '0.5rem' }}
                  >
                    <Edit size={16} />
                  </button>
                  <button
                    onClick={() => handleDelete(budget.id)}
                    className="btn btn-danger"
                    style={{ padding: '0.5rem' }}
                  >
                    <Trash2 size={16} />
                  </button>
                </div>
              </div>
              
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <div style={{ fontSize: '2rem', fontWeight: '700', color: '#2d3748' }}>
                    {formatAmount(budget.amount)}
                  </div>
                  <div style={{ color: '#718096', fontSize: '0.875rem' }}>
                    Monthly limit
                  </div>
                </div>
                <div style={{ 
                  backgroundColor: '#f7fafc', 
                  padding: '0.5rem 1rem', 
                  borderRadius: '8px',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.5rem'
                }}>
                  <Target size={16} color="#667eea" />
                  <span style={{ color: '#4a5568', fontSize: '0.875rem' }}>
                    Budget Set
                  </span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {budgets.length === 0 && (
        <div className="card">
          <div className="card-body" style={{ textAlign: 'center', padding: '3rem' }}>
            <Target size={48} style={{ marginBottom: '1rem', opacity: 0.5, color: '#718096' }} />
            <h3 style={{ color: '#718096', marginBottom: '0.5rem' }}>No budgets set</h3>
            <p style={{ color: '#a0aec0' }}>Create your first budget to start tracking your spending limits</p>
          </div>
        </div>
      )}

      {/* Add/Edit Modal */}
      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3 className="modal-title">
                {editingBudget ? 'Edit Budget' : 'Add New Budget'}
              </h3>
              <button
                className="modal-close"
                onClick={() => {
                  setShowModal(false);
                  setEditingBudget(null);
                  setFormData({
                    month: new Date().getMonth() + 1,
                    year: new Date().getFullYear(),
                    amount: '',
                    category: 'General'
                  });
                }}
              >
                ×
              </button>
            </div>
            
            <form onSubmit={handleSubmit}>
              <div className="form-row">
                <div className="form-group">
                  <label className="form-label">Month</label>
                  <select
                    value={formData.month}
                    onChange={(e) => setFormData({ ...formData, month: parseInt(e.target.value) })}
                    className="form-input"
                    required
                  >
                    {Array.from({ length: 12 }, (_, i) => (
                      <option key={i + 1} value={i + 1}>
                        {getMonthName(i + 1)}
                      </option>
                    ))}
                  </select>
                </div>
                
                <div className="form-group">
                  <label className="form-label">Year</label>
                  <input
                    type="number"
                    value={formData.year}
                    onChange={(e) => setFormData({ ...formData, year: parseInt(e.target.value) })}
                    className="form-input"
                    min="2020"
                    max="2030"
                    required
                  />
                </div>
              </div>
              
              <div className="form-group">
                <label className="form-label">Amount</label>
                <input
                  type="number"
                  step="0.01"
                  min="0"
                  value={formData.amount}
                  onChange={(e) => setFormData({ ...formData, amount: e.target.value })}
                  className="form-input"
                  placeholder="0.00"
                  required
                />
              </div>
              
              <div className="form-group">
                <label className="form-label">Category</label>
                <select
                  value={formData.category}
                  onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                  className="form-input"
                >
                  {categories.map(cat => (
                    <option key={cat} value={cat}>{cat}</option>
                  ))}
                </select>
              </div>
              
              <div style={{ display: 'flex', gap: '1rem', justifyContent: 'flex-end' }}>
                <button
                  type="button"
                  onClick={() => {
                    setShowModal(false);
                    setEditingBudget(null);
                    setFormData({
                      month: new Date().getMonth() + 1,
                      year: new Date().getFullYear(),
                      amount: '',
                      category: 'General'
                    });
                  }}
                  className="btn btn-secondary"
                >
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  {editingBudget ? 'Update' : 'Add'} Budget
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default Budgets;
