// src/App.jsx
import React, { useState } from "react";
import {
  FaBolt,
  FaWrench,
  FaHome,
  FaFan,
  FaFire,
  FaTools,
  FaPaintRoller,
  FaCouch,
  FaUserShield,
  FaCheckCircle,
  FaUserFriends,
  FaCommentDots,
  FaClock,
  FaKey,
  FaSuperpowers,

} from "react-icons/fa";

const servicios = [
  { nombre: "Electricista", icono: <FaBolt /> },
  { nombre: "Fontanero", icono: <FaWrench /> },
  { nombre: "Reformas", icono: <FaHome /> },
  { nombre: "Aire Acondicionado", icono: <FaFan /> },
  { nombre: "Calefacción", icono: <FaFire /> },
  { nombre: "Pintor", icono: <FaPaintRoller /> },
  { nombre: "Montador de muebles", icono: <FaCouch /> },
  { nombre: "Cerrajero", icono: <FaKey /> },
  { nombre: "Otros", icono: <FaTools /> },
];

export default function App() {
  const [showPopup, setShowPopup] = useState("");

  return (
    <div className="bg-gradient-to-b from-[#0F172A] to-[#1E3A8A] text-white min-h-screen font-sans">
      {/* Header */}
      <header className="flex justify-between items-center px-6 py-4">
        <div className="flex items-center gap-2">
          <FaUserShield className="text-2xl text-green-400" />
          <h1 className="text-xl font-bold">Fixhub</h1>
        </div>
        <a href="#" className="text-sm underline">¿Eres profesional?</a>
      </header>

      {/* Hero */}
      <section className="text-center py-16 px-6">
        <h2 className="text-4xl sm:text-6xl font-extrabold leading-tight">
          Encuentra tu <span className="text-transparent bg-clip-text bg-gradient-to-r from-green-400 to-blue-500">profesional de confianza</span><br /> cerca de ti
        </h2>
        <p className="mt-4 text-lg text-gray-300">Electricistas, fontaneros, pintores, instaladores de aire acondicionados, reformas, superheroes para emergencias,<br /> y más!</p>

        <div className="flex flex-col sm:flex-row gap-4 mt-8 justify-center">
          <button onClick={() => setShowPopup("pro")} className="bg-blue-600 px-6 py-3 rounded-xl hover:bg-blue-700 transition flex items-center gap-2">
            <FaWrench /> Soy profesional - Quiero ofrecer mis servicios
          </button>
          <button onClick={() => setShowPopup("cli")} className="bg-green-600 px-6 py-3 rounded-xl hover:bg-green-700 transition flex items-center gap-2">
            <FaHome /> Busco un professional - Necesito ayuda
          </button>
          <button onClic={() => setShowPopup("idk")} className="bg-red-600 px-6 py-3 rounded-xl hover:bg-red-700 transition flex items-center gap-2">
            <FaSuperpowers /> ¡Ayuda! - No se lo que necesito
          </button>

        </div>
      </section>

      {/* Popups */}
      {showPopup === "cli" && (
        <div>
          <h2 className="text-lg font-bold mb-4">¿Eres profesional?</h2>
          <form className="flex flex-col gap-3">
            <input className="border p-2 rounded" type="text" placeholder="Nombre" />
            <input className="border p-2 rounded" type="email" placeholder="Email" />
            <input className="border p-2 rounded" type="tel" placeholder="Teléfono" />
            <input className="border p-2 rounded" type="text" placeholder="Zona de trabajo" />
            <select className="border p-2 rounded">
              <option>Selecciona tu oficio</option>
              <option>Electricista</option>
              <option>Fontanero</option>
              <option>Reformas</option>
              <option>Aire acondicionado</option>
              <option>Calefacción</option>
              <option>Pintor</option>
              <option>Montador de muebles</option>
              <option>Otros</option>
            </select>
            <button className="bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition">
              Enviar
            </button>
          </form>
        </div>
      )}
      {showPopup === "pro" && (
        <div>
          <h2 className="text-lg font-bold mb-4">¿Eres profesional?</h2>
          <form className="flex flex-col gap-3">
            <input className="border p-2 rounded" type="text" placeholder="Nombre" />
            <input className="border p-2 rounded" type="email" placeholder="Email" />
            <input className="border p-2 rounded" type="tel" placeholder="Teléfono" />
            <input className="border p-2 rounded" type="text" placeholder="Zona de trabajo" />
            <select className="border p-2 rounded">
              <option>Selecciona tu oficio</option>
              <option>Electricista</option>
              <option>Fontanero</option>
              <option>Reformas</option>
              <option>Aire acondicionado</option>
              <option>Calefacción</option>
              <option>Pintor</option>
              <option>Montador de muebles</option>
              <option>Otros</option>
            </select>
            <button className="bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition">
              Enviar
            </button>
          </form>
        </div>
      )}


      {/* Servicios */}
      <section className="bg-gray-100 text-gray-900 py-12 px-4">
        <h3 className="text-2xl font-semibold text-center mb-8">Servicios Populares</h3>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-6 max-w-5xl mx-auto">
          {servicios.map(({ nombre, icono }) => (
            <div key={nombre} className="bg-white p-6 rounded-xl shadow-md text-center">
              <div className="text-3xl text-blue-500 mb-2">{icono}</div>
              <p className="font-medium">{nombre}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Cómo funciona */}
      <section className="py-16 text-center px-4">
        <h3 className="text-3xl font-bold mb-4">¿Cómo funciona?</h3>
        <p className="text-gray-300 mb-10">Conectamos clientes con profesionales en 3 simples pasos</p>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-10 max-w-5xl mx-auto">
          <div>
            <FaCommentDots className="text-4xl mx-auto text-blue-400" />
            <div className="text-blue-500 font-bold">1</div>
            <h4 className="font-semibold mt-2">Publicas tu necesidad</h4>
            <p className="text-sm text-gray-300">Describe qué necesitas, cuando y dónde</p>
          </div>
          <div>
            <FaUserFriends className="text-4xl mx-auto text-green-400" />
            <div className="text-green-500 font-bold">2</div>
            <h4 className="font-semibold mt-2">Los profesionales te contactan</h4>
            <p className="text-sm text-gray-300">Recibe ofertas de profesionales verificados de tu zona</p>
          </div>
          <div>
            <FaCheckCircle className="text-4xl mx-auto text-purple-400" />
            <div className="text-purple-500 font-bold">3</div>
            <h4 className="font-semibold mt-2">Comparas y eliges</h4>
            <p className="text-sm text-gray-300">Selecciona la mejor opción según rapidez, precio y valoraciones</p>
          </div>
        </div>
      </section>

      {/* Por qué elegirnos */}
      <section className="bg-[#1E3A8A] py-16 px-4">
        <h3 className="text-3xl font-bold text-center mb-10">¿Por qué elegirnos?</h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 max-w-6xl mx-auto">
          <div className="bg-[#0F172A] text-white p-6 rounded-xl text-center">
            <FaClock className="text-3xl mx-auto mb-2 text-blue-400" />
            <h4 className="font-semibold">Rápido</h4>
            <p className="text-sm">Encuentra profesionales en minutos</p>
          </div>
          <div className="bg-[#0F172A] text-white p-6 rounded-xl text-center">
            <FaCheckCircle className="text-3xl mx-auto mb-2 text-green-400" />
            <h4 className="font-semibold">Gratis</h4>
            <p className="text-sm">Sin costes ocultos ni comisiones</p>
          </div>
          <div className="bg-[#0F172A] text-white p-6 rounded-xl text-center">
            <FaUserFriends className="text-3xl mx-auto mb-2 text-pink-400" />
            <h4 className="font-semibold">Sin complicaciones</h4>
            <p className="text-sm">Proceso simple y directo. Sin registrarse</p>
          </div>
          <div className="bg-[#0F172A] text-white p-6 rounded-xl text-center">
            <FaUserShield className="text-3xl mx-auto mb-2 text-orange-400" />
            <h4 className="font-semibold">Profesionales verificados</h4>
            <p className="text-sm">Todos nuestros pros están verificados</p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white text-center py-6 mt-16">
        © 2025 Fixhub. Proyecto de OPOTEK. Todos los derechos reservados.
      </footer>
    </div>
  );
}
