#include <iostream>
#include <string>
#include <cstdlib>

// ANSI colors
#define GREEN   "\033[32m"
#define YELLOW  "\033[33m"
#define RED     "\033[31m"
#define BLUE    "\033[34m"
#define RESET   "\033[0m"

int run(const std::string& cmd) {
    std::cout << BLUE << "▶ " << cmd << RESET << std::endl;
    return system(cmd.c_str());
}

int main() {
    std::string commit;

    // Colored input prompt
    std::cout << GREEN << "What's your commit message: " << RESET;
    std::getline(std::cin, commit);

    if (commit.empty()) {
        std::cerr << RED << "✖ Commit message cannot be empty" << RESET << std::endl;
        return 1;
    }

    std::cout << YELLOW << "Starting Git process..." << RESET << std::endl;

    if (run("git add .") != 0) return 1;
    if (run("git commit -m \"" + commit + "\"") != 0) return 1;
    if (run("git push origin main") != 0) return 1;

    std::cout << GREEN << "✔ Done successfully" << RESET << std::endl;
    return 0;
}

