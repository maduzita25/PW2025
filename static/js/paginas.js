// Helpers JS para Ajax usados pelo projeto
// - fornece função para obter CSRF cookie
// - wrapper simples para POST via jQuery
// - expõe URLs via window.AppURLs (se window.URLS estiver definido, usa-o)

(function(window, $){
    'use strict';

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');

    function postJson(url, data, opts) {
        opts = opts || {};
        return $.ajax($.extend({
            url: url,
            method: 'POST',
            data: data,
            headers: {
                'X-CSRFToken': csrftoken
            }
        }, opts));
    }

    // monta objeto de URLs a partir de window.URLS ou do data-attribute #page-root
    function resolveUrls() {
        const urls = window.URLS || {};
        const root = document.getElementById('page-root');
        if (root) {
            urls.listar_voto = urls.listar_voto || root.dataset.listarVotoUrl;
            urls.ajax_votar = urls.ajax_votar || root.dataset.ajaxVotarUrl;
            urls.ajax_alterar_voto = urls.ajax_alterar_voto || root.dataset.ajaxAlterarVotoUrl;
            urls.ajax_comentario = urls.ajax_comentario || root.dataset.ajaxComentarioUrl;
        }
        return urls;
    }

    window.AppAjax = {
        post: postJson,
        urls: resolveUrls()
    };

})(window, jQuery);
