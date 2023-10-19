//var selectCurChoice = document.getElementById("type_id_select");
var left = document.getElementsByClassName("left")

function change_background(select){
        const option = select.querySelector(`option[value="${select.value}"]`)
        if (option != '1'){
//            document.getElementById('split_left').left.style.backgroundImage="url('../img/самолетик.jpg')";
//            document.getElementById('split_right').right.style.backgroundImage="url('../img/том круз.jpg')";
              left.style.background="url('../img/том круз.jpg')";
    }
}