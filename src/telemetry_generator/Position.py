from vector_class import Vector

# Earth's gravitational constant (km^3 / s^2)
MU = 398600.4418

dt = 1.0  # timestep in seconds, this should be a parameter

def get_initial_position():
    return Vector(6771.0, 0.0, 0.0)    # km

def get_initial_velocity():
    return Vector(0.0, 7.67, 0.0)     # km/s


def acceleration(position: Vector) -> Vector:
    r = position.norm()
    factor = -MU / (r**3)
    return Vector(
    factor * position.x,
    factor * position.y,
    factor * position.z
    )


def update_position(position, velocity):
    # Compute acceleration
    accel = acceleration(position)

    # Integrate velocity (Euler)
    velocity.x += accel.x * dt
    velocity.y += accel.y * dt
    velocity.z += accel.z * dt

    # Integrate position
    position.x += velocity.x * dt
    position.y += velocity.y * dt
    position.z += velocity.z * dt

    return position, velocity