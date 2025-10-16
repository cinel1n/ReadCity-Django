
let clicks = 0;     // счетчик нажатий
function btn_click(){

    if (this.getAttribute('class').includes('button-fav-bookmarks')){
        this.classList.add('button-fav-no-bookmarks');
        return this.classList.remove('button-fav-bookmarks');
    }
    this.classList.remove('button-fav-no-bookmarks');
    return this.classList.add('button-fav-bookmarks');
}
const buttons = document.getElementsByClassName("btn-click");
for (element of buttons){
    element.addEventListener("click", btn_click);
}


let clicks1 = 0;     // счетчик нажатий
function btn_click2(){

    if (this.getAttribute('class').includes('button-fav-basket')){
        this.classList.add('button-fav-no-basket');
        return this.classList.remove('button-fav-basket');
    }
    this.classList.remove('button-fav-no-basket');
    return this.classList.add('button-fav-basket');
}
const buttons = document.getElementsByClassName("btn-click");
for (element of buttons){
    element.addEventListener("click", btn_click2);
}