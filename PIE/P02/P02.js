const counter = document.getElementById("frame-counter");
let cidx=0;
const frames=get_all_frames();
// Obtiene todos los elementos con la clase .frame y los convierte en un array real
function get_all_frames() {
  const frames_list = document.querySelectorAll(".frame");
  return frames_list;
}
function update_counter(idx) {
  if (counter) {
    counter.textContent = `${idx + 1} / ${frames.length}`;
  }
}
function frameCache(cidx) {
  // Si se pasa un cidx como argumento, lo guardamos en sessionStorage
  if (cidx !== undefined) {
    sessionStorage.setItem('cached_cidx', cidx);
    return cidx;
  }
  // Si no se pasa argumento, lo leemos de sessionStorage
  const saved = sessionStorage.getItem('cached_cidx');
  // Si existe un valor guardado lo convertimos a número, si no, retornamos 0 por defecto
  return saved !== null ? parseInt(saved, 10) : 0;
}
// Oculta un frame específico usando el índice correcto del DOM
function set_frame(idx, frames_list) {
  // Verificamos que el índice exista dentro de la lista
  if (frames_list && frames_list[idx]) {
    // Usamos classList.add en lugar de appendClass
    frames_list.forEach((frame, i) => frame.classList.toggle("hidden", i !== idx));
    frameCache(cidx)
    update_counter(cidx)
  }
}
// Se ejecuta automáticamente en cuanto carga el DOM de la página
document.addEventListener("DOMContentLoaded", () => {
  cidx=frameCache();
  set_frame(cidx, frames); // Oculta el primer frame (índice 0)
});
document.addEventListener("keydown", (event) => {
if (["ArrowRight", "ArrowDown", "j", "l"].includes(event.key)) {
  cidx = (cidx + 1) % frames.length;
  set_frame(cidx, frames);
  }
});
document.addEventListener("keydown", (event) => {
if (["ArrowLeft", "ArrowUp", "k", "h"].includes(event.key)) {
  cidx = (cidx - 1 + frames.length) % frames.length;
  set_frame(cidx, frames);
  }
});

