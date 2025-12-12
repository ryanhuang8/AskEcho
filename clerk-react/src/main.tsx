import { StrictMode } from 'react'
  import { createRoot } from 'react-dom/client'
  import './index.css'
  import App from './App.tsx'
  import { ClerkProvider } from '@clerk/clerk-react'

  // Import your Publishable Key
  const PUBLISHABLE_KEY = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY


  if (!PUBLISHABLE_KEY) {
    document.getElementById('root')!.innerHTML = '<div style="padding:2em;color:red;font-weight:bold">Missing Clerk Publishable Key. Check your .env file and restart the dev server.</div>';
    throw new Error('Add your Clerk Publishable Key to the .env file');
  }

  createRoot(document.getElementById('root')!).render(
    <StrictMode>
      <ClerkProvider publishableKey={PUBLISHABLE_KEY}>
        <App />
      </ClerkProvider>
    </StrictMode>,
  )