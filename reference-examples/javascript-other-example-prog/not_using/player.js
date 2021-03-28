class Player extends GameObject{
    constructor(movemanager, x,y,width=15, height=19,z=1) {
        super(movemanager, x, y, width, height, z, false, 'blue', 'black')
        console.log(this)
    }
    /**
     * @overrides GameObject.paint()
     */
    paint(canvasContext){
        let old = canvasContext.globalCompositeOperation;
        canvasContext.globalCompositeOperation = "difference";
        super.paint(canvasContext);
        canvasContext.globalCompositeOperation = old;
    }

    keyboardInit() {
        const that = this;
        document.addEventListener('keydown', (event)=> {
            const keyName = event.key;
            log(keyName)
            if (keyName == 'ArrowLeft') {
                that.move_left(5);
            }
            else if(keyName == 'ArrowRight') {
                that.move_right(5);
            }
            else if(keyName == 'ArrowDown') {
                that.move_down(5);
            }
            else if(keyName == 'ArrowUp') {
                that.move_up(5);
            }
            else if(keyName == 'Q') {
                RUNNING = false;
                log('bye')
            }
        });
    }
}