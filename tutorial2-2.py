from typing import List

class Point:
	"""Represents a point in 2D coordinate system."""

	def __init__(self, x: float, y: float):
		self.x = float(x)
		self.y = float(y)

	def move(self, dx: float, dy: float):
		"""Translate the point by dx, dy."""
		self.x += dx
		self.y += dy

	def tuple(self):
		return (self.x, self.y)

	def __repr__(self):
		return f"Point(x={self.x:.2f}, y={self.y:.2f})"

	def __str__(self):
		# Friendly string for printing Point attributes.
		# Print integers without decimals when possible to match sample output.
		def fmt(n: float) -> str:
			if float(n).is_integer():
				return str(int(n))
			return f"{n:.2f}"

		return f"({fmt(self.x)}, {fmt(self.y)})"


class Shape:
	"""Base class for shapes anchored by a leftTop Point.

	leftTop: the anchor point provided by the user (top-left of bounding box)
	points: ordered list of vertices in order: top-left, top-right, bottom-right, bottom-left
	"""

	def __init__(self, leftTop: Point):
		self.leftTop = leftTop
		self.points: List[Point] = []

	def calculatePoints(self):
		"""Define the points list for the shape.

		Must be implemented by subclasses. Should populate self.points in the
		specific order: top-left, top-right, bottom-right, bottom-left.
		"""
		raise NotImplementedError("calculatePoints must be implemented by subclasses")

	def calculateArea(self) -> float:
		"""Return the area of the shape. Subclasses must implement."""
		raise NotImplementedError("calculateArea must be implemented by subclasses")

	def calculatePerimeter(self) -> float:
		"""Return the perimeter of the shape. Subclasses must implement."""
		raise NotImplementedError("calculatePerimeter must be implemented by subclasses")

	def move(self, dx: float, dy: float):
		"""Move the shape by translating the leftTop anchor and updating points.

		After moving the anchor, subclasses' calculatePoints() is called to
		recompute the vertices (this avoids accumulating floating point drift).
		"""
		self.leftTop.move(dx, dy)
		# If the subclass defines calculatePoints, recalc the vertices
		try:
			self.calculatePoints()
		except NotImplementedError:
			# If subclass doesn't implement calculatePoints, try shifting existing points
			for p in self.points:
				p.move(dx, dy)


class Rectangle(Shape):
	"""Concrete rectangle defined by leftTop (x, y), width and height.

	The rectangle's orientation is axis-aligned and the leftTop point is the
	top-left corner.
	"""

	def __init__(self, leftTop: Point, width: float, height: float):
		super().__init__(leftTop)
		self.width = float(width)
		self.height = float(height)
		self.calculatePoints()

	def calculatePoints(self):
		x = self.leftTop.x
		y = self.leftTop.y
		w = self.width
		h = self.height
		# Order: top-left, top-right, bottom-right, bottom-left
		self.points = [
			Point(x, y),
			Point(x + w, y),
			Point(x + w, y + h),
			Point(x, y + h),
		]

	def calculateArea(self) -> float:
		return self.width * self.height

	def calculatePerimeter(self) -> float:
		return 2 * (self.width + self.height)


class Circle(Shape):
	"""Concrete circle defined by the top-left of its bounding box and a radius.

	The `leftTop` point is the top-left corner of the circle's bounding box.
	For compatibility with Shape.points (4-vertex list), the circle's
	calculatePoints fills the bounding box corners in the same order as
	Rectangle: top-left, top-right, bottom-right, bottom-left.
	"""

	def __init__(self, leftTop: Point, radius: float):
		super().__init__(leftTop)
		self.radius = float(radius)
		self.calculatePoints()

	def calculatePoints(self):
		x = self.leftTop.x
		y = self.leftTop.y
		r = self.radius
		# bounding box for the circle has width and height of 2*r
		self.points = [
			Point(x, y),
			Point(x + 2 * r, y),
			Point(x + 2 * r, y + 2 * r),
			Point(x, y + 2 * r),
		]

	def calculateArea(self) -> float:
		import math

		return math.pi * (self.radius ** 2)

	def calculatePerimeter(self) -> float:
		import math

		return 2 * math.pi * self.radius


def _read_float(prompt: str) -> float:
	while True:
		try:
			val = input(prompt)
			return float(val)
		except ValueError:
			print("Invalid number, please try again.")


