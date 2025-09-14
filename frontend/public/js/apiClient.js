(function(global){
  async function post(endpoint, data = {}) {
    const localId = localStorage.getItem('deviceId');
    const payload = { ...data };
    if (!payload.deviceId && localId) payload.deviceId = localId;
    const res = await fetch(`/api-v1/${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    let body = null;
    try {
      body = await res.json();
    } catch (_) {
      // ignore json parse errors
    }

    if (!res.ok) {
      const message = body && body.message ? body.message : 'Request failed';
      const error = new Error(message);
      error.status = res.status;
      error.body = body;
      throw error;
    }

    return body;
  }

  global.apiClient = { post };
})(typeof window !== 'undefined' ? window : this);
