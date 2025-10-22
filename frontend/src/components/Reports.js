import React, { useState, useEffect } from 'react';
import axios from 'axios';
import toast from 'react-hot-toast';
import { useCurrency } from '../contexts/CurrencyContext';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { Download, Calendar, TrendingUp, DollarSign, AlertTriangle } from 'lucide-react';
import { format, startOfMonth, endOfMonth, eachDayOfInterval } from 'date-fns';

const Reports = () => {
  const { formatAmount, currency } = useCurrency();
  const [summary, setSummary] = useState(null);
  const [expenses, setExpenses] = useState([]);
  const [loading, setLoading] = useState(***REMOVED***);
  const [selectedMonth, setSelectedMonth] = useState(new Date().getMonth() + 1);
  const [selectedYear, setSelectedYear] = useState(new Date().getFullYear());

  useEffect(() => {
    fetchReportsData();
  }, [selectedMonth, selectedYear]);

  const fetchReportsData = async () => {
    try {
      const [summaryRes, expensesRes] = await Promise.all([
        axios.get(`/expenses/summary?month=${selectedMonth}`),
        axios.get(`/expenses?month=${selectedMonth}`)
      ]);
      
      setSummary(summaryRes.data);
      setExpenses(expensesRes.data);
    } catch (error) {
      toast.error('Failed to fetch reports data');
    } finally {
      setLoading(false);
    }
  };

  const handleExport = async () => {
    try {
      const response = await axios.get('/expenses/export/csv', {
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `expenses-${selectedMonth}-${selectedYear}.csv`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      
      toast.success('Report exported successfully');
    } catch (error) {
      toast.error('Failed to export report');
    }
  };

  const getMonthName = (month) => {
    return new Date(2024, month - 1).toLocaleString('default', { month: 'long' });
  };

  const generateDailyData = () => {
    const startDate = startOfMonth(new Date(selectedYear, selectedMonth - 1));
    const endDate = endOfMonth(new Date(selectedYear, selectedMonth - 1));
    const days = eachDayOfInterval({ start: startDate, end: endDate });
    
    return days.map(day => {
      const dayExpenses = expenses.filter(expense => 
        format(new Date(expense.date), 'yyyy-MM-dd') === format(day, 'yyyy-MM-dd')
      );
      const total = dayExpenses.reduce((sum, expense) => sum + expense.amount, 0);
      
      return {
        day: format(day, 'MMM dd'),
        amount: total,
        count: dayExpenses.length
      };
    });
  };

  const pieData = summary?.category_breakdown ? 
    Object.entries(summary.category_breakdown).map(([category, amount]) => ({
      name: category,
      value: amount
    })) : [];

  const COLORS = ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe'];

  if (loading) {
    return <div className="loading">Loading reports...</div>;
  }

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <div>
          <h1 style={{ fontSize: '2rem', fontWeight: '700', color: '#2d3748', marginBottom: '0.5rem' }}>
            Reports
          </h1>
          <p style={{ color: '#718096' }}>Analyze your spending patterns and trends</p>
        </div>
        
        <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
          <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
            <Calendar size={20} color="#4a5568" />
            <select
              value={selectedMonth}
              onChange={(e) => setSelectedMonth(parseInt(e.target.value))}
              className="form-input"
              style={{ width: '120px' }}
            >
              {Array.from({ length: 12 }, (_, i) => (
                <option key={i + 1} value={i + 1}>
                  {getMonthName(i + 1)}
                </option>
              ))}
            </select>
            <input
              type="number"
              value={selectedYear}
              onChange={(e) => setSelectedYear(parseInt(e.target.value))}
              className="form-input"
              style={{ width: '80px' }}
              min="2020"
              max="2030"
            />
          </div>
          <button
            onClick={handleExport}
            className="btn btn-secondary"
          >
            <Download size={16} style={{ marginRight: '0.5rem' }} />
            Export
          </button>
        </div>
      </div>

      {/* Summary Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '1.5rem', marginBottom: '2rem' }}>
        <div className="stat-card">
          <div className="stat-header">
            <span className="stat-title">Total Spent</span>
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
            <span className="stat-title">Average Daily</span>
            <div className="stat-icon" style={{ backgroundColor: '#38a16920', color: '#38a169' }}>
              <TrendingUp size={24} />
            </div>
          </div>
          <div className="stat-value">
            {formatAmount((summary?.total_expenses || 0) / new Date(selectedYear, selectedMonth, 0).getDate())}
          </div>
          <div className="stat-change">
            Per day this month
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-header">
            <span className="stat-title">Categories</span>
            <div className="stat-icon" style={{ backgroundColor: '#f093fb20', color: '#f093fb' }}>
              <BarChart size={24} />
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

      {/* Charts */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem', marginBottom: '2rem' }}>
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Daily Spending</h3>
          </div>
          <div className="card-body">
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={generateDailyData()}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="day" />
                <YAxis />
                <Tooltip formatter={(value) => [`${currency.symbol}${value.toFixed(2)}`, 'Amount']} />
                <Bar dataKey="amount" fill="#667eea" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Spending by Category</h3>
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
                  <Tooltip formatter={(value) => [`${currency.symbol}${value.toFixed(2)}`, 'Amount']} />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <div style={{ textAlign: 'center', color: '#718096', padding: '2rem' }}>
                No data to display
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Category Breakdown Table */}
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">Category Breakdown</h3>
        </div>
        <div className="card-body">
          {Object.keys(summary?.category_breakdown || {}).length > 0 ? (
            <div className="table-container">
              <table className="table">
                <thead>
                  <tr>
                    <th>Category</th>
                    <th>Amount</th>
                    <th>Percentage</th>
                  </tr>
                </thead>
                <tbody>
                  {Object.entries(summary?.category_breakdown || {}).map(([category, amount]) => {
                    const percentage = ((amount / (summary?.total_expenses || 1)) * 100).toFixed(1);
                    return (
                      <tr key={category}>
                        <td>
                          <span style={{ 
                            backgroundColor: '#f7fafc', 
                            padding: '0.25rem 0.5rem', 
                            borderRadius: '4px', 
                            fontSize: '0.75rem',
                            color: '#4a5568'
                          }}>
                            {category}
                          </span>
                        </td>
                        <td style={{ fontWeight: '600', color: '#2d3748' }}>
                          {formatAmount(amount)}
                        </td>
                        <td>
                          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                            <div style={{ 
                              width: '60px', 
                              height: '8px', 
                              backgroundColor: '#e2e8f0', 
                              borderRadius: '4px',
                              overflow: 'hidden'
                            }}>
                              <div style={{ 
                                width: `${percentage}%`, 
                                height: '100%', 
                                backgroundColor: '#667eea',
                                transition: 'width 0.3s'
                              }} />
                            </div>
                            <span style={{ fontSize: '0.875rem', color: '#4a5568' }}>
                              {percentage}%
                            </span>
                          </div>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          ) : (
            <div style={{ textAlign: 'center', color: '#718096', padding: '2rem' }}>
              No expenses found for this month
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Reports;
