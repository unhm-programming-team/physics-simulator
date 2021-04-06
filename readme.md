# physics-simulator

The purpose of this project is to provide a User Interface and Physics Environment for experimenting and visualizing 2-D physics.

It will be written in Python.

It will use Tkinter for the User Interface because of Tkinter's lightweight nature and because of the power of the Tkinter Canvas object, which is the object that will be used to display the PhysicsObjects. 

[Here is the Python 3 Tkinter reference](https://docs.python.org/3/library/tkinter.html)

[Here is the tutorial I found most useful for learning the basics of Tkinter](https://tkdocs.com/tutorial/index.html)

Todo:
 - ~~Create an object to encapsulate the Canvas object~~
 - ~~Create a Phyics Object that contains references to Vectors and will re-set its X and Y accordingly~~
 - ~~Like the pieces in `snakes_and_ladders`, a physics object should have a reference to its x and y coord, vectors for position, velocity, and acceleration, the shape(s) it draws, and the canvas object so it can move those shapes around. It will probably need a mass, though we may eventually want to abstract this, or have the option to abstract this, into a material.~~
 - ~~There will have to be a timing loop to handle updates to physics objects based on their vectors and intervals.~~
 - ~~There will need to be a way to pause and step time.~~
 - ~~The time loop will need to go through the physics objects and update them according to their vectors~~
 - ~~The time loop should run on a separate thread (really not too bad in Python!)~~
 - ~~PhysicsObjects need to have mass~~
 - ~~PhysicsObject should calculate their size based on material and mass~~
 - **Kind of a big issue**: Meters right now are equal to one pixel. That means a Silver MassObject has to weigh about 10^7 kilograms to be easily viewable. There needs to be a way to scale the viewport. Probably has to be done in the PhysicsCanvas. And, once that's implemented, the starting value should be set pretty zoomed in.
 - The UI for adding PhysicsObjects doesnt support negative numbers or decimals; validation needs to be improved/fixed
 - The color selector for adding physics objects is an ugly button, and it would be nicer if that button changed to the color selected
 - ~~PhysicsObjects need to know what forces are acting on them~~ and be able to interact with other objects, such as via gravitational pull and collision
 - ~~If you click on a Physics object, there should be a UI pane on the side that shows you the current vectors operating on it~~
 - You should be able to change vectors and forces on a particular object from the UI
 - We should be able to save and load states
 - We should have a UI to configure the Options

- Everything should be documented with Sphinx eventually. For now, we should document everything with [docstrings that Sphinx can use](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html)

## Why you might contribute to this project

- It will be fun to play with bouncing and colliding balls on the screen
- You will learn UI in Python
- It can be a portfolio project you can show off to employers when it's done, and be able to say you worked on it
- It will help learning and practicing math and physics as well as code
- There will be tons of features to implement. After distance/velocity/acceleration there's forces, including friction, drag, gravity, and normal force. There's tension. This thing could turn pretty cool.
- Maybe when it's at a good point we can fork it into a game or something.

Any and everyone should feel free to pull request this; I'm open to different directions.
