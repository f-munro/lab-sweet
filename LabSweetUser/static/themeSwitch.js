document.addEventListener('DOMContentLoaded', function () {

    function set_theme(colour) {
        document.documentElement.setAttribute('data-bs-theme', colour)
    }

    document.querySelector("#light-theme").addEventListener('click', () => set_theme("light"));
    document.querySelector("#dark-theme").addEventListener('click', () => set_theme("dark"));

});