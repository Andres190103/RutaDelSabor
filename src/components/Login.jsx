import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        setError('');

        try{
            const response = await fetch('http://localhost:8000/api/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            });
            const data = await response.json();

            if (response.ok) {
                localStorage.setItem('token', data.token);
                localStorage.setItem('rol', data.rol);
                localStorage.setItem('username', data.username);

                if(data.rol === 'Chef') {
                    navigate('/chef');
                } else if (data.rol === 'Cajero') {
                    navigate('/cajero');
                }else if (data.rol === 'Admin'){
                    navigate('/admin');
                }
            }else{
                setError('Usuario o Contraseña incorrecto')
            }
        }catch (err){
            setError('Error al conectar con el servidor, Asegurate de tener Django encendido')
        }
    };

    return (
        <div className = "min-h-screen bg-gray-200 flex items-center justify-center p-4">
            <div clsssName="bg-white p-8 rounded-xl shadow-2xl w-full max-w-md">
                <div className="text-center mb-8">
                    <h1 className="text-4xl font-black text-orange-600 uppercase tracking-widest mb-2">
                        RutaDelSabor
                    </h1>
                    <p className="font-bold text-sm">{error}</p>
                </div>

                <form onSubmit={handleLogin} className="flex flex-col gap-5">
                    {error && (
                        <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-3 rounded">
                            <p className="font-bold text-sm">{error}</p>
                        </div>
                    )}

                    <div>
                        <label className="block text-sm font-bold text-gray-700 mb-1 uppercase">Usuario</label>
                        <input
                            type="text"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            className="w-full px-4 py-3 rounded-lg border-2 border-gray-300 focus:border-orange-500 focus:ring-0 outline-none transition"
                            placeholder="Ingresa tu Usuario"
                            required
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-bold text-gray-700 mb-1 uppercase"></label>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="w-full px-4 py-3 rounded-lg border-2 border-gray-300 foucs:border-orange-500 focus:ring-0 outline-none transition"
                            placeholder="•••••••••••••••"
                            required
                        >
                        </input>
                    </div>

                    <button
                        type="submit"
                        className="w-full mt-4 bg-orange-600 hover:bg-orange-700 text-white font-bold py-4 rounded-lg shadow-lg transform active:scale-95 transition text-lg uppercase tracking-wider"
                    >
                        Entrar
                    </button>
                </form>
            </div>
        </div>
    );
}

export default Login;