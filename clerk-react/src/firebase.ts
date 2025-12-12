import { initializeApp } from 'firebase/app';
import { getFirestore, doc, setDoc, serverTimestamp } from 'firebase/firestore';

const firebaseConfig = {
  apiKey: import.meta.env.VITE_FIREBASE_API_KEY,
  authDomain: import.meta.env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_FIREBASE_APP_ID,
};

if (!firebaseConfig.apiKey || !firebaseConfig.projectId) {
  // If env is missing we still allow the app to run, but writes will fail and log helpful message.
  // This avoids hard failing in development when env vars aren't set yet.
  console.warn('Firebase environment variables are missing. Set VITE_FIREBASE_* env vars to enable saving user info to Firestore.');
}

const app = initializeApp(firebaseConfig as any);
const db = getFirestore(app);

export async function saveUserToFirestore(user: any) {
  if (!user || !user.id) return;
  try {
    const userRef = doc(db, 'users', user.id);
    await setDoc(
      userRef,
      {
        id: user.id,
        email: user.email || null,
        firstName: user.firstName || null,
        lastName: user.lastName || null,
        updatedAt: serverTimestamp(),
      },
      { merge: true }
    );
  } catch (err) {
    console.error('Failed to save user to Firestore:', err);
    throw err;
  }
}

export { db };
