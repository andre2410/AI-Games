import matplotlib.pyplot as plt

class FitnessPlotter:
    def __init__(self, file_path):
        self.file_path = file_path
        self.generations = []
        self.avg_fitness = []

    def read_data(self):
        with open(self.file_path, 'r') as file:
            for line in file:
                parts = line.strip().split()
                print(parts)
                generation = int(parts[1].split('/')[0])
                fitness = float(parts[-1])
                self.generations.append(generation)
                self.avg_fitness.append(fitness)
                if line.startswith("Gen"):
                    print(line)
                    parts = line.strip().split()
                    generation = int(parts[1].split('/')[0])
                    fitness = float(parts[-1])
                    print(generation)
                    print(fitness)
                    self.generations.append(generation)
                    self.avg_fitness.append(fitness)

    def plot(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.generations, self.avg_fitness,  linestyle='-')
        plt.title('Average Fitness of Generation')
        plt.xlabel('Generation')
        plt.ylabel('Average Fitness')
        plt.grid(True)
        plt.show()

if __name__ == "__main__":
    file_path = "mutation1_high_data.txt"  # Replace with the path to your text file
    plotter = FitnessPlotter(file_path)
    plotter.read_data()
    plotter.plot()
