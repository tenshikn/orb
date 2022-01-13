/* Foucs on hovered image */

let hovered = document.querySelectorAll('.img-thumbnail');
let N = hovered.length;
for (let i = 0; i < N; i++) {
    $(hovered[i]).hover(
        function() {
            /*
            console.log(this);
            let id = this.id;
            $('main, main *').not(`[id='${id}']`).css("-webkit-filter", "blur(2px)");
            */
            this.focus();
        },
        function() {
            /*
            let id = this.id;
            $('main, main *').not(`[id='${id}']`).css("-webkit-filter", "blur(0px)");
            */
            this.blur()
        });
}