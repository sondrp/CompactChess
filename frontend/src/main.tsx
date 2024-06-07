import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { RouterProvider, createBrowserRouter } from 'react-router-dom'
import GamePage from './pages/GamePage.tsx'
import SelectUsernamePage from './pages/SelectUsernamePage.tsx'
import UserPage from './pages/UserPage.tsx'

const queryClient = new QueryClient()
const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    children: [
      {
        path: '/',
        element: <SelectUsernamePage />
      },
      {
        path: '/:username',
        element: <UserPage />
      },
      {
        path: '/:username/:id',
        element: <GamePage />
      }

    ]
  },
])

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  </React.StrictMode>,
)
