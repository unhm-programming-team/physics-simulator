const DIV_NAME = "physics-canvas-div"
const CANVAS_NAME = "physics-area"


const container = document.getElementById(DIV_NAME);
const canvas = document.getElementById(CANVAS_NAME);

const playbar = new Playbar(container);

const mapkeeper = new Mapkeeper(canvas.getContext('2d'))

const vectorPanel = new VectorInfoPanel(mapkeeper, container);
const contextmenu = new ContextMenu(container, mapkeeper)