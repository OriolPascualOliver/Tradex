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
  FaMapMarkerAlt,
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
  const [formData, setFormData] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleCheckboxChange = (e) => {
    const { value, checked } = e.target;
    setSelectedOficios((prev) =>
      checked ? [...prev, value] : prev.filter((v) => v !== value)
    );
  };

  const getLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(async (position) => {
        const { latitude, longitude } = position.coords;
        try {
          const res = await fetch(
            `https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}`
          );
          const data = await res.json();
          const direccion = data.display_name || `${latitude}, ${longitude}`;
          setFormData((prev) => ({ ...prev, ubicacion: direccion }));
        } catch {
          setFormData((prev) => ({ ...prev, ubicacion: `${latitude}, ${longitude}` }));
        }
      });
    } else {
      alert("Geolocalización no soportada por tu navegador.");
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const sheetMap = {
      pro: "Profesionales",
      cli: "Clientes",
      idk: "Indefinidos",
    };
  const scriptURL = `https://script.google.com/macros/s/AKfycbzf2so3sSLeUXvvxmKNECizTK7pVz1d7Ha3E1OOKIEabKxZ8F-3lqQ4KYyoy014OwuR9Q/exec?sheet=${sheetMap[showPopup]}`;
  const form = new FormData();
    for (const field in formData) {
      form.append(field, formData[field]);
    }
    try {
      await fetch(scriptURL, { method: "POST", body: form });
      alert("Formulario enviado correctamente");
      setFormData({});
      setShowPopup("");
    } catch (error) {
      alert("Error al enviar formulario,", error);
    }
  };

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
      {showPopup && (
        <div className="fixed inset-0 bg-black bg-opacity-60 flex justify-center items-center z-50">
          <div className="bg-white text-black p-8 rounded-xl shadow-xl w-96 relative overflow-auto max-h-[90vh]">
            <button className="absolute top-2 right-3 text-xl" onClick={() => setShowPopup("")}>×</button>
            <form onSubmit={handleSubmit} className="flex flex-col gap-3">
              {showPopup === "pro" && (
                <>
                  <h2 className="text-lg font-bold mb-2">¿Eres profesional?</h2>
                  <input name="nombre" type="text" placeholder="Tu nombre completo" className="border p-2 rounded" value={formData.nombre || ""} onChange={handleChange} required />
                  <input name="email" type="email" placeholder="Correo electrónico" className="border p-2 rounded" value={formData.email || ""} onChange={handleChange} required />
                  <input name="telefono" type="tel" placeholder="Teléfono de contacto" className="border p-2 rounded" value={formData.telefono || ""} onChange={handleChange} required />
                  <input name="ubicacion" type="text" placeholder="Ubicación o código postal" className="border p-2 rounded" value={formData.ubicacion || ""} onChange={handleChange} required />
                  <label className="text-sm">Distancia máxima de desplazamiento: {formData.distancia || 25} km</label>
                  <input name="distancia" type="range" min="1" max="100" value={formData.distancia || 25} onChange={handleChange} className="w-full" />
                  <label className="text-sm font-medium">Selecciona tus oficios:</label>
                  <div className="grid grid-cols-2 gap-2">
                    {servicios.map(({ nombre }) => (
                      <label key={nombre} className="flex items-center gap-2">
                        <input
                          type="checkbox"
                          value={nombre}
                          checked={selectedOficios.includes(nombre)}
                          onChange={handleCheckboxChange}
                        />
                        {nombre}
                      </label>
                    ))}
                  </div>
                </>
              )}

            <form onSubmit={handleSubmit} className="flex flex-col gap-3">
              {showPopup === "cli" && (
                <>
                  <h2 className="text-lg font-bold mb-2">Necesito ayuda profesional</h2>
                  <input name="nombre" type="text" placeholder="Tu nombre completo" className="border p-2 rounded" value={formData.nombre || ""} onChange={handleChange} required />
                  <input name="email" type="email" placeholder="Correo electrónico" className="border p-2 rounded" value={formData.email || ""} onChange={handleChange} required />
                  <input name="telefono" type="tel" placeholder="Teléfono de contacto" className="border p-2 rounded" value={formData.telefono || ""} onChange={handleChange} required />

                  <div className="flex gap-2 items-center">
                    <input name="ubicacion" type="text" placeholder="Dirección o zona" className="border p-2 rounded w-full" value={formData.ubicacion || ""} onChange={handleChange} required />
                    <button type="button" onClick={getLocation} className="text-blue-600 text-sm underline">Usar mi ubicación</button>
                  </div>

                  <input name="fecha" type="date" className="border p-2 rounded" value={formData.fecha || ""} onChange={handleChange} />

                  <textarea name="descripcion" placeholder="Describe el problema lo mejor que puedas..." className="border p-2 rounded" rows="4" value={formData.descripcion || ""} onChange={handleChange} />

                  <select name="tipoProfesional" className="border p-2 rounded" value={formData.tipoProfesional || ""} onChange={handleChange}>
                    <option value="">Selecciona un tipo de profesional</option>
                    {servicios.map(({ nombre }) => (
                      <option key={nombre} value={nombre}>{nombre}</option>
                    ))}
                  </select>

                  <input name="fotos" type="file" accept="image/*" capture="environment" className="border p-2 rounded" multiple onChange={(e) => setFormData((prev) => ({ ...prev, fotos: e.target.files[0] }))} />
                </>
              )}             
              {showPopup === "idk" && (
                <>
                  <h2 className="text-lg font-bold mb-2">Ayuda general</h2>
                  <input name="nombre" type="text" placeholder="Nombre" className="border p-2 rounded" value={formData.nombre || ""} onChange={handleChange} required />
                  <input name="email" type="email" placeholder="Email" className="border p-2 rounded" value={formData.email || ""} onChange={handleChange} required />
                  <input name="telefono" type="tel" placeholder="Teléfono" className="border p-2 rounded" value={formData.telefono || ""} onChange={handleChange} required />
                  <input name="ubicacion" type="text" placeholder="Ubicación" className="border p-2 rounded" value={formData.ubicacion || ""} onChange={handleChange} required />
                  <textarea name="descripcion" placeholder="Explica lo mejor que puedas la situación" className="border p-2 rounded" rows="4" value={formData.descripcion || ""} onChange={handleChange}></textarea>
                  <input name="media" type="file" accept="image/*,video/*" multiple className="border p-2 rounded" />
                  <label className="flex items-center gap-2 text-sm">
                    <input type="checkbox" name="urgente" onChange={(e) => setFormData(prev => ({ ...prev, urgente: e.target.checked }))} /> Es urgente
                  </label>
                  {!formData.urgente && (
                    <input name="fecha" type="date" className="border p-2 rounded" value={formData.fecha || ""} onChange={handleChange} />
                  )}
                </>
              )}
              <button type="submit" className="bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition">Enviar</button>
            </form>
          </div>
        </div>
      }

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
