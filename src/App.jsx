export default function App() {
  return (
    <div className="bg-white text-gray-800">
      <header className="bg-indigo-600 text-white px-4 py-3 flex justify-between items-center">
        <div className="text-xl font-bold">Fixhub</div>
        <div>
          <a href="https://wa.me/34666666666" className="text-sm underline">¿Eres profesional?</a>
        </div>
      </header>

      <main className="text-center py-16 px-4 max-w-3xl mx-auto">
        <h1 className="text-4xl font-bold mb-4">Encuentra profesionales de confianza cerca de ti</h1>
        <p className="text-lg mb-8">Electricistas, fontaneros, reformas, y más.</p>
        <div className="flex flex-col sm:flex-row justify-center gap-4">
          <button className="bg-indigo-600 text-white px-6 py-3 rounded-lg">Soy profesional</button>
          <button className="bg-gray-200 px-6 py-3 rounded-lg">Busco ayuda</button>
        </div>
      </main>

      <section className="bg-gray-50 py-12">
        <h2 className="text-2xl font-semibold text-center mb-8">Servicios Populares</h2>
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-6 px-4 max-w-4xl mx-auto text-center">
          {["Electricista", "Fontanero", "Reformas", "Aire Acondicionado", "Calefacción", "Otros"].map(service => (
            <div key={service} className="bg-white p-4 rounded-lg shadow hover:shadow-md">
              <div className="text-lg font-medium">{service}</div>
            </div>
          ))}
        </div>
      </section>

      <footer className="bg-gray-800 text-white py-6 text-center text-sm">
        © 2025 Fixhub. Todos los derechos reservados.
      </footer>
    </div>
  );
}
