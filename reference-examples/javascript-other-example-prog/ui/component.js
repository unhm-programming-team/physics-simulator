


class Component {
    constructor(element_type) {
        this.element = document.createElement(element_type);
        this.style = this.element.style;
        this.parent = null;
        this.children = [];
    }
    on(type, listener) {
        this.element.addEventListener(type,listener);
    }
    addTo(component) {
        this.parent = component;
        component.element.append(this.element);
        component.children.push(this);
    }
    renderOn(el) {
        el.append(this.element);
    }
}