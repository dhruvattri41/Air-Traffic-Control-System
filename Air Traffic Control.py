import heapq
import tkinter as tk
from tkinter import messagebox

# Air Traffic Control System: Graph Representation of Airspace
class AirTrafficControlSystem:
    def __init__(self):
        self.airspace = {}  # Stores sectors and flight paths

        # Pre-adding sectors and flight paths
        self.add_sector("SectorA")
        self.add_sector("SectorB")
        self.add_sector("SectorC")
        self.add_sector("SectorD")

        self.add_flight_path("SectorA", "SectorB", 100)
        self.add_flight_path("SectorA", "SectorC", 150)
        self.add_flight_path("SectorB", "SectorD", 200)
        self.add_flight_path("SectorC", "SectorD", 50)

    # Add a sector to the airspace
    def add_sector(self, sector_name):
        if sector_name not in self.airspace:
            self.airspace[sector_name] = []
            return True
        return False

    # Add a flight path between two sectors
    def add_flight_path(self, sector1, sector2, weight):
        if sector1 in self.airspace and sector2 in self.airspace:
            self.airspace[sector1].append((sector2, weight))
            self.airspace[sector2].append((sector1, weight))  # Bidirectional flight path
            return True
        return False

    # Dijkstra's Algorithm to find the shortest path
    def find_shortest_path(self, start, end):
        dist = {sector: float('inf') for sector in self.airspace}
        dist[start] = 0
        pq = [(0, start)]  # Priority queue for Dijkstra’s algorithm
        
        while pq:
            current_dist, current_sector = heapq.heappop(pq)

            if current_dist > dist[current_sector]:
                continue

            for neighbor, weight in self.airspace[current_sector]:
                new_dist = current_dist + weight
                if new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist
                    heapq.heappush(pq, (new_dist, neighbor))

        return dist.get(end, float('inf'))  # Return the shortest distance


class ATCApp:
    def __init__(self, root, atc_system):
        self.root = root
        self.atc_system = atc_system
        self.root.title("Air Traffic Control System")

        # Find Optimal Path Frame
        self.find_path_frame = tk.Frame(self.root)
        self.find_path_frame.pack(pady=10)

        self.start_label = tk.Label(self.find_path_frame, text="Start Sector: ")
        self.start_label.grid(row=0, column=0)

        self.start_entry = tk.Entry(self.find_path_frame)
        self.start_entry.grid(row=0, column=1)

        self.end_label = tk.Label(self.find_path_frame, text="End Sector: ")
        self.end_label.grid(row=1, column=0)

        self.end_entry = tk.Entry(self.find_path_frame)
        self.end_entry.grid(row=1, column=1)

        self.find_path_button = tk.Button(self.find_path_frame, text="Find Path", command=self.find_path)
        self.find_path_button.grid(row=2, column=0, columnspan=2)

        # Result Label
        self.result_label = tk.Label(self.root, text="Shortest Path Distance: ")
        self.result_label.pack(pady=10)

    def find_path(self):
        start = self.start_entry.get()
        end = self.end_entry.get()
        if start in self.atc_system.airspace and end in self.atc_system.airspace:
            distance = self.atc_system.find_shortest_path(start, end)
            if distance == float('inf'):
                self.result_label.config(text=f"No path found between {start} and {end}.")
            else:
                self.result_label.config(text=f"The shortest path distance from {start} to {end} is {distance} units.")
        else:
            messagebox.showwarning("Warning", "One or both sectors not found.")
        self.start_entry.delete(0, tk.END)
        self.end_entry.delete(0, tk.END)


if __name__ == "__main__":
    atc_system = AirTrafficControlSystem()
    root = tk.Tk()
    app = ATCApp(root, atc_system)
    root.mainloop()
