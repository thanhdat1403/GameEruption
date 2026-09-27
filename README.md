# GameEruption

A real-time 2D physics simulation built with Python, Pygame, and NumPy.

The simulation models colored balls moving inside a rotating circular boundary with an opening. Each ball is affected by gravity and interacts with the circular boundary using vector-based collision calculations.

When a ball escapes through the opening, new balls are generated with randomized velocities and colors, creating a continuously evolving simulation.

## Overview

The main idea of the project is to simulate the interaction between:

- Gravity
- Moving objects
- Circular collision boundaries
- A rotating boundary
- An opening in the boundary
- Vector-based collision response

The project focuses on applying mathematical and physics concepts to a real-time graphical simulation.

## Features

- Real-time 2D physics simulation
- Multiple colored balls
- Randomized ball colors
- Gravity simulation
- Circular boundary
- Rotating opening in the boundary
- Collision detection
- Vector-based collision response
- Tangential velocity calculation
- Automatic ball generation
- 60 FPS real-time animation

## How the Simulation Works

The simulation uses an 800 × 800 Pygame window.

A circular boundary is placed at the center of the window.

```text
Window: 800 × 800
Circle center: (400, 400)
Circle radius: 150
Ball radius: 5
```

A ball initially starts near the top of the circle.

The simulation then repeatedly updates the ball's velocity and position.

The main simulation loop runs continuously until the user closes the window.

## Ball Physics

Each ball is represented by the `Ball` class.

A ball contains:

- Position
- Velocity
- Random color
- State indicating whether it is inside the circle

The position and velocity are stored as NumPy arrays.

This makes vector calculations easier when performing physics operations.

### Gravity

Gravity is simulated by continuously increasing the vertical velocity:

```python
ball.v[1] = ball.v[1] + GRAVITY
```

The current gravity value is:

```python
GRAVITY = 0.2
```

The ball's position is then updated using its velocity:

```python
ball.pos += ball.v
```

This produces the falling motion of the ball.

## Circular Collision Detection

The distance between the ball and the center of the circular boundary is calculated using the Euclidean norm:

```python
dist = np.linalg.norm(ball.pos - CIRCLE_CENTER)
```

The program checks whether the ball has reached the boundary using:

```python
if dist + BALL_RADIUS > CIRCLE_RADIUS:
```

The ball is considered to have reached the circular boundary when the distance between its center and the circle center, plus the ball radius, becomes greater than the circle radius.

## Detecting the Opening

The circular boundary contains a rotating opening.

The opening is represented using two angles:

```python
start_angle
end_angle
```

The opening initially has an angular size of:

```python
arc_degrees = 60
```

The angles are converted from degrees to radians.

The opening then rotates continuously:

```python
start_angle += spinning_speed
end_angle += spinning_speed
```

The rotation speed is:

```python
spinning_speed = 0.01
```

## Ball Angle Calculation

When a ball reaches the circular boundary, its angle relative to the center is calculated using:

```python
ball_angle = math.atan2(dy, dx)
```

This determines the direction of the ball from the center of the circle.

The angle is normalized using:

```python
angle % (2 * math.pi)
```

This keeps the angle within a complete rotation.

The program then determines whether the ball is located inside the angular range of the opening.

If the ball reaches the opening, it is marked as outside:

```python
ball.is_in = False
```

Otherwise, the ball collides with the circular boundary.

## Collision Response

When a ball hits the solid part of the circular boundary, its position is first corrected.

The vector from the circle center to the ball is calculated:

```python
d = ball.pos - CIRCLE_CENTER
```

A unit vector pointing from the center toward the ball is then calculated:

```python
d_unit = d / np.linalg.norm(d)
```

The ball is moved back to the correct position inside the circle:

```python
ball.pos = CIRCLE_CENTER + (CIRCLE_RADIUS - BALL_RADIUS) * d_unit
```

This prevents the ball from moving through the circular boundary.

## Tangent Vector

To calculate the collision response, the simulation creates a tangent vector perpendicular to the radial vector:

```python
t = np.array([-d[1], d[0]], dtype=np.float64)
```

If:

```text
d = (x, y)
```

then the tangent direction becomes:

```text
t = (-y, x)
```

This vector represents the direction tangent to the circular boundary at the collision point.

