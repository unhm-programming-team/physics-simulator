class Mapkeeper {

    log = console.log;

    constructor(canvasContext) {
        this.context = canvasContext;
        this.width = canvasContext.canvas.width;
        this.height = canvasContext.canvas.height;
        console.log(this.width, this.height)
        this.origin_x = this.width/2
        this.origin_y = this.height/2
        this.objects = [];
        this.moving_objects = [];
        let now = new Date();
        this.last_update = now.getTime();
    }

    add_physics_object(physicsObject) {
        this.objects.push(physicsObject);
        physicsObject.loaded(this)
    }

    update() {
        let now = new Date();
        let time = now.getTime();
        // interval is passed in seconds
        let interval = (time - this.last_update)/1000;
        this.last_update = time;
        this.objects.forEach( (object)=> {
            object.update(interval);
        })
        // pass interval to objects

    }
}