import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useCurrency } from '../contexts/CurrencyContext';
import { 
  Home, 
  CreditCard, 
  Target, 
  BarChart3, 
  LogOut, 
  User,
  DollarSign
} from 'lucide-react';

const Navbar = () => {
  const { user, logout } = useAuth();
  const { currency, setCurrency, currencies } = useCurrency();
  const location = useLocation();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const navItems = [
    { path: '/', icon: Home, label: 'Dashboard' },
    { path: '/expenses', icon: CreditCard, label: 'Expenses' },
    { path: '/budgets', icon: Target, label: 'Budgets' },
    { path: '/reports', icon: BarChart3, label: 'Reports' },
  ];

  return (
    <nav className="navbar">
      <div className="nav-brand">
        <h1>💰 Expense Tracker</h1>
      </div>
      
      <ul className="nav-menu">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = location.pathname === item.path;
          
          return (
            <li key={item.path} className="nav-item">
              <Link
                to={item.path}
                className={`nav-link ${isActive ? 'active' : ''}`}
              >
                <Icon />
                {item.label}
              </Link>
            </li>
          );
        })}
      </ul>
      
      <div className="nav-user">
        <div className="currency-selector" style={{ marginBottom: '1rem' }}>
          <label style={{ 
            display: 'flex', 
            alignItems: 'center', 
            fontSize: '0.875rem', 
            color: '#718096',
            marginBottom: '0.5rem'
          }}>
            <DollarSign size={16} style={{ marginRight: '0.5rem' }} />
            Currency
          </label>
          <select
            value={currency.code}
            onChange={(e) => {
              const selected = currencies.find(c => c.code === e.target.value);
              setCurrency(selected);
            }}
            style={{
              width: '100%',
              padding: '0.5rem',
              borderRadius: '6px',
              border: '1px solid #e2e8f0',
              fontSize: '0.875rem',
              backgroundColor: 'white',
              cursor: 'pointer'
            }}
          >
            {currencies.map((curr) => (
              <option key={curr.code} value={curr.code}>
                {curr.symbol} {curr.code} - {curr.name}
              </option>
            ))}
          </select>
        </div>

        <div 
          className="user-info" 
          onClick={() => navigate('/profile')}
          style={{ cursor: 'pointer', transition: 'all 0.2s' }}
          onMouseEnter={(e) => e.currentTarget.style.backgroundColor = 'rgba(255, 255, 255, 0.1)'}
          onMouseLeave={(e) => e.currentTarget.style.backgroundColor = 'transparent'}
        >
          <div className="user-avatar">
            <User size={20} />
          </div>
          <div className="user-details">
            <h3>{user?.full_name || 'User'}</h3>
            <p>{user?.email || 'user@example.com'}</p>
          </div>
        </div>
        
        <button
          onClick={handleLogout}
          className="btn btn-secondary"
          style={{ width: '100%' }}
        >
          <LogOut size={16} style={{ marginRight: '0.5rem' }} />
          Logout
        </button>
      </div>
    </nav>
  );
};

export default Navbar;
