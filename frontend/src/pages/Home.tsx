import React from 'react';

const Home: React.FC = () => {
  const handleLogin = (provider: string) => {
    window.location.href = `http://localhost:8000/api/auth/login/${provider}`;
  };

  return (
    <div>
      <h1>Relevantic Recall</h1>
      <button onClick={() => handleLogin('google')}>Login with Google</button>
      <button onClick={() => handleLogin('github')}>Login with GitHub</button>
    </div>
  );
};

export default Home;