def demo_interactive():
	"""Interactive demo: choose Rectangle or Circle and run the required checks."""
	print("Choose a shape to create:")
	print("  r - Rectangle")
	print("  c - Circle")
	choice = input("Enter choice (r/c): ").strip().lower()

	if choice == "r":
		print("Create a rectangle by entering the top-left coordinates, width and height.")
		x = _read_float("Enter leftTop x: ")
		y = _read_float("Enter leftTop y: ")
		width = _read_float("Enter width: ")
		height = _read_float("Enter height: ")
		shape = Rectangle(Point(x, y), width, height)
		shape_name = "Rectangle"

	elif choice == "c":
		print("Create a circle by entering the top-left of its bounding box and radius.")
		x = _read_float("Enter bounding-box leftTop x: ")
		y = _read_float("Enter bounding-box leftTop y: ")
		radius = _read_float("Enter radius: ")
		shape = Circle(Point(x, y), radius)
		shape_name = "Circle"

	else:
		print("Invalid choice. Exiting demo.")
		return

	print(f"\n{shape_name} created:")
	print(" Anchor (leftTop):", shape.leftTop)
	print(" Vertices (ordered):", shape.points)
	print(f" Area: {shape.calculateArea():.2f}")
	print(f" Perimeter: {shape.calculatePerimeter():.2f}")

	print("\nNow move the shape by dx, dy.")
	dx = _read_float("Enter dx: ")
	dy = _read_float("Enter dy: ")
	shape.move(dx, dy)

	print("\nAfter moving:")
	print(" Anchor (leftTop):", shape.leftTop)
	print(" Vertices (ordered):", shape.points)


if __name__ == "__main__":
	def _format_point_list(points: List[Point]) -> str:
		return ", ".join(str(p) for p in points)


	def _display_shape_info(shape: Shape):
		if isinstance(shape, Rectangle):
			print("--Rectangle--")
			print(f"Height: {int(shape.height) if shape.height.is_integer() else shape.height}")
			print(f"Width: {int(shape.width) if shape.width.is_integer() else shape.width}")
		elif isinstance(shape, Circle):
			print("--Circle--")
			r = shape.radius
			print(f"Radius: {int(r) if float(r).is_integer() else r}")
		else:
			print("--Shape--")

		print(f"Left Top Point: {shape.leftTop}")
		print(f"Area: {shape.calculateArea():.2f}")
		print(f"Perimeter: {shape.calculatePerimeter():.2f}")
		print(f"Points: {_format_point_list(shape.points)}")


	def run_console_ui():
		"""Run the infinite console UI loop until user types 'q'."""
		while True:
			choice = input("Type of Shape (q for exit): ").strip().lower()
			if choice == "q":
				break

			if choice == "r":
				# Expect: x y height width in one line (or separated)
				raw = input("Coordinate(leftTop), height and width: ")
				parts = raw.strip().split()
				if len(parts) != 4:
					print("Invalid input. Expected four numbers: x y height width")
					continue
				x, y, h, w = map(float, parts)
				shape = Rectangle(Point(x, y), w, h)
				_display_shape_info(shape)

				raw2 = input("Move object to the new coordinate(leftTop): ")
				parts2 = raw2.strip().split()
				if len(parts2) != 2:
					print("Invalid input. Expected two numbers: new_x new_y")
					continue
				new_x, new_y = map(float, parts2)
				dx = new_x - shape.leftTop.x
				dy = new_y - shape.leftTop.y
				shape.move(dx, dy)
				_display_shape_info(shape)

			elif choice == "c":
				raw = input("Coordinates(leftTop) and radius: ")
				parts = raw.strip().split()
				if len(parts) != 3:
					print("Invalid input. Expected three numbers: x y radius")
					continue
				x, y, r = map(float, parts)
				shape = Circle(Point(x, y), r)
				_display_shape_info(shape)

				raw2 = input("Move object to the new coordinate(leftTop): ")
				parts2 = raw2.strip().split()
				if len(parts2) != 2:
					print("Invalid input. Expected two numbers: new_x new_y")
					continue
				new_x, new_y = map(float, parts2)
				dx = new_x - shape.leftTop.x
				dy = new_y - shape.leftTop.y
				shape.move(dx, dy)
				_display_shape_info(shape)

			else:
				print("Unknown command. Enter 'r' for rectangle, 'c' for circle, or 'q' to quit.")

	print("#" * 80)
	run_console_ui()
	print("#" * 80)