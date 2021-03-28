class Vector {
    constructor(angle, magnitude) {
        this.angle = angle;
        this.magnitude = magnitude;
        this.calculateComponents();
    }

    /**
     * Calculates component vectors from current angle and rotation
     */
    calculateComponents() {
        this.y = this.magnitude * Math.sin(this.angle);
        this.x = this.magnitude * Math.cos(this.angle);
        if(this.x == NaN) {
            this.x = 0
        }
        if(this.y == NaN) {
            this.y = 0
        }
    }
    /**
     * Returns new vector from components
     * @param {number} x magnitude on x-axis
     * @param {number} y magnitude on y-axis
     * @returns Vector
     */
    static fromComponents(x, y) {
        let angle = Math.atan2(y,x);
        if(angle == NaN) {
            angle = 0
        }
        let magnitude = Math.sqrt(x*x + y*y);
        return new Vector(angle, magnitude);
    }
    /**
     * Returns new vector
     * @param {Vector} vector 
     * @returns 
     */
    add(vector) {
        /* console.log(`
        adding vector >> \n
        vector.x = ${vector.x}
        this.x = ${this.x}`) */
        let new_x = vector.x + this.x;
        let new_y = vector.y + this.y;
        //console.log('add components', new_x, new_y)
        return Vector.fromComponents(new_x, new_y);
    }
    /**
     * Returns new vector
     * @param {vector} vector 
     * @returns Vector
     */
    subtract(vector) {
        let new_x = this.x - vector.x;
        let new_y = this.y - vector.y;
        return Vector.fromComponents(new_x, new_y);
    }
    /**
     * Mutates
     * @param {number} radians Radians to rotate
     */
    rotate(radians) {
        let new_angle = this.angle + radians;
        let twoPi = Math.PI * 2;
        if( new_angle > twoPi) {
            new_angle -= twoPi;
        }
        else if( new_angle < 0 ) {
            new_angle = twoPi - new_angle;
        }
        this.angle = new_angle;
        this.calculateComponents();
    }
    /**
     * Mutates
     * @param {number} scalar 
     */
    scale(scalar) {
        this.magnitude *= scalar;
        this.calculateComponents();
    }

    /**
     * Utility class for constructing directional vectors
     * @param {string} direction in "n,nw,w,sw,s,se,e,ne"
     * @param {number} magnitude 
     */
    static directionalVector(direction, magnitude) {
        const convert_to_radians = (degree) => {
            return (degree * Math.PI)/180;
        }
        let angle = 0;
        switch(direction) {
            case 'n':
                angle = convert_to_radians(90);
                break;
            case 'nw':
                angle = convert_to_radians(135);
                break;
            case 'w':
                angle = Math.PI;
                break;
            case 'sw':
                angle = convert_to_radians(225);
                break;
            case 's':
                angle = convert_to_radians(270);
                break;
            case 'se':
                angle = convert_to_radians(315);
                break;
            case 'e':
                angle = 0;
                break;
        }
        return new Vector(angle, magnitude);
    }

}

class RenderShape extends Rectangle{
    constructor(width,height,z=1,fill="orange",stroke="black") {
        super(0,0,width,height,z,fill,stroke);
        this.calculateBounds();
    }
    calculateBounds() {
        this.bottom = this.y + this.height;
        this.right = this.x + this.width;
    }
    position(distance_vector, mapkeeper) {
        this.x = distance_vector.x + mapkeeper.origin_x;
        this.y = -distance_vector.y + mapkeeper.origin_y;
        this.calculateBounds();
    }

    static getSmallYellowRect() {
        return new RenderShape(15,25,1,"red","black");
    }
}

const WORLD_SCALE = 1; //how many pixels in a meter


class PhysicsObject {

    constructor(render_shape, mass, mapkeeper=null) {
        this.mapkeeper = mapkeeper;
        this.shape = render_shape;
        this.mass = mass;
        this.position = new Vector(0,0);
        this.velocity = new Vector(0,0);
        this.acceleration = new Vector(0,0);
        this.forcesChanged = true;
        this.forces = []; //array of vectors
    }

    /**
     * Called by mapkeeper when object added to map
     * @param {MapKeeper} mapkeeper 
     */
    loaded(mapkeeper) {
        this.mapkeeper = mapkeeper;
    }

