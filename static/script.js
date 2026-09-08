/*const carousel = document.getElementsByClassName("Carousel");
const news = document.getElementsByClassName("news");

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
});*/

function goToModificaPartita(){
    var select = document.getElementById('selezione_partita');
    console.log(select);
    var pk = select.value;
    if(pk){
        var urlTemplate = "{% 'modificaPartita' 0 %}";
        var targetUrl = urlTemplate.replace('0',pk);

        window.location.href = targetUrl;
    }else{
        alert("Seleziona prima una partita dall'elenco.");
    }
}