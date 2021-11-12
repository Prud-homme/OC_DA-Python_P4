from chess import (
    TournamentController,
    launch_report,
    display_menu,
    clear_display,
    choice_is_valid,
    display_message,
    edit_player_ranking,
)


def run():
    controller = TournamentController()
    clear_display()
    handler = {
        "1": controller.run,
        "2": launch_report,
        "3": edit_player_ranking,
    }
    choice = None
    while choice != "0":
        clear_display()
        choice = display_menu()
        if choice_is_valid(choice, handler):
            handler[choice]()

    display_message("\x1b[33mSee you soon\x1b[0m 👋")


if __name__ == "__main__":
    run()
