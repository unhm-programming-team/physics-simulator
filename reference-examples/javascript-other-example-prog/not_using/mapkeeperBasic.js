class Move{
    constructor(moving_object, x, y) {
        this.object = moving_object;
        this.new_x = x;
        this.new_y = y;
    }
}
class Mapkeeper {
    constructor(canvasContext) {
        this.context = canvasContext;
        this.objects = [];
        this.moves = [];
    }
    check(move) {
        let left = move.object.x + move.new_x;
        if( left < 0) { return false; }
        let right = move.object.right + move.new_x;
        if( right > context.canvas.width) { return false;}
        let top = move.object.y + move.new_y;
        if( top < 0 ) { return false; }
        let bottom = move.object.bottom + move.new_y;
        if( bottom > context.canvas.height) { return false; }

        for(let i = 0; i < this.objects.length; i++) {
            let test = this.objects[i];
            if (test === move.object) { continue; }
            if(test.passable == true) { continue; }
            let intersects_y = (top < test.y) ?
                bottom > test.y : top < test.bottom;
            let intersects_x = (left < test.x) ?
                right > test.x : left < test.right;
            let intersects_z = move.object.z == test.z;
            if( intersects_y && intersects_x && intersects_z) {
                return false
            }
        }
        return true
    }
    addObject(gameobject){
        gameobject.mapkeeper = this;
        gameobject.paint(this.context);
        this.objects.push(gameobject);
    }
    update() {
        let now = new Date();
        let time = now.getTime();
        this.objects.forEach( (obj) => {
            obj.update(time);
        })
        this.moves.forEach( (move)=> {
            if( this.check(move) ) {
                move.object.x = move.object.x + move.new_x;
                move.object.right = move.object.x + move.object.width;
                move.object.y = move.object.y + move.new_y;
                move.object.bottom = move.object.y + move.object.height;
            }
        })
        this.moves = [];
    }
}


class GameObject extends Rectangle{
    constructor(mapkeeper, x,y,width=50, height=50,z=1,passable=true,fill='firebrick',stroke='black'){
        super(x,y,width,height,z,fill,stroke)
        this.mapkeeper = mapkeeper;
        this.passable = passable;
        this.right = x + width;
        this.bottom = y + height;
    }
    move_up(n) {
        this.mapkeeper.moves.push(
            new Move(this, 0, -n)
        )
    }
    move_down(n) {
        this.mapkeeper.moves.push(
            new Move(this, 0, n)
        )
    }
    move_left(n) {
        this.mapkeeper.moves.push(
            new Move(this, -n, 0)
        )
    }
    move_right(n) {
        this.mapkeeper.moves.push(
            new Move(this, n, 0)
        )
    }
    update(interval) {
        this.paint(mapkeeper.context)
    }
}
