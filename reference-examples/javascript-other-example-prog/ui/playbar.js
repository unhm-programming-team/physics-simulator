class Playbar {
    constructor(containerDiv) {
        this.createElements(containerDiv)
    }
    createElements(containerDiv){
        this.flex = document.createElement('div')
        this.flex.style.display = 'flex';
        this.flex.style.alignItems = 'center';
        this.flex.style.justifyContent = 'space-around';

        this.playButton = document.createElement('button');
        this.playButton.innerHTML = 'Play';
        this.flex.append(this.playButton);

        this.pauseButton = document.createElement('button');
        this.pauseButton.innerHTML = 'Pause';
        this.flex.append(this.pauseButton);

        this.stepButton = document.createElement('button');
        this.stepButton.innerHTML = 'Step';
        this.flex.append(this.stepButton);
        containerDiv.append(this.flex)
    }
}
