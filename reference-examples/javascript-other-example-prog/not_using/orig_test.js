
const debug = document.getElementById('debug')

const canvas = document.getElementById('physics-area')

const context = canvas.getContext('2d')

debug.innerHTML = canvas.height

document.addEventListener('DOMContentLoaded', ()=> {
    console.log('document loaded')
})

const log = (text)=>{
    console.log(text)
}



var RUNNING = true;

let rect = new Rectangle(5,5,10,10);

const mapkeeper = new Mapkeeper(context);
const player = new Player(mapkeeper,10,10);
player.paint(context)
player.keyboardInit();

const wall = new GameObject(mapkeeper, 98,50,19,100,1,false)
const floor = new GameObject(mapkeeper, 0,100,300,150,2,true,'green','darkgreen');

mapkeeper.addObject(wall);

const sleep = (delay) => new Promise((resolve)=> setTimeout(resolve,delay));

const gameLoop = async () => {
    while (RUNNING ){
        mapkeeper.update();
        await sleep(5);
    }
}

gameLoop()