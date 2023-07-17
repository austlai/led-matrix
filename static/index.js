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

    let activeGrid = false;
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

    const handle_down = (e) => {
        draw = true;
        if (erase) {
            e.target.style.backgroundColor = fillColour;
        } else {
            e.target.style.backgroundColor = colourInput.value;
        }
        send_grid();
        e.preventDefault();
    };

    const handle_move = (e) => {
        let elementId = document.elementFromPoint(
            !isTouchDevice() ? e.clientX : e.touches[0].clientX,
            !isTouchDevice() ? e.clientY : e.touches[0].clientY
        ).id;
        checker(elementId);
    };

    const handle_up = () => {
        draw = false;
    }

    grid.addEventListener('click', () => {
        for (let i = 0; i < height; i++) {
            for (let j = 0; j < width; j++) {
                let cell = document.getElementById(`grid-${j}-${i}`);
                cell.addEventListener(events[deviceType].down, handle_down);
                cell.addEventListener(events[deviceType].move, handle_move);
                cell.addEventListener(events[deviceType].up, handle_up);
            }
        }
        socket.emit('grid_toggle', { value: true });
    });

    grid.addEventListener('mouseleave', () => {
        console.log("MOUSELEAVE")
        for (let i = 0; i < height; i++) {
            for (let j = 0; j < width; j++) {
                let cell = document.getElementById(`grid-${j}-${i}`);
                cell.removeEventListener(events[deviceType].down, handle_down);
                cell.removeEventListener(events[deviceType].move, handle_move);
                cell.removeEventListener(events[deviceType].up, handle_up);
            }
        }
    });

    // Build Grid
    for (let i = 0; i < height; i++) {
        let div = document.createElement("div");
        div.classList.add("gridRow");
        for (let j = 0; j < width; j++) {
            let col = document.createElement("div");
            col.classList.add("gridCol");
            col.setAttribute("id", `grid-${j}-${i}`);
            col.style.backgroundColor = "#000";
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
                    send_grid();
                } else if (draw && erase) {
                    element.style.backgroundColor = fillColour;
                    send_grid();
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
        let gridRows = document.querySelectorAll(".gridRow");
        if (yiq < 40) {
            gridColumns.forEach((element) => {
                element.style.borderColor = '#222'
            });
            gridRows.forEach((element) => {
                element.style.borderColor = '#222'
            });
            grid.style.backgroundColor = '#222'
        } else {
            gridColumns.forEach((element) => {
                element.style.borderColor = '#ddd'
            });
            gridRows.forEach((element) => {
                element.style.borderColor = '#ddd'
            });
            grid.style.backgroundColor = '#ddd'
        }
    }

    clearBtn.addEventListener("click", () => {
        for (let i = 0; i < height; i++) {
            for (let j = 0; j < width; j++) {
                document.getElementById(`grid-${j}-${i}`).style.backgroundColor = fillColour
            }
        }
        send_grid();
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
        send_grid();
    });

    submitBtn.addEventListener("click", () => {
        send_grid();
    });

    const send_grid = () => {
        let grid = []
        for (let i = 0; i < height; i++) {
            grid.push([])
            for (let j = 0; j < width; j++) {
                grid[i].push(document.getElementById(`grid-${j}-${i}`).style.backgroundColor)
            }
        }
        socket.emit('grid_send', { value: grid });
    }
});
