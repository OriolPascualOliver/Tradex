// src/components/NewsletterModal.jsx
import React, { useEffect, useState, useRef } from "react";

export default function NewsletterModal({
  scriptURL = "",                  // tu endpoint (Apps Script, Mailchimp, etc.)
  delayMs = 1500,                  // retraso antes de mostrar (ms)
  storageKey = "nlDismissed_v1",   // clave en localStorage
}) {
  const [open, setOpen] = useState(false);
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [ok, setOk] = useState(false);
  const dialogRef = useRef(null);

  useEffect(() => {
    if (!localStorage.getItem(storageKey)) {
      const t = setTimeout(() => setOpen(true), delayMs);
      return () => clearTimeout(t);
    }
  }, [delayMs, storageKey]);

  useEffect(() => {
    function onKey(e) { if (e.key === "Escape") setOpen(false); }
    if (open) window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open]);

  const close = () => {
    localStorage.setItem(storageKey, "1");
    setOpen(false);
  };

  const handleBackdrop = (e) => {
    if (e.target === dialogRef.current) close();
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!/^\S+@\S+\.\S+$/.test(email)) return alert("Introduce un email válido");
    try {
      setLoading(true);
      if (!scriptURL) {
        // ejemplo local (sin backend): simular envío
        await new Promise(r => setTimeout(r, 800));
      } else {
        const form = new FormData();
        form.append("email", email);
        form.append("origen", "newsletter");
        await fetch(scriptURL, { method: "POST", body: form });
      }
      setOk(true);
      localStorage.setItem(storageKey, "1"); // no mostrar de nuevo
    } catch (err) {
      alert("No se ha podido registrar el email. Inténtalo más tarde.");
    } finally {
      setLoading(false);
    }
  };

  if (!open) return null;

  return (
    <div
      ref={dialogRef}
      onClick={handleBackdrop}
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60"
      aria-modal="true" role="dialog"
    >
      <div className="w-[92%] max-w-md rounded-2xl bg-white p-6 shadow-xl">
        <button
          onClick={close}
          className="float-right text-2xl leading-none text-gray-400 hover:text-gray-600"
          aria-label="Cerrar"
        >
          ×
        </button>

        {!ok ? (
          <>
            <h3 className="mb-2 text-xl font-bold text-gray-900">
              ¡Apúntate a la newsletter!
            </h3>
            <p className="mb-4 text-sm text-gray-600">
              Novedades de Fixhub, lanzamientos y ofertas locales. Sin spam.
            </p>

            <form onSubmit={handleSubmit} className="flex flex-col gap-3">
              <input
                type="email"
                value={email}
                onChange={(e)=>setEmail(e.target.value)}
                placeholder="tu@email.com"
                className="w-full rounded-lg border border-gray-300 p-3 focus:border-blue-500 focus:outline-none"
                required
              />
              <label className="flex items-start gap-2 text-xs text-gray-600">
                <input type="checkbox" required className="mt-1"/>
                Acepto las{" "}
                <a href="/Tradex/condiciones.html" target="_blank" rel="noopener noreferrer"
                   className="text-blue-600 underline">
                  condiciones
                </a>{" "}
                y la política de privacidad.
              </label>

              <button
                type="submit"
                disabled={loading}
                className="rounded-lg bg-blue-600 px-4 py-2 font-medium text-white hover:bg-blue-700 disabled:opacity-60"
              >
                {loading ? "Enviando..." : "Quiero apuntarme"}
              </button>

              <button
                type="button"
                onClick={close}
                className="text-sm text-gray-500 underline"
              >
                No, gracias
              </button>
            </form>
          </>
        ) : (
          <div className="py-8 text-center">
            <h3 className="mb-2 text-xl font-bold text-gray-900">¡Listo!</h3>
            <p className="mb-4 text-sm text-gray-600">
              Te hemos apuntado. Revisa tu correo (puede que pida confirmar).
            </p>
            <button
              onClick={close}
              className="rounded-lg bg-blue-600 px-4 py-2 font-medium text-white hover:bg-blue-700"
            >
              Cerrar
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
