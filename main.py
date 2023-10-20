import tkinter as tk
import random


class Game15(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Игра 15")
        self.geometry("300x300")
        self.tiles = [[0, 1, 2, 3], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]]
        self.empty_row, self.empty_col = 3, 3
        self.game_over_window = None
        self.buttons = []
        self.create_widgets()
        self.shuffle_tiles()
        self.game_over_label = tk.Label(self, text="Игра окончена")
        self.game_over_label.grid(row=5, column=0, columnspan=4)
        self.game_over_label.grid_remove()  

    def create_widgets(self):
        for i in range(4):
            row = []
            for j in range(4):
                button = tk.Button(self, text="", width=5, height=2, command=lambda i=i, j=j: self.move(i, j))
                button.grid(row=i, column=j, padx=8, pady=8)
                row.append(button)
            self.buttons.append(row)

        restart_button = tk.Button(self, text="Начать заново", command=self.restart_game)
        restart_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        exit_button = tk.Button(self, text="Выход", command=self.quit)
        exit_button.grid(row=4, column=2, columnspan=2, padx=10, pady=10)

    def shuffle_tiles(self):
        try:
            self.game_over_label.grid_remove()
        except:
            pass
        numbers = list(range(1, 16))
        random.shuffle(numbers)
        while not self.is_solvable(numbers):
            random.shuffle(numbers)
        '''numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]'''
        for i in range(4):
            for j in range(4):
                if i == 3 and j == 3:
                    self.tiles[i][j] = 0
                    self.buttons[i][j].config(text="")
                else:
                    self.tiles[i][j] = numbers.pop(0)
                    self.buttons[i][j].config(text=str(self.tiles[i][j]))

    def is_solvable(self, numbers):
        inversions = 0
        for i in range(1, len(numbers)):
            if numbers[i - 1] > numbers[i]:
                inversions += 1
        return abs((inversions % 2) - 1)

    def move(self, row, col):
        if (row == self.empty_row and abs(col - self.empty_col) == 1) or \
           (col == self.empty_col and abs(row - self.empty_row) == 1):
            self.tiles[self.empty_row][self.empty_col] = self.tiles[row][col]
            self.tiles[row][col] = 0
            self.buttons[self.empty_row][self.empty_col].config(text=str(self.tiles[self.empty_row][self.empty_col]))
            self.buttons[row][col].config(text="")
            self.empty_row, self.empty_col = row, col
        self.is_solved()

    def is_solved(self):
        current_number = 1
        for i in range(4):
            for j in range(4):
                if self.tiles[i][j] != current_number:
                    return False
                current_number = (current_number + 1) % 16
        self.game_over_label.grid()

    def show_game_over_message(self):
        if self.game_over_window is None or not self.game_over_window.winfo_exists():
            self.game_over_window = tk.Toplevel(self)
            self.game_over_window.title("Игра окончена")
            game_over_label = tk.Label(self.game_over_window, text="Игра окончена, начать снова?")
            game_over_label.pack()
            restart_button = tk.Button(self.game_over_window, text="Начать заново", command=self.restart_game)
            restart_button.pack()
            game_over_label.lift()
        else:
            game_over_label = self.game_over_window.winfo_children()[0]
            game_over_label.config(text="Игра окончена, начать снова?")
            restart_button = self.game_over_window.winfo_children()[1]
            restart_button.config(command=self.restart_game)
            game_over_label.lift()
        self.game_over_window.deiconify()

    def restart_game(self):
        self.shuffle_tiles()
        self.empty_row, self.empty_col = 3, 3

        for i in range(4):
            for j in range(4):
                if self.tiles[i][j] == 0:
                    self.buttons[i][j].config(text="")
                else:
                    self.buttons[i][j].config(text=str(self.tiles[i][j]))

    def quit(self):
        self.destroy()


if __name__ == "__main__":
    app = Game15()
    app.mainloop()
