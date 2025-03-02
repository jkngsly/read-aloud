import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { Provider } from 'react-redux';  // Import the Provider from react-redux
import store from './store';  // Import your store
import './index.css'
import App from './App.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
      <Provider store={store}>  {/* Wrap your App with the Provider and pass the store */}
         <App />
      </Provider>
  </StrictMode>
)