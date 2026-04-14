#include <array>
#include <algorithm>
#include <cctype>
#include <iostream>
#include <random>
#include <string>
#include <utility>
#include <vector>

constexpr int SIZE = 4;

using Board = std::array<std::array<int, SIZE>, SIZE>;

int points = 0;

void print_board(const Board& board) {
    for (const auto& row : board) {
        for (int value : row) {
            std::cout << value << ' ';
        }
        std::cout << '\n';
    }
}

std::pair<std::array<int, SIZE>, int> merge_line(const std::array<int, SIZE>& values) {
    std::array<int, SIZE> compact{};
    int compact_size = 0;

    for (int value : values) {
        if (value != 0) {
            compact[compact_size++] = value;
        }
    }

    std::array<int, SIZE> merged{};
    int merged_size = 0;
    int gained = 0;

    for (int index = 0; index < compact_size; ) {
        if (index + 1 < compact_size && compact[index] == compact[index + 1]) {
            int combined = compact[index] * 2;
            merged[merged_size++] = combined;
            gained += combined;
            index += 2;
        } else {
            merged[merged_size++] = compact[index];
            index += 1;
        }
    }

    return {merged, gained};
}

bool move_and_merge(Board& board, const std::string& direction) {
    bool changed = false;

    if (direction == "left" || direction == "right") {
        for (int row = 0; row < SIZE; ++row) {
            std::array<int, SIZE> working{};
            for (int col = 0; col < SIZE; ++col) {
                working[col] = direction == "right" ? board[row][SIZE - 1 - col] : board[row][col];
            }

            auto [merged_row, gained] = merge_line(working);
            points += gained;

            if (direction == "right") {
                std::reverse(merged_row.begin(), merged_row.end());
            }

            for (int col = 0; col < SIZE; ++col) {
                if (board[row][col] != merged_row[col]) {
                    changed = true;
                }
                board[row][col] = merged_row[col];
            }
        }
    } else if (direction == "up" || direction == "down") {
        for (int col = 0; col < SIZE; ++col) {
            std::array<int, SIZE> working{};
            for (int row = 0; row < SIZE; ++row) {
                working[row] = direction == "down" ? board[SIZE - 1 - row][col] : board[row][col];
            }

            auto [merged_col, gained] = merge_line(working);
            points += gained;

            if (direction == "down") {
                std::reverse(merged_col.begin(), merged_col.end());
            }

            for (int row = 0; row < SIZE; ++row) {
                if (board[row][col] != merged_col[row]) {
                    changed = true;
                }
                board[row][col] = merged_col[row];
            }
        }
    }

    return changed;
}

void insert_random_tile(Board& board, std::mt19937& rng) {
    std::vector<std::pair<int, int>> empty_positions;
    for (int row = 0; row < SIZE; ++row) {
        for (int col = 0; col < SIZE; ++col) {
            if (board[row][col] == 0) {
                empty_positions.emplace_back(row, col);
            }
        }
    }

    if (empty_positions.empty()) {
        return;
    }

    std::uniform_int_distribution<std::size_t> empty_dist(0, empty_positions.size() - 1);
    std::uniform_real_distribution<double> chance_dist(0.0, 1.0);

    auto [row, col] = empty_positions[empty_dist(rng)];
    board[row][col] = chance_dist(rng) < 0.1 ? 4 : 2;
}

bool no_moves(const Board& board) {
    for (int row = 0; row < SIZE; ++row) {
        for (int col = 0; col < SIZE; ++col) {
            if (board[row][col] == 0) {
                return false;
            }
            if (row < SIZE - 1 && board[row][col] == board[row + 1][col]) {
                return false;
            }
            if (col < SIZE - 1 && board[row][col] == board[row][col + 1]) {
                return false;
            }
        }
    }
    return true;
}

int main() {
    Board board{{
        {{0, 0, 0, 0}},
        {{0, 0, 0, 0}},
        {{4, 0, 0, 0}},
        {{2, 2, 0, 0}},
    }};

    std::random_device rd;
    std::mt19937 rng(rd());

    print_board(board);

    while (true) {
        std::cout << "Enter a number (or 1 to quit):\n";

        std::string user_input;
        if (!std::getline(std::cin, user_input)) {
            std::cout << "EOF reached points: " << points << '\n';
            break;
        }

        if (!user_input.empty()) {
            for (char& ch : user_input) {
                ch = static_cast<char>(std::tolower(static_cast<unsigned char>(ch)));
            }
        }

        bool changed = false;
        if (user_input == "a") {
            changed = move_and_merge(board, "left");
        } else if (user_input == "w") {
            changed = move_and_merge(board, "up");
        } else if (user_input == "s") {
            changed = move_and_merge(board, "down");
        } else if (user_input == "d") {
            changed = move_and_merge(board, "right");
        } else if (user_input == "1") {
            std::cout << "EOF reached points: " << points << '\n';
            break;
        }

        if (changed) {
            insert_random_tile(board, rng);
        }

        print_board(board);

        if (no_moves(board)) {
            std::cout << "Died points: " << points << '\n';
            return 0;
        }
    }

    return 0;
}