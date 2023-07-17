const socket = io()
document.addEventListener("DOMContentLoaded", () => {
    socket.on('panel_update', (msg) => {
        frame = `data:image/png;base64,${String.fromCharCode(...new Uint8Array(msg.frame))}`;
        document.getElementById('panel-preview').src = frame;
    });

    slider = document.getElementById('brightness-slider');
    socket.on('init', (msg) => {
        document.getElementById('brightness-num').innerHTML = msg.brightness;
        slider.value = msg.brightness;
        document.getElementById('theme-select').value = msg.theme;
    });

    slider.addEventListener('input', () => {
        document.getElementById('brightness-num').innerHTML = slider.value;
    }, false);

    slider.addEventListener('change', () => {
        document.getElementById('brightness-num').innerHTML = slider.value;
        socket.emit("brightness_update", { value: slider.value });
    }, false);

    document.getElementById('display-toggle').addEventListener('click', () => {
        socket.emit('display_toggle', {});
    }), false;

    theme = document.getElementById('theme-select')
    theme.addEventListener('change', () => {
        socket.emit('theme_update', { value: theme.value });
    }), false;
});
