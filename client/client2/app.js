class App{
    constructor(){
        this.canvas = new fabric.Canvas('c');
        this.ctx = this.canvas.getContext('2d');
        window.addEventListener('resize', this.resize.bind(this), false);
        const rect = new fabric.Rect({
            left: 100,
            top: 140,
            fill: 'red',
            width: 20,
            height: 20
        });
        
        this.canvas.add(rect);
        this.resize();
    }

    resize() {
        this.stageWidth = document.body.clientWidth;
        this.stageHeight = document.body.clientHeight;

        this.canvas.setWidth(600);
        this.canvas.setHeight(400);
    }
}

window.onload = () => {
    new App();
}