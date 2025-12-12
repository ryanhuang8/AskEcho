
import { SignedIn, SignedOut, SignInButton, UserButton } from '@clerk/clerk-react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './Dashboard';

export default function App() {
  return (
    <div style={{ minHeight: '100vh', width: '100vw', display: 'flex', flexDirection: 'column' }}>
      <Router>
        <nav style={{
          width: '100%',
          height: 64,
          background: 'var(--nav-bg, #fff)',
          boxShadow: '0 2px 8px rgba(0,0,0,0.04)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '0 32px',
          boxSizing: 'border-box',
          position: 'sticky',
          top: 0,
          zIndex: 10
        }}>
          <div style={{ fontWeight: 700, fontSize: '1.5rem', color: 'var(--text-color, #2d3748)', letterSpacing: '0.02em' }}>
            AskEcho
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            <SignedOut>
              <div style={{ display: 'flex', alignItems: 'center' }}>
                <SignInButton>
                  <button style={{ padding: '8px 12px', borderRadius: 8, border: 'none', background: '#2b6cb0', color: '#fff', cursor: 'pointer' }}>Sign in</button>
                </SignInButton>
              </div>
            </SignedOut>
            <SignedIn>
              <div style={{ display: 'flex', alignItems: 'center' }}>
                <UserButton />
              </div>
            </SignedIn>
          </div>
        </nav>
        <div style={{ flex: 1, width: '100%' }}>
          <Routes>
            <Route
              path="/"
              element={
                <>
                  <SignedOut>
                    <div style={{ padding: 24, width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                      <div style={{ color: '#4a5568' }}>Please sign in using the button in the navbar.</div>
                    </div>
                  </SignedOut>
                  <SignedIn>
                    <Dashboard />
                  </SignedIn>
                </>
              }
            />
          </Routes>
        </div>
      </Router>
    </div>
  );
}