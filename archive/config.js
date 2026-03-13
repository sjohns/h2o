(function () {
    const params = new URLSearchParams(window.location.search);
    const useApiParam = params.get('useApi');
    const apiBaseParam = params.get('apiBase');

    const defaultUseApi = true;
    const defaultApiBaseUrl = 'http://127.0.0.1:8001';

    window.H2O_CONFIG = {
        USE_API: useApiParam === null ? defaultUseApi : useApiParam === '1',
        API_BASE_URL: apiBaseParam || defaultApiBaseUrl,
    };
})();