    render() {
        this.shape.clear(this.mapkeeper.context)
        this.shape.position(this.position, this.mapkeeper);
        this.shape.paint(this.mapkeeper.context)
    }
    calculateAcceleration() {
        let x_sum = 0;
        let y_sum = 0;
        this.forces.forEach( (force) => {
            x_sum += force.x;
            y_sum += force.y;
        })
        this.acceleration = Vector.fromComponents(x_sum, y_sum);
    }
    integrateVelocity(interval) {
        let x_translate = (this.acceleration.x * interval ) / WORLD_SCALE;
        let y_translate = (this.acceleration.y * interval ) / WORLD_SCALE;
        let translate = Vector.fromComponents(x_translate, y_translate);
        this.velocity = this.velocity.add(translate);
    }
    integratePosition(interval) {
        let x_translate = (this.velocity.x*interval) / WORLD_SCALE;
        let y_translate = (this.velocity.y*interval) / WORLD_SCALE;
        let translate = Vector.fromComponents(x_translate, y_translate);
        this.position = this.position.add(translate);
    }

    update(interval) {
        this.calculateAcceleration();
        this.integrateVelocity(interval);
        this.integratePosition(interval);
        this.render();
    }


    static getGoldBar() {
        let shape = new RenderShape(8, 16, 1, "gold","black");
        return new PhysicsObject(shape, 10);
    }
}
class RandomBouncer extends PhysicsObject {

    constructor(render_shape, mass, mapkeeper=null) {
        super(render_shape, mass, mapkeeper);
        this.topResistor = 70;
        this.bottomResistor = -70;
        this.leftResistor = -70;
        this.rightResistor = 120;
        this.velocity = new Vector(-0.3,90)
    }

    loaded(mapkeeper) {
        super.loaded(mapkeeper);
        this.topResistor = mapkeeper.height/2
        this.bottomResistor = this.topResistor * (-1) + this.shape.height
        this.rightResistor = mapkeeper.width/2
        this.leftResistor = this.rightResistor * (-1)
        this.rightResistor -= this.shape.width
    }

    integrateVelocity() {
        let v_x = this.velocity.x
        let v_y = this.velocity.y
        if(this.position.x > this.rightResistor) {
            v_x *= -1
        }
        else if(this.position.x < this.leftResistor) {
            v_x *= -1
        }
        if(this.position.y > this.topResistor) {
            v_y *= -1
        }
        else if(this.position.y < this.bottomResistor) {
            v_y *= -1
        }
        this.velocity = Vector.fromComponents(v_x, v_y);
    }

    static getBlueRandomBouncer() {
        let shape = new RenderShape(15,10,1,"navy","black");
        return new RandomBouncer(shape,10)
    }
}
class SlidingPhysicsObject extends PhysicsObject{

    constructor(render_shape, mass, mapkeeper=null) {
        super(render_shape, mass, mapkeeper);
        this.rightLimit = 20;
        this.leftLimit = -20;
        this.velocity = Vector.directionalVector('e',1);
    }
    recalculateVelocities() {
        if(this.position.x < this.leftLimit) {
            this.velocity = Vector.directionalVector('e',1);
        }
        else if(this.position.x > this.rightLimit) {
            this.velocity = Vector.directionalVector('w',1);
        }
    }

    static getGreenBlock() {
        let shape = new RenderShape(8,16,1,"green","black");
        return new SlidingPhysicsObject(shape, 10);
    }
}
class AcceleratesToMiddle extends PhysicsObject {

    constructor(render_shape, mass, mapkeeper=null) {
        super(render_shape, mass, mapkeeper);
        this.position = new Vector(1.5, 30);
        this.pull = 95;
    }

    calculateAcceleration() {
        let newx = this.acceleration.x;
        let newy = this.acceleration.y;
        if(this.position.y > 0) {
            newy = -1 * this.pull
        }
        else {
            newy = this.pull;
        }
        if(this.position.y < 4 && this.position.y > -4) {
            this.pull += 5;
        }
        this.acceleration = Vector.fromComponents(newx,newy)

    }

    static getGreenBlock() {
        let shape = new RenderShape(8,16,1,"#004242","black");
        return new AcceleratesToMiddle(shape, 10);
    }

}