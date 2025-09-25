import React, { useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';

const Callback: React.FC = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  useEffect(() => {
    const token = searchParams.get('token');
    if (token) {
      localStorage.setItem('auth_token', token);
      navigate('/');
    }
  }, [searchParams, navigate]);

  return <div>Processing login...</div>;
};

export default Callback;
