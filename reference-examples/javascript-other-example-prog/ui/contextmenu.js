class ContextMenu extends Component {

    constructor(container, mapkeeper) {
        super('div');
        const canvas = mapkeeper.context.canvas;
        this.renderOn(container);
        this.style.display = 'none';
        this.style.position = 'absolute';
        canvas.addEventListener('contextmenu', (ev)=> {
            ev.preventDefault();
            this.style.top = ev.clientY + 'px';
            this.style.left = ev.clientX + 'px';
            this.show();
        })
        canvas.addEventListener('click', (ev)=> {
            this.style.display = 'none';
            this.hide();
        })
        this.style.border = '1px dashed gray';
        
        const addVector = new ContextMenuItem(this, 'add vector');
        addVector.addTo(this);
        this. selected = 'add vector';
    }

    show() {
        this.style.display = 'block';
    }
    hide() {
        this.style.display = 'none';
    }
    fire(ev) {
        
    }

}


class ContextMenuItem extends Component {
    constructor(contextmenu, name) {
        super('div');
        this.element.innerHTML = name;
        this.on('click', (ev)=>{
            contextmenu.selected = name;
            contextmenu.hide();
            contextmenu.fire(ev);
        })
    }
}