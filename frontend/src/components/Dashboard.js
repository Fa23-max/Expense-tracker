import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useCurrency } from '../contexts/CurrencyContext';
import { DollarSign, TrendingUp, CreditCard, AlertTriangle } from 'lucide-react';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const Dashboard = () => {
  const { formatAmount } = useCurrency();
  const [summary, setSummary] = useState(null);
  const [recentExpenses, setRecentExpenses] = useState([]);
  const [loading, setLoading] = useState(***REMOVED***);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [summaryRes, expensesRes] = await Promise.all([
        axios.get('/expenses/summary'),
        axios.get('/expenses?limit=5')
      ]);
      
      console.log('Summary response:', summaryRes.data);
      console.log('Expenses response:', expensesRes.data);
      
      // Validate responses before setting state
      if (summaryRes.data && typeof summaryRes.data === 'object' && !Array.isArray(summaryRes.data.detail)) {
        setSummary(summaryRes.data);
      } else {
        console.error('Invalid summary response:', summaryRes.data);
        setSummary({ total_expenses: 0, total_count: 0, category_breakdown: {} });
      }
      
      if (Array.isArray(expensesRes.data)) {
        setRecentExpenses(expensesRes.data);
      } else {
        console.error('Invalid expenses response:', expensesRes.data);
        setRecentExpenses([]);
      }
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      console.error('Error response:', error.response?.data);
      // Set default values on error
      setSummary({ total_expenses: 0, total_count: 0, category_breakdown: {} });
      setRecentExpenses([]);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading dashboard...</div>;
  }

  const pieData = summary?.category_breakdown ? 
    Object.entries(summary.category_breakdown).map(([category, amount]) => ({
      name: category,
      value: amount
    })) : [];

  const COLORS = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe'];

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1 className="dashboard-title">Dashboard</h1>
        <p className="dashboard-subtitle">Track your expenses and manage your budget</p>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-header">
            <span className="stat-title">Total Expenses</span>
            <div className="stat-icon" style={{ backgroundColor: '#667eea20', color: '#667eea' }}>
              <DollarSign size={24} />
            </div>
          </div>
          <div className="stat-value">{formatAmount(summary?.total_expenses || 0)}</div>
          <div className="stat-change">
            {summary?.total_count || 0} transactions
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-header">
            <span className="stat-title">This Month</span>
            <div className="stat-icon" style={{ backgroundColor: '#38a16920', color: '#38a169' }}>
              <TrendingUp size={24} />
            </div>
          </div>
          <div className="stat-value">{formatAmount(summary?.total_expenses || 0)}</div>
          <div className="stat-change">
            Current month spending
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-header">
            <span className="stat-title">Categories</span>
            <div className="stat-icon" style={{ backgroundColor: '#f093fb20', color: '#f093fb' }}>
              <CreditCard size={24} />
            </div>
          </div>
          <div className="stat-value">{Object.keys(summary?.category_breakdown || {}).length}</div>
          <div className="stat-change">
            Active categories
          </div>
        </div>

        {summary?.budget_warning && (
          <div className="stat-card" style={{ borderColor: '#e53e3e' }}>
            <div className="stat-header">
              <span className="stat-title">Budget Alert</span>
              <div className="stat-icon" style={{ backgroundColor: '#e53e3e20', color: '#e53e3e' }}>
                <AlertTriangle size={24} />
              </div>
            </div>
            <div style={{ color: '#e53e3e', fontSize: '0.875rem' }}>
              {summary.budget_warning}
            </div>
          </div>
        )}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem', marginBottom: '2rem' }}>
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Expenses by Category</h3>
          </div>
          <div className="card-body">
            {pieData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={pieData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {pieData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <div style={{ textAlign: 'center', color: '#718096', padding: '2rem' }}>
                No expenses to display
              </div>
            )}
          </div>
        </div>

        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Recent Expenses</h3>
          </div>
          <div className="card-body">
            {recentExpenses.length > 0 ? (
              <div className="table-container">
                <table className="table">
                  <thead>
                    <tr>
                      <th>Description</th>
                      <th>Amount</th>
                      <th>Category</th>
                    </tr>
                  </thead>
                  <tbody>
                    {Array.isArray(recentExpenses) && recentExpenses.map((expense) => (
                      <tr key={expense.id}>
                        <td>{expense.description}</td>
                        <td>{formatAmount(expense.amount || 0)}</td>
                        <td>
                          <span style={{ 
                            backgroundColor: '#f7fafc', 
                            padding: '0.25rem 0.5rem', 
                            borderRadius: '4px', 
                            fontSize: '0.75rem',
                            color: '#4a5568'
                          }}>
                            {expense.category}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <div style={{ textAlign: 'center', color: '#718096', padding: '2rem' }}>
                No recent expenses
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
