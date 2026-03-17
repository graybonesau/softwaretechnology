SPEEDS = {
	"Very Slow": 1000,
	"Slow": 500,
	"Medium": 100,
	"Fast": 50,
	"Very Fast": 10
}

ALGORITHM_INFO = {
	"Bubble Sort": "Repeatedly steps through the list, compares adjacent elements and swaps them if they are in the wrong order.",
	"Selection Sort": "Divides the input into a sorted and unsorted region, repeatedly selects the smallest element from the unsorted region.",
	"Insertion Sort": "Builds the final sorted array one item at a time, by repeatedly inserting a new element into the sorted portion of the array.",
	"Quick Sort": "Uses a divide-and-conquer strategy, selecting a 'pivot' element and partitioning the array around it.",
	"Merge Sort": "A divide-and-conquer algorithm that recursively breaks down a problem into smaller, more manageable subproblems."
}

class SortingAlgorithms:
	def __init__(self, array, visualizer):
		self.array = array
		self.visualizer = visualizer

	def bubble_sort(self):
		n = len(self.array)
		for i in range(n):
			for j in range(0, n - i - 1):
				self.visualizer.highlight_comparison(j, j + 1)
				if self.array[j] > self.array[j + 1]:
					self.array[j], self.array[j + 1] = self.array[j + 1], self.array[j]
					self.visualizer.display_array()
			# mark the last element of this pass as sorted
			self.visualizer.mark_sorted(n - i - 1)

	def selection_sort(self):
		n = len(self.array)
		for i in range(n):
			min_idx = i
			for j in range(i + 1, n):
				self.visualizer.highlight_comparison(min_idx, j)
				if self.array[j] < self.array[min_idx]:
					min_idx = j
			if min_idx != i:
				self.array[i], self.array[min_idx] = self.array[min_idx], self.array[i]
				self.visualizer.display_array()
			self.visualizer.mark_sorted(i)

	def insertion_sort(self):
		for i in range(1, len(self.array)):
			key = self.array[i]
			j = i - 1
			while j >= 0 and self.array[j] > key:
				self.visualizer.highlight_comparison(j, j + 1)
				self.array[j + 1] = self.array[j]
				self.visualizer.display_array()
				j -= 1
			self.array[j + 1] = key
			self.visualizer.display_array()
			self.visualizer.mark_sorted(i)

	def quick_sort(self, low=None, high=None):
		if low is None:
			low = 0
		if high is None:
			high = len(self.array) - 1

		def partition(l, h):
			pivot = self.array[h]
			i = l - 1
			for j in range(l, h):
				self.visualizer.highlight_comparison(j, h)
				if self.array[j] <= pivot:
					i += 1
					self.array[i], self.array[j] = self.array[j], self.array[i]
					self.visualizer.display_array()
			self.array[i + 1], self.array[h] = self.array[h], self.array[i + 1]
			self.visualizer.display_array()
			return i + 1

		if low < high:
			pi = partition(low, high)
			self.quick_sort(low, pi - 1)
			self.quick_sort(pi + 1, high)
			# optional: mark pivot position as sorted
			self.visualizer.mark_sorted(pi)

	def merge_sort(self, left=None, right=None):
		if left is None:
			left = 0
		if right is None:
			right = len(self.array) - 1
		if left < right:
			mid = (left + right) // 2
			self.merge_sort(left, mid)
			self.merge_sort(mid + 1, right)
			self.merge(left, mid, right)
			
			for idx in range(left, right + 1):
				self.visualizer.mark_sorted(idx)

	def merge(self, left, mid, right):
		left_array = self.array[left:mid + 1]
		right_array = self.array[mid + 1:right + 1]
		i = j = 0
		k = left
		while i < len(left_array) and j < len(right_array):
			self.visualizer.highlight_comparison(left + i, mid + 1 + j)
			if left_array[i] <= right_array[j]:
				self.array[k] = left_array[i]
				i += 1
			else:
				self.array[k] = right_array[j]
				j += 1
			self.visualizer.display_array()
			k += 1
		while i < len(left_array):
			self.array[k] = left_array[i]
			self.visualizer.display_array()
			i += 1
			k += 1
		while j < len(right_array):
			self.array[k] = right_array[j]
			self.visualizer.display_array()
			j += 1
			k += 1

import os
import random
import time

class ConsoleVisualizer:
	def __init__(self):
		self.array = []
		self.comparison_indices = (-1, -1)
		self.sorted_indices = set()
		self.delay = SPEEDS["Medium"] / 1000

	def clear_screen(self):
		os.system('cls' if os.name == 'nt' else 'clear')

	def generate_array(self, size=20):
		self.array = [random.randint(1, 20) for _ in range(size)]
		self.sorted_indices = set()
		self.display_array()

	def display_array(self):
		self.clear_screen()
		print("\nSorting Visualization:")
		print("-" * 50)
		for i, value in enumerate(self.array):
			bar = "█" * value
			prefix = ">" if i in self.comparison_indices else " "
			suffix = "*" if i in self.sorted_indices else " "
			print(f"{prefix} {bar:<20} {value:2d} {suffix}")
		time.sleep(self.delay)

	def highlight_comparison(self, idx1, idx2):
		self.comparison_indices = (idx1, idx2)
		self.display_array()

	def mark_sorted(self, index):
		self.sorted_indices.add(index)
		self.display_array()

	def set_speed(self):
		print("\nSelect Speed:")
		speeds = list(SPEEDS.items())
		for i, (name, _) in enumerate(speeds, 1):
			print(f"{i}. {name}")
		try:
			choice = int(input("Enter choice (1-5): "))
			if 1 <= choice <= len(speeds):
				self.delay = speeds[choice - 1][1] / 1000
			else:
				raise ValueError
		except (ValueError, IndexError):
			print("Invalid choice. Using Medium speed.")
			self.delay = SPEEDS["Medium"] / 1000

	def run(self):
		while True:
			self.clear_screen()
			print("\nSorting Algorithm Visualizer (Console Version)")
			print("-" * 50)
			print("\nAvailable Algorithms:")
			algorithms = list(ALGORITHM_INFO.keys())
			for i, algo in enumerate(algorithms, 1):
				print(f"{i}. {algo}")
				print(f"   {ALGORITHM_INFO[algo]}\n")
			print("0. Exit")
			try:
				choice = int(input("\nSelect algorithm (0-{}): ".format(len(algorithms))))
				if choice == 0:
					break
				if choice < 1 or choice > len(algorithms):
					raise ValueError
				size = int(input("Enter array size (5-30): "))
				size = max(5, min(30, size))
				self.set_speed()
				self.generate_array(size)
				sorter = SortingAlgorithms(self.array, self)
				algorithm = algorithms[choice - 1]
				print(f"\nStarting {algorithm}...")
				time.sleep(1)
				start_time = time.time()
				if algorithm == "Bubble Sort":
					sorter.bubble_sort()
				elif algorithm == "Selection Sort":
					sorter.selection_sort()
				elif algorithm == "Insertion Sort":
					sorter.insertion_sort()
				elif algorithm == "Quick Sort":
					sorter.quick_sort()
				elif algorithm == "Merge Sort":
					sorter.merge_sort()
				end_time = time.time()
				print(f"\nTime taken: {end_time - start_time:.2f} seconds")
				input("\nPress Enter to continue...")
			except ValueError:
				print("\nInvalid input! Please try again.")
				time.sleep(2)

if __name__ == "__main__":
	visualizer = ConsoleVisualizer()
	visualizer.run()