## Velocity Projection

The ball's velocity is projected onto the tangent vector using the dot product:

```python
proj_v_t = (np.dot(ball.v, t) / np.dot(t, t)) * t
```

This determines the component of the ball's velocity that is parallel to the circular boundary.

The velocity is then reflected using:

```python
ball.v = 2 * proj_v_t - ball.v
```

This creates the bouncing effect when the ball collides with the circular boundary.

## Effect of the Rotating Boundary

The circular boundary is not stationary.

The simulation adds an additional tangential velocity:

```python
ball.v += t * spinning_speed
```

This gives the rotating boundary an influence on the ball's motion.

As the opening rotates, the collision behavior changes over time, making the movement of the balls less predictable and more dynamic.

## Ball Generation

When a ball leaves the simulation area or escapes through the opening, it is removed and new balls are generated.

New balls receive randomized velocities:

```python
random.uniform(-4, 4)
random.uniform(-1, 1)
```

Each ball also receives a random RGB color:

```python
(
    random.randint(0, 255),
    random.randint(0, 255),
    random.randint(0, 255)
)
```

This produces a continuously changing collection of colored balls.

## Main Simulation Loop

The simulation follows a repeated update cycle:

```text
1. Process window events
        ?
2. Rotate the opening
        ?
3. Update each ball
        ?
4. Apply gravity
        ?
5. Update position
        ?
6. Check boundary collision
        ?
7. Check whether the ball reaches the opening
        ?
8. Calculate collision response
        ?
9. Draw the simulation
        ?
10. Update the display
        ?
11. Maintain 60 FPS
```

The simulation maintains approximately 60 frames per second using:

```python
clock.tick(60)
```

## Mathematical Concepts Used

This project applies several mathematical concepts to simulate the physics.

### Euclidean Distance

The distance between the ball and the center of the circle is calculated using a vector norm.

### Angles

`atan2()` is used to determine the direction of the ball relative to the circle center.

### Radians

Angles are represented in radians for trigonometric calculations.

### Vectors

Position and velocity are represented as vectors.

### Dot Product

The dot product is used to calculate the projection of the ball's velocity onto the tangent vector.

### Unit Vectors

A normalized vector is used to determine the exact point where the ball should remain on the inside of the circular boundary.

### Tangential Motion

A tangent vector is used to calculate how the ball interacts with the rotating boundary.

## Technologies

- Python
- Pygame
- NumPy
- `math`
- `random`

## Project Structure

```text
GameEruption/
+-- balloon.py
+-- .gitignore
```

## Installation

Make sure Python is installed on your computer.

Install the required libraries:

```bash
pip install pygame numpy
```

Alternatively, install them individually:

```bash
pip install pygame
pip install numpy
```

## Running the Simulation

Run the following command from the project directory:

```bash
python balloon.py
```

The simulation window will open automatically.

To stop the simulation, close the Pygame window.

## Configuration

Several simulation parameters can be modified directly in `balloon.py`.

### Window Size

```python
WIDTH = 800
HEIGHT = 800
```

### Circle Radius

```python
CIRCLE_RADIUS = 150
```

### Ball Radius

```python
BALL_RADIUS = 5
```

### Gravity

```python
GRAVITY = 0.2
```

### Opening Size

```python
arc_degrees = 60
```

### Rotation Speed

```python
spinning_speed = 0.01
```

Changing these values allows different physical behaviors to be explored.

## Project Purpose

This project was created to practice combining programming, mathematics, and physics simulation.

The main concepts practiced include:

- Python object-oriented programming
- Real-time simulation
- 2D physics
- Vector mathematics
- Collision detection
- Collision response
- Trigonometry
- NumPy vector operations
- Pygame rendering
- Game loop architecture

## Possible Future Improvements

Possible improvements for future versions include:

- Add user controls for gravity
- Allow the opening size to be changed dynamically
- Add adjustable rotation speed
- Add collision sound effects
- Add particle effects
- Add a scoring system
- Add survival-time tracking
- Add different types of balls
- Add multiple circular boundaries
- Add configurable physics parameters
- Improve collision accuracy
- Add an interactive settings menu

## Author

**Thanh Dat Do**

GitHub: [@thanhdat1403](https://github.com/thanhdat1403)