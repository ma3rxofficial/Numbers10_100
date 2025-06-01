class GameEngine:
    def __init__(self, max_number=100):
        self.max_number = max_number
        self.current_number = 1
        self.used_numbers = set([1])
        self.history = [1]
        self.current_player = 1

    def get_possible_moves(self, number=None, used=None):
        if number is None:
            number = self.current_number
        if used is None:
            used = self.used_numbers
        moves = []
        for x in range(2, 11):
            r = number * x
            if r <= self.max_number and r not in used:
                moves.append(("*", x, r))
        for x in range(2, 11):
            if number % x == 0:
                r = number // x
                if r not in used:
                    moves.append(("/", x, r))
        return moves

    def make_move(self, op, operand):
        for o, x, r in self.get_possible_moves():
            if o == op and x == operand:
                self.current_number = r
                self.used_numbers.add(r)
                self.history.append(r)
                self.current_player = 3 - self.current_player
                return
        raise ValueError("Invalid move!")

    def copy(self):
        new_game = GameEngine(self.max_number)
        new_game.current_number = self.current_number
        new_game.used_numbers = set(self.used_numbers)
        new_game.history = list(self.history)
        new_game.current_player = self.current_player
        return new_game

    def is_game_over(self):
        return len(self.get_possible_moves()) == 0

    def get_winner(self):
        if self.is_game_over():
            return 3 - self.current_player
        return None


class AIPlayer:
    def __init__(self, max_depth=10):
        self.max_depth = max_depth

    def evaluate(self, game, depth):
        if game.is_game_over():
            if game.get_winner() == 2:
                return 10 - depth
            else:
                return depth - 10
        return 0

    def minimax(self, game, depth, maximizing):
        if depth == 0 or game.is_game_over():
            return self.evaluate(game, depth), None

        best_move = None
        if maximizing:
            max_eval = -float('inf')
            for op, x, r in game.get_possible_moves():
                new_game = game.copy()
                new_game.make_move(op, x)
                eval, _ = self.minimax(new_game, depth - 1, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = (op, x)
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for op, x, r in game.get_possible_moves():
                new_game = game.copy()
                new_game.make_move(op, x)
                eval, _ = self.minimax(new_game, depth - 1, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = (op, x)
            return min_eval, best_move

    def choose_move(self, game):
        _, move = self.minimax(game, self.max_depth, True)
        return move


def format_move(op, x, result):
    return f"{op}{x} → {result}"


def play_game():
    game = GameEngine()
    ai = AIPlayer(max_depth=8)

    print("Who makes a move first?")
    print("1 - You")
    print("2 - AI")
    first = input("Your choice (1 or 2): ").strip()
    if first == "2":
        game.current_player = 2

    while not game.is_game_over():
        print("\nCurrent number:", game.current_number)
        print("Story:", ' -> '.join(map(str, game.history)))
        moves = game.get_possible_moves()

        if game.current_player == 1:
            print("Available moves:")
            for op, x, r in moves:
                print(" ", format_move(op, x, r))

            move_str = input("Your move (eg *5 or /2): ").strip()
            if len(move_str) < 2 or move_str[0] not in '*/':
                print("Invalid input.")
                continue
            op = move_str[0]
            try:
                x = int(move_str[1:])
                game.make_move(op, x)
            except Exception as e:
                print("Error:", e)

        else:
            print("AI is thinking...")
            move = ai.choose_move(game)
            if move:
                op, x = move
                game.make_move(op, x)
                print(f"AI made a move: {format_move(op, x, game.current_number)}")
            else:
                print("AI can't make a move.")

    print("\nGame over! You won", game.get_winner())

if __name__ == "__main__":
    play_game()