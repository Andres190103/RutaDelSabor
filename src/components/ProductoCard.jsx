// src/components/ProductoCard.jsx
import React from 'react';

// El componente recibe "props" (propiedades). 
// Es la información del producto que le pasaremos desde App.jsx
function ProductoCard({ producto }) {
  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden border border-gray-200 hover:shadow-xl transition-shadow duration-300">
      
      {/* Sección Superior: Imagen (Si no hay imagen, mostramos un recuadro gris) */}
      <div className="h-48 bg-gray-300 w-full flex items-center justify-center">
        {producto.imagen ? (
          <img src={producto.imagen} alt={producto.nombre} className="object-cover h-full w-full" />
        ) : (
          <span className="text-gray-500 text-4xl">🌮</span>
        )}
      </div>

      {/* Sección Inferior: Detalles del producto */}
      <div className="p-5">
        <div className="flex justify-between items-start mb-2">
          <h3 className="text-xl font-bold text-gray-800 uppercase">{producto.nombre}</h3>
          <span className="bg-orange-100 text-orange-800 text-xs px-2 py-1 rounded-full font-bold uppercase">
            {producto.categoria_nombre}
          </span>
        </div>
        
        <p className="text-gray-600 text-sm mb-4 h-10 overflow-hidden">
          {producto.descripcion || "Sin descripción disponible."}
        </p>

        <div className="flex justify-between items-center mt-4 pt-4 border-t border-gray-200">
          <p className="text-2xl font-black text-green-600">
            ${producto.precio}
          </p>
          
          {/* Mostramos una etiqueta dependiendo de si está activo o no */}
          {producto.activo ? (
            <span className="text-sm font-bold text-green-600 flex items-center gap-1">
              Disponible
            </span>
          ) : (
            <span className="text-sm font-bold text-red-500 flex items-center gap-1">
              Agotado
            </span>
          )}
        </div>
      </div>
    </div>
  );
}

export default ProductoCard;