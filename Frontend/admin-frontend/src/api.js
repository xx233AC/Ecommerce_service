export const CUSTOMER_SERVICE_URL = import.meta.env.VITE_CUSTOMER_SERVICE_URL || 'http://127.0.0.1:8000'
export const ECOMMERCE_SERVICE_URL = import.meta.env.VITE_ECOMMERCE_SERVICE_URL || 'http://127.0.0.1:8001'
export const AI_SERVICE_URL = import.meta.env.VITE_AI_SERVICE_URL || 'http://127.0.0.1:8002'

async function parseResponse(response) {
  const body = await response.json().catch(() => ({ detail: response.statusText }))
  if (!response.ok) {
    const error = new Error(typeof body.detail === 'string' ? body.detail : body.detail?.message || body.message || response.statusText)
    error.status = response.status
    throw error
  }
  return body
}

export async function login(userId) {
  const role = userId.startsWith('admin_') ? 'admin' : 'agent'
  return parseResponse(await fetch(`${ECOMMERCE_SERVICE_URL}/api/v1/auth/demo-token`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id: userId, role }),
  }))
}

export async function apiFetch(baseUrl, path, token, options = {}) {
  return parseResponse(await fetch(`${baseUrl}${path}`, {
    ...options,
    headers: { Authorization: `Bearer ${token}`, ...(options.headers || {}) },
  }))
}

export const adminApi = {
  handoffs: (token) => apiFetch(CUSTOMER_SERVICE_URL, '/api/v1/handoffs', token),
  conversation: (token, id) => apiFetch(CUSTOMER_SERVICE_URL, `/api/v1/conversations/${id}`, token),
  accept: (token, id) => apiFetch(CUSTOMER_SERVICE_URL, `/api/v1/handoffs/${id}/accept`, token, { method: 'POST' }),
  takeover: (token, id, expectedAgentId) => apiFetch(CUSTOMER_SERVICE_URL, `/api/v1/handoffs/${id}/takeover`, token, {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ expected_agent_id: expectedAgentId }),
  }),
  reply: (token, id, messageId, text) => apiFetch(CUSTOMER_SERVICE_URL, `/api/v1/handoffs/${id}/messages`, token, {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ message_id: messageId, text }),
  }),
  resolve: (token, id, resolution) => apiFetch(CUSTOMER_SERVICE_URL, `/api/v1/handoffs/${id}/resolve`, token, {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ resolution }),
  }),
  serviceMetrics: (token) => apiFetch(CUSTOMER_SERVICE_URL, '/api/v1/admin/metrics', token),
  commerceSummary: (token) => apiFetch(ECOMMERCE_SERVICE_URL, '/api/v1/admin/summary', token),
  aiMetrics: (token) => apiFetch(AI_SERVICE_URL, '/api/v1/admin/metrics', token),
  runs: (token) => apiFetch(AI_SERVICE_URL, '/api/v1/runs', token),
  run: (token, id) => apiFetch(AI_SERVICE_URL, `/api/v1/runs/${id}`, token),
  documents: (token) => apiFetch(AI_SERVICE_URL, '/api/v1/knowledge/documents', token),
  upload: async (token, file, title, category) => {
    const body = new FormData()
    body.append('file', file)
    body.append('title', title)
    body.append('category', category)
    return apiFetch(AI_SERVICE_URL, '/api/v1/knowledge/documents', token, { method: 'POST', body })
  },
  evaluate: (token) => apiFetch(AI_SERVICE_URL, '/api/v1/evaluations/run', token, { method: 'POST' }),
}

export function createRealtimeConnection(token, callbacks = {}) {
  let socket
  let stopped = false
  let retryTimer
  let heartbeatTimer
  let attempts = 0
  const websocketUrl = `${CUSTOMER_SERVICE_URL.replace(/^http/, 'ws')}/api/v1/realtime`

  const clearTimers = () => {
    window.clearTimeout(retryTimer)
    window.clearInterval(heartbeatTimer)
  }
  const connect = () => {
    if (stopped) return
    callbacks.onState?.(attempts ? 'reconnecting' : 'connecting')
    socket = new WebSocket(websocketUrl)
    socket.addEventListener('open', () => socket.send(JSON.stringify({ type: 'authenticate', token })))
    socket.addEventListener('message', (browserEvent) => {
      const event = JSON.parse(browserEvent.data)
      if (event.type === 'connected') {
        attempts = 0
        callbacks.onState?.('connected')
        heartbeatTimer = window.setInterval(() => {
          if (socket?.readyState === WebSocket.OPEN) socket.send(JSON.stringify({ type: 'ping' }))
        }, 20000)
      } else if (event.type !== 'pong') {
        callbacks.onEvent?.(event)
      }
    })
    socket.addEventListener('close', () => {
      clearTimers()
      if (stopped) return callbacks.onState?.('closed')
      callbacks.onState?.('reconnecting')
      retryTimer = window.setTimeout(connect, Math.min(1000 * (2 ** attempts++), 10000))
    })
    socket.addEventListener('error', () => socket?.close())
  }
  connect()
  return { close() { stopped = true; clearTimers(); socket?.close(1000, 'client closed') } }
}
