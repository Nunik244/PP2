#include <iostream>
#include <string>
#include <cstdlib>

int run(const std::string& cmd) {
    std::cout << "▶ " << cmd << std::endl;
    return system(cmd.c_str()); // runs + prints output
}

int main() {
    std::string commit;

    std::cout << "What's your commit: ";
    std::getline(std::cin, commit);

    if (run("git add .") != 0) return 1;
    if (run("git commit -m \"" + commit + "\"") != 0) return 1;
    if (run("git push origin main") != 0) return 1;

    std::cout << "✔ Done" << std::endl;
    return 0;
}
