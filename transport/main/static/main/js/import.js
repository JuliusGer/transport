var openModalBtn = document.getElementById("open-modal-btn");
var closeModalBtn = document.getElementById("close-modal-btn");
var modalContainer = document.getElementById("modal-container");

if (openModalBtn){
    openModalBtn.addEventListener("click", function() {
     modalContainer.style.display = "flex";
     modalContainer.style.display = "flex";
    });
}

if (closeModalBtn){
    closeModalBtn.addEventListener("click", function() {
     modalContainer.style.display = "none";
    });
}
