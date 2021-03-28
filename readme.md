# physics-simulator

The purpose of this project is to provide a User Interface and Physics Environment for experimenting and visualizing 2-D physics.

It will be written in Python.

It will use Tkinter for the User Interface because of Tkinter's lightweight nature and because of the power of the Tkinter Canvas object, which is the object that will be used to display the PhysicsObjects. 

[Here is the Python 3 Tkinter reference](https://docs.python.org/3/library/tkinter.html)

[Here is the tutorial I found most useful for learning the basics of Tkinter](https://tkdocs.com/tutorial/index.html)

The `reference-examples` folder contains examples of two games I made recently for a midterm, snakes and ladders and war, using the tkinter ui. Don't worry, we can make it a _much_ more ergonomic UI than that rushed project.

The next step towards physics is creating `PhysicsObject`s which have vectors in them to represent distance, velocity, and acceleration. The lib should be written so that the origin is in the center of canvas, not the top left corner, so there will have to be a low level transposing function. That way we can do all the trigonometry the normal way. I think it makes it a lot easier. Every PhysicsObject has a displacement vector that describes where it is from center of canvas. 

I experimented with creating something like this with Javascript and I got the basics working and I included that library in `reference-examples`. The next functionality I believe we will need for physics is similar to that described in `shapes.js` in the `javascript-other-example-prog` directory.

Todo:
 - ~~Create an object to encapsulate the Canvas object~~
 - ~~Create a Phyics Object that contains references to Vectors and will re-set its X and Y accordingly~~
 - ~~Like the pieces in `snakes_and_ladders`, a physics object should have a reference to its x and y coord, vectors for position, velocity, and acceleration, the shape(s) it draws, and the canvas object so it can move those shapes around. It will probably need a mass, though we may eventually want to abstract this, or have the option to abstract this, into a material.~~
 - ~~There will have to be a timing loop to handle updates to physics objects based on their vectors and intervals.~~
 - ~~There will need to be a way to pause and step time.~~
 - ~~The time loop will need to go through the physics objects and update them according to their vectors~~
 - ~~The time loop should run on a separate thread (really not too bad in Python!)~~
 - PhysicsObjects need to have mass
 - PhysicsObjects need to know what forces are acting on them and be able to interact with other objects, such as via gravitational pull and collision
 - If you click on a Physics object, there should be a UI pane on the side that shows you the current vectors operating on it
 - You should be able to change vectors and forces on a particular object from the UI
 - We should be able to save and load states
 - We should have a UI to configure the Options

- Everything should be documented with Sphinx eventually. For now, we should document everything with [docstrings that Sphinx can use](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html)

## Why you should contribute to this project

- It will be fun to play with bouncing and colliding balls on the screen
- You will learn UI in Python
- **It can be a portfolio project you can show off to employers when it's done, and be able to say you worked on it**
- It will help us learning and practicing math and physics as well as code
- There will be tons of features to implement. After distance/velocity/acceleration there's forces, including friction, drag, gravity, and normal force. There's tension. This thing could turn out a lot cooler than I even can see right now.
- Maybe when it's at a good point we can fork it into a game or something.


I'll try to get back and work on this later this week, after I do my actual physics homework, but anyone can feel free to pull request this and I'm willing to experiment with different directions. We could even have multiple different physics simulator built into the same UI.
