const socket = io()
document.addEventListener("DOMContentLoaded", () => {
    socket.on('panel_update', (msg) => {
        frame = `data:image/png;base64,${String.fromCharCode(...new Uint8Array(msg.frame))}`;
        document.getElementById('panel-preview').src = frame;
    });

    slider = document.getElementById('brightness-slider');
    socket.on('init', (msg) => {
        console.log(msg)
        document.getElementById('brightness-num').innerHTML = msg.value;
        slider.value = msg.value;
    });

    slider.addEventListener('input', () => {
        document.getElementById('brightness-num').innerHTML = slider.value;
        socket.emit("brightness_update", { value: slider.value });
    }, false);
});
