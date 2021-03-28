class Point {
    constructor(x,y,z=1) {
        this.x = x;
        this.y = y;
        this.z = z;
    }
    down(n) { this.y += n }
    up(n) { this.y -= n }
    left(n) { this.x -= n }
    right(n) { this.x += n }
}
class ColorPoint extends Point{
    constructor(fill, stroke, x,y,z=1) {
        super(x,y,z);
        this.fill = fill;
        this.stroke = stroke;
    }
}
class Rectangle extends ColorPoint{
    constructor(x,y,width,height,z=1,fill='darkslategray',stroke='black') {
        super(fill, stroke, x, y, z);
        this.width = width;
        this.height = height;
    }
    paint(canvasContext) {
        canvasContext.fillStyle = this.fill;
        canvasContext.fillRect(
            this.x,
            this.y,
            this.width,
            this.height
        )
    }
    clear(canvasContext) {
        canvasContext.clearRect(
            this.x-1,
            this.y-1,
            this.width+2,
            this.height+2
        )
    }
}