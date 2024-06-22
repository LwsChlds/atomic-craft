let fresh = 0; // every term has an id

const sidebar = document.querySelector(".sidebar");

/* box dragging */

const toBox = (name, term) => {
    return `<div data-id=${fresh++} class="box" draggable="true" data-term="${term}">${name}</div>`;
};

let offset = { x: 0, y: 0 };
const main = document.querySelector(".main");
let water = {Hydrogen: 2, Oxygen: 1}

const addDrag = (box) => {
    box.addEventListener("dragstart", (e) => {
        const from = box.parentElement.classList[0];
        e.dataTransfer.setData("text/plain", box.getAttribute("data-id"));
        offset.x = e.clientX - box.getBoundingClientRect().left;
        offset.y = e.clientY - box.getBoundingClientRect().top;
    });
    box.addEventListener("click", () => {
        box.toggleAttribute("clicked");
    });
    box.addEventListener("contextmenu", (e) => {
        e.preventDefault();
        const name = prompt("Name this term:", box.getAttribute("data-term"));
        if (!name) return;
        const term = box.getAttribute("data-term");
        document.querySelectorAll(".box").forEach((box) => {
            if (box.getAttribute("data-term") == term) box.innerText = name;
        });
        delete inventory[term];
        discover(name, parse(term)[0]);
    });
    box.addEventListener("dblclick", (e) => {
        e.preventDefault();
        merge(box)
    });
};

const combine = (overlapping) => {
    let params = {}
    for (let i = 0; i < overlapping.length; i++) {
        let name = overlapping[i].innerText
        if (!(name in params)) {
            params[name] = 1;
        }
        else params[name] += 1;
    }
    fetch("http://0.0.0.0:8000/combine", {
      method: "POST",
      body: JSON.stringify({ "data": params
      }),
      headers: { "Content-Type": "application/json" }
    })
      .then((response) => response.json())
      .then((json) => {
          console.log(json['creates'])
          if (!json['success']) return
          for (let i = 0; i < overlapping.length; i++) {
            if (i === 0) {
                // Hardcoded as water for now
                if (discover(json['creates']['equation'], json['creates']['name'])) overlapping[i].classList.add("discovered");
                overlapping[i].setAttribute("data-term", json['creates']['equation']);
                overlapping[i].innerText = json['creates']['equation'];
            }
            else {
                overlapping[i].remove();
            }
    }
          return json
      });
    return {}
}

const merge = (box) => {

    const overlapping = [];
    main.querySelectorAll(".box").forEach((other) => {
        // if (box === other) return;

        const boxRect = box.getBoundingClientRect();
        const otherRect = other.getBoundingClientRect();
        if (
            boxRect.left < otherRect.right &&
            boxRect.right > otherRect.left &&
            boxRect.top < otherRect.bottom &&
            boxRect.bottom > otherRect.top
        ) {
            overlapping.push(other);
        }
    });
    combine(overlapping)
};

main.addEventListener("dragover", (e) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = "move";
});

main.addEventListener("drop", (e) => {
    e.preventDefault();
    const id = e.dataTransfer.getData("text/plain");
    const from = document.querySelector(`[data-id="${id}"]`);
    const box = document.createElement("div");
    box.classList.add("box");
    box.setAttribute("data-id", fresh++);
    box.setAttribute("draggable", "true");
    box.setAttribute("data-term", from.getAttribute("data-term"));
    box.innerText = from.innerText;
    addDrag(box);

    if (from.parentElement.classList[0] === "main") from.remove();

    const x = e.clientX - offset.x;
    const y = e.clientY - offset.y;
    box.style.left = `${x}px`;
    box.style.top = `${y}px`;
    box.style.position = "absolute";
    main.appendChild(box);
});

/* inventory */

const inventory = {};
const discover = (name, term) => {
    const str = term;
    if (str in inventory) return false;
    inventory[str] = name;
    sidebar.querySelector(".inventory").innerHTML = Object.keys(inventory)
        .map((term) => toBox(inventory[term], term))
        .join("");
    sidebar.querySelectorAll(".inventory .box").forEach(addDrag);
    localStorage.setItem("inventory", JSON.stringify(inventory));
    return true;
};

const load = () => {
    const inv = JSON.parse(localStorage.getItem("inventory"));
    if (inv) {
        Object.keys(inv).forEach((name) => {
            discover(inv[name], name);
        });
    }
};

load();

discover("H", "Hydrogen");
discover("O", "Oxygen");
discover("C", "Carbon");
discover("N", "Nitrogen");
/* search */

sidebar.querySelector("input").addEventListener("keyup", (e) => {
    const query = e.target.value;
    sidebar.querySelectorAll(".inventory .box").forEach((box) => {
        if (
            query == "" ||
            box.getAttribute("data-term").includes(query) ||
            box.innerText.includes(query)
        ) {
            box.style.display = "block";
        } else {
            box.style.display = "none";
        }
    });
});

/* popups */

const popup = document.querySelector(".popup");

const message = (str) => {
    window.popupText.innerHTML = str;
    window.popupClose.style.display = "block";
    popup.classList.add("active");
};

/* buttons */

window.clean.addEventListener("click", () => {
    document
        .querySelector(".main")
        .querySelectorAll(".box")
        .forEach((box) => {
            box.remove();
        });
});

window.popupClose.addEventListener("click", () => {
    popup.classList.remove("active");
});

window.help.addEventListener("click", () => {
    message(
        "Update me",
    );
});

window.github.addEventListener("click", () => {
    message(
        "Update me",
    );
});

window.support.addEventListener("click", () => {
    message(
        "Update me",
    );
});

window.restart.addEventListener("click", () => {
    if (
        !confirm(
            "Are you sure you want to restart? You will lose your entire inventory.",
        )
    )
        return;
    localStorage.clear();
    window.location.reload();
});
