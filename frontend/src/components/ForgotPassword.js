import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { Mail, ArrowLeft, Send } from 'lucide-react';
import axios from 'axios';

const ForgotPassword = () => {
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(***REMOVED***);

    try {
      await axios.post('/password-reset/request', { email });
      toast.success('Reset key has been sent to your email!');
      // Navigate to reset password page with email pre-filled
      navigate('/reset-password', { state: { email } });
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to send reset email');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <Link 
          to="/login" 
          style={{ 
            display: 'inline-flex', 
            alignItems: 'center', 
            color: '#667eea', 
            textDecoration: 'none',
            marginBottom: '1.5rem',
            fontSize: '0.875rem'
          }}
        >
          <ArrowLeft size={16} style={{ marginRight: '0.5rem' }} />
          Back to Login
        </Link>

        <h1 className="auth-title">Forgot Password</h1>
        <p style={{ color: '#718096', marginBottom: '2rem', textAlign: 'center' }}>
          Enter your email address and we'll send you a reset key
        </p>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Email Address</label>
            <div style={{ position: 'relative' }}>
              <Mail 
                style={{ 
                  position: 'absolute', 
                  left: '12px', 
                  top: '50%', 
                  transform: 'translateY(-50%)', 
                  color: '#9ca3af' 
                }} 
                size={20} 
              />
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="form-input"
                style={{ paddingLeft: '40px' }}
                placeholder="your.email@example.com"
                required
              />
            </div>
          </div>

          <button
            type="submit"
            className="btn btn-primary btn-full"
            disabled={loading}
            style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}
          >
            {loading ? (
              'Sending...'
            ) : (
              <>
                <Send size={16} style={{ marginRight: '0.5rem' }} />
                Send Reset Key
              </>
            )}
          </button>
        </form>

        <div style={{ marginTop: '2rem', textAlign: 'center' }}>
          <p style={{ color: '#718096', fontSize: '0.875rem', marginBottom: '1rem' }}>
            Already have a reset key?
          </p>
          <Link 
            to="/reset-password" 
            style={{ 
              color: '#667eea', 
              textDecoration: 'none',
              fontWeight: '500'
            }}
          >
            Enter Reset Key
          </Link>
        </div>
      </div>
    </div>
  );
};

export default ForgotPassword;
