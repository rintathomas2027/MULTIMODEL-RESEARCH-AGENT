const API_BASE_URL = 'http://127.0.0.1:8000/api';

class ApiClient {
  getAccessToken() {
    return localStorage.getItem('sp_access_token');
  }

  getRefreshToken() {
    return localStorage.getItem('sp_refresh_token');
  }

  setTokens(access, refresh) {
    if (access) localStorage.setItem('sp_access_token', access);
    if (refresh) localStorage.setItem('sp_refresh_token', refresh);
  }

  clearTokens() {
    localStorage.removeItem('sp_access_token');
    localStorage.removeItem('sp_refresh_token');
    localStorage.removeItem('sp_user');
  }

  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const token = this.getAccessToken();

    const headers = {
      ...options.headers,
    };

    if (token && !options.noAuth) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    if (!(options.body instanceof FormData) && !headers['Content-Type']) {
      headers['Content-Type'] = 'application/json';
    }

    let config = {
      ...options,
      headers,
    };

    if (options.body && !(options.body instanceof FormData) && typeof options.body === 'object') {
      config.body = JSON.stringify(options.body);
    }

    try {
      let response = await fetch(url, config);

      if (response.status === 401 && !options.isRetry) {
        // Try refreshing token
        const refreshed = await this.refreshToken();
        if (refreshed) {
          headers['Authorization'] = `Bearer ${this.getAccessToken()}`;
          config.headers = headers;
          config.isRetry = true;
          response = await fetch(url, config);
        } else {
          this.clearTokens();
          window.dispatchEvent(new Event('auth_expired'));
        }
      }

      const data = await response.json().catch(() => ({}));
      if (!response.ok) {
        throw new Error(data.error || data.detail || `Request failed with status ${response.status}`);
      }
      return data;
    } catch (err) {
      console.error(`API Error on ${endpoint}:`, err);
      throw err;
    }
  }

  async refreshToken() {
    const refresh = this.getRefreshToken();
    if (!refresh) return false;

    try {
      const response = await fetch(`${API_BASE_URL}/auth/token/refresh/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh }),
      });
      if (response.ok) {
        const data = await response.json();
        this.setTokens(data.access, data.refresh);
        return true;
      }
    } catch (e) {
      console.error('Token refresh failed:', e);
    }
    return false;
  }

  // Auth Methods
  async login(username, password) {
    const res = await this.request('/auth/login/', {
      method: 'POST',
      body: { username, password },
      noAuth: true,
    });
    this.setTokens(res.tokens.access, res.tokens.refresh);
    localStorage.setItem('sp_user', JSON.stringify(res.user));
    return res.user;
  }

  async register(data) {
    const res = await this.request('/auth/register/', {
      method: 'POST',
      body: data,
      noAuth: true,
    });
    this.setTokens(res.tokens.access, res.tokens.refresh);
    localStorage.setItem('sp_user', JSON.stringify(res.user));
    return res.user;
  }

  async getProfile() {
    const res = await this.request('/auth/profile/');
    localStorage.setItem('sp_user', JSON.stringify(res));
    return res;
  }

  async updateProfile(data) {
    const res = await this.request('/auth/profile/', {
      method: 'PATCH',
      body: data,
    });
    localStorage.setItem('sp_user', JSON.stringify(res));
    return res;
  }

  // Document Workspace Methods
  async getDocuments(search = '') {
    const query = search ? `?q=${encodeURIComponent(search)}` : '';
    return await this.request(`/workspace/documents/${query}`);
  }

  async uploadDocument(file, title) {
    const formData = new FormData();
    formData.append('file', file);
    if (title) formData.append('title', title);

    return await this.request('/workspace/documents/', {
      method: 'POST',
      body: formData,
    });
  }

  async deleteDocument(docId) {
    return await this.request(`/workspace/documents/${docId}/`, {
      method: 'DELETE',
    });
  }

  // RAG & AI Studio Methods
  async getChatHistory(docId) {
    return await this.request(`/workspace/documents/${docId}/chat/`);
  }

  async sendChatMessage(docId, question) {
    return await this.request(`/workspace/documents/${docId}/chat/`, {
      method: 'POST',
      body: { question },
    });
  }

  async summarizeDocument(docId, mode = 'detailed') {
    return await this.request(`/workspace/documents/${docId}/summarize/`, {
      method: 'POST',
      body: { mode },
    });
  }

  async getExplanation(docId, concept, academic_level) {
    return await this.request(`/workspace/documents/${docId}/explain/`, {
      method: 'POST',
      body: { concept, academic_level },
    });
  }

  async getPresentation(docId) {
    return await this.request(`/workspace/documents/${docId}/presentation/`, {
      method: 'POST',
    });
  }

  async getVivaQuestions(docId) {
    return await this.request(`/workspace/documents/${docId}/viva/`, {
      method: 'POST',
    });
  }

  async getFormulaCode(docId, query = '') {
    return await this.request(`/workspace/documents/${docId}/formula-code/`, {
      method: 'POST',
      body: { query },
    });
  }
}

export const api = new ApiClient();
