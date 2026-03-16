// src/App.jsx
import { useState, useEffect } from 'react';
import ProductoCard from './components/ProductoCard';

function App() {
  // 1. Creamos una "variable de estado" para guardar nuestros productos. 
  // Empieza como un arreglo vacío [].
  const [productos, setProductos] = useState([]);
  useEffect(() => {
    fetch('http://localhost:8000/api/productos/')
      .then(respuesta => respuesta.json())
      .then(datos => setProductos(datos))
      .catch(error => console.error("Hubo un error al conectar:", error));
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 p-8 font-sans">
      
      {/* Encabezado */}
      <header className="mb-10 text-center">
        <h1 className="text-5xl font-black text-orange-600 uppercase tracking-widest mb-2 drop-shadow-sm">
          RutaDelSabor
        </h1>
        <h2 className="text-xl text-gray-600 font-bold">Nuestro Menú</h2>
      </header>
      
      {/* Cuadrícula de Productos */}
      <div className="max-w-7xl mx-auto">
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          
          {/* Aquí usamos nuestro componente mágico. 
              Por cada producto en la lista, creamos un <ProductoCard /> */}
          {productos.map(producto => (
            <ProductoCard key={producto.id} producto={producto} />
          ))}

        </div>
      </div>

    </div>
  );
}

export default App