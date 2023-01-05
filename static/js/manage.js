let slideIndex = 1;
showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
    showSlides((slideIndex += n));
}

// Thumbnail image controls
function currentSlide(n) {
    showSlides((slideIndex = n));
}

function showSlides(n) {
    let i;
    let slides = document.getElementsByClassName("mySlides");
    //let dots = document.getElementsByClassName("dot");
    if (n > slides.length) {
        slideIndex = 1;
    }
    if (n < 1) {
        slideIndex = slides.length;
    }
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    /*
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }
    */
    slides[slideIndex - 1].style.display = "block";
    //dots[slideIndex - 1].className += " active";
}

// drag
///*
let dragindex = 0;
let dropindex = 0;
let clone = "";

function drag(e) {
    e.dataTransfer.setData("text", e.target.id);
}

function drop(e) {
    e.preventDefault();
    clone = e.target.cloneNode(true);
    let data = e.dataTransfer.getData("text");
    if (clone.id !== data) {
        let nodelist = document.getElementById("parent").childNodes;
        for (let i = 0; i < nodelist.length; i++) {
            if (nodelist[i].id == data) {
                dragindex = i;
            }
        }

        document
            .getElementById("parent")
            .replaceChild(document.getElementById(data), e.target);

        document
            .getElementById("parent")
            .insertBefore(
                clone,
                document.getElementById("parent").childNodes[dragindex]
            );
    }
}

function allowDrop(e) {
    e.preventDefault();
}
//*/

/* table move test*/
var row;

function startt(e) {
    row = e.target;
}
function dragovert(e) {
    e.preventDefault();

    let children = Array.from(e.target.parentNode.parentNode.children);

    if (children.indexOf(e.target.parentNode) > children.indexOf(row))
        e.target.parentNode.after(row);
    else e.target.parentNode.before(row);
}
