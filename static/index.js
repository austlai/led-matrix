const socket = io()
document.addEventListener("DOMContentLoaded", () => {
    socket.on('panel_update', (msg) => {
        frame = `data:image/png;base64,${String.fromCharCode(...new Uint8Array(msg.frame))}`;
        document.getElementById('panel-preview').src = frame;
    });

    const slider = document.getElementById('brightness-slider');
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

    const theme = document.getElementById('theme-select')
    theme.addEventListener('change', () => {
        socket.emit('theme_update', { value: theme.value });
    }), false;

    const grid = document.getElementById("grid");
    const submitBtn = document.getElementById("submit-btn");
    const clearBtn = document.getElementById("clear-btn");
    const colourInput = document.getElementById("colour-input");
    const eraseBtn = document.getElementById("erase-btn");
    const paintBtn = document.getElementById("paint-btn");
    const fillBtn = document.getElementById("fill-btn");
    const width = 64;
    const height = 32;

    let fillColour = '#FFF';

    let events = {
        mouse: {
            down: "mousedown",
            move: "mousemove",
            up: "mouseup",
        },
        touch: {
            down: "touchstart",
            move: "touchmove",
            up: "touchend",
        },
    };
    let deviceType = "";
    let draw = false;
    let erase = false;
    const isTouchDevice = () => {
        try {
            document.createEvent("TouchEvent");
            deviceType = "touch";
            return true;
        } catch (e) {
            deviceType = "mouse";
            return false;
        }
    };
    isTouchDevice();

    // Build Grid
    for (let i = 0; i < height; i++) {
        let div = document.createElement("div");
        div.classList.add("gridRow");
        for (let j = 0; j < width; j++) {
            let col = document.createElement("div");
            col.classList.add("gridCol");
            col.setAttribute("id", `grid-${j}-${i}`);
            col.style.backgroundColor = "#000";
            col.addEventListener(events[deviceType].down, () => {
                draw = true;
                if (erase) {
                    col.style.backgroundColor = fillColour;
                } else {
                    col.style.backgroundColor = colourInput.value;
                }
            });
            col.addEventListener(events[deviceType].move, (e) => {
                let elementId = document.elementFromPoint(
                    !isTouchDevice() ? e.clientX : e.touches[0].clientX,
                    !isTouchDevice() ? e.clientY : e.touches[0].clientY
                ).id;
                checker(elementId);
            });
            col.addEventListener(events[deviceType].up, () => {
                draw = false;
            });
            div.appendChild(col);
        }
        grid.appendChild(div);
    }

    function checker(elementId) {
        let gridColumns = document.querySelectorAll(".gridCol");
        gridColumns.forEach((element) => {
            if (elementId == element.id) {
                if (draw && !erase) {
                    element.style.backgroundColor = colourInput.value;
                } else if (draw && erase) {
                    element.style.backgroundColor = "transparent";
                }
            }
        });
    }

    function updateDark(hexcolor){
        var r = parseInt(hexcolor.substr(1,2),16);
        var g = parseInt(hexcolor.substr(3,2),16);
        var b = parseInt(hexcolor.substr(4,2),16);
        var yiq = ((r*299)+(g*587)+(b*114))/1000;
        let gridColumns = document.querySelectorAll(".gridCol");
        gridColumns.forEach((element) => {
            if (yiq < 40) {
                element.style.borderColor = '#222'
            } else {
                element.style.borderColor = '#ddd'
            }
        });
    }

    clearBtn.addEventListener("click", () => {
        for (let i = 0; i < height; i++) {
            for (let j = 0; j < width; j++) {
                document.getElementById(`grid-${j}-${i}`).style.backgroundColor = fillColour
            }
        }
    });

    eraseBtn.addEventListener("click", () => {
        erase = true;
    });

    paintBtn.addEventListener("click", () => {
        erase = false;
    });

    fillBtn.addEventListener("click", () => {
        fillColour = colourInput.value
        updateDark(fillColour)
        for (let i = 0; i < height; i++) {
            for (let j = 0; j < width; j++) {
                document.getElementById(`grid-${j}-${i}`).style.backgroundColor = fillColour
            }
        }
    });

    submitBtn.addEventListener("click", () => {
        let grid = []
        for (let i = 0; i < height; i++) {
            grid.push([])
            for (let j = 0; j < width; j++) {
                grid[i].push(document.getElementById(`grid-${j}-${i}`).style.backgroundColor)
            }
        }
        socket.emit('grid_send', { value: grid });
    });
});
