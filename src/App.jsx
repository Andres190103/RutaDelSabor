import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from './components/Login';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        
        <Route path="/chef" element={
          <div className="p-10 text-center text-3xl font-bold text-green-700">
            ¡Bienvenido al Tablero Del Chef!
          </div>
        } />

        <Route path="/cajero" element={
          <div className="p-10 text-center text-3xl font-bold text-green-700">
            ¡Bienvenido Al Panel De Punto De Venta¡
          </div>
        } />

        <Route path="/admin" element={
          <div className="p-10 text-center text-3xl font-bold text-green-700">
           ¡Bienvenido Al Panel De Administracion! 
          </div>
        } />

        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App