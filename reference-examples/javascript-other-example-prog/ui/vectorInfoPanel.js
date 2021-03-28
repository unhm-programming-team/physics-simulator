
class VectorInfoPanel extends Component{

    constructor(mapkeeper, physContainer) {
        super('div');
        this.mapkeeper = mapkeeper;
        this.renderOn(physContainer)
        const tabs = new TabBox();
        tabs.addTo(this)
    }
}

class TabBox extends Component {

    constructor() {
        super('div');

        this.style.display = 'flex';
        this.current_tab = 'vectors';

        const vectors = new Tab('vectors');
        vectors.select();
        const size = new Tab('size');
        const material = new Tab('material');

        vectors.addTo(this);
        size.addTo(this);
        material.addTo(this);

        this.children.forEach( (component) => {
            component.on('click', (ev)=> {
                this.current_tab = component.name;
                this.unselectAll();
                component.select();
            })
        })
    }
    unselectAll() {
        this.children.forEach( (component)=> {
            if(component instanceof Tab) {
                component.unselect();
            }
        })
    }
}

class Tab extends Component {

    constructor(name) {
        super('div');
        this.style.borderTop = '1px solid gray';
        this.style.borderRight = '1px solid gray';
        this.style.borderLeft = '1px solid gray';
        this.style.borderBottom = '1px solid gray';
        this.element.innerHTML = name;
    }

    unselect() {
        this.style.borderTop = '1px solid gray';
        this.style.borderRight = '1px solid gray';
        this.style.borderLeft = '1px solid gray';
        this.style.borderBottom = '1px solid gray';       
    }
    select() {
        this.style.borderTop = '1px solid black';
        this.style.borderBottom = 'none';
        this.style.borderLeft = '1px solid black';
        this.style.borderRight = '1px solid black';
    }
}