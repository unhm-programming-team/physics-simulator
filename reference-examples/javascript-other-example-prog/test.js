
const debug = document.getElementById('debug')
const canvas = document.getElementById('physics-area')
const context = canvas.getContext('2d')

document.addEventListener('DOMContentLoaded', ()=> {
    console.log('document loaded')
})

const log = (text)=>{
    console.log(text)
}



var RUNNING = true;

const mapkeeper = new Mapkeeper(context);

const bar = SlidingPhysicsObject.getGreenBlock();
const bouncer = RandomBouncer.getBlueRandomBouncer();
const grav = AcceleratesToMiddle.getGreenBlock();
mapkeeper.add_physics_object(bar);
mapkeeper.add_physics_object(bouncer);
mapkeeper.add_physics_object(grav);

/** game loop */
const FRAMERATE = 50;

const sleep = (delay) => new Promise((resolve)=> setTimeout(resolve,delay));
const gameLoop = async () => {
    while (RUNNING ){
        await sleep(FRAMERATE);
        mapkeeper.update();
    }
}
gameLoop();

const stop = ()=>{
    RUNNING=false;
}