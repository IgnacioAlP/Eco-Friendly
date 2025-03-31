const segmentos = [
    { nombre: "Cuerpo", descuento: 10 },
    { nombre: "Cabello", descuento: 20 },
    { nombre: "Rostro", descuento: 30 },
    { nombre: "Accesorios", descuento: 40 },
    { nombre: "Higiene", descuento: 50 }
]; // Descuentos y nombres
const ruleta = document.getElementById('ruleta');
const resultado = document.getElementById('resultado');
const codigo = document.getElementById('codigo');

// Colores pastel
const colores = [
    '#a8e6cf', // Verde pastel claro
    '#dcedc1', // Verde claro
    '#ffe0b2', // Amarillo pastel
    '#ffab91', // Coral pastel
    '#b9fbc0'  // Verde menta
];

// Crear segmentos de la ruleta
segmentos.forEach((segmento, index) => {
    const divSegmento = document.createElement('div');
    divSegmento.classList.add('segmento');
    divSegmento.style.transform = `rotate(${(index * (360 / segmentos.length))}deg)`;
    divSegmento.style.backgroundColor = colores[index % colores.length]; // Usar colores pastel
    divSegmento.textContent = segmento.nombre; // Mostrar nombre en el segmento
    ruleta.appendChild(divSegmento);
});

// Función para generar un código de descuento aleatorio
function generarCodigo() {
    const caracteres = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    let codigoGenerado = '';
    for (let i = 0; i < 6; i++) {
        codigoGenerado += caracteres.charAt(Math.floor(Math.random() * caracteres.length));
    }
    return codigoGenerado;
}

document.getElementById('boton').onclick = function() {
    const giro = Math.floor(Math.random() * 360 + 720); // Giro aleatorio
    ruleta.style.transition = 'transform 4s ease-out';
    ruleta.style.transform = `rotate(${giro}deg)`;

    setTimeout(() => {
        const indiceGanador = Math.floor((giro % 360) / (360 / segmentos.length));
        const descuentoGanado = segmentos[indiceGanador].descuento;
        resultado.textContent = `¡Has ganado un descuento del ${descuentoGanado}%!`; // Mostrar porcentaje de descuento
        resultado.classList.add('visible'); // Añadir clase para animación
        codigo.textContent = `Código de descuento: ${generarCodigo()}`; // Mostrar código aleatorio
    }, 4000); // Espera a que termine el giro
};
