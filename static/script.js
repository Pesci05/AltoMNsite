const carousel = document.getElementsByClassName("carousel");
const news = document.getElementsByClassName("carousel-item");

let index = 0;
let direction = 1;

function autoplay(){
    const width = news[0].clientWidth;
    if (index === 4) direction = -1;
    if(index === 0) direction = 1;
    index += direction;

    carousel[0].scrollTo({left: index*width,behavior:"smooth"});
}

let timer = setInterval(autoplay, 3000);
carousel[0].addEventListener('pointerdown', () => clearInterval(timer));

carousel[0].addEventListener('pointerup', () => {
  index = Math.round(carousel[0].scrollLeft / carousel[0].clientWidth);
  timer = setInterval(autoPlay, 3000);
});

function goToModificaPartita(){
    var select = document.getElementById('selezione_partita');
    var selectedOption = select.options[select.selectedIndex];

   var targetUrl = selectedOption.getAttribute('data-url');
    
    if (targetUrl) {
        // Reindirizza all'URL assoluto (es: /teams/partita/2/modifica/)
        window.location.href = targetUrl;
    } else {
        alert("Seleziona prima una partita dall'elenco.");
    }
}
function goToEliminaPartita() {
    var select = document.getElementById('selezione_partita');
    var selectedOption = select.options[select.selectedIndex];
    var targetUrl = selectedOption.getAttribute('data-url-elimina');
    
    console.log(targetUrl);
    if (!targetUrl) {
        alert("Seleziona prima una partita dall'elenco.");
        return;
    }

    // Popup nativo del browser
    var partitaTesto = selectedOption.text.trim();
    var conferma = confirm("Sei sicuro di voler eliminare la partita:\n" + partitaTesto + "?\n\nL'azione è irreversibile.");
    
    if (conferma) {
        window.location.href = targetUrl;
    }
}
